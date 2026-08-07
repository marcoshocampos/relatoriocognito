from __future__ import annotations

import io

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


def figura_para_png(fig: Figure, dpi: int = 200) -> bytes:
    """Rasteriza a figura via Agg diretamente — sem depender de pyplot/backend global.

    O PNG sai **exatamente** com o aspecto de `fig.get_size_inches()`, para que o
    mesmo gráfico ocupe o mesmo espaço em qualquer relatório. Antes usava
    `bbox_inches="tight"`, que recorta a figura no conteúdo desenhado: um eixo Y
    com valores de 3 dígitos gerava um PNG mais largo que o mesmo gráfico com
    valores de 1 dígito (medido: aspecto 1.12 vs 1.09), e como o PDF encaixa a
    imagem preservando o aspecto, o gráfico aparecia em escalas diferentes entre
    dois relatórios. Ver docs/context/06-decisoes.md.

    O "tight" existia para não cortar rótulo perto da borda (ex.: eixos do
    radar); quem cuida disso agora é o layout engine `constrained`, que encolhe a
    área de plotagem dentro da figura em vez de aumentar a figura.
    """
    fig.set_layout_engine("constrained", w_pad=0.01, h_pad=0.01, wspace=0, hspace=0)
    FigureCanvasAgg(fig)
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=dpi, transparent=True)
    return buffer.getvalue()
