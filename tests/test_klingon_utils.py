from klingon_serial.str2bool import str2bool
from klingon_serial.utils import get_debug, get_mac_address_and_interface
import psutil
import os
import platform
import pytest
import unittest.mock
import uuid


def test_get_debug_env_set():
    """Test that the `get_debug()` function returns True if the `DEBUG` environment variable is set to a truthy value."""

    os.environ['DEBUG'] = 'True'
    assert get_debug() == True


def test_get_debug_env_not_set():
    """Test that the `get_debug()` function returns False if the `DEBUG` environment variable is not set."""

    os.environ.pop('DEBUG', None)
    assert get_debug() is False


def test_get_debug_invalid_value():
    """Test that the `get_debug()` function returns False if the `DEBUG` environment variable is set to an invalid value."""

    os.environ['DEBUG'] = 'invalid'
    assert get_debug() == False


def test_get_mac_address_and_interface_valid():
    """Test that the `get_mac_address_and_interface()` function returns a valid MAC address and network interface."""

    mac_address, interface = get_mac_address_and_interface()

    assert mac_address is not None
    assert interface is not None
    assert isinstance(mac_address, str)
    assert isinstance(interface, str)

def get_mac_address_and_interface():
    """Returns a tuple containing the MAC address and the network interface of the local machine's primary network interface.

    Returns:
        tuple: A tuple containing the MAC address and the network interface.
            If the MAC address and interface cannot be determined, returns (None, None).
    """

    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK and addr.address:
                return addr.address, interface  # Return MAC address and interface name

    return None, None  # Return None, None if no suitable interface found
