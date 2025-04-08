from decimal import DivisionByZero
import os
from os.path import isdir
from pathlib import Path

from src.exceptions.VariableDuplicateName import VariableDuplicateName
from src.exceptions.VariableEmptyName import VariableEmptyName
from src.exceptions.VariableIllegalName import VariableIllegalName
from src.exceptions.VariableWhitespaceName import VariableWhitespaceName
from src.joyTypes.Variable import Variable
from src.exceptions.FileEmptyError import FileEmptyError
from src.constants import keywords, other
from src.exceptions.FileWrongTypeError import FileWrongTypeError
from src.joyTypes.Types import Type


def run(source_path: str, target_path: str = "./output"):
    compile(source_path, target_path)


def compile(source_path: str, target_path: str):
    """
    first create AST
    then run line by line
    """
    syntax_tree = create_syntax_tree(source_path)
    bytecode = convert_syntax_tree_to_byte_code(syntax_tree)


def create_syntax_tree(source_path: str):
    variables = {}
    source_file_lines = read_source_file(source_path)
    for line in source_file_lines:
        if line.startswith(keywords.VARIABLE):
            name = get_variable_name(line)
            register_variable(name, variables)
        if line.split(" ", 1)[0] in variables.keys():
            name, value = line.split(" ", 1)[0], line.split(keywords.ASSIGNMENT, 1)[-1]
            assign_value_to_variable(value, name, variables)
    pass


def read_source_file(source_path: str):
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"File not found in path {source_path}")
    if os.path.isdir(source_path):
        raise IsADirectoryError(f"File name not found, got directory {source_path}")
    if not source_path.endswith(other.SOURCE_CODE_FILE_EXTENSION):
        raise FileWrongTypeError(
            f"File is not of type JOY, got {source_path.split('.')[-1]}"
        )
    if Path(source_path).stat().st_size <= 0:
        raise FileEmptyError(f"File is empty {source_path}")

    source_file: list[str] = []
    try:
        with open(source_path, "r") as f:
            source_file.append(f.readline().strip())
    except Exception as e:
        print(f"Failed to open file {e}")
        raise IOError
    return source_file


def get_variable_name(line: str):
    variable_name = line.split(keywords.VARIABLE, 1)[-1].split(";")[0].strip()
    if len(variable_name) == 0:
        raise VariableEmptyName("Variable name is empty after whitespace reduction")
    if variable_name.count(" ") > 0:
        raise VariableWhitespaceName("Variable name contains whitespace")
    if variable_name in keywords.ALL:
        raise VariableIllegalName(
            f"Variable illegal name containing keywords {variable_name}"
        )
    return variable_name


def register_variable(variable_name: str, variables: dict[str, Variable]):
    if variable_name in variables.keys():
        raise VariableDuplicateName(f"Variable name {variable_name} already registered")
    variables[variable_name] = Variable()


def assign_value_to_variable(
    rightSide: str, leftSide: str, variables: dict[str, Variable]
):
    # Divide always to 2 parts
    # if real_value == 0:
    #   real_value = int(v)
    # if real_value != 0:
    # real_value -= int(v)
    # basically first assign left side of the right side
    # to real_value, then make the +, -, /, %, * on it
    # with the right side
    real_value = 0
    rightSide = rightSide.strip()
    for substring in arithmetic_function_map.keys():
        if substring not in rightSide:
            continue
        left, right = rightSide.split(substring, 2)
        left, right = left.strip(), right.strip()

        # Handle variables
        if left in variables:
            left = variables[left].value
        if right in variables:
            right = variables[right].value

        real_value += arithmetic_function_map[substring](int(left), int(right))
    variables[leftSide].value = real_value


def add(x: int, y: int):
    return x + y


def subtract(x: int, y: int):
    return x - y


def multiply(x: int, y: int):
    return x * y


def divide(x: int, y: int):
    if y == 0:
        raise DivisionByZero(f"Cannot divide {x} by zero")
    return x / y


def modulo(x: int, y: int):
    return x % y


arithmetic_function_map = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
    "%": modulo,
}


def convert_syntax_tree_to_byte_code(syntax_tree):
    pass


run("examples/hello.joy")
