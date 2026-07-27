---
titulo: Modelo visual de referência (Canva)
fonte: link Canva "Modelo Relatorio RV" (16/07/2026, atualizado 17-18/07/2026) + PNGs em docs/reference/modelo-canva/
---

# Modelo visual de referência

Fonte original: link privado do Canva fornecido pelo usuário (não é público, não deve
ser referenciado fora deste projeto). A partir de 17/07/2026, temos também os PNGs
exportados de cada página em
[`docs/reference/modelo-canva/`](../reference/modelo-canva) — usar essas imagens como
fonte primária para cor/tipografia/posicionamento; este documento é a especificação
textual (rótulos, métricas, estrutura) derivada delas.

O modelo agora tem **4 páginas** (cresceu de 2 para 4 em 17/07/2026 — confirmado
pelo usuário como escopo real do MVP, ver
[06-decisoes.md](06-decisoes.md)).

Todas as páginas trazem, no canto superior direito, um selo hexagonal com o texto
"Cognito" — é a marca/branding do próprio produto (não é o logo do time, que aparece
à esquerda do cabeçalho). Confirmado (17/07/2026) que deve aparecer fixo em todo PDF
gerado pelo sistema, independente do cliente — ver
[07-pontos-em-aberto.md](07-pontos-em-aberto.md), item 12.

## Página 1 — Dashboard de grupo ("Dashboard Overview")

Imagem: [`dashboard_overview.png`](../reference/modelo-canva/dashboard_overview.png)

Cabeçalho: logo do time + nome do grupo (ex.: "Atletico - MG") + título "Dashboard
Overview" + data (ex.: "27/04/2026").

Blocos de conteúdo:
- **Media de acertos do grupo** — rosca/pizza: "Acertos" (verde, ex. 21) x "Erros"
  (vermelho, ex. 9).
- **Media de classificação do TR** — rosca com as 4 categorias: "No tempo" 47.1%
  (verde), "Precoce" 23.5% (amarelo), "Tardio" 11.8% (laranja), "Perda de bola" 17.6%
  (vermelho). (Nota: o rótulo visível é **"No tempo"**, equivalente a `Ideal` no CSV
  — ver [02-modelo-dados.md](02-modelo-dados.md).)
