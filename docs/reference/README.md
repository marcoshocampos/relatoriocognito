# docs/reference

Material de referência visual/bruto usado para construir os documentos de contexto
em `docs/context/` — não é lido automaticamente antes de cada implementação (ao
contrário de `docs/context/`), é a fonte primária por trás deles.

Conteúdo esperado aqui:
- **`modelo-canva/`** — export em PNG das páginas do modelo Canva "Modelo Relatorio
  RV" (dashboard de grupo e dashboard individual), para fidelidade visual fina
  (cores, tipografia, posicionamento) que a especificação textual em
  [05-modelo-visual-referencia.md](../context/05-modelo-visual-referencia.md) não
  cobre — ver [../context/07-pontos-em-aberto.md](../context/07-pontos-em-aberto.md),
  item 7. Convenção de nome sugerida: `01-dashboard-grupo.png`,
  `02-dashboard-individual.png` (usar o número da página no Canva).
- Outros CSVs de exemplo reais, além do já usado em
  `tests/fixtures/sample_csvs/`, se ajudarem a validar casos como `Perda de bola`
  (ver item 2 do mesmo documento de pendências).

Se um arquivo aqui invalidar algo escrito em `docs/context/`, atualizar o documento
de contexto correspondente — `docs/context/` deve sempre refletir o entendimento
mais atual.
