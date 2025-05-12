from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from typing import Callable, override

from src.context import Context
from src.exceptions.ExpressionError import ExpressionError
from src.joyTypes.Symbol import (
    Symbol,
    SymbolType,
    binary_operators,
    keywords,
    unary_operators,
)
from src.joyTypes.Token import Token, TokenType

MAX_PRECEDENCE = 100


class Evaluator:
    operator_stack: list[Token]
    variables: dict[str, float]
    tokens: list[Token]
    i: int
    current_token: Token
    _holding_stack: deque[Symbol]
    _output_stack: deque[Symbol]
    _previous_symbol: Symbol
    strategies: dict[TokenType, Strategy]
    context: Context

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
        tokens: list[Token],
        operator_stack: list[Token] | None = None,
        variables: dict[str, float] | None = None,
    ):
        self.strategies = {}
        self.context = Context(
            operator_stack if operator_stack else [],
            variables if variables else {},
            tokens,
            0,
            tokens[0],
            deque(),
            deque(),
            Symbol("0", SymbolType.NUMBER, 0),
        )

    def _peek(self) -> Token:
        return self.context.tokens[self.i]

    def _advance(self):
        if self.context.i + 1 >= len(self.context.tokens):
            return
        self.context.i += 1
        self.context.current_token = self.context.tokens[self.context.i]

    def _match(self, type: TokenType, token: str | None = "") -> bool:
        cur = self._peek()
        if token:
            return cur.type == type and cur.token == token
        return cur.type == type

    def evaluate_tokens(self):
        self.strategies = {
            TokenType.EOF: EOFStrategy(),
            TokenType.NUMBER: NumberStrategy(),
            TokenType.PARENTHESIS_OPEN: OpenParenthesisStrategy(),
        }
        for t in self.context.tokens:
            self.strategies[t.type].execute(self.context, self.tokens)

    def _create_rpn_from_tokens(self) -> deque[Symbol]:
        while self.context.current_token.type != TokenType.EOF:
            if self.context.current_token.type == TokenType.NUMBER:
                _sym = Symbol(
                    str(self.context.current_token.value), SymbolType.NUMBER, 0
                )
                self.context._output_stack.append(_sym)
                self.context._previous_symbol = _sym
                self._advance()
                continue

            if self.context.current_token.type == TokenType.PARENTHESIS_OPEN:
                _sym = Symbol(
                    self.context.current_token.token, SymbolType.PARENTHESIS_OPEN, 0
                )
                self.context._holding_stack.appendleft(_sym)
                self.context._previous_symbol = _sym
                self._advance()
                continue

            if self.context.current_token.type == TokenType.PARENTHESIS_CLOSE:
                while (
                    self.context._holding_stack
                    and self.context._holding_stack[0].type
                    is not SymbolType.PARENTHESIS_OPEN
                ):
                    self.context._output_stack.append(
                        self.context._holding_stack.popleft()
                    )
                if not self.context._holding_stack:
                    raise ExpressionError("Parenthesis missmatched")
                if (
                    self.context._holding_stack
                    and self.context._holding_stack[0].type
                    is SymbolType.PARENTHESIS_OPEN
                ):
                    _ = self.context._holding_stack.popleft()
                self.context._previous_symbol = Symbol(
                    ")", SymbolType.PARENTHESIS_CLOSE, 0
                )
                self._advance()
                continue

            if self.context.current_token.type == TokenType.SYMBOL:
                if self.context.current_token.token not in self.context.variables:
                    self.context.variables[self.context.current_token.token] = 0.0
                _sym = Symbol(
                    str(self.context.current_token.token), SymbolType.SYMBOL, 0
                )
                self.context._output_stack.append(_sym)
                self.context._previous_symbol = _sym
                self._advance()
                continue

            if self.context.current_token.type == TokenType.KEYWORD:
                _sym = Symbol(
                    str(self.context.current_token.token), SymbolType.KEYWORD, 0
                )
                self.context._output_stack.append(_sym)
                self.context._previous_symbol = _sym
                self._advance()
                continue

            if (
                self.context.current_token.type == TokenType.OPERATOR
                and self.context.current_token.token == "="
                and self.context._previous_symbol.type == SymbolType.SYMBOL
            ):
                _sym = Symbol(
                    str(self.context.current_token.token), SymbolType.ASSIGNMENT, 0
                )
                self.context._holding_stack.append(_sym)
                self.context._previous_symbol = _sym
                self._advance()
                continue

            if (
                self.context.current_token.type == TokenType.OPERATOR
                and self.context.current_token.token == "="
            ):
                raise ExpressionError(
                    f"Got equals without symbol name {self.context._previous_symbol.__repr__()}."
                )

            if (
                self.context.current_token.token not in binary_operators.keys()
                and self.context.current_token.token not in keywords.keys()
                and self.context.current_token.type == TokenType.OPERATOR
            ):
                raise ExpressionError(
                    f"Symbol {self.context.current_token} is not a valid symbol."
                )

            new_operator = Symbol(
                self.context.current_token.token, SymbolType.OPERATOR, 2
            )
            if (
                self.context.current_token.token == "-"
                or self.context.current_token.token == "+"
            ) and (
                self.context._previous_symbol.type
                not in [
                    SymbolType.NUMBER,
                    SymbolType.PARENTHESIS_CLOSE,
                    SymbolType.SYMBOL,
                ]
                or self.context.i == 0
            ):
                new_operator.precedence = MAX_PRECEDENCE
                new_operator.argument_count = 1

            while (
                self.context._holding_stack
                and self.context._holding_stack[0].type != SymbolType.PARENTHESIS_OPEN
            ):
                if self.context._holding_stack[0].type != SymbolType.OPERATOR:
                    break

                if self.context._holding_stack[0].precedence >= new_operator.precedence:
                    _sym = self.context._holding_stack.popleft()
                    self.context._output_stack.append(_sym)
                    continue
                break
            _sym = Symbol(
                self.context.current_token.token,
                SymbolType.OPERATOR,
                new_operator.argument_count,
                new_operator.precedence,
            )
            self.context._holding_stack.appendleft(_sym)
            self.context._previous_symbol = _sym
            self._advance()
        self._handle_eof()

        return self.context._output_stack

    def _handle_eof(self):
        if len(self.context.tokens) > self.context.i + 1:
            raise ExpressionError(
                f"Found more tokens, but encountered EOF {self.tokens}"
            )
        while self.context._holding_stack:
            self.context._output_stack.append(self.context._holding_stack.popleft())
        return

    def _solve_rpn(self, stack: deque[Symbol]) -> float:
        output: deque[float] = deque()
        _is_var = False
        _variable_name = None
        _is_assignment = False

        for symbol in stack:
            args: list[float] = []
            if symbol.type == SymbolType.KEYWORD:
                if symbol.value == "var":
                    _is_var = True
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
                if symbol.value in self.context.variables and not _is_var:
                    value = self.context.variables[symbol.value]
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
                case _:
                    raise ExpressionError(
                        f"Symbol {symbol} expected {symbol.argument_count}"
                    )
            output.appendleft(result)

        if len(output) != 1:
            raise ExpressionError(f"Expression led to no result {output}")
        if len(output) == 1 and _is_var and _variable_name and _is_assignment:
            self.variables[_variable_name] = output.popleft()
            return self.variables[_variable_name]
        return output.popleft()

    def solve(self) -> float:
        rpn = self._create_rpn_from_tokens()
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


class Strategy(ABC):
    @abstractmethod
    def execute(self, context: Context, tokens: deque[Token]):
        pass


class NumberStrategy(Strategy):
    @override
    def execute(self, context: Context, tokens: deque[Token]):
        _sym = Symbol(str(context.current_token.value), SymbolType.NUMBER, 0)
        context._output_stack.append(_sym)
        context._previous_symbol = _sym
        context._advance()


class EOFStrategy(Strategy):
    @override
    def execute(self, context: Context, tokens: deque[Token]):
        return super().execute(*args)


class OpenParenthesisStrategy(Strategy):
    @override
    def execute(self, context: Context, tokens: deque[Token]):
        return super().execute(*args)
