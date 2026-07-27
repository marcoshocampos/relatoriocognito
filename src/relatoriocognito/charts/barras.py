from __future__ import annotations

from matplotlib.figure import Figure
from matplotlib.patches import Patch

from relatoriocognito.charts.util import fundo_transparente


def _rotacionar_rotulos_se_necessario(ax, categorias: list[str]) -> None:
    """Evita rótulos do eixo X se sobrepondo quando há muitas categorias ou nomes longos
    (ex.: as 6 posições em "Acertos por posição")."""
    if len(categorias) > 4 or any(len(c) > 10 for c in categorias):
        for rotulo in ax.get_xticklabels():
            rotulo.set_rotation(20)
            rotulo.set_ha("right")


def barras_simples(
    categorias: list[str],
    valores: list[float],
    cores: list[str],
    *,
    figsize: tuple[float, float] = (4.0, 3.2),
    ylabel: str | None = None,
) -> Figure:
    """Uma barra por categoria, cada uma com sua própria cor (ex.: Media de TR por pé)."""
    fig = Figure(figsize=figsize)
    ax = fig.add_subplot(111)
    ax.bar(categorias, valores, color=cores)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.spines[["top", "right"]].set_visible(False)
    _rotacionar_rotulos_se_necessario(ax, categorias)
    fundo_transparente(fig, ax)
    return fig


def barras_agrupadas(
    categorias: list[str],
    series: dict[str, list[float | None]],
    cores: dict[str, str],
    *,
    figsize: tuple[float, float] = (6.0, 4.0),
    ylabel: str | None = None,
) -> Figure:
    """Barras verticais agrupadas por categoria (ex.: Acertos por decisão, por posição).

    `None` em `series` vira barra ausente (altura 0), sem travar o gráfico — usado
    para posições sem atleta no grupo (ver docs/context/07-pontos-em-aberto.md item 9).
    Um valor real igual a 0 (ex.: atleta com 0 acertos) também vira barra de altura
    0 — visualmente idêntica a `None` sem uma marca extra, então ganha uma bolinha
    na base para diferenciar "tem dado, e é zero" de "não tem atleta nessa categoria".
    """
    fig = Figure(figsize=figsize)
    ax = fig.add_subplot(111)

    n_series = len(series)
    largura = 0.8 / max(n_series, 1)
    posicoes_base = range(len(categorias))

    for i, (nome_serie, valores) in enumerate(series.items()):
        offset = (i - (n_series - 1) / 2) * largura
        posicoes = [p + offset for p in posicoes_base]
        alturas = [0 if v is None else v for v in valores]
        ax.bar(posicoes, alturas, width=largura, label=nome_serie, color=cores[nome_serie])

        posicoes_zero = [p for p, v in zip(posicoes, valores) if v == 0]
        if posicoes_zero:
            ax.plot(
                posicoes_zero, [0] * len(posicoes_zero),
                marker="o", markersize=6, color=cores[nome_serie], linestyle="none",
            )

    ax.set_xticks(list(posicoes_base))
    ax.set_xticklabels(categorias)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    _rotacionar_rotulos_se_necessario(ax, categorias)
    fundo_transparente(fig, ax)
    return fig


def barras_posicao_atleta(
    categorias: list[str],
    medias_por_posicao: dict[str, float | None],
    valor_atleta: float,
    posicao_atleta: str,
    nome_atleta: str,
    *,
    cor_media: str,
    cor_atleta: str,
    figsize: tuple[float, float] = (9.0, 3.6),
    ylabel: str | None = None,
) -> Figure:
    """"Acertos por posição": média da posição (cinza) em todas as categorias com
    dado; o valor do próprio atleta (verde) só aparece na posição dele, ao lado da
    média daquela posição.

    A média já inclui o próprio atleta (ver `domain.metrics.acertos_por_posicao`),
    então na posição dele a barra cinza sempre existe — o `None` só sobra para
    posição sem nenhum atleta no grupo, que não desenha barra nenhuma, e para o
    caso de a posição do atleta não estar entre as `categorias` fixas. Um valor
    real igual a 0 ganha uma bolinha na base (mesmo critério de
    `barras_agrupadas`), para não parecer "sem dado".
    """
    fig = Figure(figsize=figsize)
    ax = fig.add_subplot(111)
    largura_par = 0.32
    largura_solo = largura_par * 1.7
    posicao_atleta_normalizada = posicao_atleta.strip().casefold()

    def _marcar_zero_se_necessario(x: float, valor: float | None, cor: str) -> None:
        if valor == 0:
            ax.plot([x], [0], marker="o", markersize=6, color=cor, linestyle="none")

    for i, categoria in enumerate(categorias):
        media = medias_por_posicao.get(categoria)
        # Comparação case-insensitive: o CSV real usa "Meio campista", já as 6
        # categorias fixas usam "Meio Campista" (mesma cautela de domain/metrics.py).
        if categoria.strip().casefold() == posicao_atleta_normalizada:
            if media is not None:
                x_media = i - largura_par / 2
                ax.bar(x_media, media, width=largura_par, color=cor_media)
                _marcar_zero_se_necessario(x_media, media, cor_media)
            x_atleta = i + largura_par / 2
            ax.bar(x_atleta, valor_atleta, width=largura_par, color=cor_atleta)
            _marcar_zero_se_necessario(x_atleta, valor_atleta, cor_atleta)
        elif media is not None:
            ax.bar(i, media, width=largura_solo, color=cor_media)
            _marcar_zero_se_necessario(i, media, cor_media)

    ax.set_xticks(list(range(len(categorias))))
    ax.set_xticklabels(categorias)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.legend(
        handles=[
            Patch(color=cor_media, label="Media da posição"),
            Patch(color=cor_atleta, label=nome_atleta),
        ]
    )
    ax.spines[["top", "right"]].set_visible(False)
    _rotacionar_rotulos_se_necessario(ax, categorias)
    fundo_transparente(fig, ax)
    return fig


def barras_empilhadas_horizontais(
    categorias: list[str],
    segmentos: dict[str, list[float]],
    cores: dict[str, str],
    *,
    figsize: tuple[float, float] = (6.0, 3.0),
) -> Figure:
    """Barras horizontais empilhadas (ex.: Classificação do TR por acerto e erro).

    A ordem de `segmentos` (dict preserva ordem de inserção) define a ordem
    esquerda->direita de cada segmento na pilha — segmentos com valor 0 não
    ocupam espaço visual, então a ordem escolhida pelo chamador é o que importa
    para bater com a imagem de referência.
    """
    fig = Figure(figsize=figsize)
    ax = fig.add_subplot(111)
    posicoes_y = list(range(len(categorias)))
    acumulado = [0.0] * len(categorias)

    for nome_segmento, valores in segmentos.items():
        barras = ax.barh(
            posicoes_y, valores, left=acumulado, color=cores[nome_segmento], label=nome_segmento
        )
        for barra, valor in zip(barras, valores):
            if valor:
                ax.text(
                    barra.get_x() + barra.get_width() / 2,
                    barra.get_y() + barra.get_height() / 2,
                    str(int(valor)),
                    ha="center",
                    va="center",
                )
        acumulado = [a + v for a, v in zip(acumulado, valores)]

    ax.set_yticks(posicoes_y)
    ax.set_yticklabels(categorias)
    ax.invert_yaxis()
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    fundo_transparente(fig, ax)
    return fig
