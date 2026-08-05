from __future__ import annotations

from matplotlib.figure import Figure
from matplotlib.patches import Wedge

from relatoriocognito.charts.colors import COR_BASE_PADRAO, VERMELHO, escurecer
from relatoriocognito.charts.estilo import FAMILIA_FONTE, fundo_transparente


def grafico_gauge(
    valor_percentual: float,
    *,
    cor: str = COR_BASE_PADRAO,
    figsize: tuple[float, float] = (4.0, 2.6),
) -> Figure:
    """Arco semicircular: cor de destaque do valor (acertos) até 180°, vermelho
    preenchendo o resto (erros — mesma cor semântica fixa usada no resto do
    relatório para "Erros", ver docs/context/06-decisoes.md)."""
    fig = Figure(figsize=figsize)
    ax = fig.add_subplot(111)

    valor = max(0.0, min(100.0, valor_percentual))
    angulo_preenchido = 180 * valor / 100

    ax.add_patch(Wedge((0, 0), 1.0, 180 - angulo_preenchido, 180, width=0.3, color=cor))
    ax.add_patch(Wedge((0, 0), 1.0, 0, 180 - angulo_preenchido, width=0.3, color=VERMELHO))

    ax.text(
        0,
        -0.15,
        f"{valor:.0f}%",
        ha="center",
        va="center",
        fontsize=28,
        color=escurecer(cor, 0.3),
        fontweight="bold",
        fontfamily=FAMILIA_FONTE,
    )
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-0.2, 1.1)
    ax.set_aspect("equal")
    ax.axis("off")
    fundo_transparente(fig, ax)
    return fig
