from src.evaluator import Evaluator
from src.joyTypes.AST_Nodes import (
    Comparison,
    Expression,
    IfStatement,
    Node,
    NumberLiteral,
    PrintStatement,
    ScopeStatement,
    VariableDeclaration,
    WhileStatement,
)
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

    def parse_statement(self) -> Node:
        if self.match(TokenType.KEYWORD, "if"):
            return self.parse_if_statement()
        if self.match(TokenType.KEYWORD, "while"):
            return self.parse_while_statement()
        if self.match(TokenType.KEYWORD, "print"):
            return self.parse_print_statement()
        if self.match(TokenType.KEYWORD, "var"):
            return self.parse_var_statement()
        if self.match(TokenType.OPERATOR, "{"):
            return self.parse_scope_statement()
        return self.parse_expression()

    def parse_if_statement(self) -> IfStatement:
        _ = self.consume(TokenType.KEYWORD, "if")
        _ = self.consume(TokenType.PARENTHESIS_OPEN)
        condition = self.parse_conditional()
        _ = self.consume(TokenType.PARENTHESIS_CLOSE)
        _ = self.consume(TokenType.SCOPE_OPEN)

        body = None
        if not self.match(TokenType.SCOPE_CLOSE):
            body = self.parse_statement()
        _ = self.consume(TokenType.SCOPE_CLOSE)

        else_branch: Node | None = None
        if self.match(TokenType.KEYWORD, "else"):
            else_branch = self.parse_statement()
        return IfStatement(condition, body, else_branch)

    def parse_while_statement(self) -> WhileStatement:
        _ = self.consume(TokenType.KEYWORD, "while")
        _ = self.consume(TokenType.PARENTHESIS_OPEN)
        condition = self.parse_conditional()
        _ = self.consume(TokenType.PARENTHESIS_CLOSE)
        return WhileStatement(condition, None)

    def parse_print_statement(self) -> Node:
        _ = self.consume(TokenType.KEYWORD, "print")
        _ = self.consume(TokenType.PARENTHESIS_OPEN)
        string = self.consume(TokenType.STRING)
        _ = self.consume(TokenType.PARENTHESIS_CLOSE)
        return PrintStatement(string.token)

    def parse_var_statement(self) -> VariableDeclaration:
        _ = self.consume(TokenType.KEYWORD, "var")
        name = self.consume(TokenType.SYMBOL)
        _ = self.consume(TokenType.ASSIGNMENT)
        value = self.parse_expression()
        return VariableDeclaration(name.token, value)

    def parse_scope_statement(self) -> Node:
        _ = self.consume(TokenType.SCOPE_OPEN)
        scope = self.parse_statement()
        _ = self.consume(TokenType.SCOPE_CLOSE)
        return ScopeStatement(scope)

    def parse_conditional(self) -> Comparison:
        if not self.match(TokenType.NUMBER) and self.match(TokenType.SYMBOL):
            raise SyntaxError(
                f"Expected Number or Symbol in expression, got {self.peek()}"
            )
        left = Token()
        if self.match(TokenType.NUMBER):
            left = self.consume(TokenType.NUMBER)
        if self.match(TokenType.SYMBOL):
            left = self.consume(TokenType.SYMBOL)

        operator = self.consume(TokenType.COMPARISON_OPERATOR)

        if not self.match(TokenType.NUMBER) and self.match(TokenType.SYMBOL):
            raise SyntaxError(
                f"Expected Number or Symbol in expression, got {self.peek()}"
            )

        right = Token()
        if self.match(TokenType.NUMBER):
            right = self.consume(TokenType.NUMBER)
        if self.match(TokenType.SYMBOL):
            right = self.consume(TokenType.SYMBOL)
        return Comparison(left, operator, right)

    def parse_expression(self) -> Expression:
        token_list: list[Token] = []
        cur = self.peek()
        while cur.type in [TokenType.NUMBER, TokenType.OPERATOR]:
            if cur.type == TokenType.NUMBER:
                token_list.append(self.consume(TokenType.NUMBER))
                cur = self.peek()
                continue
            token_list.append(self.consume(TokenType.OPERATOR))
            cur = self.peek()
        if cur.type != TokenType.EOF:
            token_list.append(Token("EOF", TokenType.EOF))
        else:
            token_list.append(self.consume(TokenType.EOF))
        num_value = Evaluator(token_list).solve()
        return NumberLiteral(num_value)

    def match(self, type: TokenType, value: str | None = None) -> bool:
        if self.peek().type != type:
            return False
        if value and self.peek().token != value:
            return False
        token = self.peek()
        if value:
            return token.type == type and token.token == value
        return token.type == type

    def consume(self, type: TokenType, value: str | None = None) -> Token:
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
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return self.previous()

    def previous(self):
        return self.tokens[self.current - 1]

    def advance(self):
        self.current += 1

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF
