from src.exceptions.TokenizerValueError import TokenizerValueError
from src.joyTypes.Token import Token
from src.tokenizer import Tokenizer

import pytest


def test_variable():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("x") == [Token("x", "variable")], (
        "should tokenize x to variable"
    )


def test_number():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("3") == [Token("3", "number")], (
        "should tokenize 3 to number"
    )


def test_complex_number():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("123456789") == [Token("123456789", "number")], (
        "should tokenize 123456789 to number"
    )


def test_float():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("0.1234") == [Token("0.1234", "number")], (
        "should tokenize 0.1234 to number"
    )


def test_invalid_float():
    tokenizer = Tokenizer()
    with pytest.raises(
        TokenizerValueError, match="Token 0.1234e is not a float but contains '.'"
    ):
        _ = tokenizer.to_tokens("0.1234e")


def test_equals():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("=") == [Token("=", "equals")], (
        "should tokenize = to equals"
    )


def test_two_numbers():
    tokenizer = Tokenizer()
    res = tokenizer.to_tokens("12 34")
    assert tokenizer.to_tokens("12 34") == [
        Token("12", "number"),
        Token("34", "number"),
    ], "should tokenize 12 to number and 34 to number"


def test_two_numbers_many_spaces():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("12       34") == [
        Token("12", "number"),
        Token("34", "number"),
    ], "should tokenize 12 to number, 34 to number and split on many spaces"


def test_three_numbers():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("12 34   56") == [
        Token("12", "number"),
        Token("34", "number"),
        Token("56", "number"),
    ], "should tokenize 12 to number, 34 to number and 56 to number"


def test_ten_numbers():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("12 34 56 12 34 56 12 34 56 12") == [
        Token("12", "number"),
        Token("34", "number"),
        Token("56", "number"),
        Token("12", "number"),
        Token("34", "number"),
        Token("56", "number"),
        Token("12", "number"),
        Token("34", "number"),
        Token("56", "number"),
        Token("12", "number"),
    ], (
        "should tokenize 12 to number, 34 to number and 56 to number, then 12 to number, 34 to number, 56 to number, then 12 to number, 34 to number, 56 to number and finally 12 to number"
    )


def test_two_numbers_and_float():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("12 34 0.12") == [
        Token("12", "number"),
        Token("34", "number"),
        Token("0.12", "number"),
    ], "should tokenize 12 to number, 34 to number and 0.12 to number"


def test_two_numbers_and_variable():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("12 34 bigvariablename") == [
        Token("12", "number"),
        Token("34", "number"),
        Token("bigvariablename", "variable"),
    ], "should tokenize 12 to number, 34 to number and 0.12 to number"


def test_plus():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("=") == [
        Token("=", "equals"),
    ], "should tokenize = to equals"


def test_plus():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("+") == [
        Token("+", "plus"),
    ], "should tokenize + to plus"


def test_minus():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("-") == [
        Token("-", "minus"),
    ], "should tokenize - to minus"


def test_times():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("*") == [
        Token("*", "times"),
    ], "should tokenize * to times"


def test_slash():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("/") == [
        Token("/", "slash"),
    ], "should tokenize / to slash"


def test_modulo():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("%") == [
        Token("%", "modulo"),
    ], "should tokenize % to modulo"


def test_if():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("if") == [
        Token("if", "ifsym"),
    ], "should tokenize if to ifsym"


def test_else():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("else") == [
        Token("else", "elsesym"),
    ], "should tokenize else to elsesym"


def test_while():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("while") == [
        Token("while", "whilesym"),
    ], "should tokenize while to whilesym"


def test_print():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("print") == [
        Token("print", "printsym"),
    ], "should tokenize print to printsym"


def test_var():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("var") == [
        Token("var", "varsym"),
    ], "should tokenize var to varsym"


def test_semicol():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens(";") == [
        Token(";", "semicol"),
    ], "should tokenize ; to semicol"


def test_plus_two_numbers():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("2 + 2") == [
        Token("2", "number"),
        Token("+", "plus"),
        Token("2", "number"),
    ], "should tokenize 2 + 2 to 2 number, + plus and 2 number"


def test_minus_two_numbers():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("2 - 2") == [
        Token("2", "number"),
        Token("-", "minus"),
        Token("2", "number"),
    ], "should tokenize 2 - 2 to 2 number, - minus and 2 number"


def test_quote():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens('"') == [
        Token('"', "quote"),
    ], 'should tokenize " to quote'


def test_less_than():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("<") == [
        Token("<", "less_than"),
    ], "should tokenize < to less_than"


def test_greater_than():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens(">") == [
        Token(">", "greater_than"),
    ], "should tokenize > to greater_than"


def test_less_than_or_equal():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("<=") == [
        Token("<=", "less_than_or_equal"),
    ], "should tokenize <= to less_than_or_equal"


def test_greater_than_or_equal():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens(">=") == [
        Token(">=", "greater_than_or_equal"),
    ], "should tokenize >= to greater_than_or_equal"


def test_equal_to():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("==") == [
        Token("==", "equal_to"),
    ], "should tokenize == to equal_to"


def test_not_equal_to():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("!=") == [
        Token("!=", "not_equal_to"),
    ], "should tokenize != to not_equal_to"


def test_lparen():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("(") == [
        Token("(", "lparen"),
    ], "should tokenize ( to lparen"


def test_rparen():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens(")") == [
        Token(")", "rparen"),
    ], "should tokenize ) to rparen"


def test_curly_lparen():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("{") == [
        Token("{", "curly_lparen"),
    ], "should tokenize { to curly_lparen"


def test_curly_rparen():
    tokenizer = Tokenizer()
    assert tokenizer.to_tokens("}") == [
        Token("}", "curly_rparen"),
    ], "should tokenize } to curly_rparen"
