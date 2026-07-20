---
titulo: Pontos em aberto (a validar com o usuário)
fonte: 00-planejamento-original.md (seção 12) + achados na leitura do modelo Canva e do CSV real (16-18/07/2026)
---

# Pontos em aberto

Itens que **não devem ser decididos sozinho** durante a implementação — perguntar ao
usuário quando chegar a hora de implementar a parte correspondente. Marcar aqui o
status conforme forem sendo resolvidos (não apagar o item, registrar a resposta).

## Do planejamento original

1. **Interpretação do "tempo médio separado" (2.5s / 1.8s) na visão individual.**
   Leitura adotada provisoriamente em [03-metricas.md](03-metricas.md): tempo médio
   em tentativas certas vs. erradas. Confirmar com dados reais completos.
   — Status: em aberto.

2. **Comportamento de `Perda de bola`.** Na amostra vista (`Geral_10_3_2025.csv`)
   não aparece nenhum caso dessa categoria em nenhuma das duas versões do CSV.
   Confirmar com uma planilha real mais completa se ela se comporta como as outras 3
   categorias de `ClassificacaoTR` em todos os gráficos, ou se tem tratamento
   especial.
   — Status: em aberto. Reforçado por outro achado abaixo (item 5).

## Encontrados ao ler o modelo visual (Canva) e o CSV real

3. **Categoria "Ideal" dentro de "Acertos por decisão".**
   — Status: **resolvido (18/07/2026)** — cliente confirmou que a série "Ideal" vem
   da coluna `RespostaCorreta`. Ou seja, o gráfico "Acertos por decisão" compara, por
   categoria de resposta (`Chutar ao Gol`/"Chute", `Passe a Esquerda`/"Passe Esq",
   `Passe a Direita`/"Passe Dir", `Manter Posse`/"Manutenção"), duas contagens:
   - **"Ideal"** = quantas tentativas tinham aquela categoria como `RespostaCorreta`
     (o que deveria ter sido feito).
   - **"Atletico"** (nome do grupo/time) = quantas tentativas tiveram aquela
     categoria como `RespostaDada` (o que o atleta/time efetivamente fez).
   Não é uma 5ª categoria nem uma média/meta fixa — são duas agregações por
   categoria, uma sobre `RespostaCorreta` e outra sobre `RespostaDada`. Atualizado em
   [03-metricas.md](03-metricas.md) e
   [05-modelo-visual-referencia.md](05-modelo-visual-referencia.md).

4. **Metadados do atleta na página individual** (data de nascimento, lateralidade,
   posição).
   — Status: **parcialmente resolvido (17/07/2026)** — o CSV v2 trouxe lateralidade
   e posição embutidas no campo `Jogador` (formato `"Nome - Lateralidade - Posição"`,
   ex.: `"Caio - Canhoto - Meio campista"`, ver
   [02-modelo-dados.md](02-modelo-dados.md)). Não são mais campos de entrada manual
   nem ficam de fora do MVP — devem ser extraídos do CSV. **A data de nascimento
   (ex.: "03/2013" no modelo) continua sem coluna correspondente no CSV** — esse
   pedaço específico segue em aberto, mesmo tratamento de "ignorar por ora" que
   valia para os 3 campos antes.

5. **`Perda de bola` ausente na "Classificação do TR por acerto e erro" (página
   individual).**
   — Status: **resolvido (17/07/2026)** — usuário confirmou que é proposital: esse
   gráfico específico mostra sempre só as 3 categorias ("Precoce", "No tempo",
   "Tardio"), sem "Perda de bola" (provável motivo: nessas tentativas não há tempo
   de reação válido para classificar). Implementar filtrando `ClassificacaoTR !=
   'Perda de bola'` só neste gráfico — os demais gráficos que usam `ClassificacaoTR`
   (ex.: "Media de classificação do TR" na página de grupo) continuam considerando
   as 4 categorias normalmente.

