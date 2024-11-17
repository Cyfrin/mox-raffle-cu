import boa
import pytest
from eth_utils import to_wei

from moccasin.config import get_active_network
from script.deploy_raffle import deploy_raffle

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
def raffle():
    return deploy_raffle()
#     # return active_network.manifest_named("raffle")

@pytest.fixture
def owner(raffle):
    return raffle.owner()
