"""Tests for the `generate_serial()` function in `klingon.generate_serial`.

"""
from fastapi.testclient import TestClient
from openfaas.handler import app

import pytest
from klingon_serial.generate import generate_serial, get_mac_address_hex, get_process_id, get_millisecond_epoch_hex

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

from klingon_serial.generate import generate_serial, is_valid_serial

client = TestClient(app)

def test_generate_and_validate_serial():
    """Test that a generated serial is valid according to `is_valid_serial()`."""
    serial = generate_serial()
    assert is_valid_serial(serial) == True

def test_endpoint_root():
    """Test the root endpoint `/` to ensure it returns a valid serial number."""
    client = TestClient(app)
    response = client.get("/", headers={"Accept": "application/json"})
    assert response.status_code == 200
    data = response.json()
    assert "serial" in data
    assert is_valid_serial(data["serial"])
from klingon_serial.generate import generate_serial, is_valid_serial

client = TestClient(app)

def test_generate_and_validate_serial():
    """Test that a generated serial is valid according to `is_valid_serial()`."""
    serial = generate_serial()
    assert is_valid_serial(serial) == True

def test_endpoint_root():
    """Test the root endpoint `/` to ensure it returns a valid serial number."""
    response = TestClient(app).get("/", headers={"Accept": "application/json"})
    assert response.status_code == 200
    data = response.json()
    assert "serial" in data
    assert is_valid_serial(data["serial"])
from klingon_serial.generate import generate_serial, is_valid_serial

client = TestClient(app)

def test_generate_and_validate_serial():
    """Test that a generated serial is valid according to `is_valid_serial()`."""
    serial = generate_serial()
    assert is_valid_serial(serial) == True

def test_endpoint_root():
    """Test the root endpoint `/` to ensure it returns a valid serial number."""
    response = TestClient(app).get("/", headers={"Accept": "application/json"})
    assert response.status_code == 200
    data = response.json()
    assert "serial" in data
    assert is_valid_serial(data["serial"])
