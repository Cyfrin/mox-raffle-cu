from src.mocks import link_token
from moccasin.config import get_active_network


def moccasin_main():
    link = link_token.deploy()
    print(f"Deployed LINK token at {link.address}")
    network = get_active_network()

    link = network.manifest_named("link_token")
    print(f"Retrieved LINK token at {link.address}")

    link = network.manifest_named("link_token")
    print(f"Retrieved LINK token at {link.address}")

    link = link_token.deploy()
    print(f"Deployed LINK token at {link.address}")
