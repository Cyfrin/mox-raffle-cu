from moccasin.config import get_active_network

FUND_AMOUNT = int(10e18)


def get_or_create_subscription(vrf_coordinator) -> int:
    active_network = get_active_network()
    params = active_network.extra_data

    sub_id = params.get("sub_id", 0)
    if sub_id == 0:
        sub_id = vrf_coordinator.createSubscription()
        print(f"Subscription created with id: {sub_id}")
    else:
        print(f"Using existing subscription: {sub_id}")
    return sub_id


def is_funded(sub_id: int, vrf_coordinator) -> bool:
    active_network = get_active_network()
    vrf_coordinator = active_network.manifest_named("vrf_coordinator_v2")
    subscription_details = vrf_coordinator.getSubscription(sub_id)
    if subscription_details[0] >= FUND_AMOUNT:
        return True
    return False


def fund_subscription(sub_id: int, link_token, vrf_coordinator) -> bool:
    link_token.approve(vrf_coordinator.address, FUND_AMOUNT)
    vrf_coordinator.fundSubscription(sub_id, FUND_AMOUNT)
    print("Subscription funded")
    return True


def moccasin_main():
    active_network = get_active_network()
    vrf_coordinator = active_network.manifest_named("vrf_coordinator_v2")
    link_token = active_network.manifest_named("link_token")
    sub_id = get_or_create_subscription(vrf_coordinator)
    if is_funded(sub_id):
        print("Subscription is already funded")
    else:
        fund_subscription(sub_id, link_token, vrf_coordinator)
