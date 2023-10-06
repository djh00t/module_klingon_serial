import pytest
import netifaces
import os
from klingon.utils import get_debug, get_mac_address_and_interface


class TestUtils:

    def test_get_debug_env_set(self):
        os.environ['DEBUG'] = 'True'
        assert get_debug() is True

    def test_get_debug_env_not_set(self):
        os.environ.pop('DEBUG', None)
        assert get_debug() is False

    def test_get_mac_address_and_interface_valid(self):
        mac_address, interface = get_mac_address_and_interface()
        assert mac_address is not None
        assert interface is not None

    def test_get_mac_address_and_interface_invalid(self):
        os.environ['VIRTUALBOX'] = '1'
        mac_address, interface = get_mac_address_and_interface()
        assert mac_address is None
        assert interface is None

