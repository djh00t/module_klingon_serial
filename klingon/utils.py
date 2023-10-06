import os
import netifaces
import uuid
import platform
from strtobool import strtobool

def get_debug():
    """Get debug mode from environment.

    Returns:
        bool: True if debug mode is enabled, False otherwise.
    """
    debug = os.environ.get('DEBUG')
    if debug is None:
        return False
    try:
        return bool(strtobool(debug))
    except ValueError:
        return False

def get_mac_address_and_interface():
    """Get the MAC address and the associated network interface.

    Returns:
        tuple: A tuple containing the MAC address and the network interface.
               If the MAC address and interface cannot be determined, returns (None, None).
    """
    if platform.system() == 'Darwin':
        interface = 'en0'
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_LINK in addresses:
            mac_address = addresses[netifaces.AF_LINK][0]['addr']
            return mac_address, interface
        else:
            gws = netifaces.gateways()
            default_interface = gws['default'][netifaces.AF_INET][1]
            addresses = netifaces.ifaddresses(default_interface)
            mac_address = addresses[netifaces.AF_LINK][0]['addr']
            return mac_address, default_interface
    else:
        for interface in netifaces.interfaces():
            try:
                addresses = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addresses:
                    mac_address = addresses[netifaces.AF_LINK][0]['addr']
                    return mac_address, interface
            except (IndexError, KeyError, ValueError) as e:
                continue
    return None, None

mac_address, interface = get_mac_address_and_interface()
print(mac_address)
print(interface)
