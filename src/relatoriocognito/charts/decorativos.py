from __future__ import annotations

from matplotlib.figure import Figure
from matplotlib.patches import Circle, Wedge

from relatoriocognito.charts.util import fundo_transparente

_CINZA_AVATAR = "#9E9E9E"


def icone_avatar(*, figsize: tuple[float, float] = (1.0, 1.0), cor: str = _CINZA_AVATAR) -> Figure:
    """Silhueta genérica simples (cabeça + ombros) para o espaço de foto do atleta."""
    fig = Figure(figsize=figsize)
    ax = fig.add_subplot(111)
    ax.add_patch(Circle((0.5, 0.62), 0.22, color=cor))
    ax.add_patch(Wedge((0.5, 0.14), 0.4, 0, 180, color=cor))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    fundo_transparente(fig, ax)
    return fig
