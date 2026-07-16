---
titulo: Modelo de dados (CSV de entrada)
fonte: 00-planejamento-original.md (seção 4) + tests/fixtures/sample_csvs/Geral_10_3_2025.csv
---

# Modelo de dados

Um CSV = um atleta = uma sessão de treino. Uma linha = uma tentativa/trial.

## Colunas

| Coluna | Tipo | Significado | Exemplo |
|---|---|---|---|
| `Treino` | string | Nome/identificação da sessão de treino | `Geral_10_3_2025` |
| `Jogador` | string | Identificador + nome do atleta | ` 01 Caio` |
| `TempoReacao` | float | Tempo de decisão, em **segundos** | `13.31` |
| `ClassificacaoTR` | enum | `Precoce` \| `Tardio` \| `Ideal` \| `Perda de bola` | `Precoce` |
| `Correto?` | enum | `Acertou` \| `Errou` | `Errou` |
| `RespostaCorreta` | string | Resposta ideal esperada para a jogada | `Chutar ao Gol` |
| `RespostaDada` | string | Resposta que o atleta efetivamente deu | `Manter Posse` |
| `Data` | date (`DD/MM/YYYY`) | Data do teste | `10/03/2025` |
| `Hora` | time (`HH:MM`) | Horário da tentativa | `11:02` |

**Regra de ouro:** `ClassificacaoTR` e `Correto?` **não são recalculados** pelo
sistema — já vêm prontos da ferramenta de teste. O sistema só agrega (conta, soma,
tira média) em cima do que está no CSV.

## Valores possíveis conhecidos

- `ClassificacaoTR`: `Precoce`, `Tardio`, `Ideal`, `Perda de bola` (4 valores fixos).
- `Correto?`: `Acertou`, `Errou`.
- `RespostaCorreta` / `RespostaDada` (categorias vistas até agora): `Chutar ao Gol`,
  `Manter Posse`, `Passe a Esquerda`, `Passe a Direita`. Ver
  [05-modelo-visual-referencia.md](05-modelo-visual-referencia.md) para os rótulos
  abreviados usados nos gráficos (`Chute`, `Passe Esq`, `Passe Dir`, `Manutenção`).

## Observações do arquivo de exemplo real

Arquivo de referência: [`tests/fixtures/sample_csvs/Geral_10_3_2025.csv`](../../tests/fixtures/sample_csvs/Geral_10_3_2025.csv).
Pontos que o parser **precisa** tratar, confirmados olhando o arquivo real:

- O campo `Jogador` vem com **espaço em branco à esquerda** (ex.: `" 01 Caio"`) —
  o parser deve normalizar (`strip()`) antes de usar como identificador/nome exibido.
- O arquivo termina com uma **linha totalmente vazia** (`,,,,,,,,`) — deve ser
  descartada silenciosamente (não é erro, é só um artefato de exportação), conforme
  já previsto na seção 7 do planejamento original ("CSV vazio ou sem linhas válidas").
- `TempoReacao` pode vir como inteiro sem casas decimais (`16`) ou com casas decimais
  (`13.31`) — tratar ambos como float.
- Nesta amostra específica, todas as linhas são do mesmo atleta (`01 Caio`) e todas
  têm `Correto? = Errou` — **não é representativo de um caso real de acertos, nem
  contém nenhum caso de `Perda de bola`**. Ver pendência em
  [07-pontos-em-aberto.md](07-pontos-em-aberto.md).

## Formação do "grupo"

Não existe conceito de grupo dentro do CSV. O grupo de um relatório é formado
**manualmente pelo usuário**, na tela de seleção de arquivos, escolhendo dois ou mais
CSVs de atletas. O sistema não infere agrupamento automaticamente por `Treino`, data,
ou qualquer outra coluna.
