import re

TOKEN_SPEC = [
    ("NUMERO",      r"\d+(\.\d+)?"),         # 42 ou 3.14
    ("STRING",      r"\"[^\"]*\""),            # "texto"
    ("IF",          r"\bif\b"),                 # palavra reservada
    ("ELSE",        r"\belse\b"),
    ("WHILE",       r"\bwhile\b"),
    ("FUNC",        r"\bfunc\b"),
    ("RETURN",      r"\breturn\b"),
    ("PRINT",       r"\bprint\b"),
    ("INPUT",       r"\binput\b"),
    ("IDENT",       r"[a-zA-Z_]\w*"),           # variavel ou nome de funcao
    ("OP_COMP",     r"==|!=|<=|>=|<|>"),          # comparacao
    ("OP",          r"[+\-*/]"),                 # matematica
    ("ATRIB",       r"="),                        # atribuicao (apos OP_COMP)
    ("LPAREN",      r"\("),
    ("RPAREN",      r"\)"),
    ("LBRACKET",    r"\["),
    ("RBRACKET",    r"\]"),
    ("LBRACE",      r"\{"),
    ("RBRACE",      r"\}"),
    ("VIRGULA",     r","),
    ("NOVA_LINHA",  r"\n"),                      # descartado
    ("ESPACO",      r"[ \t]+"),                  # descartado
]

def tokenizar(codigo):
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
            valor = valor[1:-1]   # remove aspas

        tokens.append((tipo, valor))

    return tokens
