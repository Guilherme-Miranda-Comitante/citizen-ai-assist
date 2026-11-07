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

ODS 8	Trabalho decente e crescimento econômico	O assistente ajuda jovens a entrar no mercado formal (Carteira de Trabalho Digital, FGTS, seguro-desemprego). 

ODS 10	Redução das desigualdades	Quem tem menos acesso à informação perde direitos e tempo. O assistente traz orientação simples e gratuita.

ODS 16	Paz, justiça e instituições eficazes	Facilita o acesso a serviços públicos e à informação confiável, com fonte oficial e transparência.

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

Ministério do Trabalho e Emprego: https://www.gov.br/trabalho-e-emprego/pt-br.
Ministério da Saúde: https://www.gov.br/saude.
Portal gov.br: https://www.gov.br.

## Teste com usuários

O assistente foi testado por 3 pessoas de fora da equipe, somando 11 atendimentos.
Nenhum nome ou dado pessoal foi registrado.

### Indicadores obtidos
| Indicador | Resultado |
|-----------|-----------|
| Atendimentos registrados | 11 |
| Resposta encontrada | 54,5% |
| Taxa de acerto (ajudou) | 54,5% |
| Tempo médio para encontrar | 37,4 s |
| Tentativas por atendimento | 1,64 |
| Facilidade de uso (1 a 5) | 3,2 |

### Dúvidas sem solução
- Como faço para tirar minha carteira de trabalho?
- Como começar a trabalhar com carteira assinada?
- Como fazer o cartão do SUS
- Como resolvo se meu produto veio com defeito?

### Análise
A busca só pontua quando a pergunta contém uma palavra-chave exatamente como está
escrita na base. Por isso, perguntas com outras palavras para o mesmo assunto
("carteira assinada", "produto veio com defeito") não atingiram os 3 pontos mínimos
e ficaram sem resposta.

### Melhoria feita a partir do teste
Foram adicionadas palavras-chave novas ao `base_conhecimento.json`:
- Orientação 1 (Carteira de Trabalho Digital): "carteira assinada"
- Orientação 10 (Reclamar de compra ou serviço): "defeito"

Depois da alteração, as perguntas sobre carteira assinada e produto com defeito
passaram a ser encontradas.
## Limitações
- Busca por palavras-chave: não entende sinônimos nem erros de digitação.
- Só responde o que está na base (12 orientações); informações oficiais podem mudar.
- Detecção de dados pessoais é simples (dígitos e `@`); não detecta nomes.

## Vídeo técnico
_Colar o link do YouTube (não listado)._
