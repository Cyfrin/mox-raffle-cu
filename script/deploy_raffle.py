from eth_utils import to_bytes
from moccasin.boa_tools import VyperContract
from moccasin.config import get_active_network

from src import raffle


def deploy_raffle() -> VyperContract:
    active_network = get_active_network()
    params = active_network.extra_data
    raffle_contract = raffle.deploy(
        params["interval"],
        int(params["entrance_fee"]),
    )
    print(f"Deployed raffle contract at {raffle_contract.address}")
    return raffle_contract


def moccasin_main():
    return deploy_raffle()
