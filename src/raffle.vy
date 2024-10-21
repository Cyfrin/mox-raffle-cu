# Layout of Contract:
# version
# imports
# errors
# Type declarations
# State variables
# Events
# Functions

# Layout of Functions:
# constructor
# receive function (if exists)
# fallback function (if exists)
# external
# public
# internal
# private
# view & pure functions

# pragma version 0.4.0
"""
@title raffle.vy
@license MIT
@author You!
@notice A sample Funding Contract
        This contract is for creating a sample funding contract
"""

from .interfaces import VRFCoordinatorV2
from snekmate.auth import ownable as ow

initializes: ow
exports: ow.__interface__

# Errors
ERROR_RAFFLE_NOT_OVER: constant(String[25]) = "Raffle: Has not finished"
ERROR_TRANSFER_FAILED: constant(String[100]) = "Raffle: Transfer failed"
ERROR_SEND_MORE_TO_ENTER_RAFFLE: constant(
    String[100]
) = "Raffle: Send more to enter raffle"
ERROR_RAFFLE_NOT_OPEN: constant(String[100]) = "Raffle: Raffle not open"


# Type declarations
flag RaffleState:
    OPEN
    CALCULATING


# State Variables
## Constants
MAX_ARRAY_SIZE: constant(uint256) = 1
REQUEST_CONFIRMATIONS: constant(uint16) = 3
NUM_WORDS: constant(uint32) = 1
MAX_NUMBER_OF_PLAYERS: constant(uint256) = 10000
EMPTY_BYTES: constant(Bytes[32]) = b"\x00"

## Immutables
CALLBACK_GAS_LIMIT: immutable(uint32)
VRF_COORDINATOR: public(immutable(VRFCoordinatorV2))
GAS_LANE: public(immutable(bytes32))
INTERVAL: public(immutable(uint256))
SUBSCRIPTION_ID: public(immutable(uint64))

## Storage Variables
entrance_fee: public(uint256)
last_timestamp: public(uint256)
recent_winner: public(address)
players: public(DynArray[address, MAX_NUMBER_OF_PLAYERS])
raffle_state: public(RaffleState)

# Events
event RequestedRaffleWinner:
    request_id: indexed(uint256)


event RaffleEntered:
    player: indexed(address)


event WinnerPicked:
    player: indexed(address)


# Constructor
@deploy
def __init__(
    subscription_id: uint64,
    gas_lane: bytes32,  # keyHash
    interval: uint256,
    entrance_fee: uint256,
    callback_gas_limit: uint32,
    vrf_coordinator_v2: address,
):
    ow.__init__()
    SUBSCRIPTION_ID = subscription_id
    GAS_LANE = gas_lane
    INTERVAL = interval
    CALLBACK_GAS_LIMIT = callback_gas_limit
    VRF_COORDINATOR = VRFCoordinatorV2(vrf_coordinator_v2)
    self.entrance_fee = entrance_fee
    self.raffle_state = RaffleState.OPEN
    self.last_timestamp = block.timestamp


# External Functions
@external
def set_fee(new_fee: uint256):
    ow._check_owner()
    self.entrance_fee = new_fee


@external
@view
def get_owner() -> address:
    return ow.owner


@external
@payable
def enter_raffle():
    assert msg.value >= self.entrance_fee, ERROR_SEND_MORE_TO_ENTER_RAFFLE
    assert self.raffle_state == RaffleState.OPEN, ERROR_RAFFLE_NOT_OPEN
    self.players.append(msg.sender)
    log RaffleEntered(msg.sender)


@external
def request_winner():
    raffle_is_ready: bool = self._is_ready_to_request()
    assert raffle_is_ready, ERROR_RAFFLE_NOT_OVER
    self.raffle_state = RaffleState.CALCULATING

    request_id: uint256 = extcall VRF_COORDINATOR.requestRandomWords(
        GAS_LANE,
        SUBSCRIPTION_ID,
        REQUEST_CONFIRMATIONS,
        CALLBACK_GAS_LIMIT,
        NUM_WORDS,
    )
    # Quiz... is this redundant?
    log RequestedRaffleWinner(request_id)


@external
def rawFulfillRandomWords(
    requestId: uint256, randomWords: DynArray[uint256, MAX_ARRAY_SIZE]
):
    """In solidity, this is the equivalent of inheriting the VRFConsumerBaseV2
    Vyper doesn't have inheritance, so we just add the function here
    Also, we need to use `DynArray` so our function selector is the same as the one Chainlink VRF is looking for:
    Function Signature: rawFulfillRandomWords(uint256,uint256[])
    Function selector: 0x1fe543e3
    """
    assert (
        msg.sender == VRF_COORDINATOR.address
    ), "Only coordinator can fulfill!"
    index_of_winner: uint256 = randomWords[0] % len(self.players)
    recent_winner: address = self.players[index_of_winner]
    self.recent_winner = recent_winner
    self.players = []
    self.raffle_state = RaffleState.OPEN
    self.last_timestamp = block.timestamp
    send(recent_winner, self.balance)
    log WinnerPicked(recent_winner)


@external
@view
def is_ready_to_request() -> bool:
    return self._is_ready_to_request()


@external
@view
def get_players() -> DynArray[address, MAX_NUMBER_OF_PLAYERS]:
    return self.players


@internal
@view
def _is_ready_to_request() -> bool:
    is_open: bool = RaffleState.OPEN == self.raffle_state
    time_passed: bool = (block.timestamp - self.last_timestamp) > INTERVAL
    has_players: bool = len(self.players) > 0
    has_balance: bool = self.balance > 0
    raffle_over: bool = time_passed and is_open and has_balance and has_players
    return raffle_over
