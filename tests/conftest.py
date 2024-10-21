import boa
import pytest
from eth_utils import to_wei

from moccasin.config import get_active_network

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


@pytest.fixture
def active_network():
    return get_active_network()


@pytest.fixture
def vrf_coordinator_v2(active_network):
    return active_network.manifest_named("vrf_coordinator_v2")


@pytest.fixture
def link_token(active_network):
    return active_network.manifest_named("link_token")


@pytest.fixture
def raffle(active_network):
    return active_network.manifest_named("raffle")


@pytest.fixture
def owner(raffle):
    return raffle.owner()
