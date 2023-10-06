import os
import netifaces
import uuid
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
    for interface in netifaces.interfaces():
        print(f"Checking interface: {interface}")
        try:
            mac_address = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
            print(f"MAC address for {interface}: {mac_address}")
            mac_address_int = int(mac_address.replace(':', ''), 16)
            if mac_address_int == uuid.getnode():
                return mac_address, interface
        except (IndexError, KeyError, ValueError) as e:
            print(f"Error for {interface}: {e}")
            continue
    return None, None

mac_address, interface = get_mac_address_and_interface()
print(mac_address)
print(interface)
