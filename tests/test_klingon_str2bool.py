"""Tests for the `str2bool()` function in `klingon.str2bool`.

"""

import pytest
from klingon_serial.str2bool import str2bool


def test_str2bool_true():
    """Test that the `str2bool()` function returns True for valid true
    values."""

    assert str2bool("y") == 1
    assert str2bool("yes") == 1
    assert str2bool("t") == 1
    assert str2bool("true") == 1
    assert str2bool("on") == 1
    assert str2bool("1") == 1


def test_str2bool_false():
    """Test that the `str2bool()` function returns False for valid false
    values."""

    assert str2bool("n") == 0
    assert str2bool("no") == 0
    assert str2bool("f") == 0
    assert str2bool("false") == 0
    assert str2bool("off") == 0
    assert str2bool("0") == 0


def test_str2bool_invalid():
    """Test that the `str2bool()` function raises a ValueError for invalid
    values."""

    with pytest.raises(ValueError):
        str2bool("invalid")
