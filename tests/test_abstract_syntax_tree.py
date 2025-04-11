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

    assert result == expected_result, "should create AST from 2 + 2"


def test_simple_multiplication():
    result = AbstractSyntaxTree()
    result.create_from("2 * 2")

    root: NodeAbstractSyntax = NodeAbstractSyntax("*")
    root.insert_left_child(NodeAbstractSyntax("2"))
    root.insert_right_child(NodeAbstractSyntax("2"))
    expected_result = AbstractSyntaxTree(root)

    assert result == expected_result, "should create AST from 2 * 2"


def test_multiple_and_add():
    result = AbstractSyntaxTree()
    result.create_from("2 * 2 + 4")

    root: NodeAbstractSyntax = NodeAbstractSyntax("+")
    root.insert_left_child(NodeAbstractSyntax("*"))
    root.insert_right_child(NodeAbstractSyntax("4"))
    root.left_child.insert_left_child(NodeAbstractSyntax("2"))
    root.left_child.insert_right_child(NodeAbstractSyntax("2"))
    expected_result = AbstractSyntaxTree(root)

    assert result == expected_result, "should create AST from 2 * 2 + 4"


def test_add_and_multiple():
    result = AbstractSyntaxTree()
    result.create_from("2 + 2 * 4")

    root: NodeAbstractSyntax = NodeAbstractSyntax("+")
    root.insert_left_child(NodeAbstractSyntax("2"))
    root.insert_right_child(NodeAbstractSyntax("*"))
    root.right_child.insert_left_child(NodeAbstractSyntax("2"))
    root.right_child.insert_right_child(NodeAbstractSyntax("4"))
    expected_result = AbstractSyntaxTree(root)

    print("Got result:", result)
    assert result == expected_result, "should create AST from 2 + 2 * 4"


def test_complex_math():
    result = AbstractSyntaxTree()
    result.create_from("2 * 2 + 2 / 2 - 2")

    root: NodeAbstractSyntax = NodeAbstractSyntax("+")
    root.insert_left_child(NodeAbstractSyntax("*"))
    root.left_child.insert_left_child(NodeAbstractSyntax("2"))
    root.left_child.insert_right_child(NodeAbstractSyntax("2"))
    root.insert_right_child(NodeAbstractSyntax("/"))
    root.right_child.insert_left_child(NodeAbstractSyntax("2"))
    root.right_child.insert_right_child(NodeAbstractSyntax("2"))

    expected_result = AbstractSyntaxTree(root)
    print("Got result:", result)
    print("Expected:", expected_result)

    assert result == expected_result, "should handle complex formulas 2 * 2 + 2 / 2"


def test_parenthesis():
    result = AbstractSyntaxTree()
    result.create_from("(2 + 2)")

    root: NodeAbstractSyntax = NodeAbstractSyntax("+")
    root.insert_left_child(NodeAbstractSyntax("2"))
    root.insert_right_child(NodeAbstractSyntax("2"))
    expected_result = AbstractSyntaxTree(root)

    print("Got result:", result)
    assert result == expected_result, "should create AST from (2 + 2)"


def test_complex_parenthesis():
    result = AbstractSyntaxTree()
    result.create_from("(2 + 2) * 2 / (2 - 2)")

    root: NodeAbstractSyntax = NodeAbstractSyntax("+")
    root.insert_left_child(NodeAbstractSyntax("2"))
    root.insert_right_child(NodeAbstractSyntax("2"))
    expected_result = AbstractSyntaxTree(root)

    print("Got result:", result)
    assert result == expected_result, "should create AST from (2 + 2)"


def test_new_var():
    result = AbstractSyntaxTree()
    result.create_from("var x = 2;")

    root: NodeAbstractSyntax = NodeAbstractSyntax("=")
    root.insert_left_child(NodeAbstractSyntax("var"))
    root.insert_right_child(NodeAbstractSyntax("2"))
    root.left_child.insert_left_child(NodeAbstractSyntax("x"))
    root.right_child.insert_right_child(NodeAbstractSyntax(";"))
    expected_result = AbstractSyntaxTree(root)

    assert result == expected_result, "should handle creating variables"
