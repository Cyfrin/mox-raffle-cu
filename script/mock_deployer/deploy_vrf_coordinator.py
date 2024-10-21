from eth_utils import to_wei
from moccasin.boa_tools import VyperContract

from src.mocks import vrf_coordinator_v2

MOCK_GAS_PRICE_LINK = int(1e9)
MOCK_BASE_FEE = to_wei(0.25, "ether")
# LINK / ETH price
MOCK_WEI_PER_UINT_LINK = int(4e15)


def deploy_vrf() -> VyperContract:
    vrf_coordinator = vrf_coordinator_v2.deploy(
        MOCK_GAS_PRICE_LINK, MOCK_BASE_FEE, MOCK_WEI_PER_UINT_LINK
    )
    return vrf_coordinator


def moccasin_main():
    return deploy_vrf()
