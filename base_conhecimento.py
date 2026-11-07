"""Classe BaseConhecimento: carrega o JSON e busca a melhor orientação."""
import json

from orientacao import Orientacao

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "ä": "a",
           "é": "e", "è": "e", "ê": "e",
           "í": "i", "ì": "i", "ï": "i",
           "ó": "o", "ò": "o", "õ": "o", "ô": "o",
           "ú": "u", "ù": "u", "ü": "u", "ç": "c"}

SINAIS = "?!.,;:()-/\"'"

PONTOS_PALAVRA_CHAVE = 3
PONTOS_TITULO = 1
TAMANHO_MIN_PALAVRA_TITULO = 4
MINIMO_PARA_RESPONDER = 3


def normalizar(texto):
    """Minúsculas, sem acentos, sem pontuação, com espaço nas pontas."""
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in SINAIS:
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []  # lista de objetos Orientacao

    def carregar(self):
        """Lê o JSON e cria os objetos Orientacao. Nunca trava o programa.
        Retorna True se carregou ao menos uma orientação."""
        self.orientacoes = []
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            print(f"Aviso: base de conhecimento não encontrada em '{self.caminho}'.")
            return False
        except json.JSONDecodeError:
            print(f"Aviso: o arquivo '{self.caminho}' está corrompido (JSON inválido).")
            return False
        except OSError as erro:
            print(f"Aviso: não foi possível abrir a base de conhecimento ({erro}).")
            return False

        if not isinstance(dados, list):
            print("Aviso: a base deve ser uma lista de orientações.")
            return False

        for posicao, registro in enumerate(dados, start=1):
            try:
                self.orientacoes.append(Orientacao.de_dicionario(registro))
            except (ValueError, TypeError) as erro:
                print(f"Aviso: registro {posicao} ignorado ({erro}).")
        return len(self.orientacoes) > 0

    def categorias(self):
        """Lista de categorias, sem repetir, na ordem em que aparecem."""
        lista = []
        for o in self.orientacoes:
            if o.categoria not in lista:
                lista.append(o.categoria)
        return lista

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        """+3 por palavra-chave presente na pergunta;
        +1 por palavra da pergunta (4+ letras) que aparece no título."""
        pergunta_norm = normalizar(pergunta)
        pontos = 0
        for chave in orientacao.palavras_chave:
            if normalizar(chave) in pergunta_norm:
                pontos += PONTOS_PALAVRA_CHAVE
        titulo_norm = normalizar(orientacao.titulo)
        for palavra in set(pergunta_norm.split()):
            if len(palavra) >= TAMANHO_MIN_PALAVRA_TITULO and f" {palavra} " in titulo_norm:
                pontos += PONTOS_TITULO
        return pontos

    def buscar(self, pergunta):
        """Devolve lista de tuplas (pontos, orientacao), da maior para a menor
        pontuação. Só entram orientações com pelo menos 1 ponto."""
        resultados = []
        for o in self.orientacoes:
            pontos = self.pontuar(pergunta, o)
            if pontos > 0:
                resultados.append((pontos, o))
        resultados.sort(key=lambda tupla: tupla[0], reverse=True)
        return resultados
