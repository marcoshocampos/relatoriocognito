---
titulo: Decisões técnicas já tomadas
fonte: 00-planejamento-original.md (seção 11) + decisões tomadas em 16/07/2026 na estruturação inicial
---

# Decisões técnicas

Estas decisões já foram tomadas e **não devem ser reabertas** durante a
implementação sem alinhar antes com o usuário — evita retrabalho e discussões
repetidas.

## Do planejamento original

- Projeto novo e independente (não depende de outro projeto existente).
- Uso interno: roda na máquina da equipe que monta os relatórios, não do cliente
  final.
- Usuário final não-técnico → interface simples de botões, sem jargão técnico.
- Formato de CSV fixo e consistente — sem mapeamento flexível de colunas no MVP.
- Um CSV por atleta; grupo formado por seleção manual de arquivos, não inferido.
- `ClassificacaoTR` e `Correto` já vêm prontos no CSV — sistema só agrega, nunca
  recalcula essas duas colunas.
- `TempoReacao` está em segundos.
- PDF final: 1 arquivo por sessão. ~~página de grupo + 1 página por atleta~~ —
  **substituído em 17/07/2026**, ver seção "Atualização de escopo" abaixo.
- Nome do grupo e logo são definidos a cada relatório (não salvos como padrão).
- Stack de dados/relatório: **Python + pandas + matplotlib + reportlab**.
- Empacotamento: **PyInstaller**, gerando um único `.exe` para Windows.

## Tomadas na estruturação inicial do repositório (16/07/2026)

- **GUI:** CustomTkinter. Motivo: visual mais moderno que Tkinter puro, mantendo
  simplicidade de empacotamento com PyInstaller (baseado em Tkinter/stdlib, poucas
  dependências extras) — adequado para usuário final não-técnico.
- **Gerenciador de ambiente/dependências:** [uv](https://docs.astral.sh/uv/).
  Motivo: mais rápido que pip/poetry, resolve dependências e gerencia o venv,
  usa `pyproject.toml`, builds reproduzíveis.
- **Nome do pacote Python interno:** `relatoriocognito` (mesmo nome do repositório).
- **Versão mínima do Python:** 3.12.
- **Layout de código:** `src/` layout (`src/relatoriocognito/...`), separando
  lógica pura (`domain/`) das bordas de I/O, gráficos, PDF e GUI — ver
  [04-arquitetura.md](04-arquitetura.md).
- **Testes:** pytest, focado em `domain/metrics.py` (não decidido explicitamente
  pelo usuário, mas é a ferramenta padrão do ecossistema Python e coerente com a
  seção 8 do planejamento original — reavaliar apenas se o usuário pedir algo
  diferente).

## Atualização de escopo — CSV v2 e modelo de 4 páginas (17/07/2026)

O cliente enviou uma nova versão do CSV de exemplo e do modelo Canva, com mudanças
confirmadas pelo usuário nesta data:

- **PDF final passa a ter 4 páginas por relatório**: 1 página de grupo ("Dashboard
  Overview") + 3 páginas por atleta selecionado ("Dashboard individual", "Ações por
  pé", "Comparação atleta grupo") — substitui a decisão original de "1 página de
  grupo + 1 por atleta". Ver [04-arquitetura.md](04-arquitetura.md) e
  [05-modelo-visual-referencia.md](05-modelo-visual-referencia.md).
- **Lateralidade e posição do atleta** vêm embutidas no campo `Jogador` do CSV
  (formato `"Nome - Lateralidade - Posição"`), não são mais entrada manual nem ficam
  de fora do MVP. Data de nascimento continua sem coluna no CSV (segue em aberto).
- **Média por posição** (página "Comparação atleta grupo") é calculada só entre os
  atletas selecionados no relatório atual — não usa histórico entre relatórios,
  mantendo a decisão de "sem histórico" já fechada acima.
- **"Taxa de acerto por resposta" aparece intencionalmente em dois formatos**: radar
  (página individual) e linha (página de comparação) — não é duplicação a remover,
  são dois componentes de gráfico distintos.
- CSV vem em **ISO-8859-1** (não UTF-8) — parser precisa decodificar corretamente
  (ver [02-modelo-dados.md](02-modelo-dados.md)).
- **"Perda de bola" fica de fora do gráfico "Classificação do TR por acerto e
  erro"** (página individual) por design — confirmado com o usuário.
- **Selo "Cognito"** aparece fixo em todo PDF gerado pelo sistema — branding do
  produto, não configurável pelo usuário.

## Atualização de respostas do cliente (18/07/2026)

- **Série "Ideal" em "Acertos por decisão"** (página de grupo) = contagem de
  `RespostaCorreta` por categoria de resposta, em contraste com a série do nome do
  grupo/time = contagem de `RespostaDada`. Não é uma 5ª categoria nem uma média —
  ver [03-metricas.md](03-metricas.md) e
  [07-pontos-em-aberto.md](07-pontos-em-aberto.md), item 3.
- **`PeEsperado`/`PeUsado` já entram na avaliação de `Correto`** feita pela
  ferramenta que gera o CSV (junto com `RespostaCorreta`/`RespostaDada`) — não existe
  nem deve ser criada uma métrica própria de "acerto de pé" no sistema. Reforça a
  regra de nunca recalcular `Correto`/`ClassificacaoTR` — ver
  [02-modelo-dados.md](02-modelo-dados.md) e
  [07-pontos-em-aberto.md](07-pontos-em-aberto.md), item 8.

## Atualização de nomes de coluna (18/07/2026)

Cliente padronizou os nomes de coluna do CSV para remover espaços, acentos e
pontuação: `Pe esperado` → `PeEsperado`, `Pé usado` → `PeUsado`, `Correto?` →
`Correto`. Os demais nomes de coluna não mudaram. Ver
[02-modelo-dados.md](02-modelo-dados.md) para o histórico completo de versões do
CSV (v1 → v2 → v3).

Todas as pendências levantadas na atualização do CSV e do modelo de 4 páginas
(16-18/07/2026) estão resolvidas — ver [07-pontos-em-aberto.md](07-pontos-em-aberto.md)
para o registro completo de cada uma.

## Como usar este documento

Antes de tomar qualquer decisão técnica nova durante a implementação, checar aqui
primeiro se ela já foi decidida. Se uma decisão listada aqui parecer errada ou
incompleta ao encontrar um caso real durante o desenvolvimento, voltar para o
usuário antes de simplesmente mudar de rumo — não decidir sozinho sobre pontos já
fechados.
