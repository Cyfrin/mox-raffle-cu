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

# pragma version ^0.4.0
"""
@title raffle.vy
@license MIT
@author You!
@notice A sample Funding Contract
        This contract is for creating a sample funding contract
"""

# from pcaversaccio.snekmate.src.snekmate.auth import ownable
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

# State Variables
## Constants
MAX_ARRAY_SIZE: constant(uint256) = 1
MAX_NUMBER_OF_PLAYERS: constant(uint256) = 10000

## Immutables
INTERVAL: public(immutable(uint256))

## Storage Variables
entrance_fee: public(uint256)
last_timestamp: public(uint256)
recent_winner: public(address)
players: public(DynArray[address, MAX_NUMBER_OF_PLAYERS])

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
    interval: uint256,
    entrance_fee: uint256,
):
    ow.__init__()
    INTERVAL = interval
    self.entrance_fee = entrance_fee
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
    self.players.append(msg.sender)
    log RaffleEntered(msg.sender)


@external
def request_winner():
    raffle_is_ready: bool = self._is_ready_to_request()
    assert raffle_is_ready, ERROR_RAFFLE_NOT_OVER

    # THIS IS NOT REALLY RANDOM!!!
    # Use Chainlink VRF: https://docs.chain.link/vrf
    index_of_winner: uint256 = convert(keccak256(concat(block.prevrandao, convert(block.timestamp, bytes32))),uint256) % len(self.players)

    recent_winner: address = self.players[index_of_winner]
    self.recent_winner = recent_winner
    self.players = []
    self.last_timestamp = block.timestamp
    raw_call(recent_winner, b"", value = self.balance)
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
    time_passed: bool = (block.timestamp - self.last_timestamp) > INTERVAL
    has_players: bool = len(self.players) > 0
    has_balance: bool = self.balance > 0
    raffle_over: bool = time_passed and has_balance and has_players
    return raffle_over
