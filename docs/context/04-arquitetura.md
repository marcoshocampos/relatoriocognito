---
titulo: Arquitetura técnica
fonte: 00-planejamento-original.md (seções 3, 6, 9) + decisões em 06-decisoes.md
---

# Arquitetura

Aplicação desktop Python, sem servidor, sem banco de dados. Cada execução é
independente — não há persistência entre gerações de relatório.

## Fluxo

```
[Tela: nome do grupo + logo]
     → [Tela: selecionar CSVs dos atletas]
     → [Leitura e validação dos CSVs]
     → [Cálculo das métricas (grupo e por atleta)]
     → [Geração dos gráficos]
     → [Montagem do PDF (capa/cabeçalho + página de grupo + páginas individuais)]
     → [Salvar arquivo .pdf]
```

## Camadas e mapeamento para pastas do código

O código em `src/relatoriocognito/` segue uma separação simples entre lógica de
negócio pura (sem I/O) e as bordas (arquivo, gráfico, PDF, GUI), para que a parte
mais sensível a erro (as contas de métricas) seja testável isoladamente sem precisar
de CSV real, matplotlib ou GUI:

- **`domain/`** — lógica de negócio pura, sem I/O. `models.py` (estruturas de dados:
  tentativa/trial, atleta, grupo) e `metrics.py` (cálculos da seção 5 de
  [03-metricas.md](03-metricas.md)). Alvo principal dos testes de unidade.
- **`io/`** — `csv_importer.py`: leitura e validação dos CSVs selecionados
  (parsing, normalização de colunas, descarte de linhas vazias, mensagens de erro —
  ver [02-modelo-dados.md](02-modelo-dados.md) e seção de tratamento de erros no
  planejamento original).
- **`charts/`** — geração dos gráficos (rosca, barras, indicador comparativo) com
  matplotlib, no estilo do modelo de referência
  ([05-modelo-visual-referencia.md](05-modelo-visual-referencia.md)).
- **`pdf/`** — montagem do PDF final com reportlab: página de capa/grupo + uma
  página por atleta, usando os gráficos gerados.
- **`gui/`** — telas em CustomTkinter: (1) nome do grupo + logo, (2) seleção dos
  CSVs dos atletas, (3) gerar relatório / salvar PDF. `gui/` só orquestra chamadas
  para `domain/`, `io/`, `charts/` e `pdf/` — não deve conter lógica de cálculo.
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
