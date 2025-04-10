import re
from src.exceptions.TokenizerValueError import TokenizerValueError
from src.joyTypes.Token import Token

tokens = {
    "=": "equals",
    "*": "times",
    "/": "slash",
    "%": "modulo",
    "+": "plus",
    "-": "minus",
    "if": "ifsym",
    "else": "elsesym",
    "while": "whilesym",
    "var": "varsym",
    "print": "printsym",
    ";": "semicol",
    "(": "lparen",
    ")": "rparen",
    "{": "curly_lparen",
    "}": "curly_rparen",
    '"': "quote",
    "<": "less_than",
    ">": "greater_than",
    "<=": "less_than_or_equal",
    ">=": "greater_than_or_equal",
    "==": "equal_to",
    "!=": "not_equal_to",
}


class Tokenizer:
    def __init__(self):
        pass

    def to_tokens(self, string: str) -> list[Token]:
        token_list: list[Token] = []
        string = string.strip().lstrip()
        char: str = string
        if string.find(" ") != -1:
            char = re.split(r"\s+", string, maxsplit=1)[0]

        type = ""
        if char in tokens:
            type = tokens[char]
        if char.isnumeric() and not type:
            type = "number"
        if char.find(".") != -1 and not type:
            try:
                _ = float(char)
                type = "number"
            except ValueError:
                raise TokenizerValueError(
                    f"Token {char} is not a float but contains '.'"
                )
        if char.isalnum() and not type:
            type = "variable"
        token_list.append(Token(char, type))

        if len(string) == len(char):
            return token_list
        char_length = len(char)
        print("New string:", string[char_length:])
        token_list += self.to_tokens(string[char_length:])
        return token_list
