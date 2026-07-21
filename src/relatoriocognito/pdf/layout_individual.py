from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfgen.canvas import Canvas

from relatoriocognito.charts.barras import barras_empilhadas_horizontais
from relatoriocognito.charts.colors import AMARELO, VERDE, VERMELHO
from relatoriocognito.charts.gauge import grafico_gauge
from relatoriocognito.charts.radar import grafico_radar
from relatoriocognito.domain import metrics
from relatoriocognito.domain.models import Athlete, Group
from relatoriocognito.pdf.layout_helpers import (
    COR_TEXTO,
    GAP,
    MARGEM,
    cabecalho,
    cartao,
    desenhar_figura,
    distribuir_colunas,
    titulo_cartao,
)

_ORDEM_RADAR = ("Chutar ao Gol", "Passe a Direita", "Manter Posse", "Passe a Esquerda")
_ROTULOS_RADAR = ("Chute", "Passe Dir", "Manutenção", "Passe Esq")


def _badge_valor(c: Canvas, x: float, y: float, w: float, h: float, cor: HexColor, texto: str) -> None:
    cartao(c, x, y, w, h, cor=cor, raio=6)
    c.saveState()
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(COR_TEXTO)
    c.drawCentredString(x + w / 2, y + h / 2 - 4, texto)
    c.restoreState()


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
        titulo_pagina="Dashboard individual",
        data=data,
        caminho_logo=caminho_logo,
        atleta=atleta,
    )

    colunas = distribuir_colunas(MARGEM, largura_pagina - 2 * MARGEM, pesos=[1.0, 1.2, 1.0])
    (x1, w1), (x2, w2), (x3, w3) = colunas

    altura_linha1 = 190
    y_linha1 = y_conteudo - altura_linha1

    # Card 1: Tentativas / Acertos / Media do grupo
    cartao(c, x1, y_linha1, w1, altura_linha1)
    tentativas = len(atleta.trials)
    acertos = metrics.contagem_acertos_erros(atleta.trials)["Acertou"]
    media_grupo = metrics.media_acertos_por_atleta(group.athletes)
    _rotulo_e_badge(c, x1, y_linha1, w1, altura_linha1, "Tentativas:", str(tentativas), HexColor("#BDBDBD"))
    _rotulo_e_badge(
        c, x1, y_linha1, w1, altura_linha1, "Acertos", str(acertos), VERDE, deslocamento=1
    )
    _rotulo_e_badge(
        c,
        x1,
        y_linha1,
        w1,
        altura_linha1,
        "Media do grupo",
        str(round(media_grupo)),
        AMARELO,
        deslocamento=2,
    )

    # Card 2: Taxa de acerto (gauge)
    cartao(c, x2, y_linha1, w2, altura_linha1)
    titulo_cartao(c, "Taxa de acerto", x2 + w2 / 2, y_linha1 + altura_linha1 - 24, tamanho=14)
    taxa = metrics.taxa_acerto(atleta.trials)
    desenhar_figura(c, grafico_gauge(taxa), x2 + 10, y_linha1 + 20, w2 - 20, altura_linha1 - 70)

    # Card 3: Media do TR (Acertos/Erros)
    cartao(c, x3, y_linha1, w3, altura_linha1)
    titulo_cartao(c, "Media do TR", x3 + w3 / 2, y_linha1 + altura_linha1 - 20)
    tr_por_resultado = metrics.media_tr_por_resultado(atleta.trials)
    _linha_rotulo_valor(
        c, x3, y_linha1 + altura_linha1 - 60, w3, "Acertos", f"{tr_por_resultado['Acertou']:.1f} s".replace(".", ","), VERDE
    )
    _linha_rotulo_valor(
        c, x3, y_linha1 + altura_linha1 - 105, w3, "Erros", f"{tr_por_resultado['Errou']:.1f} s".replace(".", ","), VERMELHO
    )

    # Linha 2: Classificação do TR por resultado + Taxa de acerto por resposta
    altura_linha2 = 220
    y_linha2 = y_linha1 - GAP - altura_linha2
    colunas2 = distribuir_colunas(MARGEM, largura_pagina - 2 * MARGEM, pesos=[1.2, 1.0])
    (xa, wa), (xb, wb) = colunas2

    cartao(c, xa, y_linha2, wa, altura_linha2)
    titulo_cartao(c, "Classificação do TR por acerto e erro", xa + wa / 2, y_linha2 + altura_linha2 - 20)
    cruzamento = metrics.classificacao_tr_por_resultado(atleta.trials)
    segmentos = {
        "Precoce": [cruzamento["Acertou"]["Precoce"], cruzamento["Errou"]["Precoce"]],
        "No tempo": [cruzamento["Acertou"]["Ideal"], cruzamento["Errou"]["Ideal"]],
        "Tardio": [cruzamento["Acertou"]["Tardio"], cruzamento["Errou"]["Tardio"]],
    }
    fig_stacked = barras_empilhadas_horizontais(
        ["Acertou", "Errou"],
        segmentos,
        {"Precoce": VERMELHO, "No tempo": VERDE, "Tardio": AMARELO},
    )
    desenhar_figura(c, fig_stacked, xa + 10, y_linha2 + 10, wa - 20, altura_linha2 - 40)

    cartao(c, xb, y_linha2, wb, altura_linha2)
    titulo_cartao(c, "Taxa de acerto por resposta", xb + wb / 2, y_linha2 + altura_linha2 - 20)
    taxa_resposta = metrics.taxa_acerto_por_resposta(atleta.trials)
    valores_radar = {rotulo: taxa_resposta[cat] for cat, rotulo in zip(_ORDEM_RADAR, _ROTULOS_RADAR)}
    desenhar_figura(c, grafico_radar(valores_radar), xb + 10, y_linha2 + 10, wb - 20, altura_linha2 - 40)


def _rotulo_e_badge(
    c: Canvas,
    x_card: float,
    y_card: float,
    w_card: float,
    h_card: float,
    rotulo: str,
    valor: str,
    cor: HexColor,
    *,
    deslocamento: int = 0,
) -> None:
    altura_bloco = h_card / 3
    y_bloco = y_card + h_card - altura_bloco * (deslocamento + 1)
    c.saveState()
    c.setFont("Helvetica", 10)
    c.setFillColor(COR_TEXTO)
    c.drawCentredString(x_card + w_card / 2, y_bloco + altura_bloco - 16, rotulo)
    c.restoreState()
    _badge_valor(c, x_card + 20, y_bloco + 8, w_card - 40, altura_bloco - 28, cor, valor)


def _linha_rotulo_valor(
    c: Canvas, x_card: float, y: float, w_card: float, rotulo: str, valor: str, cor: HexColor
) -> None:
    c.saveState()
    c.setFont("Helvetica", 11)
    c.setFillColor(COR_TEXTO)
    c.drawString(x_card + 16, y + 10, rotulo)
    c.restoreState()
    _badge_valor(c, x_card + w_card / 2 - 10, y, w_card / 2 - 10, 32, cor, valor)
