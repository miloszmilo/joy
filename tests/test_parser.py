import pytest
from src.joyTypes.Token import Token, TokenType
from src.parser import Parser


def test_match_keyword():
    parser: Parser = Parser(tokens=[Token("if", TokenType.KEYWORD)])
    assert parser.match(TokenType.KEYWORD, "if"), "should match if keyword"


def test_match_operator():
    parser: Parser = Parser(tokens=[Token("", TokenType.OPERATOR)])
    assert parser.match(TokenType.OPERATOR), "should match operator"


def test_match_eof():
    parser: Parser = Parser(tokens=[Token("", TokenType.EOF)])
    assert parser.match(TokenType.EOF), "should match EOF"


def test_consume_empty():
    parser: Parser = Parser()
    with pytest.raises(IndexError):
        parser.consume(TokenType.KEYWORD)


def test_consume_wrong():
    parser: Parser = Parser(tokens=[Token("x", TokenType.SYMBOL)])
    with pytest.raises(SyntaxError):
        parser.consume(TokenType.KEYWORD)


def test_parse_if():
    parser: Parser = Parser(
        tokens=[
            Token("(", TokenType.PARENTHESIS_OPEN),
            Token("3", TokenType.NUMBER),
            Token("<", TokenType.COMPARISON_OPERATOR),
            Token("4", TokenType.NUMBER),
            Token(")", TokenType.PARENTHESIS_CLOSE),
            Token("{", TokenType.SCOPE_OPEN),
            Token("}", TokenType.SCOPE_CLOSE),
            Token("EOF", TokenType.EOF),
        ]
    )
    parser.parse_if_statement()
