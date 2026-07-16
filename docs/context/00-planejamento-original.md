# Planejamento — Sistema de Relatório RV (Tempo de Reação / Decisão)

> Documento original de planejamento, recebido do usuário em 16/07/2026.
> Mantido aqui sem edições como registro histórico. Os demais arquivos desta
> pasta (`01-*` a `07-*`) quebram este conteúdo em tópicos e são a referência
> "viva" — se algo divergir, os arquivos numerados prevalecem, mas este
> documento explica o raciocínio original por trás das decisões.

Documento de planejamento técnico do sistema que importa CSVs de testes de
reação/decisão de atletas e gera um relatório em PDF (visão de grupo + visão
individual por atleta), no modelo enviado como referência (Canva "Modelo Relatorio RV").

Projeto novo e independente.

## 1. Objetivo

Ler arquivos CSV já exportados (um por atleta, por sessão de treino), cruzar os dados,
calcular as métricas de acerto/erro e tempo de reação, gerar os gráficos equivalentes
ao modelo de referência, e exportar tudo em um único PDF (página de grupo + uma página
por atleta).

Uso interno: o sistema roda na máquina de quem monta os relatórios (Caio/Marcos), não
na máquina do cliente final. O cliente recebe apenas o PDF pronto.

## 2. Escopo da primeira versão (MVP)

**Entra:**
- Importação de múltiplos CSVs (um por atleta) no formato já confirmado.
- Tela para o usuário definir, por relatório: nome do grupo e uma imagem/logo (ex.: escudo do time).
- Seleção manual de quais CSVs entram em cada relatório/sessão (o próprio usuário decide quais atletas formam o grupo).
- Cálculo das métricas de grupo e individuais (ver seção 5).
- Geração dos gráficos (rosca de acertos/erros, barras de classificação de tempo, barras comparativas por tipo de decisão, indicador comparando atleta x grupo).
- Exportação em um único PDF: 1 página de grupo + 1 página por atleta selecionado.
- Empacotado como um `.exe` único (Windows), sem necessidade de instalar Python.

**Não entra nesta primeira versão** (pode virar evolução futura, se fizer sentido):
- Salvar nome/logo como "padrão" para reaproveitar entre relatórios (por ora é definido a cada relatório).
- Histórico de relatórios gerados anteriormente.
- Suporte a formatos de CSV diferentes do confirmado (sem mapeamento flexível de colunas).
- Instalador para a máquina do cliente final.
- Edição do layout do PDF pelo usuário (o layout é fixo, no padrão do modelo).
- Qualquer coisa em nuvem/multiusuário.

## 3. Arquitetura geral

Aplicação desktop em Python, sem servidor, sem banco de dados. Cada execução é
independente — não há persistência entre gerações de relatório.

```
[Tela: nome do grupo + logo]
     → [Tela: selecionar CSVs dos atletas]
     → [Leitura e validação dos CSVs]
     → [Cálculo das métricas (grupo e por atleta)]
     → [Geração dos gráficos]
     → [Montagem do PDF (capa/cabeçalho + página de grupo + páginas individuais)]
     → [Salvar arquivo .pdf]
```

Empacotamento final: PyInstaller, gerando um único `.exe` — quem for usar só dá duplo
clique, sem instalar nada.

## 4. Modelo de dados (CSV de entrada)

Confirmado com um arquivo real (`Geral_10_3_2025.csv`). Uma linha por tentativa/trial:

| Coluna | Significado | Exemplo |
|---|---|---|
| `Treino` | Nome/identificação da sessão de treino | `Geral_10_3_2025` |
| `Jogador` | Identificador + nome do atleta | ` 01 Caio` |
| `TempoReacao` | Tempo de decisão, em **segundos** (confirmado) | `13.31` |
| `ClassificacaoTR` | Classificação do tempo: `Precoce`, `Tardio`, `Ideal` ou `Perda de bola` (as 4 já vêm prontas no CSV) | `Precoce` |
| `Correto?` | Se a resposta bateu com a ideal: `Acertou` ou `Errou` (já vem pronto, não é recalculado) | `Errou` |
| `RespostaCorreta` | Qual era a resposta ideal para aquela jogada | `Chutar ao Gol` |
| `RespostaDada` | Qual resposta o atleta efetivamente deu | `Manter Posse` |
| `Data` | Data do teste | `10/03/2025` |
| `Hora` | Horário da tentativa | `11:02` |

Premissa confirmada: **o sistema não recalcula `ClassificacaoTR` nem `Correto?`** — essas
colunas já vêm prontas da ferramenta de teste. O sistema só agrega (conta, soma, tira
média) em cima delas.

Um CSV = um atleta. O "grupo" de um relatório é formado manualmente pelo usuário,
selecionando dois ou mais CSVs de atletas na hora de gerar o relatório.

## 5. Métricas calculadas

**Visão de grupo** (agregando todos os CSVs selecionados):
- % de acertos / erros (rosca).
- Distribuição percentual de `ClassificacaoTR` (Precoce / Tardio / Ideal / Perda de bola).
- Tempo médio de reação do grupo.
- Comparativo de acertos por tipo de decisão (`RespostaCorreta`: Chutar ao Gol, Manter
  Posse, Passe a Esquerda, Passe a Direita) — contagem por categoria.
