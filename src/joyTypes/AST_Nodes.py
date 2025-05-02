from abc import ABC, abstractmethod
from typing import override


class Node(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


class Expression(Node, ABC):
    """Nodes evaluating to value"""

    pass


class Statement(Node, ABC):
    """Nodes performing an action"""

    pass


# Expressions
class NumberLiteral(Expression):
    def __init__(self, value: float = 0.0) -> None:
        self.value: float = value

    @override
    def accept(self, visitor):
        return visitor.visit_number_literal(self)


# Statements
class IfStatement(Statement):
    condition: Expression
    body: Expression
    elseBody: Expression | None

    def __init__(
        self,
        condition: Expression,
        body: Expression,
        elseBody: Expression | None = None,
    ):
        self.condition = condition
        self.body = body
        self.elseBody = elseBody

    @override
    def accept(self, visitor):
        return super().accept(visitor)
