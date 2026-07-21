from __future__ import annotations

from matplotlib.figure import Figure

from relatoriocognito.charts.util import fundo_transparente


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
            return f"{pct:.1f}%"
        return str(round(pct * total / 100))

    ax.pie(
        tamanhos,
        labels=categorias,
        colors=cores_wedges,
        autopct=autopct,
        startangle=90,
        counterclock=False,
        wedgeprops=dict(width=0.4) if donut else None,
    )
    ax.set_aspect("equal")
    fundo_transparente(fig, ax)
    return fig
