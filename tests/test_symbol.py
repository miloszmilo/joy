import pytest

from src.joyTypes.Symbol import symbol


def test_is_number():
    x: symbol = 3
    assert x is symbol, "number should be symbol"
