type symbol = (
    number
    | variable
    | expression
    | condition
    | plus
    | minus
    | slash
    | modulo
    | times
    | lparen
    | rparen
    | equal
    | ifsym
    | elsesym
    | whilesym
    | printsym
    | varsym
    | semicol
    | quote
)

type number = int  # 3
type variable = str  # x
type expression = str  # x + 3
type condition = str  # 3 < 0
type plus = str  # +
type minus = str  # -
type slash = str  # /
type modulo = str  # %
type times = str  # *
type lparen = str  # (
type rparen = str  # )
type equal = str  # =
type ifsym = str  # if
type elsesym = str  # else
type whilesym = str  # while
type printsym = str  # print
type varsym = str  # var
type semicol = str  # ;
type quote = str  # "
type less_than = str  # <
type less_than_or_equal = str  # <=
type greater_than = str  # >
type greater_than_or_equal = str  # >=
type equal_to = str  # ==


def is_valid_symbol():
    # return isinstance(value, symbol)
    pass
