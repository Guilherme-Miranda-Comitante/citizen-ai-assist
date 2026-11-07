"""Classe Assistente: atendimento, histórico, indicadores e CSV."""
import csv
import json
import time
from datetime import datetime

from base_conhecimento import MINIMO_PARA_RESPONDER

LIMITE_ALTA = 6
LIMITE_MEDIA = 3
CAMPOS_CSV = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
              "ajudou", "tentativas", "tempo_segundos"]


def ler_opcao(texto, minimo, maximo):
    """Pede um número entre minimo e maximo. Repete até ser válido."""
    while True:
        entrada = input(texto).strip()
        if entrada.isdigit() and minimo <= int(entrada) <= maximo:
            return int(entrada)
        print(f"Opção inválida. Digite um número de {minimo} a {maximo}.")


def ler_sim_nao(texto):
    """Pede s/n. Repete até ser válido. Retorna True para 's'."""
    while True:
        entrada = input(texto).strip().lower()
        if entrada in ("s", "n"):
            return entrada == "s"
        print("Resposta inválida. Digite apenas 's' ou 'n'.")


def tem_dado_pessoal(texto):
    """8 ou mais dígitos (CPF, telefone...) ou '@' (e-mail)."""
    digitos = sum(1 for c in texto if c.isdigit())
    return digitos >= 8 or "@" in texto


def nivel_confianca(pontos):
    if pontos >= LIMITE_ALTA:
        return "ALTA"
    if pontos >= LIMITE_MEDIA:
        return "MÉDIA"
    return None


def ler_json_lista(caminho):
    """Lê uma lista de um JSON. Arquivo ausente ou corrompido vira lista vazia."""
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        return dados if isinstance(dados, list) else []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def gravar_json(caminho, dados):
    try:
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)
    except OSError as erro:
        print(f"Aviso: não foi possível salvar '{caminho}' ({erro}).")


