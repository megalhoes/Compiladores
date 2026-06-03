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
    # Combina todos os padroes em um unico regex de grupos nomeados
    tokens = []
    padrao = "|".join(f"(?P<{nome}>{regex})" for nome, regex in TOKEN_SPEC)

    for match in re.finditer(padrao, codigo):
        tipo  = match.lastgroup
        valor = match.group()

        if tipo in ("ESPACO", "NOVA_LINHA"):
            continue
        if tipo == "NUMERO":
            valor = float(valor) if "." in valor else int(valor)
        if tipo == "STRING":
            valor = valor[1:-1]   # remove aspas da string

        tokens.append((tipo, valor))

    return tokens