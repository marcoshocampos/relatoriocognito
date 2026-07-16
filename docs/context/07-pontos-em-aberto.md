---
titulo: Pontos em aberto (a validar com o usuário)
fonte: 00-planejamento-original.md (seção 12) + achados na leitura do modelo Canva e do CSV real
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
   não aparece nenhum caso dessa categoria. Confirmar com uma planilha real mais
   completa se ela se comporta como as outras 3 categorias de `ClassificacaoTR` em
   todos os gráficos, ou se tem tratamento especial.
   — Status: em aberto. Reforçado por outro achado abaixo (item 5).

## Encontrados ao ler o modelo visual (Canva) e o CSV real

3. **Categoria "Ideal" dentro de "Acertos por decisão".** No gráfico de barras da
   página de grupo, aparece uma categoria "Ideal" junto com "Chute", "Passe Esq",
   "Passe Dir", "Manutenção" — não fica claro se "Ideal" é uma 5ª categoria de
   resposta (o que não bate com as 4 categorias de `RespostaCorreta`/`RespostaDada`
   vistas no CSV) ou uma barra de referência/meta separada. Confirmar com o usuário
   antes de implementar este gráfico específico.
   — Status: em aberto.

4. **Metadados do atleta na página individual** (data de nascimento, lateralidade
   — "Canhoto" —, posição — "Atacante"). Esses campos aparecem no template do Canva
   mas não existem no CSV atual.
   — Status: **resolvido para o MVP (16/07/2026)** — o usuário confirmou que novas
   colunas serão adicionadas futuramente ao CSV para trazer essas informações, mas
   **por ora o MVP ignora esses campos**: não implementar leitura, tela de entrada
   manual, nem exibição desses 3 campos na página individual do PDF. Quando as
   colunas novas existirem no CSV, atualizar
   [02-modelo-dados.md](02-modelo-dados.md) com o formato real e revisitar este
   item para adicionar os campos ao layout.

5. **`Perda de bola` ausente na "Classificação do TR por acerto e erro" (página
   individual).** O template mostra só "Precoce", "No tempo", "Tardio" nesse
   cruzamento específico, sem "Perda de bola". Confirmar se é omissão proposital do
   template ou se deve aparecer também quando houver dados dessa categoria.
   — Status: em aberto.

6. **Média de grupo: pooled vs. média das médias por atleta.** Ver observação em
   [03-metricas.md](03-metricas.md). O planejamento original não especifica
   explicitamente; leitura adotada é "pooled" (sobre todas as tentativas). Validar
   visualmente contra o modelo se possível, ou confirmar com o usuário.
   — Status: em aberto.

7. **Qualidade visual do modelo de referência.** Não foi possível capturar
   screenshot do Canva nesta sessão (editor baseado em canvas). A especificação em
   [05-modelo-visual-referencia.md](05-modelo-visual-referencia.md) é textual,
   extraída da árvore de acessibilidade das páginas — suficiente para estrutura e
   rótulos, mas não para cores/tipografia/posicionamento exato.
   — Status: **em andamento (16/07/2026)** — usuário vai exportar os PNGs das
   páginas do modelo Canva e colocar em
   [`docs/reference/modelo-canva/`](../reference/modelo-canva). Quando os arquivos
   chegarem lá, revisar [05-modelo-visual-referencia.md](05-modelo-visual-referencia.md)
   contra as imagens reais (cores, tipografia, posicionamento) e marcar este item
   como resolvido.
