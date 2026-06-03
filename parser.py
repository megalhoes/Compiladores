class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def atual(self):
        # Retorna o token atual sem avancar a posicao
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ("FIM", None)

    def consumir(self, tipo_esperado):
        # Consumir token atual
        tipo, valor = self.atual()
        if tipo == tipo_esperado:
            self.pos += 1
            return valor
        raise SyntaxError(
            f"Esperado '{tipo_esperado}', encontrei '{tipo}' ('{valor}')"
        )

    def parsear_programa(self):
        instrucoes = []
        while self.atual()[0] != "FIM":
            instrucoes.append(self.parsear_instrucao())
        return ("PROGRAMA", instrucoes)

    def parsear_instrucao(self):
        tipo, valor = self.atual()
        # TODO: adicionar suporte a cada tipo de instrucao para debug
        raise SyntaxError(f"Instrucao ainda nao suportada: '{tipo}' = '{valor}'")
