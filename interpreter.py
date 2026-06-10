class RetornoFuncao(Exception):
    def __init__(self, valor):
        self.valor = valor

class Interpretador:
    def __init__(self):
        self.ambiente = {}
        self.funcoes  = {}

    def executar(self, no):
        # Processa instrucoes (efeitos colaterais, sem retornar valor)
        tipo = no[0]
        if tipo == "PROGRAMA":
            for instrucao in no[1]: self.executar(instrucao)
        elif tipo == "ATRIB":
            _, nome, expr = no
            self.ambiente[nome] = self.avaliar(expr)
        elif tipo == "PRINT":
            print(self.avaliar(no[1]))
        elif tipo == "IF":
            _, condicao, bloco_if, bloco_else = no
            bloco = bloco_if if self.avaliar(condicao) else bloco_else
            for inst in bloco: self.executar(inst)
        elif tipo == "WHILE":
            _, condicao, bloco = no
            while self.avaliar(condicao):
                for inst in bloco: self.executar(inst)
        elif tipo == "FUNC_DEF":
            _, nome, params, corpo = no
            self.funcoes[nome] = (params, corpo)
        elif tipo == "RETURN":
            raise RetornoFuncao(self.avaliar(no[1]))
        elif tipo == "CHAMADA":
            self.avaliar(no)  # executa descartando o retorno
        else:
            raise RuntimeError(f"No desconhecido: {tipo}")

    def avaliar(self, no):
        tipo = no[0]
        if tipo == "NUM":   return no[1]
        elif tipo == "STR": return no[1]
        elif tipo == "VAR":
            if no[1] not in self.ambiente:
                raise NameError(f"Variavel '{no[1]}' nao foi definida.")
            return self.ambiente[no[1]]
        elif tipo == "BINOP":
            _, op, esq, dir_ = no
            a, b = self.avaliar(esq), self.avaliar(dir_)
            if op == "+": return a + b
            if op == "-": return a - b
            if op == "*": return a * b
            if op == "/":
                if b == 0: raise ZeroDivisionError("Divisao por zero detectada!")
                return a / b
        elif tipo == "COMPARACAO":
            _, op, esq, dir_ = no
            a, b = self.avaliar(esq), self.avaliar(dir_)
            ops = {">":a>b,"<":a<b,">=":a>=b,"<=":a<=b,"==":a==b,"!=":a!=b}
            return ops[op]
        elif tipo == "INPUT":
            entrada = input(no[1])
            try:    return int(entrada)
            except:
                try:    return float(entrada)
                except: return entrada
        elif tipo == "CHAMADA":
            _, nome, args = no
            if nome not in self.funcoes:
                raise NameError(f"Funcao '{nome}' nao definida.")
            params, corpo = self.funcoes[nome]
            amb_anterior = self.ambiente.copy()   # salva escopo
            for param, arg in zip(params, args):
                self.ambiente[param] = self.avaliar(arg)
            resultado = None
            try:
                for inst in corpo: self.executar(inst)
            except RetornoFuncao as r:
                resultado = r.valor
            self.ambiente = amb_anterior          # restaura escopo
            return resultado
        raise RuntimeError(f"Expressao desconhecida: {no}")
