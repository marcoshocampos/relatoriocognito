# relatoriocognito

Aplicativo desktop (Windows, `.exe` único) que gera relatórios em PDF de testes de
tempo de reação/decisão de atletas, a partir de CSVs exportados por sessão/atleta.

Uso interno da equipe que monta os relatórios — o cliente final recebe apenas o PDF
pronto. Sem servidor, sem banco de dados, sem instalação.

## Como usar (usuário final)

Guia rápido para quem só vai gerar relatórios com o `relatoriocognito.exe` — não
precisa instalar Python, `uv` nem nada deste repositório, só o `.exe`. Para o manual
completo, com mensagens de erro comuns e dicas, ver
[`manual_do_usuario.pdf`](manual_do_usuario.pdf).

1. Dê duplo clique em `relatoriocognito.exe`. Se o Windows exibir o aviso do
   SmartScreen ("O Windows protegeu o computador"), clique em "Mais informações" →
   "Executar assim mesmo" — é esperado para um programa sem assinatura digital paga.
2. **Passo 1 — Nome do grupo e logo:** preencha o nome do grupo/time (obrigatório) e,
   se quiser, clique em "Escolher imagem…" para um logo (opcional). Clique em
   "Avançar".
3. **Passo 2 — Atletas do relatório:** clique em "Adicionar CSVs…" e selecione um
   arquivo CSV por atleta, exportado pela ferramenta de teste (pelo menos um é
   obrigatório). Clique em "Avançar".
4. **Passo 3 — Gerar e salvar:** confira o resumo, clique em "Gerar e salvar PDF" e
   escolha a pasta e o nome do arquivo final.

Cada relatório é independente: nome do grupo, logo e CSVs selecionados não ficam
salvos de um relatório para o outro.

## Para desenvolvedores

As seções abaixo (documentação técnica, setup, testes, build) são para quem vai
desenvolver o projeto — não para quem só usa o `.exe` pronto.

### Documentação do projeto

Antes de implementar qualquer parte do sistema, ler
[`docs/context/`](docs/context) — é a fonte de verdade sobre objetivo, modelo de
dados, métricas, arquitetura e decisões já tomadas. Comece por
[`docs/context/01-visao-geral.md`](docs/context/01-visao-geral.md).

### Setup do ambiente

Requer [uv](https://docs.astral.sh/uv/) e Python 3.12+.

```powershell
uv sync
```

### Rodar em desenvolvimento

```powershell
uv run python -m relatoriocognito
```

### Testes

```powershell
uv run pytest
```

### Gerar o .exe

```powershell
uv run pyinstaller --name relatoriocognito --onefile --windowed src/relatoriocognito/__main__.py
```

Ou use o script pronto: `scripts/build_exe.ps1`.

### Estrutura

```
docs/context/     documentos de contexto do produto (ler antes de implementar)
docs/reference/   material bruto de referência (ex.: export do modelo Canva)
src/relatoriocognito/
    domain/       lógica de negócio pura (modelos, métricas)
    io/           leitura/validação de CSV
    charts/       geração dos gráficos (matplotlib)
    pdf/          montagem do PDF final (reportlab)
    gui/          telas (CustomTkinter)
    resources/    assets embutidos no .exe
tests/
    unit/         testes de unidade (principalmente domain/metrics.py)
    fixtures/     CSVs de exemplo reais para teste
scripts/          scripts de build/empacotamento
```
