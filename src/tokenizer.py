from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import override
from src.exceptions.TokenizerValueError import TokenizerValueError
from src.joyTypes.Token import Token, TokenType


class TokenizerStateBase(ABC):
    @abstractmethod
    def handle(self, tokenizer: Tokenizer) -> None:
        pass


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
    current_state: TokenizerStateBase
    next_state: TokenizerStateBase
    token_string: str
    token_current: Token
    operator_digits: list[str]
    operators: list[str]
    parenthesis_balance: int
    scope_balance: int
    decimal_point_found: bool
    keywords: list[str]
    _i: int
    _string: str
    char: str
    output: list[Token]

    def __init__(self):
        self.current_state = NewTokenState()
        self.next_state = NewTokenState()
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
        self._string = ""
        self.char = ""
        self.output = []

    def next_char(self):
        self._i += 1
        if self._i < len(self._string):
            self.char = self._string[self._i]

    def tokenize(self, string: str) -> list[Token]:
        self._string = string + " "
        self.char = self._string[self._i]
        while self._i in range(len(self._string)):
            self.current_state.handle(self)
            if self.next_state:
                self.current_state = self.next_state
        if self.parenthesis_balance != 0:
            raise TokenizerValueError(
                f'Parenthesis "(" & ")" not balanced. Expected {self.parenthesis_balance} more'
            )
        if self.scope_balance != 0:
            raise TokenizerValueError(
                f'Scope "{" & "}" not balanced. Expected {self.scope_balance} more.'
            )
        if isinstance(self.current_state, StringState):
            raise TokenizerValueError("Missing quotation marks.")
        return self.output


class NewTokenState(TokenizerStateBase):
    @override
    def handle(self, tokenizer: Tokenizer):
        tokenizer.token_string = ""
        tokenizer.token_current = Token()
        tokenizer.decimal_point_found = False
        tokenizer.fancy_numeric = ""

        if tokenizer.char.isspace():
            tokenizer.next_state = NewTokenState()
            tokenizer.next_char()
            return

        if tokenizer.char in tokenizer._numbers:
            if tokenizer.char == "." and tokenizer.decimal_point_found:
                raise TokenizerValueError("Found more than one decimal point in float.")
            if tokenizer.char == ".":
                tokenizer.decimal_point_found = True
            tokenizer.next_state = NumberState()
            if tokenizer.char == "0":
                tokenizer.next_state = FancyNumberState()
            tokenizer.token_string = tokenizer.char
            tokenizer.next_char()
            return

        if tokenizer.char in tokenizer.operator_digits:
            tokenizer.next_state = OperatorState()
            return

        if tokenizer.char == "(":
            tokenizer.next_state = OpenParenthesisState()
            return
        if tokenizer.char == ")":
            tokenizer.next_state = CloseParenthesisState()
            return
        if tokenizer.char == '"':
            tokenizer.next_state = StringState()
            tokenizer.next_char()
            return
        if tokenizer.char == "{":
            tokenizer.next_state = OpenScopeState()
            return
        if tokenizer.char == "}":
            tokenizer.next_state = CloseScopeState()
            return
        if tokenizer.char == ",":
            tokenizer.next_state = CommaState()
            return
        if tokenizer.char == ";":
            tokenizer.next_state = EndOfStatementState()
            return
        tokenizer.token_string += tokenizer.char
        tokenizer.next_char()
        tokenizer.next_state = SymbolNameState()


class StringState(TokenizerStateBase):
    @override
    def handle(self, tokenizer: Tokenizer):
        if tokenizer.char == '"':
            tokenizer.next_char()
            tokenizer.next_state = CompleteState()
            tokenizer.token_current = Token(tokenizer.token_string, TokenType.STRING)
            return
        tokenizer.token_string += tokenizer.char
        tokenizer.next_char()


class NumberState(TokenizerStateBase):
    @override
    def handle(self, tokenizer: Tokenizer):
        if tokenizer.char in tokenizer._numbers:
            if tokenizer.char == "." and tokenizer.decimal_point_found:
                raise TokenizerValueError("Found more than one decimal point in float.")
            if tokenizer.char == ".":
                tokenizer.decimal_point_found = True
            tokenizer.token_string += tokenizer.char
            tokenizer.next_state = NumberState()
            tokenizer.next_char()
            return
        if tokenizer.char in tokenizer._symbol_names:
            raise TokenizerValueError("Got letters in number.")
        tokenizer.next_state = CompleteState()
        tokenizer.token_current = Token(
            tokenizer.token_string, TokenType.NUMBER, float(tokenizer.token_string)
        )


class FancyNumberState(TokenizerStateBase):
    @override
    def handle(self, tokenizer: Tokenizer):
        if tokenizer.char == "x":
            tokenizer.token_string += tokenizer.char
            tokenizer.next_state = HexNumberState()
            tokenizer.next_char()
            return
        if tokenizer.char == "b":
            tokenizer.token_string += tokenizer.char
            tokenizer.next_state = BinNumberState()
            tokenizer.next_char()
            return
        raise TokenizerValueError(f"Expected binary or hex got {tokenizer.char}")


