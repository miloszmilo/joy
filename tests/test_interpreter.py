from src.interpreter import Interpreter, check_condition
from src.joyTypes.AST_Nodes import (
    Comparison,
    EmptyExpression,
    Expression,
    IfStatement,
    PrintStatement,
    VariableAccess,
    WhileStatement,
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
    interpreter = Interpreter()
    interpreter.visit_node(node)
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
    interpreter = Interpreter()
    interpreter.visit_node(node)
    assert check_condition(node) == False


def test_while_variable():
    node = WhileStatement(
        Comparison(
            Token("x", TokenType.SYMBOL, 1),
            Token(">", TokenType.COMPARISON_OPERATOR),
            Token("2", TokenType.NUMBER, 2),
        ),
        VariableAccess("x"),
    )
