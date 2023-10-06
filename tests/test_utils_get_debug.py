import os
import netifaces2 as netifaces  # type: ignore
import pytest
import uuid
from strtobool import strtobool  # type: ignore


@pytest.fixture
def setup_env():
    os.environ["DEBUG"] = "True"


def test_get_debug_returns_true_when_environment_variable_is_set_to_true(setup_env):
    assert get_debug() is True


def test_get_debug_returns_false_when_environment_variable_is_not_set():
    assert get_debug() is False


def test_get_debug_returns_false_when_environment_variable_is_set_to_false():
    os.environ["DEBUG"] = "False"
    assert get_debug() is False


def test_get_debug_returns_false_when_environment_variable_is_not_boolean():
    os.environ["DEBUG"] = "invalid"
    assert get_debug() is False


def test_get_mac_address_and_interface_returns_correct_tuple_when_mac_address_is_found(
    monkeypatch,
):
    mock_mac_address = "00:11:22:33:44:55"
    mock_interface = "eth0"

    def mock_interfaces():
        return [mock_interface]

    def mock_ifaddresses(interface):
        return {netifaces.AF_LINK: [{"addr": mock_mac_address}]}

    monkeypatch.setattr(netifaces, "interfaces", mock_interfaces)
    monkeypatch.setattr(netifaces, "ifaddresses", mock_ifaddresses)
    assert get_mac_address_and_interface() == (mock_mac_address, mock_interface)


def test_get_mac_address_and_interface_returns_none_tuple_when_mac_address_is_not_found(
    monkeypatch,
):
    def mock_interfaces():
        return []

    monkeypatch.setattr(netifaces, "interfaces", mock_interfaces)
    assert get_mac_address_and_interface() == (None, None)


def test_get_mac_address_and_interface_returns_none_tuple_when_mac_address_is_found_but_not_matching(
    monkeypatch,
):
    mock_mac_address = "00:11:22:33:44:55"
    mock_interface = "eth0"

    def mock_interfaces():
        return [mock_interface]

    def mock_ifaddresses(interface):
        return {netifaces.AF_LINK: [{"addr": "FF:EE:DD:CC:BB:AA"}]}

    monkeypatch.setattr(netifaces, "interfaces", mock_interfaces)
    monkeypatch.setattr(netifaces, "ifaddresses", mock_ifaddresses)
    assert get_mac_address_and_interface() == (None, None)


def test_get_mac_address_and_interface_returns_none_tuple_when_mac_address_cannot_be_converted_to_int(
    monkeypatch,
):
    mock_mac_address = "00:11:22:33:44:55"
    mock_interface = "eth0"

    def mock_interfaces():
        return [mock_interface]

    def mock_ifaddresses(interface):
        return {netifaces.AF_LINK: [{"addr": mock_mac_address}]}

    def mock_getnode():
        raise ValueError

    monkeypatch.setattr(netifaces, "interfaces", mock_interfaces)
    monkeypatch.setattr(netifaces, "ifaddresses", mock_ifaddresses)
    monkeypatch.setattr(uuid, "getnode", mock_getnode)
    assert get_mac_address_and_interface() == (None, None)


def test_get_mac_address_and_interface_returns_none_tuple_when_key_error_is_raised(
    monkeypatch,
):
    mock_mac_address = "00:11:22:33:44:55"
    mock_interface = "eth0"

    def mock_interfaces():
        return [mock_interface]

    def mock_ifaddresses(interface):
        raise KeyError

    monkeypatch.setattr(netifaces, "interfaces", mock_interfaces)
    monkeypatch.setattr(netifaces, "ifaddresses", mock_ifaddresses)
    assert get_mac_address_and_interface() == (None, None)


def test_get_mac_address_and_interface_returns_none_tuple_when_index_error_is_raised(
    monkeypatch,
):
    mock_mac_address = "00:11:22:33:44:55"
    mock_interface = "eth0"

    def mock_interfaces():
        return [mock_interface]

    def mock_ifaddresses(interface):
        return {netifaces.AF_LINK: [{}]}

    monkeypatch.setattr(netifaces, "interfaces", mock_interfaces)
    monkeypatch.setattr(netifaces, "ifaddresses", mock_ifaddresses)
    assert get_mac_address_and_interface() == (None, None)
