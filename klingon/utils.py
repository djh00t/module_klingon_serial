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
    """Returns a tuple containing the MAC address and the network interface of the local machine's primary network interface.

    Returns:
        tuple: A tuple containing the MAC address and the network interface.
               If the MAC address and interface cannot be determined, returns (None, None).
    """

    # Get the list of all network interfaces
    interfaces = netifaces.interfaces()

    # Find the primary network interface
    primary_interface = None
    for interface in interfaces:
        if netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr'] == uuid.getnode():
            primary_interface = interface
            break

    # If the primary network interface cannot be determined, return None
    if primary_interface is None:
        return None, None

    # Get the MAC address of the primary network interface
    mac_address = netifaces.ifaddresses(primary_interface)[netifaces.AF_LINK][0]['addr']

    # Return the MAC address and network interface of the primary network interface
    return mac_address, primary_interface


mac_address, primary_interface = get_mac_address_and_interface()
print(mac_address)
print(primary_interface)
