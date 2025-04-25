from enum import Enum
from typing import override


class TokenType(Enum):
    NUMBER = "number"
    OPERATOR = "operator"
    STRING = "string"
    PARENTHESIS_OPEN = "parenthesis_open"
    PARENTHESIS_CLOSE = "parenthesis_close"
    SYMBOL = "symbol"
    SCOPE_OPEN = "scope_open"
    SCOPE_CLOSE = "scope_close"
    COMMA = "comma"
    END_OF_STATEMENT = "end_of_statement"
    SEPARATOR = "separator"
    KEYWORD = "keyword"
    ASSIGNMENT = "assignment"


class Token:
    token: str
    type: TokenType
    value: float

    def __init__(
        self, token: str = "", type: TokenType = TokenType.STRING, value: float = 0
    ):
        self.token = token
        self.type = type
        self.value = value

    @override
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Token):
            return (
                self.token == value.token
                and self.type == value.type
                and self.value == value.value
            )
        return False

    @override
    def __str__(self) -> str:
        return f'Token(token="{self.token}", type="{self.type}, value="{self.value}")'

    @override
    def __repr__(self) -> str:
        return self.__str__()
