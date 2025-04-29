from src.abstract_syntax_tree import AbstractSyntaxTree, Node
from src.joyTypes.Token import Token, TokenType


def test_ast():
    ast = AbstractSyntaxTree()

    assert isinstance(ast, AbstractSyntaxTree)


def test_ast_hello():
    ast = AbstractSyntaxTree()
    file_path = "examples/hello.joy"
    ast.parse(file_path)

    expected_result = AbstractSyntaxTree(
        Node(
            Token("print", TokenType.KEYWORD),
            Node(Token('"Hello, World!"', TokenType.STRING)),
        )
    )

    assert ast == expected_result


def test_ast_from_var():
    ast = AbstractSyntaxTree()
    expr = "var x = 4;"
    ast._parse_line(expr)

    expected_result = AbstractSyntaxTree(
        Node(
            Token("=", TokenType.ASSIGNMENT),
            Node(
                Token("var", TokenType.KEYWORD),
                right=Node(Token("x", TokenType.SYMBOL)),
            ),
            Node(Token("4", TokenType.NUMBER)),
        )
    )

    assert ast == expected_result


def test_ast_from_var_and_expr():
    ast = AbstractSyntaxTree()
    expr = """
            var x = 4 + 3 + 2 + 1;
            var y = x + 1;
            """
    ast._parse_line(expr)

    expected_result = AbstractSyntaxTree(
        [
            Node(
                Token("=", TokenType.ASSIGNMENT),
                Node(Token("x", TokenType.SYMBOL)),
                Node(Token("10", TokenType.NUMBER)),
            ),
            Node(
                Token("=", TokenType.ASSIGNMENT),
                Node(Token("y", TokenType.SYMBOL)),
                Node("x+1", TokenType.EXPRESSION),
            ),
        ]
    )

    assert ast == expected_result
