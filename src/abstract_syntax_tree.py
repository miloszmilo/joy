from __future__ import annotations
from os.path import isfile
from typing import override
from src.constants.other import SOURCE_CODE_FILE_EXTENSION
from src.evaluator import Evaluator
from src.exceptions.FileWrongTypeError import FileWrongTypeError
from src.joyTypes.Token import Token
from src.tokenizer import Tokenizer


class Node:
    left: Node
    right: Node
    token: Token

    def __init__(
        self, token: Token = None, left: Node = None, right: Node = None
    ) -> None:
        self.token = token
        self.left = left
        self.right = right

    @override
    def __str__(self) -> str:
        return f"{self.token, self.left, self.right}"

    @override
    def __repr__(self) -> str:
        return f"Node(root={self.token}, left={self.left}, right={self.right})"

    @override
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Node):
            return (
                self.token == value.token
                and self.left == value.left
                and self.right == value.right
            )
        return False


class AbstractSyntaxTree:
    root: Node
    code: list[Node]
    keyword_precedence: dict[str, int]

    def __init__(self, root: Node = None) -> None:
        self.root = root
        self.code = []
        self.keyword_precedence = {
            "=": 5,
            "if": 4,
            "while": 3,
            "var": 2,
            "<=": 1,
            "<": 1,
            ">=": 1,
            ">": 1,
            "!=": 1,
        }

    def parse(self, file_path: str):
        if not isfile(file_path) or not file_path.endswith(SOURCE_CODE_FILE_EXTENSION):
            raise FileWrongTypeError(
                f"File {file_path} is not a file or is not of {SOURCE_CODE_FILE_EXTENSION} extension"
            )
        tokenizer = Tokenizer()
        with open(file_path) as f:
            tokens = tokenizer.tokenize(f.readline())
            syntax = self._parse_line(tokens)

    def _parse_line(self, tokens: list[Token]) -> Node:
        stack = []
        for token in tokens:
            # create precedence list for keywords
            # and create tree based on that
            pass

    @override
    def __str__(self) -> str:
        return f"{self.root}"

    @override
    def __repr__(self) -> str:
        return f"AbstractSyntaxTree({self.root})"

    @override
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, AbstractSyntaxTree):
            return self.root == value.root
        return False
