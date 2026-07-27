---
titulo: Modelo de dados (CSV de entrada)
fonte: 00-planejamento-original.md (seção 4) + tests/fixtures/sample_csvs/Geral_10_3_2025.csv (v3, atualizado em 18/07/2026)
---

# Modelo de dados

Um CSV = um atleta = uma sessão de treino. Uma linha = uma tentativa/trial.

> **Histórico:**
> - **v1 (16/07/2026)** — versão original: `Treino`, `Jogador` (só nome), `TempoReacao`,
>   `ClassificacaoTR`, `Correto?`, `RespostaCorreta`, `RespostaDada`, `Data`, `Hora`.
> - **v2 (17/07/2026)** — cliente adicionou colunas de pé (`Pe esperado`, `Pé usado`,
>   com acentuação inconsistente entre si) e mudou `Jogador` para o formato combinado
>   `"Nome - Lateralidade - Posição"`.
> - **v3 (18/07/2026)** — cliente renomeou as colunas para um padrão consistente:
>   `Pe esperado` → `PeEsperado`, `Pé usado` → `PeUsado`, `Correto?` → `Correto` (sem
>   espaços, sem acento, sem interrogação). Este documento reflete a v3, que é a
>   versão atual. Ver [07-pontos-em-aberto.md](07-pontos-em-aberto.md) para o que cada
>   mudança resolveu.

## Colunas

| Coluna | Tipo | Significado | Exemplo |
|---|---|---|---|
| `Treino` | string | Nome/identificação da sessão de treino | `Geral_10_3_2025` |
| `Jogador` | string | Nome do atleta + lateralidade + posição, separados por `" - "` | `Caio - Canhoto - Meio campista` |
| `PeEsperado` | enum | Pé que deveria ser usado na jogada (esperado) | `Esquerdo` |
| `PeUsado` | enum | Pé efetivamente usado pelo atleta na jogada | `Esquerdo` |
| `TempoReacao` | float | Tempo de decisão, em **segundos** | `13.31` |
| `ClassificacaoTR` | enum | `Precoce` \| `Tardio` \| `Ideal` \| `Perda de bola` | `Precoce` |
| `Correto` | enum | `Acertou` \| `Errou` | `Errou` |
| `RespostaCorreta` | string | Resposta ideal esperada para a jogada | `Chutar ao Gol` |
| `RespostaDada` | string | Resposta que o atleta efetivamente deu | `Manter Posse` |
| `Data` | date (`DD/MM/YYYY`) | Data do teste | `10/03/2025` |
| `Hora` | time (`HH:MM`) | Horário da tentativa | `11:02` |

**Regra de ouro:** `ClassificacaoTR` e `Correto` **não são recalculados** pelo
sistema — já vêm prontos da ferramenta de teste, que combina várias colunas
(resposta certa/dada, pé esperado/usado, etc.) para chegar nesse resultado. O
sistema só agrega (conta, soma, tira média) em cima do que está no CSV — nunca
reimplementa essa lógica de avaliação. O mesmo vale para `PeEsperado`/`PeUsado`:
são dados brutos, não recalculados (ver detalhe abaixo).

## Campo `Jogador`: nome + lateralidade + posição combinados

O campo `Jogador` não é só um identificador — é uma string composta, separada por
`" - "`:

```
"Caio - Canhoto - Meio campista"
 nome    lateralidade    posição
```

O parser precisa fazer o **split por `" - "`** e extrair 3 valores:
1. Nome do atleta (`Caio`).
2. Lateralidade/perna dominante (`Canhoto` — valores esperados provavelmente
   `Canhoto` / `Destro`, a confirmar com mais amostras).
3. Posição em campo (`Meio campista` — ver seção seguinte para o conjunto de
   posições conhecidas).

Isso **resolve parte** do ponto em aberto sobre metadados do atleta (lateralidade e
posição agora vêm no CSV, sem precisar de tela de entrada manual) — ver
[07-pontos-em-aberto.md](07-pontos-em-aberto.md), item 4. A data de nascimento
(mostrada como `03/2013` no modelo visual) **continua sem coluna correspondente no
CSV** — esse ponto específico segue em aberto.

## `PeEsperado` vs `PeUsado`

`PeEsperado` é o pé que a jogada exigia; `PeUsado` é o pé que o atleta efetivamente
usou.

**Confirmado com o cliente (18/07/2026):** `PeEsperado`/`PeUsado` **já entram no
cálculo de `Correto`**, junto com `RespostaCorreta`/`RespostaDada` — a ferramenta
que gera o CSV avalia "acertou ou errou" combinando várias colunas (resposta certa,
pé certo, etc.), não só resposta. **Isso reforça a regra de ouro acima: o sistema
não recalcula `Correto` nem tenta derivar uma métrica própria de "acerto de pé"** —
o resultado combinado já vem pronto em `Correto`. `PeUsado` é consumido nos
gráficos da página "Ações por pé" só como dado descritivo (qual pé foi mais usado,
tempo de reação por pé, cruzamento com `Correto` já existente) — ver
[03-metricas.md](03-metricas.md). `PeEsperado` não tem uso direto identificado em
nenhum gráfico do MVP (é insumo da avaliação que a ferramenta de origem já fez, não
algo que o sistema precisa reprocessar).

