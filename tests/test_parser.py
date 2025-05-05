import pytest
from src.joyTypes.AST_Nodes import (
    Comparison,
    IfStatement,
    NumberLiteral,
    PrintStatement,
    VariableDeclaration,
    WhileStatement,
)
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
            Token("if", TokenType.KEYWORD),
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
    result = parser.parse_statement()
    assert isinstance(result, IfStatement)
    expected_result = IfStatement(
        Comparison(
            Token("3", TokenType.NUMBER),
            Token("<", TokenType.COMPARISON_OPERATOR),
            Token("4", TokenType.NUMBER),
        )
    )
    assert result == expected_result


def test_parse_if_body():
    parser: Parser = Parser(
        tokens=[
            Token("if", TokenType.KEYWORD),
            Token("(", TokenType.PARENTHESIS_OPEN),
            Token("3", TokenType.NUMBER),
            Token("<", TokenType.COMPARISON_OPERATOR),
            Token("4", TokenType.NUMBER),
            Token(")", TokenType.PARENTHESIS_CLOSE),
            Token("{", TokenType.SCOPE_OPEN),
            Token("var", TokenType.KEYWORD),
            Token("x", TokenType.SYMBOL),
            Token("=", TokenType.ASSIGNMENT),
            Token("4", TokenType.NUMBER),
            Token("}", TokenType.SCOPE_CLOSE),
            Token("EOF", TokenType.EOF),
        ]
    )
    result = parser.parse_statement()
    assert isinstance(result, IfStatement)


def test_parse_var():
    parser: Parser = Parser(
        tokens=[
            Token("var", TokenType.KEYWORD),
            Token("x", TokenType.SYMBOL),
            Token("=", TokenType.ASSIGNMENT),
            Token("4", TokenType.NUMBER, 4),
            Token("EOF", TokenType.EOF),
        ]
    )
    result = parser.parse_statement()
    assert isinstance(result, VariableDeclaration)
    expected_result = VariableDeclaration("x", NumberLiteral(4))
    assert result == expected_result


def test_parse_while():
    parser: Parser = Parser(
        tokens=[
            Token("while", TokenType.KEYWORD),
            Token("(", TokenType.PARENTHESIS_OPEN),
            Token("3", TokenType.NUMBER),
            Token(">", TokenType.COMPARISON_OPERATOR),
            Token("4", TokenType.NUMBER),
            Token(")", TokenType.PARENTHESIS_CLOSE),
            Token("EOF", TokenType.EOF),
        ]
    )
    result = parser.parse_statement()
    assert isinstance(result, WhileStatement)
    expected_result = WhileStatement(
        Comparison(
            Token("3", TokenType.NUMBER),
            Token(">", TokenType.COMPARISON_OPERATOR),
            Token("4", TokenType.NUMBER),
        ),
        None,
    )
    assert result == expected_result


def test_parse_while_body():
    parser: Parser = Parser(
        tokens=[
            Token("while", TokenType.KEYWORD),
            Token("(", TokenType.PARENTHESIS_OPEN),
            Token("3", TokenType.NUMBER),
            Token(">", TokenType.COMPARISON_OPERATOR),
            Token("4", TokenType.NUMBER),
            Token(")", TokenType.PARENTHESIS_CLOSE),
            Token("{", TokenType.SCOPE_OPEN),
            Token("}", TokenType.SCOPE_CLOSE),
            Token("EOF", TokenType.EOF),
        ]
    )
    result = parser.parse_statement()
    assert isinstance(result, WhileStatement)
    expected_result = WhileStatement(
        Comparison(
            Token("3", TokenType.NUMBER),
            Token(">", TokenType.COMPARISON_OPERATOR),
            Token("4", TokenType.NUMBER),
        ),
        None,
    )
    assert result == expected_result

def test_parse_print():
    parser: Parser = Parser(
        tokens=[
            Token("print", TokenType.KEYWORD),
            Token("(", TokenType.PARENTHESIS_OPEN),
            Token("Hello, World!", TokenType.STRING),
            Token(")", TokenType.PARENTHESIS_CLOSE),
            Token("EOF", TokenType.EOF),
        ]
    )
    result = parser.parse_statement()
    assert isinstance(result, PrintStatement)
    expected_result = PrintStatement("Hello, World!")
    assert result == expected_result
