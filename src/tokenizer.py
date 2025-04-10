import re
from src.exceptions.TokenizerValueError import TokenizerValueError
from src.joyTypes.Token import Token


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
        if char == "=" and not type:
            type = "equals"
        if char == "*" and not type:
            type = "times"
        if char == "/" and not type:
            type = "slash"
        if char == "%" and not type:
            type = "modulo"
        if char == "+" and not type:
            type = "plus"
        if char == "-" and not type:
            type = "minus"
        if char == "if" and not type:
            type = "ifsym"
        if char == "else" and not type:
            type = "elsesym"
        if char == "while" and not type:
            type = "whilesym"
        if char == "var" and not type:
            type = "varsym"
        if char == "print" and not type:
            type = "printsym"
        if char == ";" and not type:
            type = "semicol"
        if char == "(" and not type:
            type = "lparen"
        if char == ")" and not type:
            type = "rparen"
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
