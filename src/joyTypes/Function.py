from src.joyTypes.Types import Type
from src.joyTypes.Variable import Variable


class Function:
    returnType: Type
    args: list[Variable]
    body: str