- Indicador de tentativas x acertos x média do grupo.

**Visão individual** (por atleta, dentro do relatório):
- Taxa de acerto por tipo de resposta, comparado com a média do grupo.
- Classificação de tempo (Precoce/Tardio/Ideal/Perda de bola) cruzada com acerto/erro.
- Tempo médio de reação do atleta.
- Taxa de acerto geral do atleta.
- Indicador comparando o atleta com a média do grupo.

> **Ponto a validar durante o desenvolvimento:** o modelo de referência mostra também
> um tempo médio "separado" (ex.: 2,5s / 1,8s) perto do indicador de acertos/erros —
> a leitura mais provável é "tempo médio nas respostas certas" vs "tempo médio nas
> respostas erradas". Vamos implementar com essa lógica e ajustar caso, ao ver com
> dados reais completos, a leitura pretendida for outra.

## 6. Componentes do sistema

- **Importador/Parser** — lê os CSVs selecionados, valida colunas esperadas e formato,
  descarta linhas vazias.
- **Motor de agregação** — calcula as métricas da seção 5, por atleta e por grupo.
- **Gerador de gráficos** — desenha os gráficos (rosca, barras, indicador comparativo)
  no estilo do modelo de referência.
- **Montador de PDF** — organiza os gráficos + cabeçalho (nome do grupo + logo) nas
  páginas (1 de grupo + 1 por atleta).
- **Interface (GUI)** — telas de: (1) nome do grupo + logo, (2) seleção dos CSVs dos
  atletas, (3) botão gerar relatório / salvar PDF.

## 7. Tratamento de erros

- CSV com colunas faltando ou fora do padrão esperado → aviso claro ("este arquivo não
  está no formato esperado") e a importação daquele arquivo é rejeitada, sem travar o
  restante.
- CSV vazio ou sem linhas válidas → aviso e atleta não entra no relatório.
- Nenhum CSV selecionado → botão de gerar fica bloqueado até selecionar ao menos um.
- Logo em formato não suportado → aviso pedindo PNG/JPG.
- Erro ao salvar o PDF (ex.: pasta sem permissão) → aviso com opção de escolher outro
  local.

## 8. Testes

Sem suíte automatizada formal prevista para o MVP (uso interno, ferramenta pequena).
Testes leves de unidade nas contas de agregação (seção 5), por serem a lógica de
negócio mais sensível a erro silencioso, e testes manuais do fluxo completo com os
CSVs reais antes da entrega.

## 9. Empacotamento e distribuição

- Empacotado com PyInstaller em um único `.exe`.
- Roda offline, sem instalar Python na máquina.
- Atualizações futuras = gerar um novo `.exe` e substituir o antigo.

## 10. Estimativa de horas (para orçamento)

Estimativa de desenvolvimento de uma pessoa, para a primeira versão (MVP) descrita
acima. Não inclui manutenção/evoluções futuras.

| Etapa | Horas (estimativa) |
|---|---|
| Setup do projeto e ambiente | 1,5 – 2h |
| Leitura e validação dos CSVs (parser) | 3 – 5h |
| Cálculos e agregações (grupo e individual) | 4 – 7h |
| Geração dos gráficos (rosca, barras, indicador) | 6 – 10h |
| Layout e montagem do PDF (cabeçalho c/ nome+logo, páginas) | 4 – 7h |
| Interface gráfica (telas de nome/logo, seleção de CSV, gerar) | 4 – 7h |
| Tratamento de erros e mensagens amigáveis | 2 – 3h |
| Empacotamento em `.exe` + testes de instalação | 2 – 3h |
| Testes com dados reais e ajustes finos de visual | 3 – 6h |
| **Total estimado** | **≈ 30 – 50 horas** |

A variação depende principalmente de quão fiel ao layout do modelo Canva o resultado
final precisa ficar (o item de gráficos costuma ser o mais demorado de ajustar
visualmente).

## 11. Decisões definidas nesta conversa

- Projeto novo e independente do `plamevservice`.
- Uso interno: roda na máquina da equipe, não do cliente.
- Usuário final não-técnico → interface simples de botões.
- Formato de CSV fixo e consistente (confirmado com arquivo real).
- Um CSV por atleta; grupo formado por seleção manual de arquivos.
- `ClassificacaoTR` e `Correto?` já vêm prontos no CSV — sistema só agrega.
- `TempoReacao` está em segundos.
- `ClassificacaoTR` tem 4 valores possíveis: Precoce, Tardio, Ideal, Perda de bola.
- PDF final: 1 arquivo por sessão, página de grupo + 1 página por atleta.
- Nome do grupo e logo são definidos por relatório (não salvos como padrão, por ora).
- Stack: Python (pandas + matplotlib + reportlab), empacotado em `.exe` via PyInstaller.

## 12. Pontos em aberto (a validar durante o desenvolvimento)

- Interpretação exata do "tempo médio separado" (acertos x erros) na visão individual (seção 5).
- Confirmar com uma planilha completa (múltiplas linhas variadas) se `Perda de bola`
  aparece do jeito esperado, já que na amostra vista não constava nenhum caso.
