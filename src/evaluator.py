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
        holding_stack: deque[Symbol] = deque()
        output_stack: deque[Symbol] = deque()
        previous_symbol: Symbol = Symbol("0", SymbolType.NUMBER, 0)

        for i, c in enumerate(tokens):
            if c.type == TokenType.NUMBER:
                _sym = Symbol(str(c.value), SymbolType.NUMBER, 0)
                output_stack.append(_sym)
                previous_symbol = _sym
                continue

            if c.type == TokenType.PARENTHESIS_OPEN:
                _sym = Symbol(c.token, SymbolType.PARENTHESIS_OPEN, 0)
                holding_stack.appendleft(_sym)
                previous_symbol = _sym
                continue

            if c.type == TokenType.PARENTHESIS_CLOSE:
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

            if c.type == TokenType.SYMBOL:
                if c.token not in self.variables:
                    self.variables[c.token] = 0.0
                _sym = Symbol(str(c.token), SymbolType.SYMBOL, 0)
                output_stack.append(_sym)
                previous_symbol = _sym
                continue

            if c.type == TokenType.KEYWORD:
                _sym = Symbol(str(c.token), SymbolType.KEYWORD, 0)
                output_stack.append(_sym)
                previous_symbol = _sym
                continue
                # if c.token == "var":
                #     previous_symbol = Symbol(str(c.token), SymbolType.KEYWORD, 0)
                #     # Or instead of doing that
                #     # save variable name
                #     # and then assign whatever we solve the right
                #     # to the variable name
                #     # after the loop ends
                #     while True:
                #         # Get symbol name
                #         # get =
                #         # get value
                #         pass
                #         break
                #     pass

            if (
                c.type == TokenType.OPERATOR
                and c.token == "="
                and previous_symbol.type == SymbolType.SYMBOL
            ):
                _sym = Symbol(str(c.token), SymbolType.ASSIGNMENT, 0)
                holding_stack.append(_sym)
                previous_symbol = _sym
                continue

            if c.type == TokenType.OPERATOR and c.token == "=":
                raise ExpressionError(
                    f"Got equals without symbol name {previous_symbol.__repr__()}."
                )

            if (
                c.token not in binary_operators.keys()
                and c.token not in keywords.keys()
                and c.type == TokenType.OPERATOR
            ):
                raise ExpressionError(f"Symbol {c} is not a valid symbol.")

            new_operator = Symbol(c.token, SymbolType.OPERATOR, 2)
            if (c.token == "-" or c.token == "+") and (
                previous_symbol.type
                not in [
                    SymbolType.NUMBER,
                    SymbolType.PARENTHESIS_CLOSE,
                    SymbolType.SYMBOL,
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
                c.token,
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
                if symbol.value in self.variables and not _is_var:
                    value = self.variables[symbol.value]
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
