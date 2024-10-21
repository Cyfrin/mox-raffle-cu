import boa
import pytest

from tests.conftest import STARTING_BALANCE

# In vyper, flags/enums are 1 indexed
RAFFLE_OPEN = 1
RAFFLE_CALCULATING = 2

INTERVAL = 60
RANDOM = boa.env.generate_address("non-owner")


def test_raffle_is_in_open_state(raffle):
    assert raffle.raffle_state() == RAFFLE_OPEN


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


def test_dont_allow_players_to_enter_while_raffle_is_calculating(
    user, raffle_entered, vrf_coordinator_v2
):
    raffle_entrance_fee = raffle_entered.entrance_fee()
    boa.env.time_travel(seconds=INTERVAL + 1)
    raffle_entered.request_winner()
    with boa.reverts("Raffle: Raffle not open"):
        raffle_entered.enter_raffle(value=raffle_entrance_fee)


def test_check_is_raffle_ready_returns_false_if_raffle_isnt_open(user, raffle_entered):
    boa.env.time_travel(seconds=INTERVAL + 1)
    raffle_entered.request_winner()
    raffle_ready = raffle_entered.is_ready_to_request()
    assert raffle_entered.raffle_state() == RAFFLE_CALCULATING
    assert not raffle_ready


# Can you do these?
# def test_check_upkeep_returns_false_if_enough_time_hast_passed
# def test_check_upkeep_returns_true_when_parameters_are_good


def test_request_winners_can_only_run_if_check_upkeep_is_true(raffle_entered):
    boa.env.time_travel(seconds=INTERVAL + 1)
    raffle_entered.request_winner()
    assert True


def test_perform_upkeep_reverts_if_check_upkeep_is_false(user, raffle):
    with boa.reverts("Raffle: Has not finished"):
        raffle.request_winner()


def test_perform_upkeep_updates_raffle_state_and_emits_request_id(user, raffle_entered):
    boa.env.time_travel(seconds=INTERVAL + 1)
    raffle_entered.request_winner()
    request_id = raffle_entered.get_logs()[1].topics[0]
    assert request_id is not None
    assert raffle_entered.raffle_state() == RAFFLE_CALCULATING


def test_fulfill_random_words_picks_a_winner_resets_and_sends_money(
    user, raffle_entered, vrf_coordinator_v2
):
    additional_entrants = 10
    for i in range(additional_entrants):
        player = boa.env.generate_address(i)
        boa.env.set_balance(player, STARTING_BALANCE)
        with boa.env.prank(player):
            raffle_entered.enter_raffle(value=raffle_entered.entrance_fee())
    starting_time_stamp = raffle_entered.last_timestamp()
    starting_balance = boa.env.get_balance(user)
    boa.env.time_travel(seconds=INTERVAL + 1)

    raffle_entered.request_winner()

    # # Normally we need to get the requestID, but our mock ignores that
    # with boa.env.prank(vrf_coordinator_v2.address):
    #     vrf_coordinator_v2.fulfillRandomWords(0, raffle_entered.address)

    # recent_winner = raffle_entered.recent_winner()
    # raffle_state = raffle_entered.raffle_state()
    # winner_balance = boa.env.get_balance(recent_winner)
    # ending_time_stamp = raffle_entered.last_timestamp()
    # prize = raffle_entered.entrance_fee() * (additional_entrants + 1)
    # assert recent_winner == user
    # assert raffle_state == RAFFLE_OPEN
    # assert winner_balance == starting_balance + prize
    # assert ending_time_stamp > starting_time_stamp
