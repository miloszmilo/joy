from src.joyTypes.Variable import Variable


def test_variables_different_values():
    assert Variable() != Variable(value=False), "should not match none to bool"


def test_variables_same_types():
    assert Variable(type="str") == Variable(type="str"), "should match str to str"


def test_variables_same_int():
    assert Variable(type="int") == Variable(type="int"), "should match int to int"


def test_variables_same_type_different_value():
    assert Variable(value=3, type="int") != Variable(value=5, type="int"), (
        "should not match int 3 to int 5"
    )
