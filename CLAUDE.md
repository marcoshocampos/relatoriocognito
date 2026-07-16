# Instruções para o Claude neste projeto

## Sempre ler antes de implementar

Antes de implementar qualquer funcionalidade, ler os documentos em
[`docs/context/`](docs/context), nesta ordem de prioridade conforme o que estiver
sendo implementado:

- [`01-visao-geral.md`](docs/context/01-visao-geral.md) — objetivo, escopo do MVP, o
  que está fora de escopo.
- [`02-modelo-dados.md`](docs/context/02-modelo-dados.md) — formato do CSV de
  entrada, casos reais observados (espaços, linha vazia final).
- [`03-metricas.md`](docs/context/03-metricas.md) — regras de cálculo de todas as
  métricas de grupo e individuais. Não inventar fórmula sem checar aqui.
- [`04-arquitetura.md`](docs/context/04-arquitetura.md) — camadas do código e onde
  cada tipo de lógica deve morar.
- [`05-modelo-visual-referencia.md`](docs/context/05-modelo-visual-referencia.md) —
  layout e rótulos do PDF final, extraído do modelo Canva.
- [`06-decisoes.md`](docs/context/06-decisoes.md) — decisões técnicas já fechadas;
  não reabrir sem alinhar com o usuário.
- [`07-pontos-em-aberto.md`](docs/context/07-pontos-em-aberto.md) — pontos que
  **ainda não foram validados com o usuário**. Se a implementação esbarrar em um
  desses pontos, perguntar antes de decidir sozinho.

`00-planejamento-original.md` é o documento bruto original — histórico, não editar.

## Regras específicas deste projeto

- `ClassificacaoTR` e `Correto?` do CSV **nunca são recalculados**, só agregados.
- `domain/` não deve importar nada de `io/`, `charts/`, `pdf/` ou `gui/` — é lógica
  pura, testável sem I/O.
- Não implementar nada listado como "fora de escopo" em
  [`01-visao-geral.md`](docs/context/01-visao-geral.md) (histórico, multiusuário,
  mapeamento flexível de CSV, etc.) a menos que o usuário peça explicitamente.
- Ao terminar de implementar algo que resolve um item de
  [`07-pontos-em-aberto.md`](docs/context/07-pontos-em-aberto.md), atualizar o
  status do item nesse arquivo em vez de apagá-lo.
- Gerenciador de ambiente é `uv` — usar `uv add`/`uv run`, não `pip install` direto.
