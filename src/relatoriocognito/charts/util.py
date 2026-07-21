from __future__ import annotations

import io

from matplotlib.axes import Axes
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


def figura_para_png(fig: Figure, dpi: int = 200) -> bytes:
    """Rasteriza a figura via Agg diretamente — sem depender de pyplot/backend global.

    Anexa um canvas Agg explícito à figura e usa `savefig` (em vez de
    `canvas.print_png` puro) para manter `bbox_inches="tight"` funcionando —
    sem isso, rótulos perto da borda (ex.: eixos do radar) ficam cortados.
    """
    FigureCanvasAgg(fig)
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=dpi, transparent=True, bbox_inches="tight")
    return buffer.getvalue()


def fundo_transparente(fig: Figure, ax: Axes) -> None:
    """As páginas do PDF desenham o cartão de fundo (cor sólida) por conta própria —
    a figura matplotlib não deve competir com isso."""
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
