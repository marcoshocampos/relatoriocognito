---
titulo: Modelo visual de referência (Canva)
fonte: link Canva "Modelo Relatorio RV" fornecido pelo usuário em 16/07/2026
---

# Modelo visual de referência

Fonte original: link privado do Canva fornecido pelo usuário (não é público, não deve
ser referenciado fora deste projeto). O editor do Canva usa canvas e não foi possível
tirar screenshot via automação de navegador nesta sessão; o conteúdo abaixo foi
extraído lendo a árvore de acessibilidade/texto das duas páginas do design. Serve como
especificação textual dos rótulos, métricas e layout geral.

**Se surgir dúvida visual fina (cores exatas, posicionamento em pixel, tipografia)
durante a implementação dos gráficos/PDF, pedir ao usuário para exportar as páginas
do Canva como imagem/PDF e adicionar em `docs/reference/`.**

## Página 1 — Dashboard de grupo ("Dashboard Overview")

Cabeçalho:
- Nome do grupo (ex.: "Atletico - MG")
- Título: "Dashboard Overview" + data (ex.: "27/04/2026")

Blocos de conteúdo:
- **Média de acertos do grupo** — gráfico de rosca com categorias "Acertos" / "Erros".
- **Média de classificação do TR** — gráfico de rosca/distribuição com as 4 categorias:
  "No tempo" 47.1%, "Precoce" 23.5%, "Perda de bola" 17.6%, "Tardio" 11.8%.
  (Nota: no modelo o rótulo usado é **"No tempo"**, equivalente a `Ideal` no CSV —
  ver [02-modelo-dados.md](02-modelo-dados.md). Ao rotular os gráficos, usar "No
  tempo" como label visível para o valor `Ideal` do CSV.)
- **Média do TR** — valor único em destaque (ex.: "2,6 s").
- **Acertos por decisão** — gráfico de barras comparando categorias: "Ideal",
  "Chute", "Passe Esq", "Passe Dir", "Manutenção". Estes são rótulos abreviados de
  exibição para as respostas do CSV — mapeamento sugerido:
  - "Chute" → `Chutar ao Gol`
  - "Passe Esq" → `Passe a Esquerda`
  - "Passe Dir" → `Passe a Direita`
  - "Manutenção" → `Manter Posse`
  - "Ideal" aqui parece ser uma categoria de referência/meta dentro do comparativo,
    não confundir com o "Ideal" de `ClassificacaoTR` — validar com o usuário ao
    implementar este gráfico especificamente (ver
    [07-pontos-em-aberto.md](07-pontos-em-aberto.md)).

## Página 2 — Dashboard individual ("Dashboard individual")

Cabeçalho:
- Nome do grupo (ex.: "Atletico - MG")
- Nome do atleta (placeholder "Nome do atleta")
- Metadados do atleta: data de nascimento (ex.: "03/2013"), lateralidade (ex.:
  "Canhoto"), posição (ex.: "Atacante") — **estes 3 campos de metadados do atleta
  não existem no CSV nem foram mencionados no planejamento original como entrada do
  sistema.** Ver pendência em [07-pontos-em-aberto.md](07-pontos-em-aberto.md) —
  não implementar como campo editável sem confirmar com o usuário se é informação
  real a ser capturada no MVP ou só decoração do template que pode ficar em branco.
- Título: "Dashboard individual" + data.

Blocos de conteúdo:
- **Indicador de tentativas/acertos** — "Tentativas: 30", "Acertos: 20", "Média do
  grupo: 15" (valores de exemplo do template, não são dados reais).
- **Classificação do TR por acerto e erro** — cruzamento visual das categorias
  "Precoce", "No tempo", "Tardio" com "Acertou"/"Errou" (nota: aqui o template não
  lista "Perda de bola" explicitamente nas categorias visíveis — confirmar se deve
  aparecer também quando houver dados dessa categoria).
- **Média do TR** — dois valores lado a lado: "2.5 s" e "1.8 s" — ver interpretação
  adotada em [03-metricas.md](03-metricas.md) (tempo médio em acertos vs. em erros).
- **Taxa de acerto** — valor único em destaque (ex.: "66%").
- **Atleta em relação ao grupo** — indicador comparativo (gráfico não totalmente
  claro pela árvore de texto — validar visualmente se possível).
- **Taxa de acerto por resposta** — tabela/gráfico com colunas "Média Grupo" /
  "Nome Atleta" por categoria de resposta: "Manutenção", "Passe Dir", "Passe Esq",
  "Chutes" (mesmas categorias abreviadas da página de grupo).

## Observações gerais

- Cores e tipografia exatas não foram capturadas (sem screenshot). Na primeira
  versão dos gráficos, usar uma paleta neutra e consistente; ajustar fino de visual
  é a última etapa prevista no cronograma do planejamento original (seção 10:
  "Testes com dados reais e ajustes finos de visual").
- O layout é fixo nesta primeira versão — o usuário não edita o layout do PDF, só o
  conteúdo (nome do grupo, logo, quais atletas entram).