- **Media do TR** — valor único em destaque (ex.: "2,6 s").
- **"Media de acertos por decisão"** (renomeado em 21/07/2026; antes "Acertos por
  decisão") — gráfico de barras com duas séries, nas categorias "Chute", "Passe
  Esq", "Passe Dir", "Manutenção", **cada valor dividido pelo número de atletas do
  grupo** (média por atleta, não soma bruta):
  - **"Atletico"** (preto, nome do grupo) = média de `RespostaDada` por
    categoria — o que o atleta/time efetivamente fez.
  - **"Ideal"** (verde) = média de `RespostaCorreta` por categoria — o que
    deveria ter sido feito. Confirmado com o cliente (18/07/2026) — ver
    [07-pontos-em-aberto.md](07-pontos-em-aberto.md), item 3.

  Mapeamento de rótulo abreviado → valor da coluna do CSV:
  - "Chute" → `Chutar ao Gol`
  - "Passe Esq" → `Passe a Esquerda`
  - "Passe Dir" → `Passe a Direita`
  - "Manutenção" → `Manter Posse`

## Página 2 — Dashboard individual ("Dashboard individual")

Imagem: [`dashboard_individual.png`](../reference/modelo-canva/dashboard_individual.png)

Cabeçalho: logo do time + nome do grupo + título "Dashboard individual" + data;
à direita, metadados do atleta: "Nome do atleta", data (ex.: "03/2013"), lateralidade
("Canhoto"), posição ("meio campista") + ícone de avatar genérico.
Lateralidade e posição vêm do campo `Jogador` (ver
[02-modelo-dados.md](02-modelo-dados.md)). A data ao lado do nome (ex.: "03/2013")
**ainda não tem coluna correspondente no CSV** — ver
[07-pontos-em-aberto.md](07-pontos-em-aberto.md), item 4.

Blocos de conteúdo:
- **Tentativas / Acertos / Média do grupo** — indicador com "Tentativas: 30",
  "Acertos: 20", "Media do grupo: 15" (valores de exemplo do template).
- **Taxa de acerto** — arco/gauge com valor em destaque (ex.: "66%").
- **Media do TR** — dois valores lado a lado: "Acertos 2.5 s" (verde) / "Erros 1.8 s"
  (vermelho) — ver interpretação adotada em [03-metricas.md](03-metricas.md).
- **Classificação do TR por acerto e erro** — barras horizontais empilhadas:
  "Acertou" (Precoce/No tempo/Tardio) e "Errou" (idem). No exemplo: Acertou = 10
  (No tempo, verde) + 10 (Tardio, amarelo); Errou = 6 (Precoce, vermelho) + 4 (No
  tempo, verde). "Perda de bola" fica de fora desse gráfico por design, confirmado
  com o usuário — ver [07-pontos-em-aberto.md](07-pontos-em-aberto.md), item 5.
- **Taxa de acerto por resposta** — gráfico radar/diamante com eixos "Chute", "Passe
  Dir", "Manutenção", "Passe Esq" — compara a distribuição do atleta.

## Página 3 — Ações por pé ("Ações por pé") — NOVA (17/07/2026)

Imagem: [`acoes_por_pe.png`](../reference/modelo-canva/acoes_por_pe.png)

Mesmo cabeçalho da página individual (time, atleta, lateralidade, posição). Usa as
colunas `PeEsperado` / `PeUsado` — ver [02-modelo-dados.md](02-modelo-dados.md) e
[03-metricas.md](03-metricas.md).

Blocos de conteúdo:
- **Ações por pé** — pizza: "Pé Esquerdo" 68.8% (verde) x "Pé direito" 31.3%
  (vermelho).
- Par de ícones de pé (esquerdo verde, direito vermelho) — decorativo.
- **Media de TR por pé** — barras: "Esquerdo" (verde, ~2s) x "Direito" (vermelho,
  ~3s).
- **Acertos por pé usado** — barras horizontais empilhadas: "Acertou" = Esquerdo 13
  (verde) + Direito 7 (vermelho); "Errou" = Esquerdo 6 (verde) + Direito 4
  (vermelho).

## Página 4 — Comparação atleta x grupo ("Comparação atleta grupo") — NOVA (17/07/2026)

Imagem: [`comparacao_atleta_grupo.png`](../reference/modelo-canva/comparacao_atleta_grupo.png)

Mesmo cabeçalho da página individual.

Blocos de conteúdo:
- **Media de acertos do grupo** — linha comparando "Media Grupo" (cinza) x "Nome
  Atleta" (verde) por categoria de resposta (Manutenção, Passa Dir, Passe Esq,
  Chutes), eixo Y em porcentagem. É a mesma métrica de "taxa de acerto por resposta"
  da página 2 (radar), exibida como linha aqui — confirmado com o usuário
  (17/07/2026) que as duas visualizações são intencionais, não uma duplicação a
  remover — ver [07-pontos-em-aberto.md](07-pontos-em-aberto.md), item 11.
- **Media de acertos posição** — mesmo formato de linha, mas comparando a posição
  do atleta (média dos outros atletas do grupo naquela posição, cinza) x "Nome
  Atleta" (verde). Se não houver nenhum outro atleta do grupo na mesma posição, a
  linha cinza é substituída por um aviso "Sem outro atleta para comparar" (ajuste
  de 22/07/2026 — uma linha cinza achatada em 0% parecia um dado real, não
  ausência de comparação).
- **Acertos por posição** — barras nas 6 posições: Zagueiro, Meio Campista,
  Atacante, Volante, Lateral Direito, Lateral Esquerdo. Confirmado (17/07/2026) que
  "média da posição" é calculada só entre os atletas do relatório atual — se o
  grupo não tiver atleta em alguma posição, essa posição fica sem barra nenhuma.
  **Refeito em 26/07/2026:** 2 séries — "Media da posição" (cinza neutro
  `#A6A6A6`, o mesmo das linhas de referência desta página) e o **nome do atleta**
  (verde). A barra cinza aparece em toda categoria com pelo menos um atleta
  carregado na sessão, e a média **inclui o próprio atleta**; a barra verde
  aparece só na posição dele, ao lado da cinza daquela posição. Ver
  [06-decisoes.md](06-decisoes.md).

## Observações gerais

- Layout fixo — o usuário não edita o layout do PDF, só o conteúdo (nome do grupo,
  logo, quais atletas entram).
- Selo "Cognito" no canto superior direito de todas as páginas — ver nota no topo
  deste documento.
