"""
This module provides a utility function to convert string representations of
boolean values to actual boolean (True or False) values.
"""
from distutils.util import strtobool as distutils_strtobool

def strtobool(val):
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'.
    False values are 'n', 'no', 'f', 'false', 'off', and '0'.

    This function is a wrapper around distutils.util.strtobool for compatibility.
    """
    return distutils_strtobool(val)