6. **Média de grupo: pooled vs. média das médias por atleta.** Ver observação em
   [03-metricas.md](03-metricas.md). O planejamento original não especifica
   explicitamente; leitura adotada é "pooled" (sobre todas as tentativas). Validar
   visualmente contra o modelo se possível, ou confirmar com o usuário.
   — Status: em aberto.

7. **Qualidade visual do modelo de referência.**
   — Status: **resolvido (17/07/2026)** — usuário exportou os PNGs das 4 páginas do
   modelo Canva, disponíveis em
   [`docs/reference/modelo-canva/`](../reference/modelo-canva)
   (`dashboard_overview.png`, `dashboard_individual.png`, `acoes_por_pe.png`,
   `comparacao_atleta_grupo.png`). [05-modelo-visual-referencia.md](05-modelo-visual-referencia.md)
   já reflete essas imagens.

## Encontrados na atualização do CSV e do modelo Canva (17/07/2026)

8. **Relação entre `PeEsperado` e `PeUsado`.**
   — Status: **resolvido (18/07/2026)** — cliente confirmou que `PeEsperado`/`PeUsado`
   já entram no cálculo de `Correto` feito pela ferramenta que gera o CSV,
   junto com `RespostaCorreta`/`RespostaDada` — a avaliação de acerto/erro combina
   várias colunas, não só a resposta. **Não existe (nem deve ser criada) uma métrica
   própria de "acerto de pé"** — reforça a regra de ouro de nunca recalcular
   `Correto`. A página "Ações por pé" usa `PeUsado` só como dado descritivo;
   `PeEsperado` não tem uso em nenhum gráfico do MVP. Atualizado em
   [02-modelo-dados.md](02-modelo-dados.md) e [03-metricas.md](03-metricas.md).

9. **Origem da "média da posição" na página "Comparação atleta grupo".**
   — Status: **resolvido (17/07/2026)** — usuário confirmou que a média por posição
   é calculada **só entre os atletas selecionados no relatório atual** (mesmo grupo
   da sessão), sem depender de histórico entre relatórios. Mantém consistência com a
   decisão de "sem histórico" em [06-decisoes.md](06-decisoes.md). Implicação prática:
   se o grupo selecionado não tiver atletas em todas as 6 posições do gráfico
   "Acertos por posição", as posições sem atleta no grupo simplesmente não têm dado
   — não travar a geração do relatório por causa disso, só não desenhar/zerar a
   barra daquela posição.

10. **Mudança de escopo: modelo cresceu de 2 para 4 páginas.**
    — Status: **resolvido (17/07/2026)** — usuário confirmou que as 4 páginas (grupo
    + Dashboard individual + Ações por pé + Comparação atleta grupo) fazem parte do
    MVP. A estimativa de horas da seção 10 do planejamento original ficou
    desatualizada (previa só 2 páginas) — considerar isso ao comunicar prazo, mas não
    é um bloqueio técnico. [04-arquitetura.md](04-arquitetura.md) atualizado para
    refletir a estrutura de 4 páginas.

11. **Possível duplicação: "taxa de acerto por resposta" aparece duas vezes.**
    — Status: **resolvido (17/07/2026)** — usuário confirmou que é intencional: o
    radar na página "Dashboard individual" e a linha na página "Comparação atleta
    grupo" convivem, mesma métrica em dois formatos visuais diferentes. Implementar
    ambos os componentes de gráfico em `charts/` (não são a mesma função reaproveitada
    com output diferente — são duas visualizações distintas da mesma métrica de
    `domain/metrics.py`).

12. **Selo "Cognito" no canto superior direito das páginas.**
    — Status: **resolvido (17/07/2026)** — usuário confirmou que o selo deve
    aparecer fixo em todo PDF gerado pelo sistema, independente do cliente/time.
    Tratar como elemento de branding fixo do produto em `pdf/` (não é
    configurável pelo usuário na GUI, ao contrário do logo do time). O arquivo de
    imagem do selo precisa ser adicionado em `src/relatoriocognito/resources/` para
    ir embutido no `.exe` — pedir ao usuário o arquivo de origem (ideal em alta
    resolução/vetor) quando chegar a hora de implementar essa parte.
