from __future__ import annotations

from matplotlib.figure import Figure

from relatoriocognito.charts.colors import CINZA_MEDIO, VERDE
from relatoriocognito.charts.util import fundo_transparente


def grafico_linha_comparativa(
    categorias: list[str],
    serie_referencia: tuple[str, list[float]] | None,
    serie_atleta: tuple[str, list[float]],
    *,
    figsize: tuple[float, float] = (4.5, 3.2),
) -> Figure:
    """Duas linhas (referência em cinza, atleta em verde) sobre as mesmas categorias.

    Reaproveitada tanto para "atleta x média do grupo" quanto "atleta x média da
    posição" (docs/context/07-pontos-em-aberto.md item 11).

    `serie_referencia=None` — sem nenhum outro atleta para comparar (ex.: nenhum
    outro atleta na mesma posição) — desenha só a linha do atleta e um aviso no
    lugar da linha cinza, em vez de uma linha achatada em 0% que pareceria um
    dado real (mesma cautela de `barras.barras_agrupadas` para valores ausentes).
    """
    fig = Figure(figsize=figsize)
    ax = fig.add_subplot(111)
    x = list(range(len(categorias)))

    if serie_referencia is not None:
        nome_ref, valores_ref = serie_referencia
        ax.plot(x, valores_ref, marker="o", color=CINZA_MEDIO, label=nome_ref)
    else:
        ax.text(
            0.5, 0.5, "Sem outro atleta\npara comparar",
            transform=ax.transAxes, ha="center", va="center",
            color=CINZA_MEDIO, fontsize=9,
        )

    nome_atleta, valores_atleta = serie_atleta
    ax.plot(x, valores_atleta, marker="o", color=VERDE, label=nome_atleta)

    ax.set_xticks(x)
    ax.set_xticklabels(categorias)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Porcentagem")
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    fundo_transparente(fig, ax)
    return fig
