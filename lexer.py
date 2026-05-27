import re


TOKEN_SPEC = [
    ("NUMERO",      r"\d+(\.\d+)?"),
    ("STRING",      r'\"[^\"]*\"'),
    ("IF",          r"\bif\b"),
    ("ELSE",        r"\belse\b"),
    ("WHILE",       r"\bwhile\b"),
    ("FUNC",        r"\bfunc\b"),
    ("RETURN",      r"\breturn\b"),
    ("PRINT",       r"\bprint\b"),
    ("INPUT",       r"\binput\b"),
    ("IDENT",       r"[a-zA-Z_]\w*"),
    ("OP_COMP",     r"==|!=|<=|>=|<|>"),
    ("OP",          r"[+\-*/]"),
    ("ATRIB",       r"="),
    ("LPAREN",      r"\("),
    ("RPAREN",      r"\)"),
    ("LBRACKET",    r"\["),
    ("RBRACKET",    r"\]"),
    ("LBRACE",      r"\{"),
    ("RBRACE",      r"\}"),
    ("VIRGULA",     r","),
    ("NOVA_LINHA",  r"\n"),
    ("ESPACO",      r"[ \t]+"),
]
def tokenizar(codigo):
    pass