from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import override

from src.joyTypes.Token import Token


class Node(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

    @override
    def __eq__(self, value: object, /) -> bool:
        if type(self) is not type(value):
            return False
        return self.__dict__ == value.__dict__


class Expression(Node, ABC):
    """Nodes evaluating to value"""

    pass


class EmptyExpression(Expression):
    @override
    def accept(self, visitor):
        return super().accept(visitor)

    pass


class Statement(Node, ABC):
    """Nodes performing an action"""

    pass


# Expressions
@dataclass
class NumberLiteral(Expression):
    value: float

    @override
    def accept(self, visitor):
        return visitor.visit_number_literal(self)


@dataclass
class VariableAccess(Expression):
    name: str

    @override
    def accept(self, visitor):
        return visitor.visit_variable_access(self)


@dataclass
class VariableDeclaration(Expression):
    name: str
    value: NumberLiteral

    @override
    def accept(self, visitor):
        return visitor.visit_variable_declaration(self)


@dataclass
class Comparison(Expression):
    left: Token
    operator: Token
    right: Token

    @override
    def accept(self, visitor):
        return visitor.visit_variable_access(self)


# Statements
@dataclass
class IfStatement(Statement):
    condition: Comparison
    body: Node | None
    elseBody: Node | None

    @override
    def accept(self, visitor):
        return super().accept(visitor)


@dataclass
class WhileStatement(Statement):
    condition: Comparison
    body: Expression | None

    @override
    def accept(self, visitor):
        return super().accept(visitor)


@dataclass
class PrintStatement(Statement):
    text: str

    @override
    def accept(self, visitor):
        return super().accept(visitor)


@dataclass
class ScopeStatement(Statement):
    body: Expression

    @override
    def accept(self, visitor):
        return super().accept(visitor)
