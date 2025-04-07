import pytest

from src.exceptions.FileEmptyError import FileEmptyError
from src.exceptions.FileWrongTypeError import FileWrongTypeError
from src.interpreter import read_source_file

def test_real_file():
    expected_list = []
    with open('tests/files/hello.joy', 'r') as f:
        expected_list.append(f.readline().strip())
    assert read_source_file("tests/files/hello.joy") == expected_list, "should read file correctly"

def test_wrong_type_file():
    with pytest.raises(FileWrongTypeError, match="File is not of type JOY, got type"):
        read_source_file("tests/files/wrong.type")

def test_non_existing_file():
    with pytest.raises(FileNotFoundError, match="File not found in path hello.joy"):
        read_source_file("hello.joy")

def test_dir():
    with pytest.raises(IsADirectoryError, match="File name not found, got directory tests/files"):
        read_source_file("tests/files")

def test_empty_file():
    with pytest.raises(FileEmptyError, match="File is empty tests/files/empty.joy"):
        read_source_file("tests/files/empty.joy")
