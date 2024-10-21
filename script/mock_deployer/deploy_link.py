from moccasin.boa_tools import VyperContract

from src.mocks import link_token


def deploy_link() -> VyperContract:
    return link_token.deploy()


def moccasin_main() -> VyperContract:
    return deploy_link()
