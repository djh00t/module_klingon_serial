"""
This module provides utility functions for the klingon_serial package, including
retrieving the MAC address and network interface, and determining the debug mode.
"""
import os
import psutil
import uuid
import platform
from .strtobool import strtobool


def validate_serial(serial):
    """Validate the generated serial number against the expected format.

    Args:
        serial (str): The serial number to validate.

    Returns:
        bool: True if the serial number is valid, False otherwise.
    """
    pattern = re.compile(r'^[a-fA-F0-9]{12}[a-fA-F0-9]{5}[a-fA-F0-9]{11}$')
    return bool(pattern.match(serial))

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
    try:
        # Get primary network interface by looking at the default route
        primary_interface = None
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == psutil.AF_LINK:
                    primary_interface = interface
                    mac_address = addr.address
                    return mac_address, primary_interface  # Return on first found interface
    except Exception as e:
        print(f"Error retrieving network interface: {e}")
    # Get primary network interface by looking at the default route
    primary_interface = None
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                primary_interface = interface
                mac_address = addr.address
                return mac_address, primary_interface  # Return on first found interface

    return None, None  # Return None, None if no interface found
