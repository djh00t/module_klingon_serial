import pytest
import os
import netifaces2 as netifaces  # type: ignore
import uuid
from strtobool import strtobool  # type: ignore


@pytest.fixture
def mocked_env_no_debug(monkeypatch):
    monkeypatch.delenv("DEBUG", raising=False)


@pytest.fixture
def mocked_env_debug(monkeypatch):
    monkeypatch.setenv("DEBUG", "1")


@pytest.fixture
def mocked_interfaces():
    return ["eth0", "eth1", "eth2"]


@pytest.fixture
def mocked_mac_addresses():
    return ["00:11:22:33:44:55", "aa:bb:cc:dd:ee:ff", "ff:ee:dd:cc:bb:aa"]


@pytest.fixture
def mocked_missing_mac_address(monkeypatch):
    netifaces_mock = MagicMock(netifaces.interfaces)
    netifaces_mock.return_value = ["eth0", "eth1", "eth2"]

    ifaddresses_mock = netifaces_mock.ifaddresses
    ifaddresses_mock.return_value = {}

    monkeypatch.setattr("netifaces.interfaces", netifaces_mock)


def test_get_debug_no_env(mocked_env_no_debug):
    assert get_debug() == False


def test_get_debug_with_env(mocked_env_debug):
    assert get_debug() == True


def test_get_debug_invalid_value():
    with pytest.raises(ValueError):
        get_debug() == True


def test_get_mac_address_and_interface_found(mocked_interfaces, mocked_mac_addresses):
    for interface, mac_address in zip(mocked_interfaces, mocked_mac_addresses):
        mac_address, interface_name = get_mac_address_and_interface()
        assert mac_address == mac_address
        assert interface_name == interface


def test_get_mac_address_and_interface_not_found(mocked_missing_mac_address):
    mac_address, interface_name = get_mac_address_and_interface()
    assert mac_address == None
    assert interface_name == None
