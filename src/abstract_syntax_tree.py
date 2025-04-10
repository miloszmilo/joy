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


class AbstractSyntaxTree:
    root: NodeAbstractSyntax

    def __init__(self, root: NodeAbstractSyntax = None):
        self.root = root

    def create_from(self, code_line: str = ""):
        tokenizer = Tokenizer()
        tokens: list[Token] = tokenizer.to_tokens(code_line)
        if tokens[-1].token not in required_tokens:
            raise SyntaxError(
                f"Line {code_line} with tokens {tokens} doesn't contain required tokens {required_tokens}"
            )
        # Create priorities in dict
        # then set root accordingly
        scored_tokens = [
            (priorities_token[x.token], x)
            for x in tokens
            if x.token in priorities_token
        ]
        scored_tokens.sort(key=lambda x: x[0])
        print("Scored tokens:", scored_tokens)
        # then recursively call this until end
        self.root = scored_tokens[0][1]

    @override
    def __str__(self) -> str:
        return self.root.__str__()
