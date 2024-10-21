from eth_utils import to_bytes
from moccasin.boa_tools import VyperContract
from moccasin.config import get_active_network

from src import raffle


def deploy_raffle() -> VyperContract:
    active_network = get_active_network()
    vrf_coordinator_v2 = active_network.manifest_named("vrf_coordinator_v2")
    params = active_network.extra_data
    raffle_contract = raffle.deploy(
        params["sub_id"],
        to_bytes(hexstr=params["gas_lane"]),
        params["interval"],
        int(params["entrance_fee"]),
        params["callback_gas_limit"],
        vrf_coordinator_v2.address,
    )
    print(f"Deployed raffle contract at {raffle_contract.address}")
    return raffle_contract


def moccasin_main():
    return deploy_raffle()
