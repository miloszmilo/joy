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
    expr = "1 + 2 * 4 - 3"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    result = Evaluator(tokens)
    rpn = result._create_rpn_from_tokens()

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
    expr = "1 + 2 * 4 - 3"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    result = Evaluator(tokens)
    rpn = result._create_rpn_from_tokens()
    result = result._solve_rpn(rpn)

    expected_result = 6

    assert result == expected_result, f"should solve RPN from {expr}"


def test_simple_parenthesis_end():
    expr = "1 + 2 * (4 - 3)"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    result = Evaluator(tokens)
    rpn = result._create_rpn_from_tokens()
    result = result._solve_rpn(rpn)

    expected_result = 3

    assert result == expected_result, (
        f"should solve RPN from {expr} to {expected_result}"
    )


def test_simple_parenthesis_start():
    expr = "(1 + 2) * 4 - 3"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    result = Evaluator(tokens)
    rpn = result._create_rpn_from_tokens()
    result = result._solve_rpn(rpn)

    expected_result = 9

    assert result == expected_result, (
        f"should solve RPN from {expr} to {expected_result}"
    )


def test_multiple_parenthesis():
    expr = "(1 + 2) * (((4 - 3)-2))"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    result = Evaluator(tokens)
    rpn = result._create_rpn_from_tokens()
    result = result._solve_rpn(rpn)

    expected_result = -3

    assert result == expected_result, (
        f"should solve RPN from {expr} to {expected_result}"
    )


def test_invalid_expression():
    expr = "(1 + 2) * 4 -"

    with pytest.raises(ExpressionError, match="Expression invalid"):
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(expr)
        result = Evaluator(tokens)
        rpn = result._create_rpn_from_tokens()
        result = result._solve_rpn(rpn)


def test_negative_numbers():
    expr = "1 + 2 * - 4 - 3"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    result = Evaluator(tokens)
    rpn = result._create_rpn_from_tokens()

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
    expr = "-((1 + 2)/((6*-7)+(7*-4)/2)-3)"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    result = Evaluator(tokens)
    rpn = result._create_rpn_from_tokens()

    result = result._solve_rpn(rpn)

    expected_result = 3.0535714285714284

    assert result == expected_result, (
        f"should solve RPN from {expr} to {expected_result}"
    )


def test_evaluate():
    expr = "2+4+6+8-4*3-3*4-1/3*2"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    result = Evaluator(tokens).solve()

    expected_result = -4.666666666666667

    assert result == expected_result, (
        f"should solve RPN from {expr} to {expected_result}"
    )


def test_rpn_notation_tokens():
    expr = "1 + 2 * 4 - 3"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    result = Evaluator(tokens)
    rpn = result._create_rpn_from_tokens()

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
    expr = "0x1 + 0b10 * 4 - 3.0"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    eval = Evaluator(tokens)
    result = eval.solve()

    expected_result = 6
    assert result == expected_result, (
        f"should solve RPN from {expr} to {expected_result}"
    )


def test_functions_fail():
    expr = "f(1,2)"
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(expr)
    eval = Evaluator(tokens)
    with pytest.raises(ExpressionError):
        _res = eval.solve()
