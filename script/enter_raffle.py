import time

from moccasin.boa_tools import VyperContract
from moccasin.config import get_active_network


def enter_raffle(raffle: VyperContract):
    raffle.enter_raffle()

def moccasin_main():
    active_network = get_active_network()
    raffle = active_network.get_latest_contract_unchecked()
    enter_raffle(raffle)
