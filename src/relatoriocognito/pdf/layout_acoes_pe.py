from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfgen.canvas import Canvas

from relatoriocognito.charts.barras import barras_empilhadas_horizontais, barras_simples
from relatoriocognito.charts.colors import Paleta, VERMELHO
from relatoriocognito.charts.pizza import grafico_pizza
from relatoriocognito.domain import metrics
from relatoriocognito.domain.models import Athlete, Group
from relatoriocognito.paths import caminho_recurso
from relatoriocognito.pdf.layout_helpers import (
    GAP,
    MARGEM,
    cabecalho,
    cartao,
    desenhar_figura,
    distribuir_colunas,
    rodape,
    titulo_cartao,
)


def desenhar(
    c: Canvas,
    group: Group,
    atleta: Athlete,
    caminho_logo: str | Path | None,
    data: str,
    *,
    largura_pagina: float,
    altura_pagina: float,
    paleta: Paleta = Paleta(),
    data_emissao: str | None = None,
) -> None:
    y_conteudo = cabecalho(
        c,
        largura_pagina=largura_pagina,
        altura_pagina=altura_pagina,
        nome_grupo=group.nome,
        titulo_pagina="Ações por pé",
        data=data,
        caminho_logo=caminho_logo,
        atleta=atleta,
        paleta=paleta,
    )

    colunas = distribuir_colunas(MARGEM, largura_pagina - 2 * MARGEM, pesos=[1.1, 0.8, 1.1])
    (x1, w1), (x2, w2), (x3, w3) = colunas

    # Alturas escaladas para preencher o espaço vertical disponível (mesmo ajuste
    # de hierarquia aplicado às outras 3 páginas).
    altura_linha1 = 265
    y_linha1 = y_conteudo - altura_linha1

    # Card 1: Ações por pé (pizza) — pé esquerdo usa a cor de destaque, pé direito
    # fica com o vermelho fixo (mesma convenção de Acertos/Erros: um lado ganha a
    # cor escolhida, o outro é sempre o par neutro/fixo).
    cartao(c, x1, y_linha1, w1, altura_linha1, cor=HexColor(paleta.fundo_cartao))
    titulo_cartao(c, "Ações por pé", x1 + w1 / 2, y_linha1 + altura_linha1 - 20)
    distribuicao = metrics.distribuicao_pe_usado(atleta.trials)
    fig_pizza = grafico_pizza(
        {"Pé Esquerdo": distribuicao["Esquerdo"], "Pé direito": distribuicao["Direito"]},
        {"Pé Esquerdo": paleta.destaque, "Pé direito": VERMELHO},
        mostrar_percentual=True,
    )
    desenhar_figura(c, fig_pizza, x1 + 10, y_linha1 + 10, w1 - 20, altura_linha1 - 40)

    # Card 2: imagem de par de pés (decorativo)
    cartao(c, x2, y_linha1, w2, altura_linha1, cor=HexColor(paleta.fundo_cartao))
    c.drawImage(
        str(caminho_recurso("par_de_pes.png")),
        x2 + 15,
        y_linha1 + 40,
        width=w2 - 30,
        height=altura_linha1 - 80,
        preserveAspectRatio=True,
        anchor="c",
        mask="auto",
    )

    # Card 3: Media de TR por pé
    cartao(c, x3, y_linha1, w3, altura_linha1, cor=HexColor(paleta.fundo_cartao))
    titulo_cartao(c, "Media de TR por pé", x3 + w3 / 2, y_linha1 + altura_linha1 - 20)
    media_tr_pe = metrics.media_tr_por_pe(atleta.trials)
    fig_barras = barras_simples(
        ["Esquerdo", "Direito"],
        [media_tr_pe["Esquerdo"], media_tr_pe["Direito"]],
        [paleta.destaque, VERMELHO],
    )
    desenhar_figura(c, fig_barras, x3 + 10, y_linha1 + 10, w3 - 20, altura_linha1 - 40)

    # Linha 2: Acertos por pé usado (largura total)
    altura_linha2 = 180
    y_linha2 = y_linha1 - GAP - altura_linha2
    largura_total = largura_pagina - 2 * MARGEM
    cartao(c, MARGEM, y_linha2, largura_total, altura_linha2, cor=HexColor(paleta.fundo_cartao))
    titulo_cartao(c, "Acertos por pé usado", MARGEM + largura_total / 2, y_linha2 + altura_linha2 - 20)
    acertos_pe = metrics.acertos_por_pe(atleta.trials)
    segmentos = {
        "Esquerdo": [acertos_pe["Acertou"]["Esquerdo"], acertos_pe["Errou"]["Esquerdo"]],
        "Direito": [acertos_pe["Acertou"]["Direito"], acertos_pe["Errou"]["Direito"]],
    }
    fig_stacked = barras_empilhadas_horizontais(
        ["Acertou", "Errou"], segmentos, {"Esquerdo": paleta.destaque, "Direito": VERMELHO}, figsize=(9.0, 2.4)
    )
    desenhar_figura(c, fig_stacked, MARGEM + 16, y_linha2 + 10, largura_total - 32, altura_linha2 - 40)

    rodape(c, largura_pagina=largura_pagina, data_emissao=data_emissao)
