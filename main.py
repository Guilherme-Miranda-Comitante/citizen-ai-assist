"""Citizen Assist AI - assistente de orientação ao cidadão (terminal)."""
import os

from assistente import Assistente, ler_opcao
from base_conhecimento import BaseConhecimento

PASTA = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(PASTA, "data")


def mostrar_menu(nome):
    print(f"\n===== {nome} =====")
    print("1. Fazer uma pergunta")
    print("2. Navegar por categorias")
    print("3. Ver indicadores")
    print("4. Exportar atendimentos para CSV")
    print("0. Sair")


def main():
    os.makedirs(DATA, exist_ok=True)

    base = BaseConhecimento(os.path.join(DATA, "base_conhecimento.json"))
    base.carregar()  # lê o JSON e cria os objetos Orientacao

    assistente = Assistente(
        "Citizen Assist AI", base,
        caminho_historico=os.path.join(DATA, "historico.json"),
        caminho_csv=os.path.join(DATA, "atendimentos.csv"),
        caminho_notas=os.path.join(DATA, "notas.json"),
    )

    print("Olá! Eu oriento jovens no primeiro emprego sobre documentos, trabalho,")
    print("saúde e direitos, usando só fontes oficiais.")
    print("Aviso: este assistente NÃO é um canal oficial e não pede dados pessoais.")

    try:
        while True:
            mostrar_menu(assistente.nome)
            opcao = ler_opcao("Escolha uma opção: ", 0, 4)
            if opcao == 1:
                assistente.perguntar()
            elif opcao == 2:
                assistente.navegar()
            elif opcao == 3:
                assistente.exibir_indicadores()
            elif opcao == 4:
                assistente.exportar_csv()
            else:
                assistente.pedir_nota()
                break
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrando...")

    assistente.exportar_csv()
    print("Obrigado por usar o Citizen Assist AI!")


if __name__ == "__main__":
    main()
