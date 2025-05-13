from enum import Enum
from typing import override


class SymbolType(Enum):
    NUMBER = "number"
    OPERATOR = "operator"
    PARENTHESIS_OPEN = "parenthesis_open"
    PARENTHESIS_CLOSE = "parenthesis_close"
    KEYWORD = "keyword"
    ASSIGNMENT = "assignment"
    SYMBOL = "symbol"
    UNKNOWN = None


class Symbol:
    value: str
    type: SymbolType
    argument_count: int
    precedence: int

    def __init__(
        self,
        value: str = "",
        type: SymbolType = SymbolType.UNKNOWN,
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
    "!=": Symbol("==", SymbolType.OPERATOR, 2, 9),
    "==": Symbol("==", SymbolType.OPERATOR, 2, 8),
    "<=": Symbol("<=", SymbolType.OPERATOR, 2, 7),
    "<": Symbol("<", SymbolType.OPERATOR, 2, 6),
    ">=": Symbol(">=", SymbolType.OPERATOR, 2, 5),
    ">": Symbol(">", SymbolType.OPERATOR, 2, 4),
    "=": Symbol("=", SymbolType.OPERATOR, 2, 3),
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

keywords: dict[str, Symbol] = {"var": Symbol("var", SymbolType.KEYWORD, 1, 5)}
