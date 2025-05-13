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
    holding_stack: deque[Symbol]
    output_stack: deque[Symbol]
    previous_symbol: Symbol

@dataclass
class SolveContext:
    is_var: bool
    variable_name: str | None
    is_assignment: bool
