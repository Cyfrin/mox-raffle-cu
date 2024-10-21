# pragma version 0.4.0
"""
@title auth.vy
@license MIT
@author You!
@dev This is our version of an auth contract!
"""

owner: public(address)


event OwnershipTransferred:
    previous_owner: indexed(address)
    new_owner: indexed(address)


@deploy
def __init__():
    self._transfer_ownership(msg.sender)


@internal
def _check_owner():
    assert msg.sender == self.owner, "ownable: caller is not the owner"


@internal
def _transfer_ownership(new_owner: address):
    old_owner: address = self.owner
    self.owner = new_owner
    log OwnershipTransferred(old_owner, new_owner)
