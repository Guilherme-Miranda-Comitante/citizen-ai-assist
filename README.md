# Citizen Assist AI

Assistente de terminal (Python, sem bibliotecas externas) que orienta **jovens no primeiro emprego**
sobre documentos, trabalho, saúde e direitos, usando apenas uma base de conhecimento verificada.

## Integrantes
| Nome | RM |
|------|----|
| Guilherme Miranda | 573107 |

| Nome | RM |
|------|----|
| Rafael Gandolfi | 569036 |

| Nome | RM |
|------|----|
| Carlos Eduardo | 572949 |

## Público e problema
- **Público:** jovens no primeiro emprego.
- **Problema:** a informação sobre documentos e direitos está espalhada, em linguagem técnica e misturada com sites falsos.

## ODS relacionados
_Preencher (sugestões a conferir: ODS 8 – Trabalho decente, ODS 10 – Redução das desigualdades, ODS 16 – Instituições eficazes)._

## Como executar
```bash
python main.py
```
Requer Python 3.8+. Não há dependências externas.

## Estrutura
```
main.py              menu principal
orientacao.py        classe Orientacao (um registro do JSON)
base_conhecimento.py classe BaseConhecimento (carrega, normaliza, pontua, busca)
assistente.py        classe Assistente (atendimento, histórico, indicadores, CSV)
data/                base_conhecimento.json, historico.json, atendimentos.csv, notas.json
```
Composição: `Assistente` → `BaseConhecimento` → lista de `Orientacao`.

## Regra de pontuação
Pergunta e títulos são normalizados (minúsculas, sem acento, sem pontuação).
- Palavra-chave da orientação presente na pergunta: **+3**
- Palavra da pergunta com 4+ letras presente no título: **+1** (cada palavra conta uma vez)
- **6+ pontos:** confiança ALTA · **3 a 5:** MÉDIA · **menos de 3:** "não encontrei", com sugestão de categorias
- `buscar()` devolve lista de tuplas `(pontos, orientacao)` em ordem decrescente; mostramos a melhor e até 2 alternativas.

## Regras de atendimento
- Menu com `0` para voltar; entradas inválidas nunca encerram o programa.
- Pergunta com 8+ dígitos ou `@` é recusada e **não** é registrada.
- Toda resposta mostra fonte, data de verificação e aviso de que não é canal oficial.
- JSON ausente ou corrompido não trava o programa.
- `notas.json` guarda a nota de facilidade (1 a 5) pedida ao sair.

## Integrações com outras disciplinas
Nenhuma.

## Fontes consultadas
_Preencher com os sites oficiais usados (gov.br, Receita Federal, TSE, Caixa, INSS, consumidor.gov.br...) e a data da conferência._

## Teste com usuários
_Preencher: nº de pessoas (mín. 3 de fora da equipe), nº de atendimentos (mín. 10), indicadores obtidos, dúvidas sem solução e a melhoria feita a partir do teste. Não registrar nomes nem dados pessoais._

## Limitações
- Busca por palavras-chave: não entende sinônimos nem erros de digitação.
- Só responde o que está na base (12 orientações); informações oficiais podem mudar.
- Detecção de dados pessoais é simples (dígitos e `@`); não detecta nomes.

## Vídeo técnico
_Colar o link do YouTube (não listado)._
