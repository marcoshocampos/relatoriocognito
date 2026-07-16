# relatoriocognito

Aplicativo desktop (Windows, `.exe` único) que gera relatórios em PDF de testes de
tempo de reação/decisão de atletas, a partir de CSVs exportados por sessão/atleta.

Uso interno da equipe que monta os relatórios — o cliente final recebe apenas o PDF
pronto. Sem servidor, sem banco de dados, sem instalação.

## Documentação do projeto

Antes de implementar qualquer parte do sistema, ler
[`docs/context/`](docs/context) — é a fonte de verdade sobre objetivo, modelo de
dados, métricas, arquitetura e decisões já tomadas. Comece por
[`docs/context/01-visao-geral.md`](docs/context/01-visao-geral.md).

## Setup do ambiente

Requer [uv](https://docs.astral.sh/uv/) e Python 3.12+.

```powershell
uv sync
```

## Rodar em desenvolvimento

```powershell
uv run python -m relatoriocognito
```

## Testes

```powershell
uv run pytest
```

## Gerar o .exe

```powershell
uv run pyinstaller --name relatoriocognito --onefile --windowed src/relatoriocognito/__main__.py
```

Ou use o script pronto: `scripts/build_exe.ps1`.

## Estrutura

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
