"""Tests for the `generate_serial()` function in `klingon.generate_serial`.

"""

import pytest
from klingon_serial.generate_serial import generate_serial, get_mac_address_hex, get_process_id, get_millisecond_epoch_hex

def test_get_mac_address_hex():
    """Test that the `get_mac_address_hex()` function returns a valid MAC address hex string."""

    mac_address_hex = get_mac_address_hex()

    assert isinstance(mac_address_hex, str)
    assert len(mac_address_hex) == 12

def test_get_process_id():
    """Test that the `get_process_id()` function returns a valid process ID hex string."""

    process_id = get_process_id()

    assert isinstance(process_id, str)
    assert len(process_id) == 5

def test_get_millisecond_epoch_hex():
    """Test that the `get_millisecond_epoch_hex()` function returns a valid millisecond epoch hex string."""

    epoch_millis_hex = get_millisecond_epoch_hex()

    assert isinstance(epoch_millis_hex, str)
    assert len(epoch_millis_hex) == 11

def test_generate_serial():
    """Test that the `generate_serial()` function returns a valid serial number."""

    serial = generate_serial()

    assert isinstance(serial, str)
    assert len(serial) == 28
