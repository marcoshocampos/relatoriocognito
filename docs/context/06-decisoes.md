---
titulo: Decisões técnicas já tomadas
fonte: 00-planejamento-original.md (seção 11) + decisões tomadas em 16/07/2026 na estruturação inicial
---

# Decisões técnicas

Estas decisões já foram tomadas e **não devem ser reabertas** durante a
implementação sem alinhar antes com o usuário — evita retrabalho e discussões
repetidas.

## Do planejamento original

- Projeto novo e independente (não depende de outro projeto existente).
- Uso interno: roda na máquina da equipe que monta os relatórios, não do cliente
  final.
- Usuário final não-técnico → interface simples de botões, sem jargão técnico.
- Formato de CSV fixo e consistente — sem mapeamento flexível de colunas no MVP.
- Um CSV por atleta; grupo formado por seleção manual de arquivos, não inferido.
- `ClassificacaoTR` e `Correto` já vêm prontos no CSV — sistema só agrega, nunca
  recalcula essas duas colunas.
- `TempoReacao` está em segundos.
- PDF final: 1 arquivo por sessão. ~~página de grupo + 1 página por atleta~~ —
  **substituído em 17/07/2026**, ver seção "Atualização de escopo" abaixo.
- Nome do grupo e logo são definidos a cada relatório (não salvos como padrão).
- Stack de dados/relatório: **Python + pandas + matplotlib + reportlab**.
- Empacotamento: **PyInstaller**, gerando um único `.exe` para Windows.

## Tomadas na estruturação inicial do repositório (16/07/2026)

- **GUI:** CustomTkinter. Motivo: visual mais moderno que Tkinter puro, mantendo
  simplicidade de empacotamento com PyInstaller (baseado em Tkinter/stdlib, poucas
  dependências extras) — adequado para usuário final não-técnico.
