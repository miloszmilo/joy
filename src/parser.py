from src.joyTypes.AST_Nodes import Comparison, IfStatement, Node
from src.joyTypes.Token import Token, TokenType


class Parser:
    current: int
    tokens: list[Token]

    def __init__(self, current: int = 0, tokens: list[Token] | None = None) -> None:
        self.current = current
        self.tokens = tokens if tokens else []

    def parse(self):
        statements = []
        while self.current < len(self.tokens):
            statements.append(self.parse_statement())
        return

    def parse_statements(self) -> Node:
        if self.match(TokenType.KEYWORD, "if"):
            self.parse_if_statement()
        if self.match(TokenType.KEYWORD, "while"):
            self.parse_while_statement()
        if self.match(TokenType.KEYWORD, "print"):
            self.parse_print_statement()
        if self.match(TokenType.KEYWORD, "var"):
            self.parse_var_statement()
        if self.match(TokenType.OPERATOR, "{"):
            self.parse_scope_statement()
        return self.parse_expression()

    def parse_if_statement(self) -> Node:
        _ = self.consume(TokenType.PARENTHESIS_OPEN)
        condition = self.parse_expression()
        _ = self.consume(TokenType.PARENTHESIS_CLOSE)

        _ = self.consume(TokenType.SCOPE_OPEN)
        # If body is empty, continue
        body = None
        if not self.match(TokenType.SCOPE_CLOSE):
            body = self.parse_statements()
        _ = self.consume(TokenType.SCOPE_CLOSE)

        else_branch: Node | None = None
        if self.match(TokenType.KEYWORD, "else"):
            else_branch = self.parse_statement()
        return IfStatement(condition, body, else_branch)

    def parse_while_statement(self) -> Node:
        self.consume(TokenType.PARENTHESIS_OPEN)
        condition = self.parse_expression()
        self.consume(TokenType.PARENTHESIS_CLOSE)
        pass

    def parse_print_statement(self) -> Node:
        pass

    def parse_var_statement(self) -> Node:
        pass

    def parse_scope_statement(self) -> Node:
        pass

    def parse_expression(self) -> Node:
        if not self.match(TokenType.NUMBER) and self.match(TokenType.SYMBOL):
            raise SyntaxError(
                f"Expected Number or Symbol in expression, got {self.peek()}"
            )
        left = None
        if self.match(TokenType.NUMBER):
            left = self.consume(TokenType.NUMBER)
        if self.match(TokenType.SYMBOL):
            left = self.consume(TokenType.SYMBOL)

        operator = self.consume(TokenType.COMPARISON_OPERATOR)

        if not self.match(TokenType.NUMBER) and self.match(TokenType.SYMBOL):
            raise SyntaxError(
                f"Expected Number or Symbol in expression, got {self.peek()}"
            )

        right = None
        if self.match(TokenType.NUMBER):
            right = self.consume(TokenType.NUMBER)
        if self.match(TokenType.SYMBOL):
            right = self.consume(TokenType.SYMBOL)
        return Comparison(left, operator, right)

    def match(self, type: TokenType, value: str | None = None) -> bool:
        if self.peek().type != type:
            return False
        if value and self.peek().token != value:
            return False
        token = self.peek()
        if value:
            return token.type == type and token.token == value
        return token.type == type

    def consume(self, type: TokenType, value: str | None = None):
        if self.peek().type != type:
            raise SyntaxError(f"Expected {type} but found {self.peek()}")
        if value and self.peek().token != value:
            raise SyntaxError(f"Expected {type}, {value} but found {self.peek()}")
        token = self.peek()
        if value and token.type == type and token.token == value:
            self.advance()
            return self.previous()
        if token.type == type:
            self.advance()
            return self.previous()
        raise SyntaxError(f"Expected {type} but found {self.peek()}")

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def advance(self):
        if not self.is_at_end():
            self.current += 1

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF
