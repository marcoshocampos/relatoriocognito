"""Estilo visual comum a todos os gráficos.

Centraliza o que o modelo Canva (docs/reference/modelo-canva/) tem de recorrente e
que o matplotlib não faz por padrão: legenda horizontal sem moldura acima do
gráfico, grade horizontal fraca, nenhuma borda de eixo, rótulos em cinza.

Sobre a fonte: os gráficos são rasterizados em PNG antes de entrar no PDF, então
a fonte usada aqui vira pixel e não precisa ser embutida. Mesmo assim a lista
prioriza Arial, que é metricamente compatível com a Helvetica usada pelo
reportlab nos textos do PDF — assim título de cartão e rótulo de eixo não
parecem de famílias diferentes. "Helvetica" em si não entra na lista porque não
existe como arquivo de fonte instalável (é um nome padrão de PDF, não uma fonte
de sistema) — matplotlib avisaria "not found" a cada gráfico antes de cair para
o fallback. Ver docs/context/06-decisoes.md.
"""

from __future__ import annotations

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from relatoriocognito.charts.colors import CINZA_CLARO, CINZA_MEDIO, GRAFITE

FAMILIA_FONTE = ["Arial", "DejaVu Sans"]

TAMANHO_ROTULO = 9
TAMANHO_LEGENDA = 9
TAMANHO_VALOR = 9


def _aplicar_fonte(ax: Axes) -> None:
    for texto in [ax.title, ax.xaxis.label, ax.yaxis.label, *ax.get_xticklabels(), *ax.get_yticklabels()]:
        texto.set_fontfamily(FAMILIA_FONTE)


def fundo_transparente(fig: Figure, ax: Axes) -> None:
    """As páginas do PDF desenham o cartão de fundo (cor sólida) por conta própria —
    a figura matplotlib não deve competir com isso."""
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)


def estilo_cartesiano(
    fig: Figure,
    ax: Axes,
    *,
    grade: bool = True,
    eixo_x_visivel: bool = True,
) -> None:
    """Aplica o estilo padrão a um gráfico de eixos (barras, linha).

    `grade=False` para gráficos que já rotulam o valor dentro da barra (as
    empilhadas horizontais), onde a grade só polui.
    """
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_visible(eixo_x_visivel)
    ax.spines["bottom"].set_color(CINZA_CLARO)

    if grade:
        ax.set_axisbelow(True)
        ax.yaxis.grid(True, color=CINZA_CLARO, linewidth=0.8)
        ax.xaxis.grid(False)

    ax.tick_params(axis="both", length=0, labelsize=TAMANHO_ROTULO, colors=CINZA_MEDIO, pad=6)
    for rotulo in ax.get_xticklabels():
        rotulo.set_color(GRAFITE)
    ax.yaxis.label.set_color(CINZA_MEDIO)
    ax.yaxis.label.set_fontsize(TAMANHO_ROTULO)
    _aplicar_fonte(ax)
    fundo_transparente(fig, ax)


def legenda_topo(ax: Axes, *, handles: list | None = None, colunas: int | None = None) -> None:
    """Legenda horizontal centralizada acima do gráfico, sem moldura — é assim que
    o modelo Canva apresenta as séries, em vez da caixa flutuante que o
    matplotlib põe dentro da área de plotagem (onde ela cobre barras)."""
    if handles is None:
        handles, rotulos = ax.get_legend_handles_labels()
    else:
        rotulos = [h.get_label() for h in handles]
    if not handles:
        return

    legenda = ax.legend(
        handles,
        rotulos,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.01),
        ncol=colunas or len(handles),
        frameon=False,
        handlelength=0.9,
        handleheight=0.9,
        handletextpad=0.5,
        columnspacing=1.6,
        fontsize=TAMANHO_LEGENDA,
    )
    for texto in legenda.get_texts():
        texto.set_color(GRAFITE)
        texto.set_fontfamily(FAMILIA_FONTE)


def rotular_barras_verticais(ax: Axes, barras, *, formato: str = "{:.0f}") -> None:
    """Valor escrito acima de cada barra. O modelo Canva depende do eixo Y para
    isso, mas nos cartões estreitos do PDF o valor exato fica ilegível — o rótulo
    resolve sem precisar aumentar o gráfico."""
    for barra in barras:
        altura = barra.get_height()
        ax.annotate(
            formato.format(altura),
            xy=(barra.get_x() + barra.get_width() / 2, altura),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=TAMANHO_VALOR,
            color=GRAFITE,
            fontfamily=FAMILIA_FONTE,
        )
