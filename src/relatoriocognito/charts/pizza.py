from __future__ import annotations

from matplotlib.figure import Figure

from relatoriocognito.charts.colors import GRAFITE, cor_texto_sobre
from relatoriocognito.charts.estilo import (
    FAMILIA_FONTE,
    TAMANHO_VALOR,
    formatar_uma_casa,
    fundo_transparente,
)

# Espessura do anel da rosca, em fração do raio (o furo começa em 1 - _LARGURA_ANEL).
_LARGURA_ANEL = 0.4


def grafico_pizza(
    valores: dict[str, float],
    cores: dict[str, str],
    *,
    donut: bool = False,
    mostrar_percentual: bool = False,
    figsize: tuple[float, float] = (4.0, 4.0),
) -> Figure:
    """Pizza (donut=False) ou rosca com furo (donut=True).

    Rótulos mostram a contagem bruta por padrão (como em "Media de acertos do
    grupo"), ou percentual se `mostrar_percentual=True` (como em "Media de
    classificação do TR").
    """
    fig = Figure(figsize=figsize)
    ax = fig.add_subplot(111)

    categorias = list(valores.keys())
    tamanhos = [valores[c] for c in categorias]
    cores_wedges = [cores[c] for c in categorias]
    total = sum(tamanhos) or 1

    def autopct(pct: float) -> str:
        if mostrar_percentual:
            return f"{formatar_uma_casa(pct)}%"
        return str(round(pct * total / 100))

    # Onde o valor é escrito, em fração do raio. Na rosca o anel vai de
    # (1 - _LARGURA_ANEL) a 1, então o meio dele é o que centraliza o texto na
    # faixa colorida — o default do matplotlib (0.6) caía exatamente na borda
    # interna do anel, deixando o número espremido na quina da fatia.
    distancia_valor = 1 - _LARGURA_ANEL / 2 if donut else 0.62

    _, rotulos_categoria, rotulos_valor = ax.pie(
        tamanhos,
        labels=categorias,
        colors=cores_wedges,
        autopct=autopct,
        pctdistance=distancia_valor,
        startangle=90,
        counterclock=False,
        wedgeprops=(
            dict(width=_LARGURA_ANEL, edgecolor="white", linewidth=1.5)
            if donut
            else dict(edgecolor="white", linewidth=1.5)
        ),
        textprops={"fontfamily": FAMILIA_FONTE, "color": GRAFITE, "fontsize": 10},
    )
    # Percentual/contagem escrito dentro da fatia precisa de contraste com a cor
    # dela — texto escuro sobre uma fatia escura (ex.: vermelho saturado) some.
    # Negrito porque, mesmo com a cor certa, o número dentro de uma área colorida
    # saturada continuava difícil de ler.
    for rotulo_valor, cor_fatia in zip(rotulos_valor, cores_wedges):
        rotulo_valor.set_color(cor_texto_sobre(cor_fatia))
        rotulo_valor.set_fontsize(TAMANHO_VALOR)
        rotulo_valor.set_fontweight("bold")
    ax.set_aspect("equal")
    fundo_transparente(fig, ax)
    return fig
