from typing import List
from types.Types import Type
from types.Variable import Variable


class Function():
    returnType: Type
    args: List[Variable]
    body: str
