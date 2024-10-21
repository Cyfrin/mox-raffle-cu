import time

from moccasin.boa_tools import VyperContract
from moccasin.config import get_active_network


def request_winner(raffle: VyperContract):
    if len(raffle.get_players()) == 0:
        raffle.enter_raffle()

    while raffle.is_ready_to_request() is False:
        print("Sleeping...")
        time.sleep(5)


def moccasin_main():
    active_network = get_active_network()
    raffle = active_network.get_latest_contract_unchecked()
    request_winner(raffle)
