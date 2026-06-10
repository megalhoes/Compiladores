class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def atual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ("FIM", None)

    def consumir(self, tipo_esperado):
        tipo, valor = self.atual()
        if tipo == tipo_esperado:
            self.pos += 1
            return valor
        raise SyntaxError(f"Esperado '{tipo_esperado}', encontrei '{tipo}' ('{valor}')")

    def parsear_programa(self):
        instrucoes = []
        while self.atual()[0] != "FIM":
            instrucoes.append(self.parsear_instrucao())
        return ("PROGRAMA", instrucoes)

    def parsear_instrucao(self):
        tipo, valor = self.atual()
        if tipo == "IF":      return self.parsear_if()
        elif tipo == "WHILE":   return self.parsear_while()
        elif tipo == "FUNC":    return self.parsear_func()
        elif tipo == "RETURN":  return self.parsear_return()
        elif tipo == "PRINT":   return self.parsear_print()
        elif tipo == "IDENT":   return self.parsear_atribuicao_ou_chamada()
        raise SyntaxError(f"Instrucao desconhecida: '{tipo}' = '{valor}'")

    def parsear_expressao(self):
        # Nivel baixo: + e - (resolvidos por ultimo)
        esquerda = self.parsear_termo()
        while self.atual()[0] == "OP" and self.atual()[1] in ("+", "-"):
            op = self.consumir("OP")
            esquerda = ("BINOP", op, esquerda, self.parsear_termo())
        if self.atual()[0] == "OP_COMP":
            op = self.consumir("OP_COMP")
            esquerda = ("COMPARACAO", op, esquerda, self.parsear_termo())
        return esquerda

    def parsear_termo(self):
        # Nivel alto: * e / (resolvidos antes de + e -)
        esquerda = self.parsear_fator()
        while self.atual()[0] == "OP" and self.atual()[1] in ("*", "/"):
            op = self.consumir("OP")
            esquerda = ("BINOP", op, esquerda, self.parsear_fator())
        return esquerda

    def parsear_fator(self):
        # Unidade basica: numero, variavel, chamada ou agrupamento
        tipo, valor = self.atual()
        if tipo == "NUMERO":
            self.consumir("NUMERO"); return ("NUM", valor)
        elif tipo == "STRING":
            self.consumir("STRING"); return ("STR", valor)
        elif tipo == "INPUT":
            return self.parsear_input()
        elif tipo == "IDENT":
            self.consumir("IDENT")
            if self.atual()[0] == "LPAREN":
                return self.parsear_args_chamada(valor)
            return ("VAR", valor)
        elif tipo in ("LPAREN", "LBRACKET", "LBRACE"):
            # (), [] e {} funcionam igual como agrupadores
            fechamento = {"LPAREN":"RPAREN","LBRACKET":"RBRACKET","LBRACE":"RBRACE"}
            self.consumir(tipo)
            expr = self.parsear_expressao()
            self.consumir(fechamento[tipo])
            return expr
        raise SyntaxError(f"Fator inesperado: '{tipo}' = '{valor}'")

    def parsear_if(self):
        self.consumir("IF")
        condicao = self.parsear_expressao()
        self.consumir("LBRACE")
        bloco_if = self.parsear_bloco()
        self.consumir("RBRACE")
        bloco_else = []
        if self.atual()[0] == "ELSE":
            self.consumir("ELSE")
            self.consumir("LBRACE")
            bloco_else = self.parsear_bloco()
            self.consumir("RBRACE")
        return ("IF", condicao, bloco_if, bloco_else)

    def parsear_while(self):
        self.consumir("WHILE")
        condicao = self.parsear_expressao()
        self.consumir("LBRACE")
        bloco = self.parsear_bloco()
        self.consumir("RBRACE")
        return ("WHILE", condicao, bloco)

    def parsear_func(self):
        self.consumir("FUNC")
        nome = self.consumir("IDENT")
        self.consumir("LPAREN")
        params = []
        while self.atual()[0] != "RPAREN":
            params.append(self.consumir("IDENT"))
            if self.atual()[0] == "VIRGULA":
                self.consumir("VIRGULA")
        self.consumir("RPAREN")
        self.consumir("LBRACE")
        corpo = self.parsear_bloco()
        self.consumir("RBRACE")
        return ("FUNC_DEF", nome, params, corpo)

    def parsear_return(self):
        self.consumir("RETURN")
        return ("RETURN", self.parsear_expressao())

    def parsear_print(self):
        self.consumir("PRINT")
        self.consumir("LPAREN")
        expr = self.parsear_expressao()
        self.consumir("RPAREN")
        return ("PRINT", expr)

    def parsear_input(self):
        self.consumir("INPUT")
        self.consumir("LPAREN")
        msg = self.consumir("STRING")
        self.consumir("RPAREN")
        return ("INPUT", msg)

    def parsear_atribuicao_ou_chamada(self):
        nome = self.consumir("IDENT")
        if self.atual()[0] == "ATRIB":
            self.consumir("ATRIB")
            return ("ATRIB", nome, self.parsear_expressao())
        elif self.atual()[0] == "LPAREN":
            return self.parsear_args_chamada(nome)
        raise SyntaxError(f"Instrucao invalida apos '{nome}'")

    def parsear_args_chamada(self, nome):
        self.consumir("LPAREN")
        args = []
        while self.atual()[0] != "RPAREN":
            args.append(self.parsear_expressao())
            if self.atual()[0] == "VIRGULA":
                self.consumir("VIRGULA")
        self.consumir("RPAREN")
        return ("CHAMADA", nome, args)

    def parsear_bloco(self):
        instrucoes = []
        while self.atual()[0] not in ("RBRACE", "FIM"):
            instrucoes.append(self.parsear_instrucao())
        return instrucoes