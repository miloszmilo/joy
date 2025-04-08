import pytest

from src.exceptions.FileEmptyError import FileEmptyError
from src.exceptions.FileWrongTypeError import FileWrongTypeError
from src.exceptions.VariableDuplicateName import VariableDuplicateName
from src.exceptions.VariableEmptyName import VariableEmptyName
from src.exceptions.VariableIllegalName import VariableIllegalName
from src.exceptions.VariableWhitespaceName import VariableWhitespaceName
from src.interpreter import (
    assign_value_to_variable,
    get_variable_name,
    read_source_file,
    register_variable,
)
from src.joyTypes.Variable import Variable


def test_real_file():
    expected_list = []
    with open("tests/files/hello.joy", "r") as f:
        expected_list.append(f.readline().strip())
    assert read_source_file("tests/files/hello.joy") == expected_list, (
        "should read file correctly"
    )


def test_wrong_type_file():
    with pytest.raises(FileWrongTypeError, match="File is not of type JOY, got type"):
        _ = read_source_file("tests/files/wrong.type")


def test_non_existing_file():
    with pytest.raises(FileNotFoundError, match="File not found in path hello.joy"):
        _ = read_source_file("hello.joy")


def test_dir():
    with pytest.raises(
        IsADirectoryError, match="File name not found, got directory tests/files"
    ):
        _ = read_source_file("tests/files")


def test_empty_file():
    with pytest.raises(FileEmptyError, match="File is empty tests/files/empty.joy"):
        _ = read_source_file("tests/files/empty.joy")


def test_get_variable_name():
    assert get_variable_name("var variable;") == "variable", (
        "should read variable name correctly"
    )


def test_empty_variable_name():
    with pytest.raises(
        VariableEmptyName, match="Variable name is empty after whitespace reduction"
    ):
        _ = get_variable_name("var;")


def test_whitespace_variable_name():
    with pytest.raises(
        VariableEmptyName, match="Variable name is empty after whitespace reduction"
    ):
        _ = get_variable_name("var           ;")


def test_whitespace_separated_variable_name():
    with pytest.raises(
        VariableWhitespaceName,
        match="Variable name contains whitespace",
    ):
        _ = get_variable_name("var var var var able name;")


def test_variable_keyword_name():
    with pytest.raises(
        VariableIllegalName, match="Variable illegal name containing keywords var"
    ):
        _ = get_variable_name("var var;")


def test_register_duplicate_variable():
    prepared_dict: dict[str, Variable] = {"variable": Variable()}
    with pytest.raises(
        VariableDuplicateName, match="Variable name variable already registered"
    ):
        register_variable("variable", prepared_dict)


def test_register_variable():
    result_dict = {}
    expected_dict = {"variable": Variable()}
    register_variable("variable", result_dict)
    assert list(result_dict.keys()) == list(expected_dict.keys()) and list(
        result_dict.values()
    ) == list(expected_dict.values()), "should read variable name correctly"


def test_variables_different_types():
    result_dict = {}
    expected_dict = {"variable": Variable()}
    register_variable("variable", result_dict)
    assert list(result_dict.keys()) == list(expected_dict.keys()) and list(
        result_dict.values()
    ) == list(expected_dict.values()), "should read variable name correctly"


def test_addition():
    result_dict = {"variable": Variable(type="int", value=0)}
    expected_dict = {"variable": Variable(type="int", value=4)}
    assign_value_to_variable("2 + 2", "variable", result_dict)
    assert result_dict == expected_dict, "should add to variable"


def test_single_addition():
    result_dict = {"variable": Variable(type="int", value=0)}
    expected_dict = {"variable": Variable(type="int", value=2)}
    assign_value_to_variable("+ 2", "variable", result_dict)
    assert result_dict == expected_dict, "should add two to variable"


def test_subtraction():
    result_dict = {"variable": Variable(type="int", value=0)}
    expected_dict = {"variable": Variable(type="int", value=-2)}
    assign_value_to_variable("0 - 2", "variable", result_dict)
    assert result_dict == expected_dict, "should subtract to variable"


def test_single_subtraction():
    result_dict = {"variable": Variable(type="int", value=0)}
    expected_dict = {"variable": Variable(type="int", value=-2)}
    assign_value_to_variable("- 2", "variable", result_dict)
    assert result_dict == expected_dict, "should subtract to variable"
