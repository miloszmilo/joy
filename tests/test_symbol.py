import pytest

from src.joyTypes.Symbol import Symbol



def test_is_number():
    x: Symbol = 3
    assert x is Symbol, "number should be symbol"
