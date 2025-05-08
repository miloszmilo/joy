from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque
from typing import Callable, override

from src.exceptions.ExpressionError import ExpressionError
from src.joyTypes.Symbol import (
    Symbol,
    SymbolType,
    binary_operators,
    keywords,
    unary_operators,
)
from src.joyTypes.Token import Token, TokenType
from src.tokenizer import Tokenizer

MAX_PRECEDENCE = 100


class Evaluator:
    operator_stack: list[Token]
    variables: dict[str, float]
    _holding_stack: deque[Symbol] = deque()
    _output_stack: deque[Symbol] = deque()
    _previous_symbol: Symbol = Symbol("0", SymbolType.NUMBER, 0)

    operations: dict[str, Callable[[float, float], float]] = {
        "!=": lambda x, y: int(x != y),
        "==": lambda x, y: int(x == y),
        "<=": lambda x, y: int(x <= y),
        "<": lambda x, y: int(x < y),
        ">=": lambda x, y: int(x >= y),
        ">": lambda x, y: int(x > y),
        "/": lambda x, y: x / y,
        "*": lambda x, y: x * y,
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
    }

    unary_operations: dict[str, Callable[[float], float]] = {
        "+": lambda x: +x,
        "-": lambda x: -x,
    }

    def __init__(
        self,
        operator_stack: list[Token] | None = None,
        variables: dict[str, float] | None = None,
    ):
        self.operator_stack = operator_stack if operator_stack else []
        self.variables = variables if variables else {}

    def _create_rpn_from_tokens(self, tokens: list[Token]) -> deque[Symbol]:
        for i, c in enumerate(tokens):
            if c.type == TokenType.EOF:
                break
            if c.type == TokenType.NUMBER:
                self._handle_number_token(c.value)
                continue

            if c.type == TokenType.PARENTHESIS_OPEN:
                self._handle_open_parenthesis(c.token)
                continue

            if c.type == TokenType.PARENTHESIS_CLOSE:
                self._handle_close_parenthesis()
                continue

            if c.type == TokenType.SYMBOL:
                self._handle_symbol(c.token)
                continue

            if c.type == TokenType.KEYWORD:
                self._handle_keyword(c.token)
                continue

            if self._handle_operator(c):
                continue

            self._handle_start_line_with_equals(c)
            self._handle_unknown_symbol(c)

            self._handle_new_operator(c, i)

            while (
                self._holding_stack
                and self._holding_stack[0].type != SymbolType.PARENTHESIS_OPEN
            ):
                if self._holding_stack[0].type != SymbolType.OPERATOR:
                    break

                if self._holding_stack[0].precedence >= new_operator.precedence:
                    _sym = self._holding_stack.popleft()
                    self._output_stack.append(_sym)
                    continue
                break
            _sym = Symbol(
                c.token,
                SymbolType.OPERATOR,
                new_operator.argument_count,
                new_operator.precedence,
            )
            self._holding_stack.appendleft(_sym)
            self._previous_symbol = _sym
        while self._holding_stack:
            self._output_stack.append(self._holding_stack.popleft())

        return self._output_stack

    def _solve_rpn(self, stack: deque[Symbol]) -> float:
        output: deque[float] = deque()
        _is_var = False
        _variable_name = None
        _is_assignment = False
        _is_if = False
        _had_if = False
        _is_condition_false = False
        _is_reassignment = False

        for symbol in stack:
            args: list[float] = []
            if _is_condition_false and symbol.value != "}":
                continue
            if _is_condition_false and symbol.value == "}":
                _is_condition_false = False
                continue
            if symbol.type == SymbolType.KEYWORD:
                if symbol.value == "var":
                    _is_var = True
                if symbol.value == "if":
                    _is_if = True
                    _had_if = True
                continue
            if symbol.type == SymbolType.NUMBER:
                output.appendleft(float(symbol.value))
                continue
            if symbol.type == SymbolType.OPERATOR:
                if symbol.value == "=":
                    _is_assignment = True
                    continue
                args = []
                for _ in range(symbol.argument_count):
                    if not output:
                        raise ExpressionError(
                            f"Expression invalid, expected {symbol.argument_count} got {len(output)}, left {symbol.argument_count - len(args)} {symbol}"
                        )
                    args.append(output.popleft())
            if symbol.type == SymbolType.SYMBOL:
                if symbol.value in self.variables and (
                    _is_assignment or _is_reassignment or _is_if
                ):
                    value = self.variables[symbol.value]
                    _is_reassignment = True
                    _variable_name = symbol.value
                    output.appendleft(value)
                    continue
                if _variable_name and _is_var:
                    raise ExpressionError(
                        f"Got two variable names in assignment {symbol}"
                    )
                _variable_name = symbol.value
                continue

            result: float = 0
            match symbol.argument_count:
                case 2:
                    if symbol.value not in binary_operators:
                        raise ExpressionError(
                            f"Unknown operator '{symbol.value}' for {symbol.argument_count}"
                        )
                    if symbol.value == "(":
                        continue
                    if symbol.value in self.operations:
                        result = self.operations[symbol.value](args[1], args[0])
                case 1:
                    if symbol.value not in unary_operators.keys():
                        raise ExpressionError(
                            f"Unknown operator '{symbol.value}' for {symbol.argument_count}"
                        )
                    if symbol.value in self.unary_operations:
                        result = self.unary_operations[symbol.value](args[0])
                case 0:
                    if symbol.value == "var":
                        _is_var = True
                        continue
                    if symbol.value == "=":
                        _is_assignment = True
                        continue
                    if symbol.value in ["{", "}"]:
                        _is_if = False
                        continue
                case _:
                    raise ExpressionError(
                        f"Symbol {symbol} expected {symbol.argument_count}"
                    )

            if _is_if:
                _is_condition_false = result == 0.0
                _is_if = False
                continue
            output.appendleft(result)

        if len(output) != 1 and not _had_if:
            raise ExpressionError(f"Expression led to no result {output}")
        if len(output) == 1 and _is_var and _variable_name and _is_assignment:
            self.variables[_variable_name] = output.popleft()
            return self.variables[_variable_name]
        print(f"Got variable name {_variable_name} and {_is_assignment} in {output}")
        if len(output) == 1 and _variable_name and (_is_reassignment or _is_assignment):
            print(f"Output {output[0]}")
            self.variables[_variable_name] = output.popleft()
            return self.variables[_variable_name]
        if len(output) != 1 and _had_if:
            return 0.0
        return output.popleft()

    def _handle_number_token(self, token_value: float):
        _sym = Symbol(str(token_value), SymbolType.NUMBER, 0)
        self._output_stack.append(_sym)
        self._previous_symbol = _sym

    def _handle_open_parenthesis(self, parenthesis: str):
        _sym = Symbol(parenthesis, SymbolType.PARENTHESIS_OPEN, 0)
        self._holding_stack.appendleft(_sym)
        self._previous_symbol = _sym

    def _handle_close_parenthesis(self):
        while (
            self._holding_stack
            and self._holding_stack[0].type is not SymbolType.PARENTHESIS_OPEN
        ):
            self._output_stack.append(self._holding_stack.popleft())
        if not self._holding_stack:
            raise ExpressionError("Parenthesis missmatched")
        if (
            self._holding_stack
            and self._holding_stack[0].type is SymbolType.PARENTHESIS_OPEN
        ):
            _ = self._holding_stack.popleft()
        self._previous_symbol = Symbol(")", SymbolType.PARENTHESIS_CLOSE, 0)

    def _handle_symbol(self, token: str):
        if token not in self.variables:
            self.variables[token] = 0.0
        _sym = Symbol(str(token), SymbolType.SYMBOL, 0)
        self._output_stack.append(_sym)
        self._previous_symbol = _sym

    def _handle_keyword(self, token: str):
        _sym = Symbol(str(token), SymbolType.KEYWORD, 0)
        self._output_stack.append(_sym)
        self._previous_symbol = _sym

    def _handle_operator(self, c: Token) -> bool:
        if (
            c.type == TokenType.OPERATOR
            and c.token == "="
            and self._previous_symbol.type == SymbolType.SYMBOL
        ):
            _sym = Symbol(str(c.token), SymbolType.ASSIGNMENT, 0)
            self._holding_stack.append(_sym)
            self._previous_symbol = _sym
            return True
        return False

    def _handle_start_line_with_equals(self, c: Token):
        if c.type == TokenType.OPERATOR and c.token == "=":
            raise ExpressionError(
                f"Got equals without symbol name {self._previous_symbol.__repr__()}."
            )

    def _handle_unknown_symbol(self, c: Token):
        if (
            c.token not in binary_operators.keys()
            and c.token not in keywords.keys()
            and c.type == TokenType.OPERATOR
        ):
            raise ExpressionError(f"Symbol {c} is not a valid symbol.")

    def _handle_new_operator(self, c: Token, i: int):
        new_operator = Symbol(c.token, SymbolType.OPERATOR, 2)
        if (c.token == "-" or c.token == "+") and (
            self._previous_symbol.type
            not in [
                SymbolType.NUMBER,
                SymbolType.PARENTHESIS_CLOSE,
                SymbolType.SYMBOL,
            ]
            or i == 0
        ):
            new_operator.precedence = MAX_PRECEDENCE
            new_operator.argument_count = 1
        if c.token == "{" or c.token == "}":
            new_operator.argument_count = 0

    def evaluate(self, code_line: str = "") -> float:
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(code_line)
        rpn = self._create_rpn_from_tokens(tokens)
        result = self._solve_rpn(rpn)
        return result

    @override
    def __str__(self) -> str:
        return f"Evaulator's operator stack: {self.operator_stack}"

    @override
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Evaluator):
            return self.operator_stack == value.operator_stack
        return False

    @override
    def __repr__(self) -> str:
        return f"Evaluator({self.operator_stack})"