## Valores possíveis conhecidos

- `ClassificacaoTR`: `Precoce`, `Tardio`, `Ideal`, `Perda de bola` (4 valores fixos).
- `Correto`: `Acertou`, `Errou`.
- `PeEsperado` / `PeUsado`: `Esquerdo`, `Direito` (2 valores vistos até agora).
- Lateralidade (dentro de `Jogador`): `Canhoto` visto até agora (provavelmente também
  `Destro`, a confirmar).
- Posição (dentro de `Jogador`): `Meio campista` visto no CSV de exemplo. O modelo
  visual (página "Comparação atleta grupo") lista 6 posições fixas usadas nos
  gráficos: `Zagueiro`, `Meio Campista`, `Atacante`, `Volante`, `Lateral Direito`,
  `Lateral Esquerdo` — provavelmente o conjunto completo de valores possíveis, mas
  não confirmado com o usuário.
- `RespostaCorreta` / `RespostaDada` (categorias vistas até agora): `Chutar ao Gol`,
  `Manter Posse`, `Passe a Esquerda`, `Passe a Direita`. Ver
  [05-modelo-visual-referencia.md](05-modelo-visual-referencia.md) para os rótulos
  abreviados usados nos gráficos (`Chute`, `Passe Esq`, `Passe Dir`, `Manutenção`).

## Observações do arquivo de exemplo real

Arquivo de referência: [`tests/fixtures/sample_csvs/Geral_10_3_2025.csv`](../../tests/fixtures/sample_csvs/Geral_10_3_2025.csv).
Pontos que o parser **precisa** tratar, confirmados olhando o arquivo real:

- **O arquivo não está em UTF-8, e sim em ISO-8859-1 (Latin-1)** — confirmado via
  `file` e teste de decodificação. Ler o CSV assumindo UTF-8 quebra caracteres
  acentuados (`é` vira `�`) nos **valores** de algumas colunas (ex.: dentro de
  `Jogador`/posição, se algum dia tiver acento). O parser precisa decodificar como
  `latin-1` (ou tentar `utf-8` primeiro e cair para `latin-1`/`cp1252` em caso de
  erro — abordagem mais robusta caso o cliente varie a ferramenta de exportação
  entre sessões). Ainda vale mesmo os nomes de coluna não tendo mais acento na v3.
- **Normalizar nomes de coluna mesmo assim** (case-insensitive, sem assumir grafia
  exata) — é uma boa prática defensiva mesmo com a v3 já padronizada, considerando
  que a v1→v2 já mudou nomes de coluna uma vez e a v2 teve inconsistência de acento
  entre `Pe esperado`/`Pé usado`. Não hardcodar comparação de string exata sensível a
  maiúsculas/acento.
- Terminação de linha é `CRLF` (arquivo de origem Windows) — não assumir `LF`.
- `TempoReacao` pode vir como inteiro sem casas decimais (`16`) ou com casas decimais
  (`13.31`) — tratar ambos como float.
- **`TempoReacao` pode vir com vírgula decimal** (`"13,31"`, entre aspas — a aspa
  aparece porque a vírgula decimal colide com a vírgula separadora de campos do
  CSV) em vez de ponto. Acontece quando o arquivo é reexportado/editado no Excel
  com localidade PT-BR. Confirmado em 22/07/2026 com um arquivo real do cliente
  que causava erro "nenhuma tentativa válida" — o parser tenta `float()` direto
  primeiro e cai para trocar `,` por `.` antes de tentar de novo (ver
  `io/csv_importer.py::_parse_tempo_reacao`).
- Nesta amostra específica, não há linha vazia final — mas o parser deve continuar
  descartando linhas vazias/inválidas por segurança (não assumir que toda exportação
  futura virá limpa), conforme seção 7 do planejamento original.
- Todas as linhas desta amostra são do mesmo atleta (`Caio`) e todas têm
  `Correto = Errou` — **não é representativo de um caso real de acertos, nem
  contém nenhum caso de `Perda de bola`**. Ver pendência em
  [07-pontos-em-aberto.md](07-pontos-em-aberto.md).

## Formação do "grupo"

Não existe conceito de grupo dentro do CSV. O grupo de um relatório é formado
**manualmente pelo usuário**, na tela de seleção de arquivos, escolhendo dois ou mais
CSVs de atletas. O sistema não infere agrupamento automaticamente por `Treino`, data,
ou qualquer outra coluna.
