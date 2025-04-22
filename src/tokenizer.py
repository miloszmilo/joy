from abc import ABC, abstractmethod
from enum import Enum
from src.exceptions.TokenizerValueError import TokenizerValueError
from src.joyTypes.Token import Token, TokenType


class TokenizerState(Enum):
    NEW_TOKEN = "new_token"
    NUMBER = "number"
    PARENTHESIS_OPEN = "parenthesis_open"
    PARENTHESIS_CLOSE = "parenthesis_close"
    OPERATOR = "operator"
    COMPLETE_TOKEN = "complete_token"
    SYMBOL_NAME = "symbol_name"
    FANCY_NUMBER = "fancy_number"
    HEX = "hex"
    BINARY = "binary"
    STRING = "string"
    SCOPE_OPEN = "scope_open"
    SCOPE_CLOSE = "scope_close"
    COMMA = "comma"
    END_OF_STATEMENT = "end_of_statement"


class Tokenizer:
    current_state: TokenizerState
    next_state: TokenizerState
    token_string: str
    token_current: Token
    operator_digits: list[str]
    operators: list[str]
    parenthesis_balance: int
    scope_balance: int
    decimal_point_found: bool
    keywords: list[str]
    _i: int

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
        self.scope_balance = 0
        self._numbers: str = ".0123456789"
        self._hex_numbers: str = "0123456789abcdefABCDEF"  # prefix 0x
        self._bin_numbers: str = "01"  # prefix 0b
        self._symbol_names: str = (
            "abcdefghijklmnoprstuwvxyz.ABCDEFGHIJKLMNOPRSTUWVXYZ_0123456789"
        )
        self.decimal_point_found = False
        self.fancy_numeric: str = ""
        self.keywords = ["var", "if"]
        self._i = 0

    def tokenize(self, string: str) -> list[Token]:
        output: list[Token] = []
        while self._i in range(len(string)):
            char = string[self._i]
            self.current_state = self.next_state

            # First character analysis
            if self.current_state == TokenizerState.NEW_TOKEN:
                self.token_string = ""
                self.token_current = Token()
                self.decimal_point_found = False
                self.fancy_numeric = ""

                if char.isspace():
                    self.next_state = TokenizerState.NEW_TOKEN
                    self._i += 1
                    continue

                if char in self._numbers:
                    if char == "." and self.decimal_point_found:
                        raise TokenizerValueError(
                            f"Found more than one decimal point in float. {string}"
                        )
                    if char == ".":
                        self.decimal_point_found = True
                    self.next_state = TokenizerState.NUMBER
                    if char == "0":
                        self.next_state = TokenizerState.FANCY_NUMBER
                    self.token_string = char
                    self._i += 1
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
                if char == "{":
                    self.next_state = TokenizerState.SCOPE_OPEN
                    continue
                if char == "}":
                    self.next_state = TokenizerState.SCOPE_CLOSE
                    continue
                if char == ",":
                    self.next_state = TokenizerState.COMMA
                    continue
                if char == ";":
                    self.next_state = TokenizerState.END_OF_STATEMENT
                    continue
                if char == '"':
                    self.next_state = TokenizerState.STRING
                    self._i += 1
                    continue
                self.token_string += char
                self._i += 1
                self.next_state = TokenizerState.SYMBOL_NAME
                continue

            if self.current_state == TokenizerState.STRING:
                if char == '"':
                    self._i += 1
                    self.next_state = TokenizerState.COMPLETE_TOKEN
                    self.token_current = Token(self.token_string, TokenType.STRING)
                    continue
                self.token_string += char
                self._i += 1
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
                    self._i += 1
                    continue
                if char in self._symbol_names:
                    raise TokenizerValueError(f"Got letters in number. {string}")
                self.next_state = TokenizerState.COMPLETE_TOKEN
                self.token_current = Token(
                    self.token_string, TokenType.NUMBER, float(self.token_string)
                )

            if self.current_state == TokenizerState.FANCY_NUMBER:
                if char == "x":
                    self.token_string += char
                    self.next_state = TokenizerState.HEX
                    self._i += 1
                    continue
                if char == "b":
                    self.token_string += char
                    self.next_state = TokenizerState.BINARY
                    self._i += 1
                    continue
                raise TokenizerValueError(f"Expected binary or hex got {char}")

            if self.current_state == TokenizerState.HEX:
                if char in self._hex_numbers:
                    self.token_string += char
                    self.fancy_numeric += char
                    self._i += 1
                    self.next_state = TokenizerState.HEX
                    continue
                if char in self._symbol_names:
                    raise TokenizerValueError(f"Expected hex got {char}")
                self.next_state = TokenizerState.COMPLETE_TOKEN
                self.token_current = Token(
                    self.token_string,
                    TokenType.NUMBER,
                    float(int(self.fancy_numeric, 16)),
                )
                continue

            if self.current_state == TokenizerState.BINARY:
                if char in self._bin_numbers:
                    self.token_string += char
                    self.fancy_numeric += char
                    self._i += 1
                    self.next_state = TokenizerState.BINARY
                    continue
                if char in self._symbol_names:
                    raise TokenizerValueError(f"Expected binary got {char}")
                self.next_state = TokenizerState.COMPLETE_TOKEN
                self.token_current = Token(
                    self.token_string,
                    TokenType.NUMBER,
                    float(int(self.fancy_numeric, 2)),
                )
                continue

            if self.current_state == TokenizerState.OPERATOR:
                if char in self.operator_digits:
                    if (self.token_string + char) in self.operators:
                        self.token_string += char
                        self._i += 1
                        continue
                    if self.token_string in self.operators:
                        self.token_current = Token(
                            self.token_string, TokenType.OPERATOR
                        )
                        self.next_state = TokenizerState.COMPLETE_TOKEN
                        continue
                    self.token_string += char
                    self._i += 1
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
                self._i += 1
                continue
            if self.current_state == TokenizerState.PARENTHESIS_CLOSE:
                self.token_string += char
                self.parenthesis_balance -= 1
                self.token_current = Token(
                    self.token_string, TokenType.PARENTHESIS_CLOSE
                )
                self.next_state = TokenizerState.COMPLETE_TOKEN
                self._i += 1
                continue
            if self.current_state == TokenizerState.SCOPE_OPEN:
                self.token_string += char
                self.scope_balance += 1
                self.token_current = Token(self.token_string, TokenType.SCOPE_OPEN)
                self.next_state = TokenizerState.COMPLETE_TOKEN
                self._i += 1
                continue
            if self.current_state == TokenizerState.SCOPE_CLOSE:
                self.token_string += char
                self.scope_balance -= 1
                self.token_current = Token(self.token_string, TokenType.SCOPE_CLOSE)
                self.next_state = TokenizerState.COMPLETE_TOKEN
                self._i += 1
                continue
            if self.current_state == TokenizerState.COMMA:
                self.token_string += char
                self.token_current = Token(self.token_string, TokenType.COMMA)
                self.next_state = TokenizerState.COMPLETE_TOKEN
                self._i += 1
            if self.current_state == TokenizerState.END_OF_STATEMENT:
                self.token_string += char
                self.token_current = Token(
                    self.token_string, TokenType.END_OF_STATEMENT
                )
                self.next_state = TokenizerState.COMPLETE_TOKEN
                self._i += 1
            if self.current_state == TokenizerState.SYMBOL_NAME:
                if char in self._symbol_names:
                    self.token_string += char
                    self._i += 1
                    continue
                self.token_current = Token(self.token_string, TokenType.SYMBOL)
                if char in self.keywords:
                    self.token_current = Token(self.token_string, TokenType.KEYWORD)
                self.next_state = TokenizerState.COMPLETE_TOKEN
                continue
            if self.current_state == TokenizerState.COMPLETE_TOKEN:
                output.append(self.token_current)
                self.next_state = TokenizerState.NEW_TOKEN
                continue

        if self.parenthesis_balance != 0:
            raise TokenizerValueError(
                f'Parenthesis "(" & ")" not balanced. Expected {self.parenthesis_balance} more'
            )
        if self.scope_balance != 0:
            raise TokenizerValueError(
                f'Scope "{" & "}" not balanced. Expected {self.scope_balance} more.'
            )
        if self.current_state == TokenizerState.STRING:
            raise TokenizerValueError("Missing quotation marks.")
        return output


