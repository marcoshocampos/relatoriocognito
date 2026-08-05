from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfgen.canvas import Canvas

from relatoriocognito.charts.barras import barras_agrupadas
from relatoriocognito.charts.colors import AMARELO, LARANJA, Paleta, VERMELHO
from relatoriocognito.charts.pizza import grafico_pizza
from relatoriocognito.domain import metrics
from relatoriocognito.domain.models import Group
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

_CATEGORIAS_RESPOSTA_CSV = ("Chutar ao Gol", "Passe a Esquerda", "Passe a Direita", "Manter Posse")
_CATEGORIAS_RESPOSTA_ROTULO = ("Chute", "Passe Esq", "Passe Dir", "Manutenção")


def desenhar(
    c: Canvas,
    group: Group,
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
        titulo_pagina="Dashboard Overview",
        data=data,
        caminho_logo=caminho_logo,
        paleta=paleta,
    )

    trials = metrics.trials_do_grupo(group.athletes)

    colunas = distribuir_colunas(MARGEM, largura_pagina - 2 * MARGEM, pesos=[1.0, 1.0, 1.3])
    (x1, w1), (x2, w2), (x3, w3) = colunas

    # Alturas escaladas para preencher o espaço vertical disponível — a versão
    # original (210/90) deixava ~1/3 da página em branco abaixo dos cartões.
    altura_cartao_pequeno = 310
    altura_media_tr = 135
    altura_total = altura_cartao_pequeno + GAP + altura_media_tr
    y_cartao_pequeno = y_conteudo - altura_cartao_pequeno
    y_media_tr = y_cartao_pequeno - GAP - altura_media_tr

    # Card 1: Media de acertos do grupo (pizza Acertos x Erros)
    cartao(c, x1, y_cartao_pequeno, w1, altura_cartao_pequeno, cor=HexColor(paleta.fundo_cartao))
    titulo_cartao(c, "Media de acertos do grupo", x1 + w1 / 2, y_cartao_pequeno + altura_cartao_pequeno - 20)
    contagem = metrics.contagem_acertos_erros(trials)
    fig_pizza = grafico_pizza(
        {"Acertos": contagem["Acertou"], "Erros": contagem["Errou"]},
        {"Acertos": paleta.destaque, "Erros": VERMELHO},
    )
    desenhar_figura(c, fig_pizza, x1 + 10, y_cartao_pequeno + 10, w1 - 20, altura_cartao_pequeno - 40)

    # Card 2: Media de classificação do TR (donut, fundo em destaque)
    cartao(
        c, x2, y_cartao_pequeno, w2, altura_cartao_pequeno,
        cor=HexColor(paleta.fundo_cartao_destaque),
    )
    titulo_cartao(c, "Media de classificação do TR", x2 + w2 / 2, y_cartao_pequeno + altura_cartao_pequeno - 20)
    dist = metrics.distribuicao_classificacao_tr(trials)
    fig_donut = grafico_pizza(
        {
            "No tempo": dist["Ideal"],
            "Precoce": dist["Precoce"],
            "Tardio": dist["Tardio"],
            "Perda de bola": dist["Perda de bola"],
        },
        {"No tempo": paleta.destaque, "Precoce": AMARELO, "Tardio": LARANJA, "Perda de bola": VERMELHO},
        donut=True,
        mostrar_percentual=True,
    )
    desenhar_figura(c, fig_donut, x2 + 10, y_cartao_pequeno + 10, w2 - 20, altura_cartao_pequeno - 40)

    # Card 3: Media de acertos por decisão (altura combinada das duas linhas)
    cartao(c, x3, y_media_tr, w3, altura_total, cor=HexColor(paleta.fundo_cartao))
    titulo_cartao(c, "Media de acertos por decisão", x3 + w3 / 2, y_media_tr + altura_total - 20)
    decisao = metrics.acertos_por_decisao(group.athletes)
    ideal = [decisao[cat][0] for cat in _CATEGORIAS_RESPOSTA_CSV]
    dado = [decisao[cat][1] for cat in _CATEGORIAS_RESPOSTA_CSV]
    fig_barras = barras_agrupadas(
        list(_CATEGORIAS_RESPOSTA_ROTULO),
        {group.nome: dado, "Ideal": ideal},
        {group.nome: paleta.destaque, "Ideal": paleta.referencia},
        figsize=(6.0, 5.0),
    )
    desenhar_figura(c, fig_barras, x3 + 10, y_media_tr + 10, w3 - 20, altura_total - 40)

    # Media do TR (abaixo dos cards 1+2)
    largura_media_tr = (x2 + w2) - x1
    cartao(c, x1, y_media_tr, largura_media_tr, altura_media_tr, cor=HexColor(paleta.fundo_cartao))
    titulo_cartao(c, "Media do TR", x1 + largura_media_tr / 2, y_media_tr + altura_media_tr - 22)
    media_tr = metrics.media_tr(trials)
    c.saveState()
    c.setFont("Helvetica-Bold", 24)
    valor_formatado = f"{media_tr:.1f} s".replace(".", ",")
    c.drawCentredString(x1 + largura_media_tr / 2, y_media_tr + 26, valor_formatado)
    c.restoreState()

    rodape(c, largura_pagina=largura_pagina, data_emissao=data_emissao)
