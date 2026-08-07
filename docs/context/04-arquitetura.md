---
titulo: Arquitetura técnica
fonte: 00-planejamento-original.md (seções 3, 6, 9) + decisões em 06-decisoes.md (atualizado 17/07/2026: MVP passou a ter 4 páginas)
---

# Arquitetura

Aplicação desktop Python, sem servidor, sem banco de dados. Cada execução é
independente — não há persistência entre gerações de relatório.

## Fluxo

```
[Tela: nome do grupo + logo + cor base do time]
     → [Tela: selecionar CSVs dos atletas]
     → [Leitura e validação dos CSVs]
     → [Cálculo das métricas (grupo, por atleta, por atleta x posição)]
     → [Geração dos gráficos, usando a cor base escolhida]
     → [Montagem do PDF (1 página de grupo + 3 páginas por atleta selecionado)]
     → [Salvar arquivo .pdf]
```

A cor base (`charts.colors.Paleta`, ver [06-decisoes.md](06-decisoes.md)) é
escolhida na primeira tela e atravessa todas as camadas até `pdf/` e `charts/`
como um parâmetro explícito (`paleta: Paleta`) — não é estado global nem
configuração salva em disco, existe só durante a geração daquele relatório.

O PDF final tem, por relatório: 1 página de grupo ("Dashboard Overview") +, para
cada atleta selecionado, 3 páginas ("Dashboard individual", "Ações por pé",
"Comparação atleta grupo") — ver
[05-modelo-visual-referencia.md](05-modelo-visual-referencia.md) e decisão de escopo
em [07-pontos-em-aberto.md](07-pontos-em-aberto.md), item 10.

## Camadas e mapeamento para pastas do código

O código em `src/relatoriocognito/` segue uma separação simples entre lógica de
negócio pura (sem I/O) e as bordas (arquivo, gráfico, PDF, GUI), para que a parte
mais sensível a erro (as contas de métricas) seja testável isoladamente sem precisar
de CSV real, matplotlib ou GUI:

- **`domain/`** — lógica de negócio pura, sem I/O. `models.py` (estruturas de dados:
  tentativa/trial, atleta — incluindo lateralidade e posição extraídas do campo
  `Jogador`, ver [02-modelo-dados.md](02-modelo-dados.md) — e grupo) e `metrics.py`
  (cálculos da seção 5 de [03-metricas.md](03-metricas.md), incluindo as métricas por
  pé e por posição). Alvo principal dos testes de unidade.
- **`io/`** — `csv_importer.py`: leitura e validação dos CSVs selecionados
  (parsing, normalização de colunas — inclusive acento/maiúscula inconsistentes,
  decodificação ISO-8859-1 — descarte de linhas vazias, mensagens de erro — ver
  [02-modelo-dados.md](02-modelo-dados.md) e seção de tratamento de erros no
  planejamento original).
- **`charts/`** — geração dos gráficos (rosca, barras, radar, linha, indicador
  comparativo) com matplotlib, no estilo do modelo de referência
  ([05-modelo-visual-referencia.md](05-modelo-visual-referencia.md)). O radar
  (página individual) e a linha (página de comparação) são componentes de gráfico
  distintos, mesmo representando a métrica "taxa de acerto por resposta" — ver
  [07-pontos-em-aberto.md](07-pontos-em-aberto.md), item 11. `colors.py` define a
  `Paleta` (cor base escolhida pelo usuário + cores fixas semânticas/neutras) e
  `estilo.py` centraliza os ajustes visuais comuns a todos os gráficos (legenda,
  grid, fonte) — ver [06-decisoes.md](06-decisoes.md).
- **`pdf/`** — montagem do PDF final com reportlab: página de grupo + as 3 páginas
  por atleta, usando os gráficos gerados. Um módulo de layout por tipo de página
  (`layout_grupo.py`, `layout_individual.py`, `layout_acoes_pe.py`,
  `layout_comparacao_grupo.py`) mantém cada página isolada e fácil de ajustar
  visualmente sem afetar as outras; `layout_helpers.py` reúne o que é comum às 4
  (cabeçalho, cartão, rodapé com a data de emissão). É `layout_helpers.desenhar_figura`
  que define o tamanho final de cada gráfico — ele redimensiona a figura para a
  caixa do cartão antes de rasterizar, então **o tamanho de um gráfico se ajusta
  mudando a caixa aqui, não o `figsize` em `charts/`** (ver
  [06-decisoes.md](06-decisoes.md)).
- **`gui/`** — telas em CustomTkinter: (1) nome do grupo + logo + cor base do
  time, (2) seleção dos CSVs dos atletas, (3) gerar relatório / salvar PDF.
  `gui/` só orquestra chamadas para `domain/`, `io/`, `charts/` e `pdf/` — não
  deve conter lógica de cálculo.
- **`resources/`** — assets estáticos embutidos no `.exe` (ex.: fontes, ícone do
  app). Não confundir com `docs/reference/` (material de referência para
  desenvolvimento, não embutido no executável).

## Empacotamento

- PyInstaller, gerando um único `.exe` (Windows), sem necessidade de instalar Python
  na máquina de quem usa.
- Script de build em `scripts/` (ver [06-decisoes.md](06-decisoes.md) para o
  gerenciador de ambiente usado).
- Atualizações futuras = gerar novo `.exe` e substituir o antigo. Não há
  auto-update, não há verificação de versão.

## Testes

Sem suíte automatizada formal completa prevista para o MVP. Escopo de teste:
- Testes de unidade em `domain/metrics.py` (a lógica mais sensível a erro
  silencioso) usando `tests/fixtures/sample_csvs/` como dado real de referência.
- Teste manual do fluxo completo com CSVs reais antes de cada entrega.
