import pytest

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.joyTypes.NodeAbstractSyntax import NodeAbstractSyntax


def test_no_required_semicolon():
    ast = AbstractSyntaxTree()
    with pytest.raises(SyntaxError, match="Line var x = 2"):
        ast.create_from("var x = 2")


def test_simple_addition():
    result = AbstractSyntaxTree()
    result.create_from("2 + 2")

    root: NodeAbstractSyntax = NodeAbstractSyntax("+")
    root.insert_left_child(NodeAbstractSyntax("2"))
    root.insert_right_child(NodeAbstractSyntax("2"))
    expected_result = AbstractSyntaxTree(root)

    assert result == expected_result


def test_simple_multiplication():
    result = AbstractSyntaxTree()
    result.create_from("2 * 2")

    root: NodeAbstractSyntax = NodeAbstractSyntax("*")
    root.insert_left_child(NodeAbstractSyntax("2"))
    root.insert_right_child(NodeAbstractSyntax("2"))
    expected_result = AbstractSyntaxTree(root)

    assert result == expected_result


def test_complex_math():
    result = AbstractSyntaxTree()
    result.create_from("2 * 2 + 2 / 2")

    root: NodeAbstractSyntax = NodeAbstractSyntax("*")
    root.insert_left_child(NodeAbstractSyntax("2"))
    root.insert_right_child(NodeAbstractSyntax("2"))

    expected_result = AbstractSyntaxTree(root)

    assert result == expected_result


def test_new_var():
    result = AbstractSyntaxTree()
    result.create_from("var x = 2;")

    root: NodeAbstractSyntax = NodeAbstractSyntax("=")
    root.insert_left_child(NodeAbstractSyntax("var"))
    root.insert_right_child(NodeAbstractSyntax("2"))
    root.left_child.insert_left_child(NodeAbstractSyntax("x"))
    root.right_child.insert_right_child(NodeAbstractSyntax(";"))
    expected_result = AbstractSyntaxTree(root)

    assert result == expected_result
