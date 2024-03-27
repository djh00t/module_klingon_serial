from distutils.util import strtobool as str2bool

def strtobool(val):
    """Convert a string representation of truth to true (True) or false (False).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'.
    False values are 'n', 'no', 'f', 'false', 'off', and '0'.

    This function is a wrapper around str2bool for compatibility.
    """
    return str2bool(val)
