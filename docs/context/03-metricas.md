---
titulo: Métricas calculadas (regras de negócio)
fonte: 00-planejamento-original.md (seção 5) + 05-modelo-visual-referencia.md (atualizado 18/07/2026: nomes de coluna v3 e pendências resolvidas)
---

# Métricas

Esta é a lógica de negócio mais sensível do sistema — é a que ganha teste de unidade
obrigatório (ver seção 8 do planejamento original). Antes de implementar qualquer
cálculo aqui, reconferir contra este documento e, se houver dúvida de leitura, contra
[07-pontos-em-aberto.md](07-pontos-em-aberto.md) — não assumir.

## Visão de grupo

Agregando todos os CSVs (atletas) selecionados para o relatório:

- **% de acertos / erros** — proporção de linhas com `Correto = Acertou` vs `Errou`,
  sobre o total de tentativas do grupo. Exibido em gráfico de rosca.
- **Distribuição percentual de `ClassificacaoTR`** — % de linhas em cada uma das 4
  categorias (`Precoce`, `Tardio`, `Ideal`, `Perda de bola`), sobre o total de
  tentativas do grupo.
- **Tempo médio de reação do grupo** — média de `TempoReacao` sobre todas as
  tentativas de todos os atletas do grupo (não é média das médias por atleta).
- **"Media de acertos por decisão"** (título atualizado em 21/07/2026; antes
  "Acertos por decisão") — duas médias por categoria de resposta (`Chutar ao Gol`,
  `Manter Posse`, `Passe a Esquerda`, `Passe a Direita`), lado a lado: contagem de
  tentativas com aquela categoria em `RespostaCorreta` (série "Ideal" — o que
  deveria ter sido feito) e em `RespostaDada` (série com o nome do grupo — o que foi
  efetivamente feito), **cada uma dividida pelo número de atletas do grupo**
  (total/atletas, mesma convenção de "Acertos por posição" — ver item 14 de
  [07-pontos-em-aberto.md](07-pontos-em-aberto.md)), não a soma bruta. Fonte das
  categorias confirmada com o cliente em 18/07/2026, ver
  [07-pontos-em-aberto.md](07-pontos-em-aberto.md), item 3.
- **Indicador de tentativas x acertos x média do grupo** — total de tentativas do
  grupo, total de acertos, e a média usada como referência de comparação
  individual. **Resolvido (19/07/2026, ver [07-pontos-em-aberto.md](07-pontos-em-aberto.md)
  item 14):** essa "média do grupo" é a média, entre os atletas do grupo, da
  contagem bruta de tentativas `Correto=Acertou` de cada atleta — não uma
  porcentagem/taxa (essa já é coberta separadamente pelo gauge "Taxa de acerto").

## Visão individual (por atleta, dentro do relatório)

- **Taxa de acerto por tipo de resposta**, comparada com a média do grupo na mesma
  categoria.
- **Classificação de tempo cruzada com acerto/erro** — cruzamento de
  `ClassificacaoTR` x `Correto` para aquele atleta especificamente.
- **Tempo médio de reação do atleta** — média de `TempoReacao` das tentativas
  daquele atleta.
- **Taxa de acerto geral do atleta** — % de `Acertou` sobre o total de tentativas
  daquele atleta.
- **Indicador atleta x média do grupo** — comparação direta (ex.: taxa de acerto do
  atleta vs. taxa de acerto média do grupo).

## Visão "Ações por pé"

Usa as colunas `PeEsperado` e `PeUsado` (ver
[02-modelo-dados.md](02-modelo-dados.md)). Todas as métricas abaixo são por atleta:

- **% de ações por pé usado** — proporção de `PeUsado = Esquerdo` vs `Direito`
  sobre o total de tentativas do atleta. Gráfico de rosca/pizza.
- **Tempo médio de reação por pé usado** — média de `TempoReacao`, separada por
  `PeUsado = Esquerdo` vs `Direito`.
- **Acertos por pé usado** — cruzamento de `Correto` (Acertou/Errou) x `PeUsado`
  (Esquerdo/Direito), em barras empilhadas horizontais.

Não há métrica própria de "acertou o pé" a calcular: `PeEsperado` já entra na
avaliação de `Correto` feita pela ferramenta de origem (junto com
`RespostaCorreta`/`RespostaDada`) — ver [02-modelo-dados.md](02-modelo-dados.md).
Esta página usa só `PeUsado` como dado descritivo; `PeEsperado` não aparece em
nenhum gráfico do MVP.

## Visão "Comparação atleta x grupo"

Também por atleta, com dois eixos de comparação:

