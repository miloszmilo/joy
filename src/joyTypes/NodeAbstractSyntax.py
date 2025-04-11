from typing import override


class NodeAbstractSyntax:
    def __init__(
        self,
        value: str = "",
    ):
        self.value = value
        self.left_child = None
        self.right_child = None

    def insert_left_child(self, left_child):
        self.left_child: NodeAbstractSyntax | None = left_child

    def insert_right_child(self, right_child):
        self.right_child: NodeAbstractSyntax | None = right_child

    @override
    def __str__(self) -> str:
        return f"Node({self.value},{self.left_child}, {self.right_child})"

    @override
    def __repr__(self) -> str:
        return f"NodeAbstractSyntax(value={self.value}, left_child={self.left_child}, right_child={self.right_child})"

    @override
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, NodeAbstractSyntax):
            return (
                self.value == value.value
                and self.left_child == value.left_child
                and self.right_child == value.right_child
            )
        return False
