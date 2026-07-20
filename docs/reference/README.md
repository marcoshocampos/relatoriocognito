# docs/reference

Material de referência visual/bruto usado para construir os documentos de contexto
em `docs/context/` — não é lido automaticamente antes de cada implementação (ao
contrário de `docs/context/`), é a fonte primária por trás deles.

Conteúdo aqui:
- **`modelo-canva/`** — export em PNG das 4 páginas do modelo Canva "Modelo
  Relatorio RV": `dashboard_overview.png`, `dashboard_individual.png`,
  `acoes_por_pe.png`, `comparacao_atleta_grupo.png`. Fonte primária de fidelidade
  visual (cores, tipografia, posicionamento); a especificação textual está em
  [05-modelo-visual-referencia.md](../context/05-modelo-visual-referencia.md).
- Outros CSVs de exemplo reais, além do já usado em
  `tests/fixtures/sample_csvs/`, se ajudarem a validar casos como `Perda de bola`
  (ver item 2 de [../context/07-pontos-em-aberto.md](../context/07-pontos-em-aberto.md)).

Se um arquivo aqui invalidar algo escrito em `docs/context/`, atualizar o documento
de contexto correspondente — `docs/context/` deve sempre refletir o entendimento
mais atual.