- **Taxa de acerto por resposta: atleta x média do grupo** — mesma métrica de "taxa
  de acerto por tipo de resposta" já descrita na visão individual acima, mas exibida
  como gráfico de linha (`Media Grupo` vs `Nome Atleta` por categoria de resposta),
  em vez do radar mostrado na página "Dashboard individual". Confirmado com o
  usuário que as duas visualizações da mesma métrica são intencionais (não é
  duplicação a remover).
- **Taxa de acerto por resposta: atleta x média da posição** — mesma métrica, mas
  comparando o atleta contra a média de **outros atletas do relatório que jogam na
  mesma posição** (`Meio campista`, no exemplo), em vez da média geral do grupo.
  **Ajustado em 22/07/2026:** quando não existe nenhum outro atleta do grupo na
  mesma posição, o gráfico não desenha mais uma linha cinza achatada em 0% (que
  parecia um dado real de "0% de acerto") — em vez disso, mostra só a linha do
  atleta e um aviso "Sem outro atleta para comparar" no lugar da linha de
  referência.
- **Acertos por posição** — gráfico de barras com 6 categorias fixas de posição
  (`Zagueiro`, `Meio Campista`, `Atacante`, `Volante`, `Lateral Direito`,
  `Lateral Esquerdo`). Valores em contagem bruta de tentativas `Correto=Acertou`
  (não porcentagem) — **Resolvido (19/07/2026, ver
  [07-pontos-em-aberto.md](07-pontos-em-aberto.md) item 14).** Duas séries:
  `Media da posição` (cinza neutro) e o **nome do atleta** (verde).
  - `Media da posição` = média da contagem de acertos entre **todos** os atletas
    carregados na sessão naquela posição, **incluindo o próprio atleta do
    relatório**. Aparece em qualquer categoria que tenha pelo menos um atleta
    carregado. Posição sem nenhum atleta no grupo continua sem barra nenhuma.
  - A série do atleta = contagem de acertos dele, desenhada **só** na categoria
    correspondente à posição dele, pareada com a barra cinza daquela posição.

  **Ajustado em 26/07/2026:** a média deixou de excluir o próprio atleta. Antes,
  quando ele era o único do grupo naquela posição, a barra de referência sumia e
  só sobrava a barra verde; agora a barra de média existe sempre que a posição
  tem dado. Consequência esperada e aceita pelo usuário: com um único atleta na
  posição, as duas barras ficam iguais por definição.

A "média da posição" usada nesses três gráficos é calculada **só entre os atletas
selecionados no relatório atual** (mesmo grupo da sessão) — confirmado com o
usuário, sem depender de histórico entre relatórios (mantém
[06-decisoes.md](06-decisoes.md)). Atenção a uma diferença deliberada entre os
gráficos: a linha "Media de acertos posição" **exclui** o próprio atleta (a
comparação ali é "eu x os outros", daí o aviso "Sem outro atleta para comparar"),
enquanto a barra "Acertos por posição" **inclui** todos. São funções separadas em
`domain/metrics.py` (`trials_por_posicao` vs. `acertos_por_posicao`) — não
unificar. Se o grupo não tiver atleta em alguma das 6 posições, essa posição fica
sem dado no gráfico "Acertos por posição" — não travar a geração do relatório por
causa disso.

## Pendência de interpretação: "tempo médio separado" (acertos x erros)

O modelo de referência mostra, na página individual, dois valores de tempo próximos
ao indicador de acertos/erros: `2.5 s` e `1.8 s` (ver
[05-modelo-visual-referencia.md](05-modelo-visual-referencia.md)).

Leitura adotada até validação com dados reais completos:
- `2.5 s` = tempo médio de reação **nas tentativas em que o atleta acertou**.
- `1.8 s` = tempo médio de reação **nas tentativas em que o atleta errou**.

Implementar com essa lógica primeiro. Se, ao testar com uma planilha real mais
completa, os números não baterem com essa leitura, revisar — não travar a
implementação por causa disso, mas deixar a função isolada e fácil de ajustar
(ver [04-arquitetura.md](04-arquitetura.md), módulo `domain/metrics.py`).

## Observação sobre o cálculo de médias em grupo

Tomar cuidado para não confundir "média das médias por atleta" com "média sobre
todas as tentativas do grupo" — são valores diferentes quando os atletas têm números
de tentativas distintos. O planejamento original não deixa 100% explícito qual é
esperado; a leitura mais direta e mais comum nesse tipo de relatório é média sobre
todas as tentativas (pooled), não média das médias. Confirmar visualmente comparando
com o modelo de referência ao implementar.
