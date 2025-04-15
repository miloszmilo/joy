from collections import deque
import pytest

from src.abstract_syntax_tree import AbstractSyntaxTree, Symbol, SymbolType
from src.exceptions.ExpressionError import ExpressionError
from src.joyTypes.NodeAbstractSyntax import NodeAbstractSyntax


def test_rpn_notation():
    result = AbstractSyntaxTree()
    expr = "1 + 2 * 4 - 3"
    rpn = result._create_rpn_from(expr)

    expected_result = deque(
        [
            Symbol("1", SymbolType.NUMBER),
            Symbol("2", SymbolType.NUMBER),
            Symbol("4", SymbolType.NUMBER),
            Symbol("*", SymbolType.OPERATOR),
            Symbol("+", SymbolType.OPERATOR),
            Symbol("3", SymbolType.NUMBER),
            Symbol("-", SymbolType.OPERATOR),
        ]
    )

    assert rpn == expected_result, f"should create RPN from {expr}"


def test_simple_add_mul_subtract():
    result = AbstractSyntaxTree()
    expr = "1 + 2 * 4 - 3"
    rpn = result._create_rpn_from(expr)
    result = result._solve_rpn(rpn)

    expected_result = 6

    assert result == expected_result, f"should solve RPN from {expr}"


def test_simple_parenthesis_end():
    result = AbstractSyntaxTree()
    expr = "1 + 2 * (4 - 3)"
    rpn = result._create_rpn_from(expr)
    result = result._solve_rpn(rpn)

    expected_result = 3

    assert result == expected_result, f"should solve RPN from {expr}"


def test_simple_parenthesis_start():
    result = AbstractSyntaxTree()
    expr = "(1 + 2) * 4 - 3"
    rpn = result._create_rpn_from(expr)
    result = result._solve_rpn(rpn)

    expected_result = 9

    assert result == expected_result, f"should solve RPN from {expr}"


def test_multiple_parenthesis():
    result = AbstractSyntaxTree()
    expr = "(1 + 2) * (((4 - 3)-2))"
    rpn = result._create_rpn_from(expr)
    result = result._solve_rpn(rpn)
    print(f"Got rpn {list(rpn)}")

    expected_result = -3

    assert result == expected_result, f"should solve RPN from {expr}"


def test_invalid_expression():
    result = AbstractSyntaxTree()
    expr = "(1 + 2) * 4 -"

    with pytest.raises(ExpressionError, match="expression invalid"):
        rpn = result._create_rpn_from(expr)
        result = result._solve_rpn(rpn)
