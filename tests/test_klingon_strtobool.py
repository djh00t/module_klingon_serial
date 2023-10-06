"""Tests for the `strtobool()` function in `klingon.strtobool`.

"""
import pytest
from klingon_serial.strtobool import strtobool


def test_strtobool_true():
    """Test that the `strtobool()` function returns True for valid true
    values."""
    
    assert strtobool("y") == 1
    assert strtobool("yes") == 1
    assert strtobool("t") == 1
    assert strtobool("true") == 1
    assert strtobool("on") == 1
    assert strtobool("1") == 1


def test_strtobool_false():
    """Test that the `strtobool()` function returns False for valid false
    values."""
    
    assert strtobool("n") == 0
    assert strtobool("no") == 0
    assert strtobool("f") == 0
    assert strtobool("false") == 0
    assert strtobool("off") == 0
    assert strtobool("0") == 0


def test_strtobool_invalid():
    """Test that the `strtobool()` function raises a ValueError for invalid
    values."""
    
    with pytest.raises(ValueError):
        strtobool("invalid")
