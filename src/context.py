from collections import deque
from dataclasses import dataclass
from src.joyTypes.Symbol import Symbol
from src.joyTypes.Token import Token


@dataclass
class Context:
    operator_stack: list[Token]
    variables: dict[str, float]
    tokens: list[Token]
    i: int
    current_token: Token
    _holding_stack: deque[Symbol]
    _output_stack: deque[Symbol]
    _previous_symbol: Symbol
