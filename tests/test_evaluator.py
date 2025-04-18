from collections import deque
import pytest

from src.evaluator import (
    MAX_PRECEDENCE,
    Evaluator,
)
from src.exceptions.ExpressionError import ExpressionError
from src.joyTypes.Symbol import Symbol, SymbolType


def test_rpn_notation():
    result = Evaluator()
    expr = "1 + 2 * 4 - 3"
    rpn = result._create_rpn_from(expr)

    expected_result = deque(
        [
            Symbol("1", SymbolType.NUMBER, 0),
            Symbol("2", SymbolType.NUMBER, 0),
            Symbol("4", SymbolType.NUMBER, 0),
            Symbol("*", SymbolType.OPERATOR),
            Symbol("+", SymbolType.OPERATOR),
            Symbol("3", SymbolType.NUMBER, 0),
            Symbol("-", SymbolType.OPERATOR),
        ]
    )

    assert rpn == expected_result, f"should solve RPN from {expr} to {expected_result}"


def test_simple_add_mul_subtract():
    result = Evaluator()
    expr = "1 + 2 * 4 - 3"
    rpn = result._create_rpn_from(expr)
    result = result._solve_rpn(rpn)

    expected_result = 6

    assert result == expected_result, f"should solve RPN from {expr}"


def test_simple_parenthesis_end():
    result = Evaluator()
    expr = "1 + 2 * (4 - 3)"
    rpn = result._create_rpn_from(expr)
    result = result._solve_rpn(rpn)

    expected_result = 3

    assert result == expected_result, (
        f"should solve RPN from {expr} to {expected_result}"
    )


def test_simple_parenthesis_start():
    result = Evaluator()
    expr = "(1 + 2) * 4 - 3"
    rpn = result._create_rpn_from(expr)
    result = result._solve_rpn(rpn)

    expected_result = 9

    assert result == expected_result, (
        f"should solve RPN from {expr} to {expected_result}"
    )


def test_multiple_parenthesis():
    result = Evaluator()
    expr = "(1 + 2) * (((4 - 3)-2))"
    rpn = result._create_rpn_from(expr)
    result = result._solve_rpn(rpn)

    expected_result = -3

    assert result == expected_result, (
        f"should solve RPN from {expr} to {expected_result}"
    )


def test_invalid_expression():
    result = Evaluator()
    expr = "(1 + 2) * 4 -"

    with pytest.raises(ExpressionError, match="Expression invalid"):
        rpn = result._create_rpn_from(expr)
        result = result._solve_rpn(rpn)


def test_negative_numbers():
    result = Evaluator()
    expr = "1 + 2 * - 4 - 3"
    rpn = result._create_rpn_from(expr)

    expected_rpn = deque(
        [
            Symbol("1", SymbolType.NUMBER, 0),
            Symbol("2", SymbolType.NUMBER, 0),
            Symbol("4", SymbolType.NUMBER, 0),
            Symbol("-", SymbolType.OPERATOR, 1, MAX_PRECEDENCE),
            Symbol("*", SymbolType.OPERATOR),
            Symbol("+", SymbolType.OPERATOR),
            Symbol("3", SymbolType.NUMBER, 0),
            Symbol("-", SymbolType.OPERATOR),
        ]
    )
    assert rpn == expected_rpn, f"should screate RPN from {expr} to {expected_rpn}"

    result = result._solve_rpn(rpn)

    expected_result = -10

    assert result == expected_result, (
        f"should solve RPN from {expr} to {expected_result}"
    )


def test_negative_numbers():
    result = Evaluator()
    expr = "-1 + 2 *- 4 - 3"
    rpn = result._create_rpn_from(expr)

    expected_rpn = deque(
        [
            Symbol("1", SymbolType.NUMBER, 0),
            Symbol("-", SymbolType.OPERATOR, 1, MAX_PRECEDENCE),
            Symbol("2", SymbolType.NUMBER, 0),
            Symbol("4", SymbolType.NUMBER, 0),
            Symbol("-", SymbolType.OPERATOR, 1, MAX_PRECEDENCE),
            Symbol("*", SymbolType.OPERATOR),
            Symbol("+", SymbolType.OPERATOR),
            Symbol("3", SymbolType.NUMBER, 0),
            Symbol("-", SymbolType.OPERATOR),
        ]
    )
    assert rpn == expected_rpn, f"should screate RPN from {expr} to {expected_rpn}"

    result = result._solve_rpn(rpn)

    expected_result = -12

    assert result == expected_result, (
        f"should solve RPN from {expr} to {expected_result}"
    )


def test_negative_numbers_complex():
    result = Evaluator()
    expr = "-((1 + 2)/((6*-7)+(7*-4)/2)-3)"
    rpn = result._create_rpn_from(expr)

    result = result._solve_rpn(rpn)

    expected_result = 3.0535714285714284

    assert result == expected_result, (
        f"should solve RPN from {expr} to {expected_result}"
    )


def test_evaluate():
    result = Evaluator()
    expr = "2+4+6+8-4*3-3*4-1/3*2"
    result = result.evaluate(expr)

    expected_result = -4.666666666666667

    assert result == expected_result, (
        f"should solve RPN from {expr} to {expected_result}"
    )
