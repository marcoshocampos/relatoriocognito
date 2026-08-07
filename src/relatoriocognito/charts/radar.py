from __future__ import annotations

import math

import matplotlib.patheffects as path_effects
from matplotlib.figure import Figure

from relatoriocognito.charts.colors import CINZA_CLARO, COR_BASE_PADRAO, GRAFITE
from relatoriocognito.charts.estilo import FAMILIA_FONTE, fundo_transparente


def grafico_radar(
    valores: dict[str, float],
    *,
    figsize: tuple[float, float] = (4.0, 4.0),
    cor: str = COR_BASE_PADRAO,
) -> Figure:
    """Radar/diamante. `valores` já deve vir na ordem desejada dos eixos (o
    primeiro fica no topo, os demais em sentido horário)."""
    fig = Figure(figsize=figsize)
    ax = fig.add_subplot(111, projection="polar")

    categorias = list(valores.keys())
    n = len(categorias)
    angulos = [2 * math.pi * i / n for i in range(n)]
    dados = list(valores.values())
    angulos_fechado = angulos + angulos[:1]
    dados_fechado = dados + dados[:1]

    ax.plot(angulos_fechado, dados_fechado, color=cor, linewidth=2)
    ax.fill(angulos_fechado, dados_fechado, color=cor, alpha=0.3)

    # Em r=0 o vértice fica invisível (todos os ângulos colapsam no centro) — sem
    # isso, um eixo com taxa=0 parece "sem dado" em vez de "0%". Uma bolinha no
    # centro para cada eixo zerado deixa isso visível.
    angulos_zero = [ang for ang, val in zip(angulos, dados) if val == 0]
    if angulos_zero:
        ax.plot(angulos_zero, [0] * len(angulos_zero), marker="o", markersize=6, color=cor, linestyle="none")

    ax.set_xticks(angulos)
    ax.set_xticklabels(categorias, fontfamily=FAMILIA_FONTE, color=GRAFITE)
    ax.set_ylim(0, 100)
    ax.set_yticks([25, 50, 75, 100])
    # Esses rótulos caem por cima da área preenchida do radar, então cinza claro
    # sumia contra o preenchimento (e mais ainda com uma cor base escura). Texto
    # escuro com contorno branco fica legível tanto sobre o preenchimento quanto
    # sobre o fundo do cartão, sem precisar mover o rótulo para fora do gráfico.
    ax.set_yticklabels(["25%", "50%", "75%", "100%"], fontsize=8, color=GRAFITE)
    for rotulo in ax.get_yticklabels():
        rotulo.set_fontweight("bold")
        rotulo.set_fontfamily(FAMILIA_FONTE)
        rotulo.set_path_effects([path_effects.withStroke(linewidth=2.5, foreground="white")])
    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)
    ax.spines["polar"].set_color(CINZA_CLARO)
    ax.grid(color=CINZA_CLARO, linewidth=0.8)
    fundo_transparente(fig, ax)
    return fig
