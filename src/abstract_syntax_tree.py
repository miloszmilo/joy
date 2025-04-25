from __future__ import annotations
from typing import override
from src.joyTypes.Token import Token


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
        return f"{self.token.__str__()}"

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

    def __init__(self, root: Node = None) -> None:
        self.root = root

    @override
    def __str__(self) -> str:
        return f"{self.root}"

    @override
    def __repr__(self) -> str:
        return f"AbstractSyntaxTree({self.root})"
