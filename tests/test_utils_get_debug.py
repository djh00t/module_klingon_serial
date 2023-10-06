from klingon import utils
import os
import pytest
import netifaces
import uuid
from strtobool import strtobool  # type: ignore


def test_get_debug_enabled():
    os.environ["DEBUG"] = "1"
    assert get_debug() == True


def test_get_debug_disabled():
    os.environ["DEBUG"] = "0"
    assert get_debug() == False


def test_get_debug_invalid():
    os.environ["DEBUG"] = "test"
    assert get_debug() == False


def test_get_debug_not_set():
    if "DEBUG" in os.environ:
        del os.environ["DEBUG"]
    assert get_debug() == False


def test_get_mac_address_and_interface_found():
    mock_netifaces = {
        "interfaces": ["lo", "eth0"],
        "ifaddresses": {
            "lo": {netifaces.AF_LINK: [{"addr": "00:00:00:00:00:00"}]},
            "eth0": {netifaces.AF_LINK: [{"addr": "00:11:22:33:44:55"}]},
        },
    }
    # monkey patch netifaces to return the mocked data
    original_netifaces = netifaces
    netifaces = type("MockNetifaces", (object,), mock_netifaces)
    assert get_mac_address_and_interface() == ("00:11:22:33:44:55", "eth0")
    # revert monkey patch
    netifaces = original_netifaces


def test_get_mac_address_and_interface_not_found():
    mock_netifaces = {
        "interfaces": ["lo", "eth0"],
        "ifaddresses": {
            "lo": {netifaces.AF_LINK: [{"addr": "00:00:00:00:00:00"}]},
            "eth0": {netifaces.AF_LINK: [{"addr": "11:22:33:44:55:66"}]},
        },
    }
    # monkey patch netifaces to return the mocked data
    original_netifaces = netifaces
    netifaces = type("MockNetifaces", (object,), mock_netifaces)
    assert get_mac_address_and_interface() == (None, None)
    # revert monkey patch
    netifaces = original_netifaces


def test_get_mac_address_and_interface_invalid():
    mock_netifaces = {
        "interfaces": ["lo", "eth0"],
        "ifaddresses": {
            "lo": {netifaces.AF_LINK: [{"addr": "test"}]},
            "eth0": {netifaces.AF_LINK: [{"addr": "11:22:33:44:55:66"}]},
        },
    }
    # monkey patch netifaces to return the mocked data
    original_netifaces = netifaces
    netifaces = type("MockNetifaces", (object,), mock_netifaces)
    assert get_mac_address_and_interface() == (None, None)
    # revert monkey patch
    netifaces = original_netifaces
