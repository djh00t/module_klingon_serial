from str2bool import str2bool as strtobool

def strtobool(val):
    """Convert a string representation of truth to true (True) or false (False).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'.
    False values are 'n', 'no', 'f', 'false', 'off', and '0'.

    This function is a wrapper around str2bool for compatibility.
    """
    return strtobool(val)
