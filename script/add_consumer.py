from moccasin.config import get_active_network


def add_consumer(raffle=None):
    active_network = get_active_network()
    if raffle is None:
        raffle = active_network.manifest_named("raffle")
    vrf_coordinator = active_network.manifest_named("vrf_coordinator_v2")
    sub_id = raffle.SUBSCRIPTION_ID()
    vrf_coordinator.addConsumer(sub_id, raffle.address)


def moccasin_main():
    add_consumer()
