from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from typing import Callable, override

from src.context import Context, SolveContext
from src.exceptions.ExpressionError import ExpressionError
from src.joyTypes.Symbol import (
    Symbol,
    SymbolType,
    binary_operators,
    unary_operators,
)
from src.joyTypes.Token import Token, TokenType

MAX_PRECEDENCE = 100


class Evaluator:
    strategies: dict[TokenType, EvaluatorStrategy]
    solve_strategies: dict[SymbolType, SolverStrategy]
    rpn_context: Context
    solve_context: SolveContext
    output: deque[float]
    args: list[float]

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
        self.solve_strategies = {}
        self.rpn_context = Context(
            operator_stack if operator_stack else [],
            variables if variables else {},
            tokens,
            0,
            tokens[0],
            deque(),
            deque(),
            Symbol("0", SymbolType.NUMBER, 0),
        )
        self.solve_context = SolveContext(False, None, False)
        self.output = deque()
        self.args = []

    def _peek(self) -> Token:
        return self.rpn_context.tokens[self.rpn_context.i]

    def advance(self):
        if self.rpn_context.i + 1 >= len(self.rpn_context.tokens):
            return
        self.rpn_context.i += 1
        self.rpn_context.current_token = self.rpn_context.tokens[self.rpn_context.i]

    def _match(self, type: TokenType, token: str | None = "") -> bool:
        cur = self._peek()
        if token:
            return cur.type == type and cur.token == token
        return cur.type == type

    def evaluate_tokens(self) -> deque[Symbol]:
        self.strategies = {
            TokenType.EOF: EOFStrategy(),
            TokenType.NUMBER: NumberStrategy(),
            TokenType.PARENTHESIS_OPEN: OpenParenthesisStrategy(),
            TokenType.PARENTHESIS_CLOSE: CloseParenthesisStrategy(),
            TokenType.SYMBOL: SymbolStrategy(),
            TokenType.KEYWORD: KeywordStrategy(),
            TokenType.OPERATOR: OperatorStrategy(),
            TokenType.COMMA: CommaStrategy(),
        }
        for t in self.rpn_context.tokens:
            self.strategies[t.type].execute(self.rpn_context, self)
        return self.rpn_context.output_stack

    def _solve_rpn(self, stack: deque[Symbol]) -> float:
        self.solve_strategies = {
            SymbolType.KEYWORD: SolveKeywordStrategy(),
            SymbolType.NUMBER: SolveNumberStrategy(),
            SymbolType.OPERATOR: SolveOperatorStrategy(),
            SymbolType.SYMBOL: SolveSymbolStrategy(),
        }
        for symbol in stack:
            self.args = []
            self.solve_strategies[symbol.type].execute(self, symbol)

        if len(self.output) != 1:
            raise ExpressionError(f"Expression led to no result {self.output}")
        if (
            len(self.output) == 1
            and self.solve_context.is_var
            and self.solve_context.variable_name
            and self.solve_context.is_assignment
        ):
            self.rpn_context.variables[self.solve_context.variable_name] = (
                self.output.popleft()
            )
            return self.rpn_context.variables[self.solve_context.variable_name]
        return self.output.popleft()

    def handle_argument_count(self, symbol: Symbol, args: list[float]) -> None:
        result: float = 0
        match symbol.argument_count:
            case 2:
                if symbol.value not in binary_operators:
                    raise ExpressionError(
                        f"Unknown operator '{symbol.value}' for {symbol.argument_count}"
                    )
                if symbol.value == "(":
                    self.advance()
                    return
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
                    self.solve_context.is_var = True
                    self.advance()
                    return
                if symbol.value == "=":
                    self.solve_context.is_assignment = True
                    self.advance()
                    return
            case _:
                raise ExpressionError(
                    f"Symbol {symbol} expected {symbol.argument_count}"
                )
        self.output.appendleft(result)

    def solve(self) -> float:
        rpn = self.evaluate_tokens()
        result = self._solve_rpn(rpn)
        return result

    @override
    def __str__(self) -> str:
        return f"Evaulator's operator stack: {self.rpn_context.operator_stack}"

    @override
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Evaluator):
            return self.rpn_context.operator_stack == value.rpn_context.operator_stack
        return False

    @override
    def __repr__(self) -> str:
        return f"Evaluator({self.rpn_context.operator_stack})"


class EvaluatorStrategy(ABC):
    @abstractmethod
    def execute(self, context: Context, evaluator: Evaluator):
        pass


class NumberStrategy(EvaluatorStrategy):
    @override
    def execute(self, context: Context, evaluator: Evaluator):
        _sym = Symbol(str(context.current_token.value), SymbolType.NUMBER, 0)
        context.output_stack.append(_sym)
        context.previous_symbol = _sym
        evaluator.advance()


class EOFStrategy(EvaluatorStrategy):
    @override
    def execute(self, context: Context, evaluator: Evaluator):
        if len(context.tokens) > context.i + 1:
            raise ExpressionError(
                f"Found more tokens, but encountered EOF {context.tokens}"
            )
        while context.holding_stack:
            context.output_stack.append(context.holding_stack.popleft())
        return


