import os
from os.path import isdir

from src.exceptions.FileWrongTypeError import FileWrongTypeError


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
    source_file_lines = read_source_file(source_path)
    pass

def read_source_file(source_path: str):
    if not source_path.endswith('.joy'):
        print(f'File is not of type JOY, got {source_path.split(".")[-1]}')
        raise FileWrongTypeError
    if not os.path.exists(source_path):
        print(f'File not found in path {source_path}')
        raise FileNotFoundError
    if os.path.isdir(source_path):
        print(f'File name not found, got directory {source_path}')
        raise IsADirectoryError

    source_file: list[str] = []
    try:
        with open(source_path, 'r') as f:
            source_file.append(f.readline().strip())
    except Exception as e:
        print(f'Failed to open file {e}')
        raise IOError
    return source_file

def convert_syntax_tree_to_byte_code(syntax_tree):
    pass

run('examples/hello.joy')
