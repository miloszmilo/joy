from collections import deque
import pytest

from src.evaluator import (
    MAX_PRECEDENCE,
    Evaluator,
)
from src.exceptions.ExpressionError import ExpressionError
from src.joyTypes.Symbol import Symbol, SymbolType
from src.tokenizer import Tokenizer


def test_rpn_notation():
    result = Evaluator()
    expr = "1 + 2 * 4 - 3"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    rpn = result._create_rpn_from_tokens(tokens)

    expected_result = deque(
        [
            Symbol("1.0", SymbolType.NUMBER, 0),
            Symbol("2.0", SymbolType.NUMBER, 0),
            Symbol("4.0", SymbolType.NUMBER, 0),
            Symbol("*", SymbolType.OPERATOR),
            Symbol("+", SymbolType.OPERATOR),
            Symbol("3.0", SymbolType.NUMBER, 0),
            Symbol("-", SymbolType.OPERATOR),
        ]
    )

    assert rpn == expected_result, f"should solve RPN from {expr} to {expected_result}"


def test_simple_add_mul_subtract():
    result = Evaluator()
    expr = "1 + 2 * 4 - 3"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    rpn = result._create_rpn_from_tokens(tokens)
    result = result._solve_rpn(rpn)

    expected_result = 6

    assert result == expected_result, f"should solve RPN from {expr}"


def test_simple_parenthesis_end():
    result = Evaluator()
    expr = "1 + 2 * (4 - 3)"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    rpn = result._create_rpn_from_tokens(tokens)
    result = result._solve_rpn(rpn)

    expected_result = 3

    assert result == expected_result, (
        f"should solve RPN from {expr} to {expected_result}"
    )


def test_simple_parenthesis_start():
    result = Evaluator()
    expr = "(1 + 2) * 4 - 3"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    rpn = result._create_rpn_from_tokens(tokens)
    result = result._solve_rpn(rpn)

    expected_result = 9

    assert result == expected_result, (
        f"should solve RPN from {expr} to {expected_result}"
    )


def test_multiple_parenthesis():
    result = Evaluator()
    expr = "(1 + 2) * (((4 - 3)-2))"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    rpn = result._create_rpn_from_tokens(tokens)
    result = result._solve_rpn(rpn)

    expected_result = -3

    assert result == expected_result, (
        f"should solve RPN from {expr} to {expected_result}"
    )


def test_invalid_expression():
    result = Evaluator()
    expr = "(1 + 2) * 4 -"

    with pytest.raises(ExpressionError, match="Expression invalid"):
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(expr)
        rpn = result._create_rpn_from_tokens(tokens)
        result = result._solve_rpn(rpn)


def test_negative_numbers():
    result = Evaluator()
    expr = "1 + 2 * - 4 - 3"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    rpn = result._create_rpn_from_tokens(tokens)

    expected_rpn = deque(
        [
            Symbol("1.0", SymbolType.NUMBER, 0),
            Symbol("2.0", SymbolType.NUMBER, 0),
            Symbol("4.0", SymbolType.NUMBER, 0),
            Symbol("-", SymbolType.OPERATOR, 1, MAX_PRECEDENCE),
            Symbol("*", SymbolType.OPERATOR),
            Symbol("+", SymbolType.OPERATOR),
            Symbol("3.0", SymbolType.NUMBER, 0),
            Symbol("-", SymbolType.OPERATOR),
        ]
    )
    assert rpn == expected_rpn, f"should screate RPN from {expr} to {expected_rpn}"

    result = result._solve_rpn(rpn)

    expected_result = -10

    assert result == expected_result, (
        f"should solve RPN from {expr} to {expected_result}"
    )


def test_negative_numbers_complex():
    result = Evaluator()
    expr = "-((1 + 2)/((6*-7)+(7*-4)/2)-3)"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    rpn = result._create_rpn_from_tokens(tokens)

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


def test_rpn_notation_tokens():
    result = Evaluator()
    expr = "1 + 2 * 4 - 3"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    rpn = result._create_rpn_from_tokens(tokens)

    expected_result = deque(
        [
            Symbol("1.0", SymbolType.NUMBER, 0),
            Symbol("2.0", SymbolType.NUMBER, 0),
            Symbol("4.0", SymbolType.NUMBER, 0),
            Symbol("*", SymbolType.OPERATOR),
            Symbol("+", SymbolType.OPERATOR),
            Symbol("3.0", SymbolType.NUMBER, 0),
            Symbol("-", SymbolType.OPERATOR),
        ]
    )

    assert rpn == expected_result, f"should solve RPN from {expr} to {expected_result}"


def test_rpn_notation_complex():
    eval = Evaluator()
    expr = "0x1 + 0b10 * 4 - 3.0"
    result = eval.evaluate(expr)

    expected_result = 6
    assert result == expected_result, (
        f"should solve RPN from {expr} to {expected_result}"
    )


def test_functions():
    eval = Evaluator()
    expr = "f(1,2)"
    with pytest.raises(ExpressionError):
        _res = eval.evaluate(expr)


def test_add_with_variable():
    eval = Evaluator()
    expr = "x + 4"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    rpn = eval._create_rpn_from_tokens(tokens)
    expected_rpn = deque(
        [
            Symbol("x", SymbolType.SYMBOL, 0),
            Symbol("4.0", SymbolType.NUMBER, 0),
            Symbol("+", SymbolType.OPERATOR, 2),
        ]
    )
    assert rpn == expected_rpn, f"should create rpn from {expr} to {expected_rpn}"

    eval.variables = {"x": 3}
    result = eval.evaluate(expr)
    expected_result = 7

    assert result == expected_result


def test_variable_evaluate():
    eval = Evaluator()
    expr = "x = 4"
    with pytest.raises(ExpressionError):
        _res = eval.evaluate(expr)


def test_add_only_variables():
    eval = Evaluator()
    expr = "x + y"
    eval.variables = {"x": 4, "y": 3}
    rpn = eval.evaluate(expr)
    expected_result = 7
    assert rpn == expected_result, f"should evaluate {expr} to {expected_result}"
