import pytest

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.joyTypes.NodeAbstractSyntax import NodeAbstractSyntax


def test_no_required_tokens():
    ast = AbstractSyntaxTree()
    with pytest.raises(SyntaxError, match="Line var x = 2"):
        ast.create_from("var x = 2")


def test_new_var():
    result = AbstractSyntaxTree()
    result.create_from("var x = 2;")

    root: NodeAbstractSyntax = NodeAbstractSyntax("=")
    root.insert_left_child(NodeAbstractSyntax("var"))
    root.insert_right_child(NodeAbstractSyntax("2"))
    root.left_child.insert_left_child(NodeAbstractSyntax("x"))
    root.right_child.insert_right_child(NodeAbstractSyntax(";"))
    expected_result = AbstractSyntaxTree(root)
    # assert ast.create_from("var x = 2;") == root
    assert result == expected_result
