from src.interpreter import check_condition, interpret, visit_node
from src.joyTypes.AST_Nodes import (
    Comparison,
    EmptyExpression,
    IfStatement,
    PrintStatement,
)
from src.joyTypes.Token import Token, TokenType


def test_condition():
    node = IfStatement(
        Comparison(
            Token("1", TokenType.NUMBER, 1),
            Token("<", TokenType.COMPARISON_OPERATOR),
            Token("2", TokenType.NUMBER, 2),
        ),
        EmptyExpression(),
        EmptyExpression(),
    )
    assert check_condition(node) == True


def test_condition_false():
    node = IfStatement(
        Comparison(
            Token("1", TokenType.NUMBER, 1),
            Token(">", TokenType.COMPARISON_OPERATOR),
            Token("2", TokenType.NUMBER, 2),
        ),
        EmptyExpression(),
        EmptyExpression(),
    )
    assert check_condition(node) == False


def test_condition_equals():
    node = IfStatement(
        Comparison(
            Token("1", TokenType.NUMBER, 1),
            Token("==", TokenType.COMPARISON_OPERATOR),
            Token("2", TokenType.NUMBER, 2),
        ),
        EmptyExpression(),
        EmptyExpression(),
    )
    assert check_condition(node) == False


def test_condition_greater_equal():
    node = IfStatement(
        Comparison(
            Token("1", TokenType.NUMBER, 1),
            Token(">=", TokenType.COMPARISON_OPERATOR),
            Token("2", TokenType.NUMBER, 2),
        ),
        EmptyExpression(),
        EmptyExpression(),
    )
    assert check_condition(node) == False


def test_condition_less_equal():
    node = IfStatement(
        Comparison(
            Token("1", TokenType.NUMBER, 1),
            Token("<=", TokenType.COMPARISON_OPERATOR),
            Token("2", TokenType.NUMBER, 2),
        ),
        EmptyExpression(),
        EmptyExpression(),
    )
    assert check_condition(node) == True


def test_condition_body():
    node = IfStatement(
        Comparison(
            Token("1", TokenType.NUMBER, 1),
            Token("<", TokenType.COMPARISON_OPERATOR),
            Token("2", TokenType.NUMBER, 2),
        ),
        PrintStatement("We run the body"),
        EmptyExpression(),
    )
    visit_node(node)
    assert check_condition(node) == True


def test_condition_else_body():
    node = IfStatement(
        Comparison(
            Token("1", TokenType.NUMBER, 1),
            Token(">", TokenType.COMPARISON_OPERATOR),
            Token("2", TokenType.NUMBER, 2),
        ),
        EmptyExpression(),
        PrintStatement("We run the else body"),
    )
    visit_node(node)
    assert check_condition(node) == False
