import pytest
from klingon.generate_serial import get_mac_address_hex, get_process_id, get_millisecond_epoch_hex, generate_serial

def test_get_mac_address_hex():
    mac_address_hex = get_mac_address_hex()
    assert isinstance(mac_address_hex, str)
    assert len(mac_address_hex) == 12

def test_get_process_id():
    process_id = get_process_id()
    assert isinstance(process_id, str)
    assert len(process_id) == 5

def test_get_millisecond_epoch_hex():
    epoch_millis_hex = get_millisecond_epoch_hex()
    assert isinstance(epoch_millis_hex, str)
    assert len(epoch_millis_hex) == 11

def test_generate_serial():
    serial = generate_serial()
    assert isinstance(serial, str)
    assert len(serial) == 28
