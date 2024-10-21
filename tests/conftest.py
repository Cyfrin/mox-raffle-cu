import boa
import pytest
from eth_utils import to_wei

from moccasin.config import get_active_network
from script.deploy_raffle import deploy_raffle
from script.mock_deployer import deploy_vrf_coordinator, deploy_link

STARTING_BALANCE = to_wei(1000, "ether")

@pytest.fixture
def user():
    with boa.env.prank(boa.env.eoa):
        boa.env.set_balance(boa.env.eoa, STARTING_BALANCE)
        yield boa.env.eoa

@pytest.fixture
def other_user():
    with boa.env.prank(boa.env.eoa):
        boa.env.set_balance(boa.env.eoa, STARTING_BALANCE)
        yield boa.env.eoa

# @pytest.fixture
# def active_network():
#     return get_active_network()

@pytest.fixture
def vrf_coordinator_v2():
    active_network = get_active_network()
    return active_network.manifest_named("vrf_coordinator_v2")

@pytest.fixture
def link_token():
    active_network = get_active_network()
    return active_network.manifest_named("link_token")

# @pytest.fixture 
# def link_token():
#     return deploy_link.deploy_link()

# @pytest.fixture
# def vrf_coordinator_v2():
#     return deploy_vrf_coordinator.deploy_vrf()

@pytest.fixture
def raffle():
    return deploy_raffle()
#     # return active_network.manifest_named("raffle")

@pytest.fixture
def owner(raffle):
    return raffle.owner()
