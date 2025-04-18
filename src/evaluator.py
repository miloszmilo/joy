from collections import deque
from enum import EnumType
from typing import Callable, override

from src.exceptions.ExpressionError import ExpressionError
from src.joyTypes.Token import Token

MAX_PRECEDENCE = 100


class SymbolType(EnumType):
    NUMBER: str = "number"
    OPERATOR: str = "operator"
    PARENTHESIS_OPEN: str = "parenthesis_open"
    PARENTHESIS_CLOSE: str = "parenthesis_close"
    UNKNOWN: None = None


class Symbol:
    value: str
    type: str | None
    argument_count: int
    precedence: int

    def __init__(
        self,
        value: str = "",
        type: str | None = SymbolType.UNKNOWN,
        argument_count: int = 2,
        precedence: int = -1,
    ) -> None:
        self.value = value
        self.type = type
        self.argument_count = argument_count
        _precedence = precedence
        if precedence == -1:
            _precedence = binary_operators.get(value, -1)
            if isinstance(_precedence, Symbol):
                _precedence = _precedence.precedence
        self.precedence = _precedence

    @override
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Symbol):
            return (
                self.value == value.value
                and self.type == value.type
                and self.argument_count == value.argument_count
                and self.precedence == value.precedence
            )
        return False

    @override
    def __str__(self) -> str:
        return f"{self.value}"

    @override
    def __repr__(self) -> str:
        return f"Symbol({self.value}, {self.type}, {self.argument_count})"


binary_operators: dict[str, Symbol] = {
    "*": Symbol("*", SymbolType.OPERATOR, 2, 2),
    "/": Symbol("/", SymbolType.OPERATOR, 2, 2),
    "%": Symbol("%", SymbolType.OPERATOR, 2, 2),
    "+": Symbol("+", SymbolType.OPERATOR, 2, 1),
    "-": Symbol("-", SymbolType.OPERATOR, 2, 1),
}

unary_operators: dict[str, Symbol] = {
    "-": Symbol("-", SymbolType.OPERATOR, 1, 100),
    "+": Symbol("+", SymbolType.OPERATOR, 1, 100),
}


class Evaluator:
    operator_stack: list[Token]

    operations: dict[str, Callable[[float, float], float]] = {
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
        operator_stack: list[Token] = [],
    ):
        self.operator_stack = operator_stack

    def _create_rpn_from(self, code_line: str = "") -> deque[Symbol]:
        holding_stack: deque[Symbol] = deque()
        output_stack: deque[Symbol] = deque()
        previous_symbol: Symbol = Symbol("0", SymbolType.NUMBER, 0)

        for i, c in enumerate(code_line.strip().replace(" ", "")):
            if c.isdigit():
                _sym = Symbol(c, SymbolType.NUMBER, 0)
                output_stack.append(_sym)
                previous_symbol = _sym
                continue

            if c == "(":
                _sym = Symbol(c, SymbolType.PARENTHESIS_OPEN, 0)
                holding_stack.appendleft(_sym)
                previous_symbol = _sym
                continue

            if c == ")":
                while (
                    holding_stack
                    and holding_stack[0].type is not SymbolType.PARENTHESIS_OPEN
                ):
                    output_stack.append(holding_stack.popleft())
                if not holding_stack:
                    raise ExpressionError("Parenthesis missmatched")
                if (
                    holding_stack
                    and holding_stack[0].type is SymbolType.PARENTHESIS_OPEN
                ):
                    _ = holding_stack.popleft()
                previous_symbol = Symbol(")", SymbolType.PARENTHESIS_CLOSE, 0)
                continue

            if c not in binary_operators.keys():
                raise ExpressionError(f"Symbol {c} is not a valid symbol")

            new_operator = Symbol(c, SymbolType.OPERATOR, 2)
            if (c == "-" or c == "+") and (
                previous_symbol.type
                not in [
                    SymbolType.NUMBER,
                    SymbolType.PARENTHESIS_CLOSE,
                ]
                or i == 0
            ):
                new_operator.precedence = MAX_PRECEDENCE
                new_operator.argument_count = 1

            while (
                holding_stack and holding_stack[0].type != SymbolType.PARENTHESIS_OPEN
            ):
                if holding_stack[0].type != SymbolType.OPERATOR:
                    break

                if holding_stack[0].precedence >= new_operator.precedence:
                    _sym = holding_stack.popleft()
                    output_stack.append(_sym)
                    continue
                break
            _sym = Symbol(
                c,
                SymbolType.OPERATOR,
                new_operator.argument_count,
                new_operator.precedence,
            )
            holding_stack.appendleft(_sym)
            previous_symbol = _sym
        while holding_stack:
            output_stack.append(holding_stack.popleft())

        return output_stack

    def _solve_rpn(self, stack: deque[Symbol]) -> float:
        output: deque[float] = deque()

        for symbol in stack:
            args: list[float] = []
            if symbol.type == SymbolType.NUMBER:
                output.appendleft(int(symbol.value))
                continue
            if symbol.type == SymbolType.OPERATOR:
                args = []
                for _ in range(symbol.argument_count):
                    if not output:
                        raise ExpressionError(
                            f"Expression invalid, expected {symbol.argument_count} got {len(output)}, left {symbol.argument_count - len(args)} {symbol}"
                        )
                    args.append(output.popleft())

            result: float = 0
            if symbol.argument_count == 2:
                if symbol.value not in binary_operators:
                    raise ExpressionError(
                        f"Unknown operator '{symbol.value}' for {symbol.argument_count}"
                    )
                if symbol.value == "(":
                    continue
                if symbol.value in self.operations:
                    result = self.operations[symbol.value](args[1], args[0])

            if symbol.argument_count == 1:
                if symbol.value not in unary_operators.keys():
                    raise ExpressionError(
                        f"Unknown operator '{symbol.value}' for {symbol.argument_count}"
                    )
                if symbol.value in self.unary_operations:
                    result = self.unary_operations[symbol.value](args[0])
            output.appendleft(result)

        if len(output) != 1:
            raise ExpressionError(f"Expression led to no result {output}")
        return output.popleft()

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
