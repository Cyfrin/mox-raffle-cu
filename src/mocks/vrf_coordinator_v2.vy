# SPDX-License-Identifier: MIT
# @version 0.4.0

MAX_ARRAY_SIZE: constant(uint256) = 10

BASE_FEE: immutable(uint96)
GAS_PRICE_LINK: immutable(uint96)
WEI_PER_UNIT_LINK: immutable(int256)

struct Subscription:
    balance: uint96 
    nativeBalance: uint96
    reqCount: uint64

struct SubscriptionConfig:
    owner: address 
    requestedOwner: address 
    consumers: DynArray[address, MAX_ARRAY_SIZE]

struct ConsumerConfig:
    active: bool 
    nonce: uint64 
    pendingReqCount: uint64

dummy_address: address
s_subscriptions: HashMap[uint256, Subscription]
s_subscriptionsConfig: HashMap[uint256, SubscriptionConfig]
s_consumers: HashMap[address, HashMap[uint256, ConsumerConfig]]


event RandomWordsFulfilled:
    requestId: indexed(uint256)
    outputSeed: uint256
    payment: uint96
    success: bool


event RandomWordsRequested:
    keyHash: indexed(bytes32)
    requestId: uint256
    preSeed: uint256
    subId: indexed(uint64)
    minimumRequestConfirmations: uint16
    callbackGasLimit: uint32
    numWords: uint32
    sender: indexed(address)


event SubscriptionCreated:
    subId: indexed(uint64)
    owner: address


@deploy
def __init__(
    gas_price_link: uint96, base_fee: uint96, wei_per_unit_link: int256
):
    BASE_FEE = base_fee
    GAS_PRICE_LINK = gas_price_link
    WEI_PER_UNIT_LINK = wei_per_unit_link
    self.dummy_address = msg.sender


@external
def fulfillRandomWords(requestId: uint256, consumer: address):
    """Returns an array of random numbers. In this mock contract, we ignore the requestId and consumer.

    Args:
        requestId (uint256): The request Id number
        consumer (address): The consumer address to
    """
    # Default to 77 as a mocking example
    words: DynArray[uint256, MAX_ARRAY_SIZE] = [77]
    self.fulfillRandomWordsWithOverride(requestId, consumer, words)


@internal
def fulfillRandomWordsWithOverride(
    requestId: uint256,
    consumer: address,
    words: DynArray[uint256, MAX_ARRAY_SIZE],
):
    """Returns an array of random numbers. In this mock contract, we ignore the requestId and consumer.

    Args:
        requestId (uint256): The request Id number
        consumer (address): The consumer address to
        words (DynArray[uint256, MAX_ARRAY_SIZE]): The array of random numbers, we are defaulting to MAX_ARRAY_SIZE for vyper
    """
    call_data: Bytes[3236] = abi_encode(
        requestId,
        words,
        method_id=method_id("rawFulfillRandomWords(uint256,uint256[])"),
    )
    response: Bytes[32] = raw_call(consumer, call_data, max_outsize=32)
    log RandomWordsFulfilled(requestId, requestId, 0, True)


@external
def requestRandomWords(
    key_hash: bytes32,
    sub_id: uint64,
    minimum_request_confirmations: uint16,
    callback_gas_limit: uint32,
    num_words: uint32,
) -> uint256:
    log RandomWordsRequested(
        key_hash,
        0,
        0,
        sub_id,
        minimum_request_confirmations,
        callback_gas_limit,
        num_words,
        msg.sender,
    )
    return 0


@external
def fundSubscription(subId: uint256, amount: uint96):
    """Funds a subscription. 

    Args:
        subId (uint256): The subscription Id number
        amount (uint96): The amount to fund the subscription
    """
    self.s_subscriptions[subId].balance += amount


@external
def addConsumer(subId: uint256, consumer: address):
    """Adds consumer to subscription. 

    Args:
        subId (uint256): The subId
        consumer (address): Consumer / contract address that will be getting random numbers
    """
    consumer_config: ConsumerConfig = self.s_consumers[consumer][subId]
    if consumer_config.active:
        return
    consumer_config.active = True
    self.s_subscriptionsConfig[subId].consumers.append(consumer)
    


@external
def createSubscription() -> uint256:
    """
    Create a subscription. Keeping returning 1 for the mock.
    """
    new_dyn_array: DynArray[address, MAX_ARRAY_SIZE] = empty(DynArray[address, MAX_ARRAY_SIZE])
    self.s_subscriptionsConfig[1] = SubscriptionConfig(
        owner=msg.sender, requestedOwner=msg.sender, consumers=new_dyn_array
    )
    log SubscriptionCreated(1, msg.sender)
    return 1


@external
@view
def getSubscription(subId: uint256) -> (uint96, uint64, address, address[1]):
    """
    Get a subscription. 
    """
    sub_owner: address = self.s_subscriptionsConfig[subId].owner
    assert sub_owner != 0x0000000000000000000000000000000000000000
    return (
        self.s_subscriptions[subId].balance,
        self.s_subscriptions[subId].reqCount,
        sub_owner,
        [self.s_subscriptionsConfig[subId].requestedOwner],
    )


    