class Assistente:
    def __init__(self, nome, base, caminho_historico="data/historico.json",
                 caminho_csv="data/atendimentos.csv", caminho_notas="data/notas.json"):
        self.nome = nome
        self.base = base
        self.caminho_historico = caminho_historico
        self.caminho_csv = caminho_csv
        self.caminho_notas = caminho_notas
        self.historico = ler_json_lista(caminho_historico)
        self.notas = ler_json_lista(caminho_notas)

    # ---------- atendimento por pergunta ----------
    def perguntar(self):
        """Atendimento por texto livre. Um atendimento termina quando a pessoa
        diz que a dúvida foi resolvida ou quando volta ao menu (0)."""
        tentativas = 0
        inicio = None
        ultima = None  # (pergunta, id_orientacao, encontrou, tempo)

        while True:
            if inicio is None:
                inicio = time.time()
            texto = input("\nDigite sua dúvida (0 para voltar): ").strip()

            if texto == "0":
                if ultima is not None:
                    self.registrar("pergunta", ultima[0], ultima[1], ultima[2],
                                   False, tentativas, ultima[3])
                return
            if texto == "":
                print("Você não digitou nada. Escreva sua dúvida ou 0 para voltar.")
                continue
            if tem_dado_pessoal(texto):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            resultados = self.base.buscar(texto)
            tempo = round(time.time() - inicio, 1)

            if not resultados or resultados[0][0] < MINIMO_PARA_RESPONDER:
                print("\nNão encontrei uma orientação para essa dúvida.")
                print("Tente outras palavras (ex.: o nome do documento ou serviço) "
                      "ou use a navegação por categorias:")
                for cat in self.base.categorias():
                    print(f"  - {cat}")
                ultima = (texto, None, False, tempo)
                continue

            pontos, melhor = resultados[0]
            print(f"\nConfiança da resposta: {nivel_confianca(pontos)} ({pontos} pontos)")
            melhor.exibir()

            alternativas = [(p, o) for p, o in resultados[1:3] if p >= 1]
            if alternativas:
                print("\nOutras orientações parecidas:")
                for p, o in alternativas:
                    print(f"  - {o.titulo} [{o.categoria}] ({p} pontos)")

            ajudou = ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            if ajudou:
                self.registrar("pergunta", texto, melhor.id, True, True, tentativas, tempo)
                tentativas = 0
                inicio = None
                ultima = None
            else:
                print("Tudo bem. Tente reescrever a pergunta com outras palavras.")
                ultima = (texto, melhor.id, True, tempo)

    # ---------- navegação por categorias ----------
    def navegar(self):
        categorias = self.base.categorias()
        if not categorias:
            print("Não há categorias disponíveis (base de conhecimento vazia).")
            return

        while True:
            print("\n=== Categorias ===")
            for i, cat in enumerate(categorias, start=1):
                print(f"{i}. {cat}")
            print("0. Voltar")
            escolha = ler_opcao("Escolha uma categoria: ", 0, len(categorias))
            if escolha == 0:
                return
            categoria = categorias[escolha - 1]
            self._navegar_orientacoes(categoria)

    def _navegar_orientacoes(self, categoria):
        orientacoes = self.base.por_categoria(categoria)
        inicio = time.time()
        while True:
            print(f"\n=== {categoria} ===")
            for i, o in enumerate(orientacoes, start=1):
                print(f"{i}. {o.titulo}")
            print("0. Voltar")
            escolha = ler_opcao("Escolha uma orientação: ", 0, len(orientacoes))
            if escolha == 0:
                return
            orientacao = orientacoes[escolha - 1]
            orientacao.exibir()
            tempo = round(time.time() - inicio, 1)
            ajudou = ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            self.registrar("categoria", orientacao.titulo, orientacao.id,
                           True, ajudou, 1, tempo)
            inicio = time.time()

    # ---------- histórico ----------
    def registrar(self, origem, pergunta, id_orientacao, encontrou, ajudou,
                  tentativas, tempo):
        atendimento = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo,
        }
        self.historico.append(atendimento)
        gravar_json(self.caminho_historico, self.historico)
        return atendimento

    def pedir_nota(self):
        """Ao sair, pede a nota de facilidade de uso (1 a 5)."""
        nota = ler_opcao("\nDe 1 a 5, quão fácil foi usar o assistente? ", 1, 5)
        self.notas.append({"data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           "nota": nota})
        gravar_json(self.caminho_notas, self.notas)

    # ---------- indicadores ----------
    def indicadores(self):
        total = len(self.historico)
        encontrados = [a for a in self.historico if a["encontrou"]]
        ajudaram = [a for a in self.historico if a["ajudou"]]
        sem_solucao = [a["pergunta"] for a in self.historico if not a["ajudou"]]

        def pct(parte):
            return round(100 * parte / total, 1) if total else 0.0

        tempo_medio = (round(sum(a["tempo_segundos"] for a in encontrados) / len(encontrados), 1)
                       if encontrados else 0.0)
        tentativas_media = (round(sum(a["tentativas"] for a in self.historico) / total, 2)
                            if total else 0.0)
        facilidade = (round(sum(n["nota"] for n in self.notas) / len(self.notas), 1)
                      if self.notas else None)

        return {
            "total": total,
            "encontrada_pct": pct(len(encontrados)),
            "acerto_pct": pct(len(ajudaram)),
            "tempo_medio": tempo_medio,
            "tentativas_media": tentativas_media,
            "facilidade": facilidade,
            "sem_solucao": sem_solucao,
        }

    def exibir_indicadores(self):
        ind = self.indicadores()
        print("\n=== Indicadores ===")
        if ind["total"] == 0:
            print("Ainda não há atendimentos registrados.")
        print(f"Atendimentos registrados:      {ind['total']}")
        print(f"Resposta encontrada:           {ind['encontrada_pct']}%")
        print(f"Taxa de acerto (ajudou):       {ind['acerto_pct']}%")
        print(f"Tempo médio para encontrar:    {ind['tempo_medio']} s")
        print(f"Tentativas por atendimento:    {ind['tentativas_media']}")
        facil = ind["facilidade"]
        print(f"Facilidade de uso (1 a 5):     {facil if facil is not None else 'sem notas ainda'}")
        print("Dúvidas sem solução:")
        if ind["sem_solucao"]:
            for pergunta in ind["sem_solucao"]:
                print(f"  - {pergunta}")
        else:
            print("  - Nenhuma")

    # ---------- CSV ----------
    def exportar_csv(self):
        try:
            with open(self.caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS_CSV)
                escritor.writeheader()
                for atendimento in self.historico:
                    escritor.writerow(atendimento)
            print(f"Atendimentos exportados para {self.caminho_csv}.")
            return True
        except OSError as erro:
            print(f"Não foi possível exportar o CSV ({erro}).")
            return False
