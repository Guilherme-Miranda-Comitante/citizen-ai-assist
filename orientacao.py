"""Classe Orientacao: representa um registro da base de conhecimento."""

AVISO = "este assistente NÃO é um canal oficial."


class Orientacao:
    CAMPOS = ("id", "categoria", "titulo", "palavras_chave", "resposta",
              "documentos", "onde", "fonte", "verificado_em")

    def __init__(self, id, categoria, titulo, palavras_chave, resposta,
                 documentos, onde, fonte, verificado_em):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.documentos = documentos
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em

    @classmethod
    def de_dicionario(cls, dados):
        """Cria uma Orientacao a partir de um dicionário do JSON.
        Levanta ValueError se faltar algum campo obrigatório."""
        faltando = [c for c in cls.CAMPOS if c not in dados]
        if faltando:
            raise ValueError("campos ausentes: " + ", ".join(faltando))
        return cls(**{c: dados[c] for c in cls.CAMPOS})

    def exibir(self):
        print(f"\n>> {self.titulo}  [{self.categoria}]")
        print(self.resposta)
        print("Documentos necessários:")
        if self.documentos:
            for doc in self.documentos:
                print(f"  - {doc}")
        else:
            print("  - Nenhum documento específico")
        print(f"Onde: {self.onde}")
        print(f"Fonte: {self.fonte} (verificado em {self.verificado_em})")
        print(f"Aviso: {AVISO}")
