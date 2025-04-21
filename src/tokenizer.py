from enum import Enum
import re
from src.exceptions.TokenizerValueError import TokenizerValueError
from src.joyTypes.Token import Token, TokenType

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


class TokenizerState(Enum):
    NEW_TOKEN = "new_token"
    NUMBER = "number"
    PARENTHESIS_OPEN = "parenthesis_open"
    PARENTHESIS_CLOSE = "parenthesis_close"
    OPERATOR = "operator"
    COMPLETE_TOKEN = "complete_token"
    SYMBOL_NAME = "symbol_name"


class Tokenizer:
    current_state: TokenizerState
    next_state: TokenizerState
    token_string: str
    token_current: Token
    operator_digits: list[str]
    operators: list[str]
    parenthesis_balance: int
    decimal_point_found: bool

    def __init__(self):
        self.current_state = TokenizerState.NEW_TOKEN
        self.next_state = TokenizerState.NEW_TOKEN
        self.token_string = ""
        self.token_current = Token()
        self.operator_digits = [
            "!",
            "$",
            "%",
            "^",
            "&",
            "*",
            "+",
            "-",
            "=",
            "#",
            "@",
            "?",
            "|",
            "`",
            "/",
            "\\",
            "<",
            ">",
            "~",
        ]
        self.operators = ["+", "-", "/", "*"]
        self.parenthesis_balance = 0
        self._numbers: str = ".0123456789"
        self._symbol_names: str = (
            "abcdefghijklmnoprstuwvxyz.ABCDEFGHIJKLMNOPRSTUWVXYZ_0123456789"
        )
        self.decimal_point_found = False

    def tokenize(self, string: str) -> list[Token]:
        output: list[Token] = []
        i = 0
        while i in range(len(string)):
            char = string[i]
            self.current_state = self.next_state

            # First character analysis
            if self.current_state == TokenizerState.NEW_TOKEN:
                self.token_string = ""
                self.token_current = Token()
                self.decimal_point_found = False

                if char.isspace():
                    self.next_state = TokenizerState.NEW_TOKEN
                    i += 1
                    continue

                if char in self._numbers:
                    if char == "." and self.decimal_point_found:
                        raise TokenizerValueError(
                            f"Found more than one decimal point in float. {string}"
                        )
                    if char == ".":
                        self.decimal_point_found = True
                    self.token_string = char
                    self.next_state = TokenizerState.NUMBER
                    i += 1
                    continue

                if char in self.operator_digits:
                    self.next_state = TokenizerState.OPERATOR
                    continue

                if char == "(":
                    self.next_state = TokenizerState.PARENTHESIS_OPEN
                    continue
                if char == ")":
                    self.next_state = TokenizerState.PARENTHESIS_CLOSE
                    continue
                self.token_string += char
                i += 1
                self.next_state = TokenizerState.SYMBOL_NAME
                continue
            if self.current_state == TokenizerState.NUMBER:
                if char in self._numbers:
                    if char == "." and self.decimal_point_found:
                        raise TokenizerValueError(
                            f"Found more than one decimal point in float. {string}"
                        )
                    if char == ".":
                        self.decimal_point_found = True
                    self.token_string += char
                    self.next_state = TokenizerState.NUMBER
                    i += 1
                    continue
                if char in self._symbol_names:
                    raise TokenizerValueError(f"Got letters in number. {string}")
                self.next_state = TokenizerState.COMPLETE_TOKEN
                self.token_current = Token(
                    self.token_string, TokenType.NUMBER, float(self.token_string)
                )
            if self.current_state == TokenizerState.OPERATOR:
                if char in self.operator_digits:
                    if (self.token_string + char) in self.operators:
                        self.token_string += char
                        i += 1
                        continue
                    if self.token_string in self.operators:
                        self.token_current = Token(
                            self.token_string, TokenType.OPERATOR
                        )
                        self.next_state = TokenizerState.COMPLETE_TOKEN
                        continue
                    self.token_string += char
                    i += 1
                    continue
                if self.token_string in self.operators:
                    self.token_current = Token(self.token_string, TokenType.OPERATOR)
                    self.next_state = TokenizerState.COMPLETE_TOKEN
                    continue
                raise TokenizerValueError(
                    f'Unrecognized operator "{self.token_string}".'
                )
            if self.current_state == TokenizerState.PARENTHESIS_OPEN:
                self.token_string += char
                self.parenthesis_balance += 1
                self.token_current = Token(
                    self.token_string, TokenType.PARENTHESIS_OPEN
                )
                self.next_state = TokenizerState.COMPLETE_TOKEN
                i += 1
                continue
            if self.current_state == TokenizerState.PARENTHESIS_CLOSE:
                self.token_string += char
                self.parenthesis_balance -= 1
                self.token_current = Token(
                    self.token_string, TokenType.PARENTHESIS_CLOSE
                )
                self.next_state = TokenizerState.COMPLETE_TOKEN
                i += 1
                continue
            if self.current_state == TokenizerState.SYMBOL_NAME:
                if char in self._symbol_names:
                    self.token_string += char
                    i += 1
                    continue
                self.token_current = Token(self.token_string, TokenType.SYMBOL)
                self.next_state = TokenizerState.COMPLETE_TOKEN
                continue
            if self.current_state == TokenizerState.COMPLETE_TOKEN:
                output.append(self.token_current)
                self.next_state = TokenizerState.NEW_TOKEN
                continue
        #
        # while True:
        #     if self.current_state == TokenizerState.NUMBER:
        #         self.token_current = Token(
        #             self.token_string, TokenType.NUMBER, float(self.token_string)
        #         )
        #         self.current_state = TokenizerState.COMPLETE_TOKEN
        #         continue
        #     if self.current_state == TokenizerState.OPERATOR:
        #         if self.token_string in self.operators:
        #             self.token_current = Token(self.token_string, TokenType.OPERATOR)
        #             self.current_state = TokenizerState.COMPLETE_TOKEN
        #             continue
        #         raise TokenizerValueError(
        #             f'Unrecognized operator "{self.token_string}".'
        #         )
        #     if self.current_state == TokenizerState.PARENTHESIS_OPEN:
        #         self.parenthesis_balance += 1
        #         self.token_current = Token(
        #             self.token_string, TokenType.PARENTHESIS_OPEN
        #         )
        #         self.current_state = TokenizerState.COMPLETE_TOKEN
        #         continue
        #     if self.current_state == TokenizerState.PARENTHESIS_CLOSE:
        #         self.parenthesis_balance -= 1
        #         self.token_current = Token(
        #             self.token_string, TokenType.PARENTHESIS_CLOSE
        #         )
        #         self.current_state = TokenizerState.COMPLETE_TOKEN
        #         continue
        #     if self.current_state == TokenizerState.SYMBOL_NAME:
        #         self.token_current = Token(self.token_string, TokenType.SYMBOL)
        #         self.current_state = TokenizerState.COMPLETE_TOKEN
        #         continue
        #     output.append(self.token_current)
        #     self.token_string = ""
        #     break
        if self.parenthesis_balance != 0:
            raise TokenizerValueError('Parenthesis "(" & ")" not balanced.')
        return output

    def to_tokens(self, string: str) -> list[Token]:
        token_list: list[Token] = []
        string = string.strip().lstrip()
        char: str = string
        if string.find(" ") != -1:
            char = re.split(r"\s+", string, maxsplit=1)[0]

        type = ""
        if char in tokens:
            type = tokens[char]
        if ";" in char and not type:
            char = char[:-1]
            string = " ;"
        if char.isdigit() and not type:
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

        if len(string) == len(char) and char == string:
            return token_list
        char_length = len(char)
        token_list += self.to_tokens(string[char_length:])
        return token_list