- **Gerenciador de ambiente/dependências:** [uv](https://docs.astral.sh/uv/).
  Motivo: mais rápido que pip/poetry, resolve dependências e gerencia o venv,
  usa `pyproject.toml`, builds reproduzíveis.
- **Nome do pacote Python interno:** `relatoriocognito` (mesmo nome do repositório).
- **Versão mínima do Python:** 3.12.
- **Layout de código:** `src/` layout (`src/relatoriocognito/...`), separando
  lógica pura (`domain/`) das bordas de I/O, gráficos, PDF e GUI — ver
  [04-arquitetura.md](04-arquitetura.md).
- **Testes:** pytest, focado em `domain/metrics.py` (não decidido explicitamente
  pelo usuário, mas é a ferramenta padrão do ecossistema Python e coerente com a
  seção 8 do planejamento original — reavaliar apenas se o usuário pedir algo
  diferente).

## Atualização de escopo — CSV v2 e modelo de 4 páginas (17/07/2026)

O cliente enviou uma nova versão do CSV de exemplo e do modelo Canva, com mudanças
confirmadas pelo usuário nesta data:

- **PDF final passa a ter 4 páginas por relatório**: 1 página de grupo ("Dashboard
  Overview") + 3 páginas por atleta selecionado ("Dashboard individual", "Ações por
  pé", "Comparação atleta grupo") — substitui a decisão original de "1 página de
  grupo + 1 por atleta". Ver [04-arquitetura.md](04-arquitetura.md) e
  [05-modelo-visual-referencia.md](05-modelo-visual-referencia.md).
- **Lateralidade e posição do atleta** vêm embutidas no campo `Jogador` do CSV
  (formato `"Nome - Lateralidade - Posição"`), não são mais entrada manual nem ficam
  de fora do MVP. Data de nascimento continua sem coluna no CSV (segue em aberto).
- **Média por posição** (página "Comparação atleta grupo") é calculada só entre os
  atletas selecionados no relatório atual — não usa histórico entre relatórios,
  mantendo a decisão de "sem histórico" já fechada acima.
- **"Taxa de acerto por resposta" aparece intencionalmente em dois formatos**: radar
  (página individual) e linha (página de comparação) — não é duplicação a remover,
  são dois componentes de gráfico distintos.
- CSV vem em **ISO-8859-1** (não UTF-8) — parser precisa decodificar corretamente
  (ver [02-modelo-dados.md](02-modelo-dados.md)).
- **"Perda de bola" fica de fora do gráfico "Classificação do TR por acerto e
  erro"** (página individual) por design — confirmado com o usuário.
- **Selo "Cognito"** aparece fixo em todo PDF gerado pelo sistema — branding do
  produto, não configurável pelo usuário.

## Atualização de respostas do cliente (18/07/2026)

- **Série "Ideal" em "Acertos por decisão"** (página de grupo) = contagem de
  `RespostaCorreta` por categoria de resposta, em contraste com a série do nome do
  grupo/time = contagem de `RespostaDada`. Não é uma 5ª categoria nem uma média —
  ver [03-metricas.md](03-metricas.md) e
  [07-pontos-em-aberto.md](07-pontos-em-aberto.md), item 3.
- **`PeEsperado`/`PeUsado` já entram na avaliação de `Correto`** feita pela
  ferramenta que gera o CSV (junto com `RespostaCorreta`/`RespostaDada`) — não existe
  nem deve ser criada uma métrica própria de "acerto de pé" no sistema. Reforça a
  regra de nunca recalcular `Correto`/`ClassificacaoTR` — ver
  [02-modelo-dados.md](02-modelo-dados.md) e
  [07-pontos-em-aberto.md](07-pontos-em-aberto.md), item 8.

## Atualização de nomes de coluna (18/07/2026)

Cliente padronizou os nomes de coluna do CSV para remover espaços, acentos e
pontuação: `Pe esperado` → `PeEsperado`, `Pé usado` → `PeUsado`, `Correto?` →
`Correto`. Os demais nomes de coluna não mudaram. Ver
[02-modelo-dados.md](02-modelo-dados.md) para o histórico completo de versões do
CSV (v1 → v2 → v3).

Todas as pendências levantadas na atualização do CSV e do modelo de 4 páginas
(16-18/07/2026) estão resolvidas — ver [07-pontos-em-aberto.md](07-pontos-em-aberto.md)
para o registro completo de cada uma.

## Ajustes visuais pós-implementação (21-22/07/2026)

Depois do MVP implementado, o cliente testou com dados reais/`.exe` gerado e pediu
ajustes de clareza visual — nenhum muda métrica de negócio, só como ela é
desenhada:

- "Acertos por decisão" → renomeado "Media de acertos por decisão"; valores agora
  são média por atleta (total/atletas), não soma bruta do grupo.
- Radar "Taxa de acerto por resposta": eixo com taxa 0% ganha uma bolinha central
  (senão o vértice em r=0 fica invisível, parecendo "sem dado").
- "Ações por pé": a imagem de referência do cliente (par de pés verde/vermelho,
  `docs/reference/imagens/Chuteira.png`) substituiu o desenho vetorial de
  "chuteiras" — copiada para `src/relatoriocognito/resources/par_de_pes.png`,
  carregada via novo helper `relatoriocognito.paths.caminho_recurso` (resolve o
  caminho tanto no código-fonte quanto no `.exe` empacotado).
- "Acertos por posição": mesmo problema do radar, mas em barra — um valor real
  igual a 0 (ex.: atleta com 0 acertos) ficava idêntico a "sem atleta na posição".
  Ganhou o mesmo tratamento (bolinha na base). Também foi redesenhado (duas
  iterações em 22/07/2026): o valor do próprio atleta (verde) só aparece na
  posição dele, não mais repetido nas 6 categorias. A primeira iteração usava uma
  3ª cor (cinza) para "outras posições" e um aviso de texto quando a posição do
  atleta não tinha comparação — **o cliente pediu para simplificar**: só 2 cores
  (preto = "Media da posição", em qualquer categoria com dado; verde = "Jogador",
  só na posição do atleta) e sem texto de aviso — se não houver comparação, só a
  barra verde aparece, sem substituto.
- Linha "Media de acertos posição": sem nenhum outro atleta do grupo na mesma
  posição, a linha de referência (antes achatada em 0%, parecendo dado real) vira
  um aviso "Sem outro atleta para comparar" — esse aviso continua só nessa linha
  (o cliente pediu para tirar o equivalente da barra "Acertos por posição", ver
  acima).
- `TempoReacao` com vírgula decimal (`"13,31"`, comum em CSV reexportado/editado
  no Excel com localidade PT-BR) causava erro "nenhuma tentativa válida" — não
  tem relação com o atleta ter ou não acertos. Parser agora aceita `.` ou `,`
  como separador decimal — ver [02-modelo-dados.md](02-modelo-dados.md).

## Refazimento de "Acertos por posição" (26/07/2026)

O usuário pediu para refazer só esse gráfico da página "Comparação atleta grupo".
Mudanças confirmadas ponto a ponto antes de implementar:

- **A média da posição passa a incluir o próprio atleta.** Antes ela era calculada
  só entre os *outros* atletas da posição, então quando o atleta era o único do
  grupo naquela posição a barra de referência simplesmente não existia. Agora a
  barra cinza aparece em toda posição com pelo menos um atleta carregado na
  sessão. Consequência aceita pelo usuário: com um único atleta na posição, a
  barra de média e a do atleta ficam idênticas por definição.
- **Cor da série de média: preto → cinza neutro** (`CINZA_MEDIO`, `#A6A6A6`) —
  reaproveita o cinza já usado nas linhas de referência dos outros dois gráficos
  da mesma página, em vez de introduzir um tom novo.
- **Legenda da série verde: "Jogador" → nome real do atleta**, como já acontece
  nos gráficos de linha da mesma página.
- **Mantido como estava:** as 6 categorias fixas no eixo X (posição sem atleta
  continua sem barra e sem aviso), a barra verde só na posição do próprio atleta,
  e a bolinha na base para distinguir valor real 0 de ausência de dado.
- **Não mexer junto:** a linha "Media de acertos posição" continua *excluindo* o
  próprio atleta e mantendo o aviso "Sem outro atleta para comparar" — ali a
  comparação é "eu x os outros". São duas funções distintas em
  `domain/metrics.py` (`trials_por_posicao` vs. `acertos_por_posicao`) e a
  divergência é intencional.

## Cor base configurável, rodapé de emissão e restyle geral (03/08/2026)

Pedido do usuário: times que recebem o relatório reclamam quando a cor exibida
é a de um rival. Três mudanças implementadas juntas nessa rodada:

- **Cor base escolhida pelo usuário na tela 1 do wizard** (`gui/tela_grupo.py`),
  com seletor nativo (`tkinter.colorchooser`) e amostra visual. Guardada em
  `JanelaPrincipal.cor_base` (default = verde do modelo Canva, `COR_BASE_PADRAO`
  em `charts/colors.py`, para quem não mexer no seletor ter o resultado de
  sempre). `tela_gerar.py` monta um `charts.colors.Paleta(base=cor_base)` e
  repassa para `gerar_relatorio_pdf`, que propaga a mesma instância para as 4
  funções de layout em `pdf/`.
  - **O que responde à cor base:** tudo que representa o time/atleta/dado real —
    a série de destaque nos gráficos de "Acertos por decisão" e "Acertos por
    posição", a linha do atleta nos gráficos de comparação, o gauge de taxa de
    acerto, o radar, a fatia "Acertou" das pizzas, os badges de valor da página
    individual — e o fundo dos cartões (a cor base misturada com branco, ver
    abaixo).
  - **O que NÃO responde — permanece fixo:** vermelho/amarelo/laranja
    (`VERMELHO`/`AMARELO`/`LARANJA` em `charts/colors.py`) continuam com
    significado semântico fixo (erro, precoce, tardio) — derivá-los da cor base
    quebraria a leitura desses gráficos. O cinza de referência (`CINZA_MEDIO`,
    usado em "Media Grupo"/"Media da posição") também é fixo — ele existe
    justamente para servir de pano de fundo neutro ao dado real. O selo
    "Cognito" também não muda de cor — é branding do produto, não do time (ver
    item 12 de [07-pontos-em-aberto.md](07-pontos-em-aberto.md)).
  - **Fundo dos cartões:** pedido do usuário foi "a mesma cor com alpha de 20%
    ou menos". Implementado como mistura sólida com branco (`misturar_com_branco`
    em `charts/colors.py`), não transparência real — PDF não garante suporte de
    alpha entre leitores/impressão, e a cor pré-misturada dá o mesmo resultado
    visual em qualquer lugar. Intensidade: 12% nos cartões normais, 20% no
    cartão de destaque que antes era lavanda fixa (`COR_CARTAO_LAVANDA`,
    removida).
  - **Contraste de texto:** como a cor base agora é livre (pode ser bem clara ou
    bem escura), os badges de valor (página individual) calculam a cor do texto
    em cima da cor de fundo (`cor_texto_sobre`, luminância relativa WCAG) em vez
    de usar preto fixo — evita texto ilegível com cores escuras (ex.: azul-marinho).
- **Rodapé "Relatório emitido em dd/mm/aaaa"** em todas as 4 páginas
  (`layout_helpers.rodape`). Usa `datetime.date.today()` calculada **uma única
  vez** por PDF gerado (em `pdf/report.py`, repassada como `data_emissao` para
  as 4 funções de layout) — evita que um relatório que atravesse a meia-noite
  durante a geração mostre datas diferentes em páginas diferentes. Não confundir
  com a data que já existia no cabeçalho (`data`), que vem do CSV (data da
  sessão de coleta) — são conceitualmente diferentes (emissão do relatório vs.
  data da coleta) e ambas aparecem no PDF.
- **Restyle geral dos gráficos** (`charts/estilo.py`, novo módulo): legendas
  horizontais no topo (sem moldura), grid horizontal leve, remoção das bordas
  superior/direita dos eixos, rótulos de valor nas barras, fonte única
  (Arial/Helvetica) consistente com o texto desenhado pelo reportlab. Objetivo:
  aproximar o visual do modelo Canva de referência, que não tem bordas de eixo
  nem grid pesado.
- **Hierarquia visual — alturas dos cartões recalculadas.** As páginas
  "Dashboard Overview" e "Ações por pé" deixavam cerca de 1/3 da altura da
  página em branco abaixo dos cartões (alturas antigas dimensionadas para um
  conteúdo menor, nunca reajustadas). Alturas aumentadas para preencher o
  espaço vertical disponível, com a mesma folga acima do rodapé nas 4 páginas
  (~38pt). Gráficos com aspecto circular/polar (pizza, rosca, gauge, radar) não
  ficam maiores com isso — o `bbox_inches="tight"` do matplotlib sempre corta
  para o formato natural do conteúdo — então o ganho ali é o cartão colorido
  preencher mais a página, não o desenho em si crescer. Gráficos cartesianos
  (barra, linha) recebem `figsize` ajustado nos cartões que mudaram de
  proporção de forma mais acentuada.

## Escala dos gráficos, formato da página e fundos (05/08/2026)

Três problemas relatados pelo usuário depois de ver os PDFs gerados:

- **Gráficos saíam em escalas diferentes entre dois relatórios.** Causa:
  `charts/util.py` rasterizava com `bbox_inches="tight"`, que **recorta a figura
  no conteúdo desenhado** — um eixo Y com valores de 3 dígitos gerava um PNG
  mais largo que o mesmo gráfico com valores de 1 dígito (medido: aspecto 1.1247
  vs 1.0941 no mesmo `figsize`). Como o PDF encaixava a imagem com
  `preserveAspectRatio=True`, a sobra mudava conforme os dados e o gráfico
  aparecia maior ou menor. **Corrigido** trocando o "tight" pelo layout engine
  `constrained`, que encolhe a área de plotagem *dentro* da figura em vez de
  aumentar a figura — o aspecto do PNG passa a ser exatamente o do `figsize`
  (verificado: 1.6000 constante variando dados e comprimento de nome).
  O "tight" existia para não cortar rótulo perto da borda (eixos do radar); o
  `constrained` cobre esse caso.
- **Gráficos pequenos demais.** `pdf/layout_helpers.desenhar_figura` agora
  redimensiona a figura para o tamanho exato da caixa do cartão
  (`fig.set_size_inches(w / 72, h / 72)`) antes de rasterizar, em vez de gerar
  num `figsize` arbitrário e reduzir para caber. Além de acabar com a sobra,
  isso torna a tipografia previsível: desenhado 1:1, um texto de 9pt no
  matplotlib sai com 9pt no PDF — antes a figura era reduzida e a mesma fonte
  saía com ~5pt. **Consequência para quem for mexer em `charts/`:** o `figsize`
  dessas funções virou só um default para uso isolado (teste, exploração) —
  dentro do relatório ele é sempre sobrescrito, então mudar `figsize` ali não
  muda mais nada no PDF; para mudar o tamanho de um gráfico, mude a caixa do
  cartão no `pdf/layout_*.py`.
- **Página mais larga.** `TAMANHO_PAGINA` passou de `landscape(A4)`
  (841.89 x 595.28) para 16:9 mantendo a altura (1058.27 x 595.28). O relatório
  é um painel para ver na tela, não um documento para imprimir, e 16:9 é a
  proporção do modelo Canva de referência. Manter a altura foi deliberado:
  preserva todo o ajuste vertical dos cartões já calibrado, e a largura extra vai
  direto para os gráficos, já que as colunas saem de `distribuir_colunas`
  (proporcional à largura da página).
- **Fundos mais claros.** `_INTENSIDADE_FUNDO` / `_INTENSIDADE_FUNDO_DESTAQUE`
  em `charts/colors.py` foram de 12%/20% para 7%/12%.
- **Cartões "Media do TR" (páginas de grupo e individual)** tinham o conteúdo
  ancorado no topo, deixando quase metade do cartão vazia embaixo — agora é
  centralizado no espaço abaixo do título, e o valor único da página de grupo
  subiu de 24pt para 34pt, proporcional à largura nova.

O teste de `Paleta.fundo_cartao` foi reescrito nessa rodada para checar a
*relação* (fundo é um tom claro da base; destaque é mais forte que o comum) em
vez dos valores exatos de intensidade — a versão anterior fixava 12%/20% e
quebrou no primeiro ajuste visual, que é justamente o tipo de coisa que muda com
frequência.

## Legibilidade dos números nos gráficos (05/08/2026)

Relatado pelo usuário testando com cor base preta:

- **Números pouco visíveis.** Todos os valores desenhados sobre área colorida
  (fatias de pizza/rosca, segmentos das barras empilhadas) e acima das barras
  agora saem em **negrito**, e `TAMANHO_VALOR` subiu de 9 para 10.
- **Percentuais da rosca espremidos na quina da fatia.** O `pctdistance` do
  matplotlib tem default 0.6, que numa rosca de espessura 0.4 (anel de r=0.6 a
  r=1.0) cai exatamente na **borda interna** do anel. Agora é calculado como o
  meio da faixa colorida (`1 - largura_anel / 2`), então o número fica centrado
  na fatia. A pizza cheia continua com o valor a 0.62 do raio.
- **Rótulo de barra contradizendo a altura desenhada.** As médias de "Media de
  acertos por decisão" são total/atletas, então dão valores como 6,75 — que o
  formato `{:.0f}` arredondava para "7" sobre uma barra visivelmente abaixo da
  linha de grade do 7. `charts/estilo.formatar_valor` agora mostra inteiro só
  quando o valor é redondo, e uma casa decimal quando não é ("6,8"). Rótulo de
  barra virou função formatadora (`formatador=`) em vez de string de formato.
- **Vírgula decimal em todo lugar.** "Media de TR por pé" mostrava `14.6` e a
  rosca `10.0%`, com ponto, enquanto o reportlab escrevia `14,3 s` com vírgula
  na mesma página. Padronizado em vírgula (`formatar_uma_casa`).
- **Percentuais do radar sumindo.** Ficam por cima da área preenchida, e em
  cinza claro desapareciam (pior ainda com cor base escura). Agora são texto
  escuro em negrito com **contorno branco** (`path_effects.withStroke`), que
  funciona tanto sobre o preenchimento quanto sobre o fundo do cartão sem
  precisar mover o rótulo para fora do gráfico.

## Feedback de progresso e abertura automática do PDF (05/08/2026)

Durante a geração do PDF a janela não dava sinal nenhum de vida (alguns segundos
desenhando gráficos), e o usuário pediu um indicador de carregamento e que o
arquivo abrisse sozinho no fim.

- **A geração saiu da thread da interface.** Era a mudança obrigatória: rodando
  no mesmo thread, o laço de eventos do Tk fica parado, a janela congela e
  *nenhuma* animação roda — um spinner ficaria imóvel. Agora
  `gui/tela_gerar.py` dispara uma `threading.Thread` (daemon) e acompanha o fim
  dela com `after` a cada 100ms. A thread de trabalho não toca em widget nenhum:
  devolve o resultado por `self._erro_geracao`, lido de volta na thread da
  interface. Seguro do lado do matplotlib porque `charts/` monta as figuras via
  `Figure()` + `FigureCanvasAgg` explícito, sem o estado global do pyplot —
  verificado gerando um PDF completo pelo caminho da GUI.
- **"Voltar" também é desabilitado durante a geração.** Sem isso, sair da tela no
  meio destruiria o frame e o acompanhamento da thread mexeria em widget já
  destruído.
- **Spinner:** `gui/widgets/spinner.py`, arco em canvas girando via `after`. O
  CustomTkinter só traz `CTkProgressBar` (barra), e um glifo animado ("◐") ficaria
  à mercê da fonte instalada. Fica **ao lado** do botão, não dentro: sobrepor um
  canvas no `CTkButton` exigiria mexer na estrutura interna do widget, e o botão
  já sinaliza o estado ficando desabilitado com o texto "Gerando PDF…".
- **Abertura automática:** `abrir_arquivo()` usa `os.startfile` no Windows (com
  ramo para macOS/Linux) e **falha em silêncio** — o PDF já foi salvo, então não
  ter leitor associado não transforma a geração em erro, e a tela continua
  mostrando o caminho do arquivo.
- **O messagebox de sucesso foi removido.** Com o PDF abrindo sozinho, o modal
  virava um passo a mais para fechar antes de ver o resultado; o caminho do
  arquivo agora aparece no rótulo de status verde da própria tela. Os
  messageboxes de **erro** continuam.

**Lembrete importante:** o `.exe` em `dist/` não se atualiza sozinho — é preciso
rodar `scripts/build_exe.ps1` (ou o comando `pyinstaller` do `README.md`) depois
de qualquer mudança de código para gerar um `.exe` novo.

## Como usar este documento

Antes de tomar qualquer decisão técnica nova durante a implementação, checar aqui
primeiro se ela já foi decidida. Se uma decisão listada aqui parecer errada ou
incompleta ao encontrar um caso real durante o desenvolvimento, voltar para o
usuário antes de simplesmente mudar de rumo — não decidir sozinho sobre pontos já
fechados.
