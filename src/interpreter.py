from os.path import isdir, exists
from pathlib import Path

from src.exceptions.FileEmptyError import FileEmptyError
from src.constants import other
from src.exceptions.FileWrongTypeError import FileWrongTypeError
from src.joyTypes.AST_Nodes import Node, PrintStatement
from src.parser import Parser
from src.tokenizer import Tokenizer


def run(source_path: str):
    interpret(source_path)


def read_source_file(source_path: str):
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

def interpret(source_path: str) -> None:
    file_lines = read_source_file(source_path)
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize_multiple_lines(file_lines)
    parser = Parser(tokens=tokens)
    nodes = parser.parse()
    for node in nodes:
        visit_node(node)

def visit_node(node: Node):
    if isinstance(node, PrintStatement):
        # print
        print(node.text)
        return
    pass
#
# run("examples/hello.joy")
