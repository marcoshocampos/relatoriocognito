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
- `ClassificacaoTR` e `Correto?` já vêm prontos no CSV — sistema só agrega, nunca
  recalcula essas duas colunas.
- `TempoReacao` está em segundos.
- PDF final: 1 arquivo por sessão, página de grupo + 1 página por atleta.
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

## Como usar este documento

Antes de tomar qualquer decisão técnica nova durante a implementação, checar aqui
primeiro se ela já foi decidida. Se uma decisão listada aqui parecer errada ou
incompleta ao encontrar um caso real durante o desenvolvimento, voltar para o
usuário antes de simplesmente mudar de rumo — não decidir sozinho sobre pontos já
fechados.