class OpenParenthesisStrategy(EvaluatorStrategy):
    @override
    def execute(self, context: Context, evaluator: Evaluator):
        _sym = Symbol(context.current_token.token, SymbolType.PARENTHESIS_OPEN, 0)
        context.holding_stack.appendleft(_sym)
        context.previous_symbol = _sym
        evaluator.advance()
        return


class CloseParenthesisStrategy(EvaluatorStrategy):
    @override
    def execute(self, context: Context, evaluator: Evaluator):
        while (
            context.holding_stack
            and context.holding_stack[0].type is not SymbolType.PARENTHESIS_OPEN
        ):
            context.output_stack.append(context.holding_stack.popleft())
        if not context.holding_stack:
            raise ExpressionError("Parenthesis missmatched")
        if (
            context.holding_stack
            and context.holding_stack[0].type is SymbolType.PARENTHESIS_OPEN
        ):
            _ = context.holding_stack.popleft()
        context.previous_symbol = Symbol(")", SymbolType.PARENTHESIS_CLOSE, 0)
        evaluator.advance()
        return


class SymbolStrategy(EvaluatorStrategy):
    @override
    def execute(self, context: Context, evaluator: Evaluator):
        if context.current_token.token not in context.variables:
            context.variables[context.current_token.token] = 0.0
        _sym = Symbol(str(context.current_token.token), SymbolType.SYMBOL, 0)
        context.output_stack.append(_sym)
        context.previous_symbol = _sym
        evaluator.advance()
        return


class KeywordStrategy(EvaluatorStrategy):
    @override
    def execute(self, context: Context, evaluator: Evaluator):
        _sym = Symbol(str(context.current_token.token), SymbolType.KEYWORD, 0)
        context.output_stack.append(_sym)
        context.previous_symbol = _sym
        evaluator.advance()
        return


class OperatorStrategy(EvaluatorStrategy):
    @override
    def execute(self, context: Context, evaluator: Evaluator):
        if (
            context.current_token.token == "="
            and context.previous_symbol.type == SymbolType.SYMBOL
        ):
            _sym = Symbol(str(context.current_token.token), SymbolType.ASSIGNMENT, 0)
            context.holding_stack.append(_sym)
            context.previous_symbol = _sym
            evaluator.advance()
            return

        if context.current_token.token == "=":
            raise ExpressionError(
                f"Got equals without symbol name {context.previous_symbol.__repr__()}."
            )

        new_operator = Symbol(context.current_token.token, SymbolType.OPERATOR, 2)
        if (
            context.current_token.token == "-" or context.current_token.token == "+"
        ) and (
            context.previous_symbol.type
            not in [
                SymbolType.NUMBER,
                SymbolType.PARENTHESIS_CLOSE,
                SymbolType.SYMBOL,
            ]
            or context.i == 0
        ):
            new_operator.precedence = MAX_PRECEDENCE
            new_operator.argument_count = 1

        while (
            context.holding_stack
            and context.holding_stack[0].type != SymbolType.PARENTHESIS_OPEN
        ):
            if context.holding_stack[0].type != SymbolType.OPERATOR:
                break

            if context.holding_stack[0].precedence >= new_operator.precedence:
                _sym = context.holding_stack.popleft()
                context.output_stack.append(_sym)
                continue
            break
        _sym = Symbol(
            context.current_token.token,
            SymbolType.OPERATOR,
            new_operator.argument_count,
            new_operator.precedence,
        )
        context.holding_stack.appendleft(_sym)
        context.previous_symbol = _sym
        evaluator.advance()


class CommaStrategy(EvaluatorStrategy):
    @override
    def execute(self, context: Context, evaluator: Evaluator):
        raise ExpressionError(f"Unexpected comma {context}")


class SolverStrategy(ABC):
    @abstractmethod
    def execute(self, evaluator: Evaluator, symbol: Symbol):
        pass


class SolveKeywordStrategy(SolverStrategy):
    @override
    def execute(self, evaluator: Evaluator, symbol: Symbol):
        if symbol.value == "var":
            evaluator.solve_context.is_var = True


class SolveNumberStrategy(SolverStrategy):
    @override
    def execute(self, evaluator: Evaluator, symbol: Symbol):
        evaluator.output.appendleft(float(symbol.value))


class SolveOperatorStrategy(SolverStrategy):
    @override
    def execute(self, evaluator: Evaluator, symbol: Symbol):
        if symbol.value == "=":
            evaluator.solve_context.is_assignment = True
            return
        for _ in range(symbol.argument_count):
            if not evaluator.output:
                raise ExpressionError(
                    f"Expression invalid, expected {symbol.argument_count} got {len(evaluator.output)}, left {symbol.argument_count - len(evaluator.args)} {symbol}"
                )
            evaluator.args.append(evaluator.output.popleft())
        evaluator.handle_argument_count(symbol, evaluator.args)


class SolveSymbolStrategy(SolverStrategy):
    @override
    def execute(self, evaluator: Evaluator, symbol: Symbol):
        if (
            symbol.value in evaluator.rpn_context.variables
            and not evaluator.solve_context.is_var
        ):
            value = evaluator.rpn_context.variables[symbol.value]
            evaluator.output.appendleft(value)
            return
        if evaluator.solve_context.variable_name and evaluator.solve_context.is_var:
            raise ExpressionError(f"Got two variable names in assignment {symbol}")
        evaluator.solve_context.variable_name = symbol.value
