from abc import ABC
from collections import deque
from dataclasses import dataclass
from typing import Callable

from src.exceptions.ExpressionError import ExpressionError
from src.joyTypes.Token import Token, TokenType


class ExpressionEvaluator:
    operations: dict[str, Callable[[float, float], float]] = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
    }

    def convert_to_rpn(self, expression: list[Token]):
        numbers: deque[float] = deque()
        operators: deque[str] = deque()
        output: deque[float] = deque()
        self.state = state[expression[0]]
        for i in expression:
            self.state.handle()
            if i.type == TokenType.NUMBER:
                numbers.append(float(i.token))
                continue
            if i.type == TokenType.OPERATOR and len(numbers) > 1:
                right = numbers.popleft()
                left = numbers.popleft()
                result: float = self.operations[i.token](left, right)
                output.append(result)
                continue
            if i.type == TokenType.OPERATOR:
                operators.append(i.token)
                continue

    def solve(self, expression: str):
        pass


@dataclass
class State(ABC):
    pass


class StateFactory:
    def state(self, token: Token) -> State:
        match token.type:
            case TokenType.NUMBER:
                return NumberState()
            case TokenType.OPERATOR:
                return OperatorState()
            case TokenType.PARENTHESIS_OPEN:
                return OpenParenthesisState()
            case TokenType.PARENTHESIS_CLOSE:
                return CloseParenthesisState()
            case _:
                raise ExpressionError
