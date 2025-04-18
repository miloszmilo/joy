from enum import EnumType
from typing import override


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
