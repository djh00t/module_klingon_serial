import pytest

from klingon import strtobool


def test_strtobool_true():
    assert strtobool("y") == 1
    assert strtobool("yes") == 1
    assert strtobool("t") == 1
    assert strtobool("true") == 1
    assert strtobool("on") == 1
    assert strtobool("1") == 1


def test_strtobool_false():
    assert strtobool("n") == 0
    assert strtobool("no") == 0
    assert strtobool("f") == 0
    assert strtobool("false") == 0
    assert strtobool("off") == 0
    assert strtobool("0") == 0


def test_strtobool_invalid():
    with pytest.raises(ValueError):
        strtobool("invalid")
