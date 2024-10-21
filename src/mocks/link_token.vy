# SPDX-License-Identifier: MIT
# @version 0.4.0

from snekmate.tokens import erc20
from snekmate.auth import ownable as ow

initializes: ow
initializes: erc20[ownable := ow]
exports: erc20.__interface__

INITIAL_SUPPLY: constant(uint256) = 100 * 10**18
NAME: constant(String[25]) = "Chainlink"
SYMBOL: constant(String[5]) = "LINK"
DECIMALS: constant(uint8) = 18
NAME_EIP712: constant(String[50]) = "CHAINLINK TOKEN"


@deploy
def __init__():
    ow.__init__()
    erc20.__init__(NAME, SYMBOL, DECIMALS, NAME_EIP712, "1")
    erc20._mint(msg.sender, INITIAL_SUPPLY)
