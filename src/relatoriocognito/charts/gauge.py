from __future__ import annotations

from matplotlib.figure import Figure
from matplotlib.patches import Wedge

from relatoriocognito.charts.colors import VERDE, VERMELHO
from relatoriocognito.charts.util import fundo_transparente


def grafico_gauge(
    valor_percentual: float,
    *,
    figsize: tuple[float, float] = (4.0, 2.6),
) -> Figure:
    """Arco semicircular: verde do valor até 180°, vermelho preenchendo o resto."""
    fig = Figure(figsize=figsize)
    ax = fig.add_subplot(111)

    valor = max(0.0, min(100.0, valor_percentual))
    angulo_preenchido = 180 * valor / 100

    ax.add_patch(Wedge((0, 0), 1.0, 180 - angulo_preenchido, 180, width=0.3, color=VERDE))
    ax.add_patch(Wedge((0, 0), 1.0, 0, 180 - angulo_preenchido, width=0.3, color=VERMELHO))

    ax.text(
        0,
        -0.15,
        f"{valor:.0f}%",
        ha="center",
        va="center",
        fontsize=28,
        color=VERDE,
        fontweight="bold",
    )
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-0.2, 1.1)
    ax.set_aspect("equal")
    ax.axis("off")
    fundo_transparente(fig, ax)
    return fig
