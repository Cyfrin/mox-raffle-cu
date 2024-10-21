from script.create_and_fund_subscription import (
    get_or_create_subscription,
    fund_subscription,
)
from script.add_consumer import add_consumer


def test_fund_subscription(raffle, link_token, vrf_coordinator_v2):
    # Arrange
    sub_id = get_or_create_subscription(vrf_coordinator_v2)

    # Act
    fund_subscription(sub_id, link_token, vrf_coordinator_v2)
    add_consumer(raffle=raffle)

    # Assert
    subscription = vrf_coordinator_v2.getSubscription(sub_id)
