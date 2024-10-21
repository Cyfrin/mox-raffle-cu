import time

import pytest
from moccasin.config import get_active_network


@pytest.mark.staging
def test_start_raffle():
    active_network = get_active_network()
    raffle = active_network.get_latest_contract_unchecked()
    raffle.enter_raffle()

    while raffle.is_ready_to_request() is False:
        print("Sleeping...")
        time.sleep(5)

    raffle.request_winner()