class TokenizerStateBase(ABC):
    @abstractmethod
    def handle(self, tokenizer: Tokenizer, char: str):
        pass


class NewTokenState(TokenizerStateBase):
    def handle(self, tokenizer: Tokenizer, char: str):
        tokenizer.token_string = ""
        tokenizer.token_current = Token()
        tokenizer.decimal_point_found = False
        tokenizer.fancy_numeric = ""

        if char.isspace():
            tokenizer.next_state = TokenizerState.NEW_TOKEN
            tokenizer._i += 1
            return

        if char in tokenizer._numbers:
            if char == "." and tokenizer.decimal_point_found:
                raise TokenizerValueError(
                    f"Found more than one decimal point in float. {string}"
                )
            if char == ".":
                tokenizer.decimal_point_found = True
            tokenizer.next_state = TokenizerState.NUMBER
            if char == "0":
                tokenizer.next_state = TokenizerState.FANCY_NUMBER
            tokenizer.token_string = char
            tokenizer._i += 1
            return

        if char in tokenizer.operator_digits:
            tokenizer.next_state = TokenizerState.OPERATOR
            return

        if char == "(":
            tokenizer.next_state = TokenizerState.PARENTHESIS_OPEN
            return
        if char == ")":
            tokenizer.next_state = TokenizerState.PARENTHESIS_CLOSE
            return
        if char == '"':
            tokenizer.next_state = TokenizerState.STRING
            tokenizer._i += 1
            return
        tokenizer.token_string += char
        tokenizer._i += 1
        tokenizer.next_state = TokenizerState.SYMBOL_NAME
        return
