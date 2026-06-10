import sys
from lexer       import tokenizar
from parser      import Parser
from interpreter import Interpretador

def executar_codigo(codigo):
    tokens = tokenizar(codigo)                  # 1. Analise Lexica
    ast    = Parser(tokens).parsear_programa()  # 2. AST
    Interpretador().executar(ast)               # 3. Interpretacao

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            codigo = f.read()
        try:
            executar_codigo(codigo)
        except SyntaxError       as e: print(f"[ERRO DE SINTAXE] {e}")
        except NameError         as e: print(f"[ERRO DE NOME] {e}")
        except ZeroDivisionError as e: print(f"[ERRO MATEMATICO] {e}")
        except Exception         as e: print(f"[ERRO] {e}")
    else:
        print("=== NovaLang REPL === (digite 'sair' para encerrar)")
        linhas = []
        while True:
            try:   linha = input(">>> ")
            except EOFError: break
            if linha.strip() == "sair": break
            linhas.append(linha)
            try:
                executar_codigo("\n".join(linhas))
                linhas = []
            except SyntaxError:
                pass   # aguarda mais linhas

if __name__ == "__main__":
    main()
