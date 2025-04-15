from collections import deque
from enum import EnumType
from typing import override

from src.exceptions.ExpressionError import ExpressionError
from src.joyTypes.NodeAbstractSyntax import NodeAbstractSyntax
from src.joyTypes.Token import Token

operators = {
    "*": 1,
    "/": 2,
    "%": 3,
    "+": 4,
    "-": 5,
}


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

    def __init__(
        self,
        value: str = "",
        type: str | None = SymbolType.UNKNOWN,
        argument_count: int = 2,
    ) -> None:
        self.value = value
        self.type = type
        self.argument_count = argument_count

    @override
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Symbol):
            return self.value == value.value and self.type == value.type
        return False

    @override
    def __str__(self) -> str:
        return f"{self.value}"

    @override
    def __repr__(self) -> str:
        return f"Symbol({self.value}, {self.type}, {self.argument_count})"


class AbstractSyntaxTree:
    root: NodeAbstractSyntax
    expression_stack: list[NodeAbstractSyntax]
    operator_stack: list[Token]

    def __init__(
        self,
        root: NodeAbstractSyntax = None,
        expression_stack: list[NodeAbstractSyntax] = [],
        operator_stack: list[Token] = [],
    ):
        self.root = root
        self.expression_stack = expression_stack
        self.operator_stack = operator_stack

    def create_from(self, code_line: str = ""):
        """
        go through line of code
        if it's digit, add to expression
        if operator, and the top of operator stack
            has lower priority
            then push current operator on stack
        if stack operator has higher priority
            than current operator
            pop that operator
            pop last two expressions
            create new node with operator as root
            and expressions as nodes
        parenthesis are also pushed onto operator stack

        when you want to produce code from that ast, you do Post Order
        Tree Traversal and for number you generate constant
        for operator you do operation, like for + you'd do 'add'
        """

    def _create_rpn_from(self, code_line: str = "") -> deque[Symbol]:
        holding_stack: deque[Symbol] = deque()
        output_stack: deque[Symbol] = deque()
        for c in code_line.strip().replace(" ", ""):
            if c.isdigit():
                output_stack.append(Symbol(c, SymbolType.NUMBER))
                continue

            if c == "(":
                holding_stack.appendleft(Symbol(c, SymbolType.PARENTHESIS_OPEN))
                continue

            if c == ")":
                while (
                    len(holding_stack) != 0
                    and holding_stack[0].type is not SymbolType.PARENTHESIS_OPEN
                ):
                    output_stack.append(holding_stack.popleft())
                if len(holding_stack) == 0:
                    raise ExpressionError("Parenthesis missmatched")
                if (
                    len(holding_stack) != 0
                    and holding_stack[0].type is SymbolType.PARENTHESIS_OPEN
                ):
                    _ = holding_stack.popleft()
                continue

            if c not in operators.keys():
                raise ExpressionError(f"Symbol {c} is not a valid symbol")

            while (
                len(holding_stack) != 0
                and holding_stack[0].type is not SymbolType.PARENTHESIS_OPEN
            ):
                if holding_stack[0].type != SymbolType.OPERATOR:
                    break
                if operators.get(holding_stack[0].value, 0) <= operators.get(c, 0):
                    output_stack.append(holding_stack.popleft())
                    continue
                break
            holding_stack.appendleft(Symbol(c, SymbolType.OPERATOR))
        while len(holding_stack) != 0:
            output_stack.append(holding_stack.popleft())

        return output_stack

    def _solve_rpn(self, stack: deque[Symbol] = []) -> int:
        output: deque[int] = deque()
        result: int = 0
        for symbol in stack:
            args = []
            if symbol.type is SymbolType.NUMBER:
                output.append(int(symbol.value))
                continue
            if symbol.type is SymbolType.OPERATOR:
                for x in range(symbol.argument_count):
                    if len(output) < x:
                        raise ExpressionError(
                            f"expression invalid, expected {symbol.argument_count} got {len(output)}"
                        )
                    args.append(output.pop())
            result = 0
            if symbol.argument_count == 2:
                if symbol.value[0] == "/":
                    result = args[1] / args[0]
                if symbol.value[0] == "*":
                    result = args[1] * args[0]
                if symbol.value[0] == "+":
                    result = args[1] + args[0]
                if symbol.value[0] == "-":
                    result = args[1] - args[0]
            output.appendleft(result)
        return result if result else 0

    @override
    def __str__(self) -> str:
        return self.root.__str__()

    @override
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, AbstractSyntaxTree):
            return (
                self.root == value.root
                and self.expression_stack == value.expression_stack
                and self.operator_stack == value.operator_stack
            )
        return False