class HexNumberState(TokenizerStateBase):
    @override
    def handle(self, tokenizer: Tokenizer):
        if tokenizer.char in tokenizer._hex_numbers:
            tokenizer.token_string += tokenizer.char
            tokenizer.fancy_numeric += tokenizer.char
            tokenizer.next_char()
            tokenizer.next_state = HexNumberState()
            return
        if tokenizer.char in tokenizer._symbol_names:
            raise TokenizerValueError(f"Expected hex got {tokenizer.char}")
        tokenizer.next_state = CompleteState()
        tokenizer.token_current = Token(
            tokenizer.token_string,
            TokenType.NUMBER,
            float(int(tokenizer.fancy_numeric, 16)),
        )


class BinNumberState(TokenizerStateBase):
    @override
    def handle(self, tokenizer: Tokenizer):
        if tokenizer.char in tokenizer._bin_numbers:
            tokenizer.token_string += tokenizer.char
            tokenizer.fancy_numeric += tokenizer.char
            tokenizer.next_char()
            tokenizer.next_state = BinNumberState()
            return
        if tokenizer.char in tokenizer._symbol_names:
            raise TokenizerValueError(f"Expected binary got {tokenizer.char}")
        tokenizer.next_state = CompleteState()
        tokenizer.token_current = Token(
            tokenizer.token_string,
            TokenType.NUMBER,
            float(int(tokenizer.fancy_numeric, 2)),
        )


class OperatorState(TokenizerStateBase):
    @override
    def handle(self, tokenizer: Tokenizer):
        if tokenizer.char in tokenizer.operator_digits:
            if (tokenizer.token_string + tokenizer.char) in tokenizer.operators:
                tokenizer.token_string += tokenizer.char
                tokenizer.next_char()
                return
            if tokenizer.token_string in tokenizer.operators:
                tokenizer.token_current = Token(
                    tokenizer.token_string, TokenType.OPERATOR
                )
                tokenizer.next_state = CompleteState()
                return
            tokenizer.token_string += tokenizer.char
            tokenizer.next_char()
            return
        if tokenizer.token_string in tokenizer.operators:
            tokenizer.token_current = Token(tokenizer.token_string, TokenType.OPERATOR)
            tokenizer.next_state = CompleteState()
            return
        raise TokenizerValueError(f'Unrecognized operator "{tokenizer.token_string}".')


class OpenParenthesisState(TokenizerStateBase):
    @override
    def handle(self, tokenizer: Tokenizer):
        tokenizer.token_string += tokenizer.char
        tokenizer.parenthesis_balance += 1
        tokenizer.token_current = Token(
            tokenizer.token_string, TokenType.PARENTHESIS_OPEN
        )
        tokenizer.next_state = CompleteState()
        tokenizer.next_char()


class CloseParenthesisState(TokenizerStateBase):
    @override
    def handle(self, tokenizer: Tokenizer):
        tokenizer.token_string += tokenizer.char
        tokenizer.parenthesis_balance -= 1
        tokenizer.token_current = Token(
            tokenizer.token_string, TokenType.PARENTHESIS_CLOSE
        )
        tokenizer.next_state = CompleteState()
        tokenizer.next_char()


class OpenScopeState(TokenizerStateBase):
    @override
    def handle(self, tokenizer: Tokenizer):
        tokenizer.token_string += tokenizer.char
        tokenizer.scope_balance += 1
        tokenizer.token_current = Token(tokenizer.token_string, TokenType.SCOPE_OPEN)
        tokenizer.next_state = CompleteState()
        tokenizer.next_char()


class CloseScopeState(TokenizerStateBase):
    @override
    def handle(self, tokenizer: Tokenizer):
        tokenizer.token_string += tokenizer.char
        tokenizer.scope_balance -= 1
        tokenizer.token_current = Token(tokenizer.token_string, TokenType.SCOPE_CLOSE)
        tokenizer.next_state = CompleteState()
        tokenizer.next_char()


class CommaState(TokenizerStateBase):
    @override
    def handle(self, tokenizer: Tokenizer):
        tokenizer.token_string += tokenizer.char
        tokenizer.token_current = Token(tokenizer.token_string, TokenType.COMMA)
        tokenizer.next_state = CompleteState()
        tokenizer.next_char()


class EndOfStatementState(TokenizerStateBase):
    @override
    def handle(self, tokenizer: Tokenizer):
        tokenizer.token_string += tokenizer.char
        tokenizer.token_current = Token(
            tokenizer.token_string, TokenType.END_OF_STATEMENT
        )
        tokenizer.next_state = CompleteState()
        tokenizer.next_char()


class SymbolNameState(TokenizerStateBase):
    @override
    def handle(self, tokenizer: Tokenizer):
        if tokenizer.char in tokenizer._symbol_names:
            tokenizer.token_string += tokenizer.char
            tokenizer.next_char()
            return
        tokenizer.token_current = Token(tokenizer.token_string, TokenType.SYMBOL)
        if tokenizer.char in tokenizer.keywords:
            tokenizer.token_current = Token(tokenizer.token_string, TokenType.KEYWORD)
        tokenizer.next_state = CompleteState()


class CompleteState(TokenizerStateBase):
    @override
    def handle(self, tokenizer: Tokenizer):
        tokenizer.output.append(tokenizer.token_current)
        tokenizer.next_state = NewTokenState()
