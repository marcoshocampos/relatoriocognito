---
titulo: Visão geral do produto
fonte: 00-planejamento-original.md (seções 1 e 2)
---

# Visão geral

## O que é

Aplicativo desktop Windows (`.exe` único, sem instalação, sem Python na máquina do
usuário) que gera relatórios em PDF de testes de tempo de reação/decisão de atletas,
a partir de CSVs já exportados por uma ferramenta de teste externa.

Uso interno da equipe que monta os relatórios — o cliente final só recebe o PDF pronto.
Não é um produto multiusuário, não tem servidor, não tem banco de dados. Cada execução
é isolada: abre, gera um relatório, fecha.

## Fluxo de uso (usuário final não-técnico)

1. Abre o `.exe`.
2. Informa nome do grupo (ex.: nome do time) e escolhe uma imagem de logo.
3. Seleciona manualmente os CSVs dos atletas que vão compor aquele relatório.
4. Clica em gerar → sistema calcula métricas, monta gráficos, gera o PDF.
5. Salva o PDF onde quiser.

## Escopo do MVP — está dentro

- Importar múltiplos CSVs (um por atleta).
- Definir nome do grupo + logo por relatório (não é salvo como padrão).
- Seleção manual de quais CSVs formam o grupo.
- Cálculo de métricas de grupo e individuais ([03-metricas.md](03-metricas.md)).
- Gráficos: rosca de acertos/erros, barras de classificação de tempo, barras
  comparativas por tipo de decisão, indicador atleta x grupo.
- PDF único: 1 página de grupo + 1 página por atleta selecionado.
- Empacotamento em `.exe` único via PyInstaller.

## Escopo do MVP — fica de fora (evolução futura)

- Salvar nome/logo como padrão reaproveitável entre relatórios.
- Histórico de relatórios já gerados.
- Suporte a formatos de CSV diferentes / mapeamento flexível de colunas.
- Instalador para a máquina do cliente final.
- Edição de layout do PDF pelo usuário (layout é fixo, ver
  [05-modelo-visual-referencia.md](05-modelo-visual-referencia.md)).
- Qualquer coisa em nuvem ou multiusuário.

**Importante ao implementar:** não construir abstrações para esses itens "fora de
escopo" antecipando a evolução futura. Se surgir a tentação de generalizar algo para
"quando tiver histórico" ou "quando for multiusuário", não fazer — resolve-se quando
(e se) a evolução for pedida.
