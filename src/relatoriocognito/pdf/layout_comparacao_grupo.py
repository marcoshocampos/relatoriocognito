from __future__ import annotations

from pathlib import Path

from reportlab.pdfgen.canvas import Canvas

from relatoriocognito.charts.barras import barras_agrupadas
from relatoriocognito.charts.colors import PRETO, VERDE
from relatoriocognito.charts.linha import grafico_linha_comparativa
from relatoriocognito.domain import metrics
from relatoriocognito.domain.models import Athlete, Group
from relatoriocognito.pdf.layout_helpers import (
    GAP,
    MARGEM,
    cabecalho,
    cartao,
    desenhar_figura,
    distribuir_colunas,
    titulo_cartao,
)

_ORDEM_RESPOSTA = ("Manter Posse", "Passe a Direita", "Passe a Esquerda", "Chutar ao Gol")
_ROTULOS_RESPOSTA = ("Manutenção", "Passe Dir", "Passe Esq", "Chutes")


def desenhar(
    c: Canvas,
    group: Group,
    atleta: Athlete,
    caminho_logo: str | Path | None,
    data: str,
    *,
    largura_pagina: float,
    altura_pagina: float,
) -> None:
    y_conteudo = cabecalho(
        c,
        largura_pagina=largura_pagina,
        altura_pagina=altura_pagina,
        nome_grupo=group.nome,
        titulo_pagina="Comparação atleta grupo",
        data=data,
        caminho_logo=caminho_logo,
        atleta=atleta,
    )

    taxa_atleta = metrics.taxa_acerto_por_resposta(atleta.trials)
    valores_atleta = [taxa_atleta[cat] for cat in _ORDEM_RESPOSTA]

    altura_linha1 = 230
    y_linha1 = y_conteudo - altura_linha1
    colunas = distribuir_colunas(MARGEM, largura_pagina - 2 * MARGEM, pesos=[1.0, 1.0])
    (x1, w1), (x2, w2) = colunas

    # Card 1: Media de acertos do grupo (atleta x grupo)
    cartao(c, x1, y_linha1, w1, altura_linha1)
    titulo_cartao(c, "Media de acertos do grupo", x1 + w1 / 2, y_linha1 + altura_linha1 - 20)
    taxa_grupo = metrics.taxa_acerto_por_resposta(metrics.trials_do_grupo(group.athletes))
    valores_grupo = [taxa_grupo[cat] for cat in _ORDEM_RESPOSTA]
    fig1 = grafico_linha_comparativa(
        list(_ROTULOS_RESPOSTA),
        ("Media Grupo", valores_grupo),
        (atleta.nome, valores_atleta),
    )
    desenhar_figura(c, fig1, x1 + 10, y_linha1 + 10, w1 - 20, altura_linha1 - 40)

    # Card 2: Media de acertos posição (atleta x média da posição, excluindo o próprio atleta)
    cartao(c, x2, y_linha1, w2, altura_linha1)
    titulo_cartao(c, "Media de acertos posição", x2 + w2 / 2, y_linha1 + altura_linha1 - 20)
    trials_posicao = metrics.trials_por_posicao(group.athletes, atleta.posicao, excluir_atleta=atleta)
    taxa_posicao = metrics.taxa_acerto_por_resposta(trials_posicao)
    valores_posicao = [taxa_posicao[cat] for cat in _ORDEM_RESPOSTA]
    fig2 = grafico_linha_comparativa(
        list(_ROTULOS_RESPOSTA),
        (atleta.posicao, valores_posicao),
        (atleta.nome, valores_atleta),
    )
    desenhar_figura(c, fig2, x2 + 10, y_linha1 + 10, w2 - 20, altura_linha1 - 40)

    # Linha 2: Acertos por posição (largura total, 6 categorias)
    altura_linha2 = 220
    y_linha2 = y_linha1 - GAP - altura_linha2
    largura_total = largura_pagina - 2 * MARGEM
    cartao(c, MARGEM, y_linha2, largura_total, altura_linha2)
    titulo_cartao(c, "Acertos por posição", MARGEM + largura_total / 2, y_linha2 + altura_linha2 - 20)

    media_por_posicao = metrics.acertos_por_posicao(group.athletes, atleta)
    acertos_atleta = metrics.contagem_acertos_erros(atleta.trials)["Acertou"]
    posicoes = list(metrics.POSICOES)
    fig3 = barras_agrupadas(
        posicoes,
        {
            "Media da posição": [media_por_posicao[p] for p in posicoes],
            "Jogador": [acertos_atleta for _ in posicoes],
        },
        {"Media da posição": PRETO, "Jogador": VERDE},
        figsize=(9.0, 3.6),
    )
    desenhar_figura(c, fig3, MARGEM + 16, y_linha2 + 10, largura_total - 32, altura_linha2 - 40)
