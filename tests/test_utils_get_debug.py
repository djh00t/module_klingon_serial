import os
import pytest
import netifaces
import uuid
from strtobool import strtobool  # type: ignore


def test_get_debug_env_true():
    os.environ["DEBUG"] = "true"
    assert get_debug() == True


def test_get_debug_env_false():
    os.environ["DEBUG"] = "false"
    assert get_debug() == False


def test_get_debug_env_none():
    os.environ["DEBUG"] = None
    assert get_debug() == False


def test_get_debug_invalid_input():
    os.environ["DEBUG"] = "Invalid"
    assert get_debug() == False


def test_get_mac_address_and_interface_valid():
    mock_interface = "eth0"
    mock_mac_address = "00:11:22:33:44:55"
    mock_mac_address_int = int(mock_mac_address.replace(":", ""), 16)
    assert get_mac_address_and_interface() == (mock_mac_address, mock_interface)


def test_get_mac_address_and_interface_invalid_interface():
    mock_interface = "invalid"
    mock_mac_address = "00:11:22:33:44:55"
    mock_mac_address_int = int(mock_mac_address.replace(":", ""), 16)
    assert get_mac_address_and_interface() == (None, None)


def test_get_mac_address_and_interface_invalid_mac_address():
    mock_interface = "eth0"
    mock_mac_address = "Invalid"
    assert get_mac_address_and_interface() == (None, None)
