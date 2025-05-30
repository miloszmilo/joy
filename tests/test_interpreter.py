from collections import deque
from src.context import EvaluatorContext, InterpreterContext
from src.interpreter import Interpreter, check_condition
from src.joyTypes.AST_Nodes import (
    Comparison,
    EmptyExpression,
    IfStatement,
    MathExpression,
    NumberLiteral,
    PrintStatement,
    VariableAccess,
    VariableAssignment,
    WhileStatement,
)
from src.joyTypes.Symbol import Symbol, SymbolType
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
    assert check_condition(node)


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
    assert not check_condition(node)


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
    assert not check_condition(node)


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
    assert not check_condition(node)


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
    assert check_condition(node)


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
    assert check_condition(node)


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
    assert not check_condition(node)


def test_while_variable():
    context = InterpreterContext(
        {"x": 1},
    )
    node = WhileStatement(
        Comparison(
            Token("x", TokenType.SYMBOL, 1),
            Token("<", TokenType.COMPARISON_OPERATOR),
            Token("2", TokenType.NUMBER, 2),
        ),
        # x = x - 1
        # MathExpression(VariableAccess("x"), MathExpression(VariableAccess("x"), Number(1), "-"))
        # Maybe solve it instead?
        VariableAssignment("x", NumberLiteral(2)),
    )
    interpreter = Interpreter(context)
    interpreter.visit_node(node)
    assert check_condition(node)

    assert context.variables["x"] == 2
