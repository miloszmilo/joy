from os.path import isdir, exists
from pathlib import Path
from typing import Callable

from src.context import InterpreterContext
from src.exceptions.FileEmptyError import FileEmptyError
from src.constants import other
from src.exceptions.FileWrongTypeError import FileWrongTypeError
from src.joyTypes.AST_Nodes import (
    IfStatement,
    Node,
    PrintStatement,
    VariableAccess,
    VariableDeclaration,
    WhileStatement,
)
from src.parser import Parser
from src.tokenizer import Tokenizer


class Interpreter:
    context: InterpreterContext

    def __init__(self) -> None:
        self.context = InterpreterContext({})

    def run(self, source_path: str):
        self.interpret(source_path)

    def interpret(self, source_path: str) -> None:
        file_lines = self.read_source_file(source_path)
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize_multiple_lines(file_lines)
        parser = Parser(tokens=tokens)
        nodes = parser.parse()
        for node in nodes:
            self.visit_node(node)

    def visit_node(self, node: Node):
        """
        node.accept()
        """
        if isinstance(node, PrintStatement):
            print(node.text)
            return
        if isinstance(node, IfStatement):
            if check_condition(node):
                if not node.body:
                    return
                self.visit_node(node.body)
                return
            if not node.elseBody:
                return
            self.visit_node(node.elseBody)
            return
        if isinstance(node, WhileStatement):
            while check_condition(node):
                if not node.body:
                    return
                self.visit_node(node.body)
                return
            return
        if isinstance(node, VariableDeclaration):
            # declare if not declared, else throw error
            pass
        if isinstance(node, VariableAccess):
            # return variable value?
            pass
        pass

    def read_source_file(self, source_path: str):
        if not exists(source_path):
            raise FileNotFoundError(f"File not found in path {source_path}")
        if isdir(source_path):
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


def check_condition(node: IfStatement | WhileStatement) -> bool:
    comparisons: dict[str, Callable[[float, float], bool]] = {
        "<": lambda x, y: x < y,
        ">": lambda x, y: x > y,
        "<=": lambda x, y: x <= y,
        ">=": lambda x, y: x >= y,
        "==": lambda x, y: x == y,
        "!=": lambda x, y: x != y,
    }
    return comparisons[node.condition.operator.token](
        node.condition.left.value, node.condition.right.value
    )


#
# run("examples/hello.joy")
