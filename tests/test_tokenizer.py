from multiprocessing.sharedctypes import Value
from src.exceptions.TokenizerValueError import TokenizerValueError
from src.joyTypes.Token import Token, TokenType
from src.tokenizer import Tokenizer

import pytest


def test_tokenizer_simple():
    tokenizer = Tokenizer()
    expr = "100+(20*40)-30000 "
    result = tokenizer.tokenize(expr)
    expected_result = [
        Token("100", TokenType.NUMBER, 100.0),
        Token("+", TokenType.OPERATOR),
        Token("(", TokenType.PARENTHESIS_OPEN),
        Token("20", TokenType.NUMBER, 20.0),
        Token("*", TokenType.OPERATOR),
        Token("40", TokenType.NUMBER, 40.0),
        Token(")", TokenType.PARENTHESIS_CLOSE),
        Token("-", TokenType.OPERATOR),
        Token("30000", TokenType.NUMBER, 30000.0),
    ]

    assert result == expected_result, f"should tokenizer {expr} got {result}"


def test_tokenizer_floats():
    tokenizer = Tokenizer()
    expr = "1.00+(2.0*40)-30.000 "
    result = tokenizer.tokenize(expr)
    expected_result = [
        Token("1.00", TokenType.NUMBER, 1.0),
        Token("+", TokenType.OPERATOR),
        Token("(", TokenType.PARENTHESIS_OPEN),
        Token("2.0", TokenType.NUMBER, 2.0),
        Token("*", TokenType.OPERATOR),
        Token("40", TokenType.NUMBER, 40.0),
        Token(")", TokenType.PARENTHESIS_CLOSE),
        Token("-", TokenType.OPERATOR),
        Token("30.000", TokenType.NUMBER, 30.000),
    ]

    assert result == expected_result, f"should tokenizer {expr} got {result}"


def test_tokenizer_multiple_dots_float():
    tokenizer = Tokenizer()
    expr = "1.0.0+(2.0*40)-30.00.0 "
    with pytest.raises(TokenizerValueError):
        _result = tokenizer.tokenize(expr)


def test_tokenizer_start_with_dot():
    tokenizer = Tokenizer()
    expr = ".1+(2.0*40)-30.000 "
    result = tokenizer.tokenize(expr)
    expected_result = [
        Token(".1", TokenType.NUMBER, 0.1),
        Token("+", TokenType.OPERATOR),
        Token("(", TokenType.PARENTHESIS_OPEN),
        Token("2.0", TokenType.NUMBER, 2.0),
        Token("*", TokenType.OPERATOR),
        Token("40", TokenType.NUMBER, 40.0),
        Token(")", TokenType.PARENTHESIS_CLOSE),
        Token("-", TokenType.OPERATOR),
        Token("30.000", TokenType.NUMBER, 30.000),
    ]

    assert result == expected_result, f"should tokenizer {expr} got {result}"


def test_tokenizer_letters_in_floats():
    tokenizer = Tokenizer()
    expr = "1.00+(2.0*40)-30.abcd00.efgh0 "
    with pytest.raises(TokenizerValueError):
        _result = tokenizer.tokenize(expr)


def test_tokenizer_letters_before_float():
    tokenizer = Tokenizer()
    expr = "1.00+(2.0*40)-abc30.00.0 "
    result = tokenizer.tokenize(expr)

    expected_result = [
        Token("1.00", TokenType.NUMBER, 1.00),
        Token("+", TokenType.OPERATOR),
        Token("(", TokenType.PARENTHESIS_OPEN),
        Token("2.0", TokenType.NUMBER, 2.0),
        Token("*", TokenType.OPERATOR),
        Token("40", TokenType.NUMBER, 40.0),
        Token(")", TokenType.PARENTHESIS_CLOSE),
        Token("-", TokenType.OPERATOR),
        Token("abc30.00.0", TokenType.SYMBOL),
    ]

    assert result == expected_result, f"should tokenizer {expr} got {result}"


def test_tokenizer_symbol_space_float():
    tokenizer = Tokenizer()
    expr = "abc 1.0 "
    result = tokenizer.tokenize(expr)

    expected_result = [
        Token("abc", TokenType.SYMBOL),
        Token("1.0", TokenType.NUMBER, 1.0),
    ]

    assert result == expected_result, f"should tokenizer {expr} got {result}"


def test_tokenizer_hex_and_binary():
    tokenizer = Tokenizer()
    expr = "0b0110 0xABC34 23.176 9 "
    result = tokenizer.tokenize(expr)

    expected_result = [
        Token("0b0110", TokenType.NUMBER, float(int("0110", 2))),
        Token("0xABC34", TokenType.NUMBER, float(int("ABC34", 16))),
        Token("23.176", TokenType.NUMBER, 23.176),
        Token("9", TokenType.NUMBER, 9),
    ]

    assert result == expected_result, f"should tokenizer {expr} got {result}"


def test_tokenizer_malformed_hex():
    tokenizer = Tokenizer()
    expr = "0b0110 0xABmC34 23.176 9 "
    with pytest.raises(TokenizerValueError):
        _result = tokenizer.tokenize(expr)


def test_tokenizer_scope_simple():
    tokenizer = Tokenizer()
    expr = "{0b0110 0xABC34 23.176 9} "
    result = tokenizer.tokenize(expr)

    expected_result = [
        Token("{", TokenType.SCOPE_OPEN),
        Token("0b0110", TokenType.NUMBER, float(int("0110", 2))),
        Token("0xABC34", TokenType.NUMBER, float(int("ABC34", 16))),
        Token("23.176", TokenType.NUMBER, 23.176),
        Token("9", TokenType.NUMBER, 9),
        Token("}", TokenType.SCOPE_CLOSE),
    ]

    assert result == expected_result, f"should tokenizer {expr} got {result}"


def test_tokenizer_scope_unbalanced():
    tokenizer = Tokenizer()
    expr = "{0b0110 0xABC34 23.176 9 "
    with pytest.raises(TokenizerValueError):
        _result = tokenizer.tokenize(expr)


def test_tokenizer_scope_unbalanced_closing():
    tokenizer = Tokenizer()
    expr = "0b0110 0xABC34 23.176 9} "
    with pytest.raises(TokenizerValueError):
        _result = tokenizer.tokenize(expr)
