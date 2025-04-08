from src.joyTypes.Types import Type, TypeOfTypes


class Variable:
    value: Type
    type: TypeOfTypes

    def __init__(self, value: Type = None, type: str = None) -> None:
        self.value = value
        self.type = type

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Variable):
            return self.value == value.value and self.type == value.type
        return False
