import os
import psutil
import uuid
import platform
from .strtobool import strtobool

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

    # Get primary network interface by looking at the default route
    primary_interface = None
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                primary_interface = interface
                mac_address = addr.address
                return mac_address, primary_interface  # Return on first found interface

    return None, None  # Return None, None if no interface found
