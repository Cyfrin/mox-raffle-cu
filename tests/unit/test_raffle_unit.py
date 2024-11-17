import boa
import pytest

from tests.conftest import STARTING_BALANCE

INTERVAL = 60
RANDOM = boa.env.generate_address("non-owner")


def test_raffle_entrance_fee(raffle):
    assert raffle.entrance_fee() == int(1e17)


def test_raffle_reverts_when_you_dont_pay_enough(user, raffle):
    with boa.reverts("Raffle: Send more to enter raffle"):
        raffle.enter_raffle()


def test_raffle_records_player_when_they_enter(user, raffle):
    raffle_entrance_fee = raffle.entrance_fee()
    raffle.enter_raffle(value=raffle_entrance_fee)
    assert raffle.players(0) == user


def test_emits_event_on_entrance(user, raffle):
    raffle_entrance_fee = raffle.entrance_fee()
    raffle.enter_raffle(value=raffle_entrance_fee)
    assert raffle.get_logs()[0].topics[0] == user


def test_owner_can_change_fee(owner, raffle):
    new_fee = 100
    assert raffle.entrance_fee() != new_fee
    with boa.env.prank(owner):
        raffle.set_fee(new_fee)
    assert raffle.entrance_fee() == new_fee


def test_user_cannot_change_fee(raffle):
    new_fee = 100
    with boa.env.prank(RANDOM):
        with boa.reverts("ownable: caller is not the owner"):
            raffle.set_fee(new_fee)


@pytest.fixture
def raffle_entered(user, raffle):
    raffle_entrance_fee = raffle.entrance_fee()
    raffle.enter_raffle(value=raffle_entrance_fee)
    return raffle

# Can you some tests to pick the winner?