from typing import override

from src.joyTypes.NodeAbstractSyntax import NodeAbstractSyntax
from src.joyTypes.Token import Token
from src.tokenizer import Tokenizer

required_tokens = [";", "{", "}"]
priorities_token = {
    "=": 1,
    "if": 1,
    "while": 1,
    "else": 1,
    "print": 1,
    "(": 2,
    ")": 2,
    "var": 2,
    "==": 3,
    "!=": 3,
    "<": 3,
    ">": 3,
    "<=": 3,
    ">=": 3,
    "*": 4,
    "/": 4,
    "%": 4,
    "+": 5,
    "-": 5,
    '"': 5,
}
operators = ["=", "(", ")", "*", "/", "%", "+", "-"]


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

    def _get_abstract_node_from_stack(self):
        operator = self.operator_stack.pop()
        exp2 = self.expression_stack.pop()
        exp1 = self.expression_stack.pop()

        node = NodeAbstractSyntax(operator.token)
        node.left_child = NodeAbstractSyntax(exp1.value)
        if exp1.left_child:
            node.left_child.left_child = exp1.left_child
        if exp1.right_child:
            node.left_child.right_child = exp1.right_child
        node.right_child = NodeAbstractSyntax(exp2.value)
        if exp2.left_child:
            node.left_child.left_child = exp2.left_child
        if exp2.right_child:
            node.left_child.right_child = exp2.right_child

        self.expression_stack.insert(0, node)

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
        tokenizer = Tokenizer()
        tokens: list[Token] = tokenizer.to_tokens(code_line)
        # if tokens[-1].token not in required_tokens:
        #     raise SyntaxError(
        #         f"Line {code_line} with tokens {tokens} doesn't contain required tokens {required_tokens}"
        #     )

        for token in tokens:
            token_type = token.type
            if token_type == "number":
                self.expression_stack.insert(0, NodeAbstractSyntax(token.token))
                continue
            if token_type == "lparen":
                self.operator_stack.insert(0, token)
                continue
            if token.token in operators:
                if len(self.operator_stack) == 0:
                    self.operator_stack.insert(0, token)
                    continue

                assert self.operator_stack[0].token in priorities_token
                assert token.token in priorities_token

                while self.operator_stack and (
                    priorities_token[self.operator_stack[0].token]
                    >= priorities_token[token.token]
                ):
                    self._get_abstract_node_from_stack()
                self.operator_stack.insert(0, token)
                continue
            if token_type == "rparen":
                while self.operator_stack[0] != "lparen":
                    self._get_abstract_node_from_stack()
                _ = self.operator_stack.pop()
                continue
            raise SyntaxError(
                f"Line {code_line} with tokens {tokens} didn't lead to valid AST"
            )

        while self.operator_stack:
            self._get_abstract_node_from_stack()

        assert len(self.expression_stack) == 1
        self.root = self.expression_stack.pop()

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
