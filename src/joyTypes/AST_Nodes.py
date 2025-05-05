from abc import ABC, abstractmethod
from typing import override

from src.joyTypes.Token import Token


class Node(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


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
class NumberLiteral(Expression):
    def __init__(self, value: float = 0.0) -> None:
        self.value: float = value

    @override
    def accept(self, visitor):
        return visitor.visit_number_literal(self)

    @override
    def __repr__(self) -> str:
        return f"NumberLiteral(value={self.value})"

    @override
    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, NumberLiteral):
            return False
        return self.value == value.value


class VariableAccess(Expression):
    def __init__(self, name: str) -> None:
        self.name: float = name

    @override
    def accept(self, visitor):
        return visitor.visit_variable_access(self)


class VariableDeclaration(Expression):
    def __init__(self, name: str, value: Expression) -> None:
        self.name: str = name
        self.value: Expression = value

    @override
    def accept(self, visitor):
        return visitor.visit_variable_declaration(self)

    @override
    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, VariableDeclaration):
            return False
        return self.name == value.name and self.value == value.value

    @override
    def __repr__(self) -> str:
        return f"VariableDeclaration(name={self.name}, value={self.value})"


class Comparison(Expression):
    left: Token
    operator: Token
    right: Token

    def __init__(self, left: Token, operator: Token, right: Token) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    @override
    def accept(self, visitor):
        return visitor.visit_variable_access(self)

    @override
    def __str__(self) -> str:
        return f"{self.left.__str__()} {self.operator.__str__()} {self.right.__str__()}"

    @override
    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, Comparison):
            return False
        return (
            self.left == value.left
            and self.operator == value.operator
            and self.right == value.right
        )


# Statements
class IfStatement(Statement):
    condition: Comparison
    body: Node | None
    elseBody: Node | None

    def __init__(
        self,
        condition: Comparison,
        body: Node | None = None,
        elseBody: Node | None = None,
    ):
        self.condition = condition
        self.body = body
        self.elseBody = elseBody

    @override
    def accept(self, visitor):
        return super().accept(visitor)

    @override
    def __str__(self) -> str:
        return f"if ({self.condition}) \nthen {{ \n{self.body}\n}}\nelse {{\n{self.elseBody}\n}}"

    @override
    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, IfStatement):
            return False
        return (
            self.condition == value.condition
            and self.body == value.body
            and self.elseBody == value.elseBody
        )

    @override
    def __repr__(self) -> str:
        return f"IfStatement(condition={self.condition}, body={self.body}, elseBody={self.elseBody})"


class WhileStatement(Statement):
    condition: Comparison
    body: Expression | None

    def __init__(self, condition: Comparison, body: Expression | None) -> None:
        self.condition = condition
        self.body = body

    @override
    def accept(self, visitor):
        return super().accept(visitor)

    @override
    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, WhileStatement):
            return False
        return self.condition == value.condition and self.body == value.body

    @override
    def __str__(self) -> str:
        return f"while ({self.condition})\nthen {{\n{self.body}\n}}"

    @override
    def __repr__(self) -> str:
        return f"WhileStatement(condition={self.condition}, body={self.body})"

class PrintStatement(Statement):
    text: str
    def __init__(self, text: str = "") -> None:
        self.text = text

    @override
    def accept(self, visitor):
        return super().accept(visitor)

    @override
    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, PrintStatement):
            return False
        return self.text == value.text

    @override
    def __str__(self) -> str:
        return self.text

    @override
    def __repr__(self) -> str:
        return f'PrintStatement(text={self.text})'
