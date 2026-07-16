---
titulo: Métricas calculadas (regras de negócio)
fonte: 00-planejamento-original.md (seção 5) + 05-modelo-visual-referencia.md
---

# Métricas

Esta é a lógica de negócio mais sensível do sistema — é a que ganha teste de unidade
obrigatório (ver seção 8 do planejamento original). Antes de implementar qualquer
cálculo aqui, reconferir contra este documento e, se houver dúvida de leitura, contra
[07-pontos-em-aberto.md](07-pontos-em-aberto.md) — não assumir.

## Visão de grupo

Agregando todos os CSVs (atletas) selecionados para o relatório:

- **% de acertos / erros** — proporção de linhas com `Correto? = Acertou` vs `Errou`,
  sobre o total de tentativas do grupo. Exibido em gráfico de rosca.
- **Distribuição percentual de `ClassificacaoTR`** — % de linhas em cada uma das 4
  categorias (`Precoce`, `Tardio`, `Ideal`, `Perda de bola`), sobre o total de
  tentativas do grupo.
- **Tempo médio de reação do grupo** — média de `TempoReacao` sobre todas as
  tentativas de todos os atletas do grupo (não é média das médias por atleta).
- **Comparativo de acertos por tipo de decisão** — contagem de tentativas por
  categoria de `RespostaCorreta` (`Chutar ao Gol`, `Manter Posse`, `Passe a Esquerda`,
  `Passe a Direita`).
- **Indicador de tentativas x acertos x média do grupo** — total de tentativas do
  grupo, total de acertos, e a média (aparentemente numérica, ver pendência em
  07) usada como referência de comparação individual.

## Visão individual (por atleta, dentro do relatório)

- **Taxa de acerto por tipo de resposta**, comparada com a média do grupo na mesma
  categoria.
- **Classificação de tempo cruzada com acerto/erro** — cruzamento de
  `ClassificacaoTR` x `Correto?` para aquele atleta especificamente.
- **Tempo médio de reação do atleta** — média de `TempoReacao` das tentativas
  daquele atleta.
- **Taxa de acerto geral do atleta** — % de `Acertou` sobre o total de tentativas
  daquele atleta.
- **Indicador atleta x média do grupo** — comparação direta (ex.: taxa de acerto do
  atleta vs. taxa de acerto média do grupo).

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
