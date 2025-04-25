import uuid
import re
import os
from datetime import datetime, timezone
from .str2bool import str2bool
from .utils import get_debug, get_mac_address_and_interface

def is_valid_serial(serial):
    """Validate the serial number format.

    Args:
        serial (str): The serial number to validate.

    Returns:
        bool: True if the serial number is valid, False otherwise.
    """
    pattern = r'^[a-fA-F0-9]{12}[a-fA-F0-9]{5}[a-fA-F0-9]{11}$'
    return bool(re.match(pattern, serial))

def get_mac_address_hex():
    """Get the MAC address from the environment as a hexadecimal string.

    Returns:
        str: The MAC address as a hexadecimal string, padded to 12 characters.
    """
    try:
        mac_address_hex = hex(uuid.getnode())[2:]
        return mac_address_hex.zfill(12)
    except:
        return None

def get_process_id():
    """Get the process ID as a fixed-length hexadecimal string.

    Returns:
        str: The process ID as a fixed-length hexadecimal string, padded to 5 characters.
    """
    process_id_hex = hex(os.getpid())[2:]
    return process_id_hex.zfill(5)

def get_millisecond_epoch_hex():
    """Get the epoch time in milliseconds as a fixed-length hexadecimal string.

    Returns:
        str: The epoch time in milliseconds as a fixed-length hexadecimal string, padded to 11 characters.
    """
    epoch = int(datetime.now(timezone.utc).timestamp() * 1000)
    epoch_hex = hex(epoch)[2:]
    return epoch_hex.zfill(11)

def generate_serial():
    """Generate a fixed-length serial number.

    Returns:
        str: The generated serial number, consisting of the MAC address, process ID, and epoch time.
    """
    mac_address_hex = get_mac_address_hex()
    process_id = get_process_id()
    epoch_millis_hex = get_millisecond_epoch_hex()
    serial = f"{mac_address_hex}{process_id}{epoch_millis_hex}"
    return serial

debug = get_debug()

if debug:
    mac_address, interface = get_mac_address_and_interface()
    print("Network Interface:       ", interface) 
    print("MAC Address (int):       ",uuid.getnode())
    print("MAC Address (hex):       ",get_mac_address_hex())
    print("Process ID (hex):        ",get_process_id())
    print("Epoch datetime (ms):     ",int(datetime.now(timezone.utc).timestamp() * 1000))
    print("Epoch datetime (hex):    ",get_millisecond_epoch_hex())
    print("Generated Serial:        ",generate_serial())
    print("Serial Valid:            ", is_valid_serial(generate_serial()))
    print("Serial Length:           ",len(generate_serial()))
