from typing import override


class Token:
    token: str
    type: str

    def __init__(self, token: str = "", type: str = ""):
        self.token = token
        self.type = type

    @override
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Token):
            return self.token == value.token and self.type == value.type
        return False

    @override
    def __str__(self) -> str:
        return f'Token(token="{self.token}", type="{self.type}")'

    @override
    def __repr__(self) -> str:
        return self.__str__()
