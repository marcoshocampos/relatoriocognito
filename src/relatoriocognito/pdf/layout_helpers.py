from __future__ import annotations

import io
import math
from datetime import date
from pathlib import Path

from matplotlib.figure import Figure
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

from relatoriocognito.charts.colors import Paleta
from relatoriocognito.charts.decorativos import icone_avatar
from relatoriocognito.charts.util import figura_para_png
from relatoriocognito.domain.models import Athlete

# Fallbacks estáticos — usados só por quem chamar `cartao()` sem passar `cor`
# explicitamente. Todo `pdf/layout_*.py` novo deve passar `HexColor(paleta.fundo_cartao)`
# / `HexColor(paleta.fundo_cartao_destaque)` em vez de depender destas constantes,
# para que o fundo responda à cor escolhida pelo usuário — ver docs/context/06-decisoes.md.
COR_CARTAO = HexColor("#E4E4E4")
COR_CARTAO_LAVANDA = HexColor("#CDDBFF")
COR_TEXTO = HexColor("#1A1A1A")
COR_SELO_VERDE = HexColor("#2E7D32")
COR_RODAPE = HexColor("#8C8C8C")

MARGEM = 24
GAP = 16
ALTURA_CABECALHO = 56


def cartao(
    c: Canvas,
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    cor: HexColor = COR_CARTAO,
    raio: float = 10,
) -> None:
    c.saveState()
    c.setFillColor(cor)
    c.roundRect(x, y, w, h, raio, stroke=0, fill=1)
    c.restoreState()


def titulo_cartao(c: Canvas, texto: str, x_centro: float, y: float, *, tamanho: float = 12) -> None:
    c.saveState()
    c.setFillColor(COR_TEXTO)
    c.setFont("Helvetica-Bold", tamanho)
    c.drawCentredString(x_centro, y, texto)
    c.restoreState()


def desenhar_figura(c: Canvas, fig: Figure, x: float, y: float, w: float, h: float) -> None:
    png_bytes = figura_para_png(fig)
    imagem = ImageReader(io.BytesIO(png_bytes))
    c.drawImage(imagem, x, y, width=w, height=h, preserveAspectRatio=True, anchor="c", mask="auto")


def distribuir_colunas(
    x_inicial: float, largura_total: float, pesos: list[float], *, gap: float = GAP
) -> list[tuple[float, float]]:
    """Divide uma faixa horizontal em colunas proporcionais a `pesos`.

    Retorna [(x, largura), ...] — a altura de cada cartão fica a critério de
    quem chama, já que varia por página (ver layout_grupo.py para um caso onde
    uma coluna ocupa a altura combinada de duas linhas).
    """
    n = len(pesos)
    largura_util = largura_total - gap * (n - 1)
    soma_pesos = sum(pesos)
    resultado = []
    cursor = x_inicial
    for peso in pesos:
        largura = largura_util * peso / soma_pesos
        resultado.append((cursor, largura))
        cursor += largura + gap
    return resultado


def selo_cognito(c: Canvas, x_direita: float, y_topo: float, *, tamanho: float = 44) -> None:
    """Selo hexagonal placeholder (formas vetoriais simples) — o arquivo oficial do
    selo "Cognito" ainda não foi enviado, ver docs/context/07-pontos-em-aberto.md
    item 12. Trocar por `c.drawImage(...)` do asset real quando disponível.
    """
    c.saveState()
    raio = tamanho / 2
    cx = x_direita - raio
    cy = y_topo - raio
    pontos = [
        (cx + raio * math.cos(math.pi / 2 + i * math.pi / 3), cy + raio * math.sin(math.pi / 2 + i * math.pi / 3))
        for i in range(6)
    ]
    caminho = c.beginPath()
    caminho.moveTo(*pontos[0])
    for px, py in pontos[1:]:
        caminho.lineTo(px, py)
    caminho.close()
    c.setFillColor(HexColor("#FFFFFF"))
    c.setStrokeColor(COR_SELO_VERDE)
    c.setLineWidth(1.5)
    c.drawPath(caminho, fill=1, stroke=1)
    c.setFillColor(COR_SELO_VERDE)
    c.setFont("Helvetica-Bold", tamanho * 0.24)
    c.drawCentredString(cx, cy - tamanho * 0.08, "Cognito")
    c.restoreState()


def cabecalho(
    c: Canvas,
    *,
    largura_pagina: float,
    altura_pagina: float,
    nome_grupo: str,
    titulo_pagina: str,
    data: str,
    caminho_logo: str | Path | None,
    atleta: Athlete | None = None,
    paleta: Paleta = Paleta(),
) -> float:
    """Desenha o cabeçalho comum às 4 páginas. Retorna o Y logo abaixo dele
    (topo disponível para o conteúdo da página)."""
    x = MARGEM
    w = largura_pagina - 2 * MARGEM
    y_topo = altura_pagina - MARGEM
    y_cartao = y_topo - ALTURA_CABECALHO
    meio_vertical = y_cartao + ALTURA_CABECALHO / 2

    cartao(c, x, y_cartao, w, ALTURA_CABECALHO, cor=HexColor(paleta.fundo_cartao))

    if caminho_logo:
        c.drawImage(
            str(caminho_logo),
            x + 14,
            y_cartao + 10,
            width=36,
            height=36,
            preserveAspectRatio=True,
            anchor="c",
            mask="auto",
        )

    c.saveState()
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(COR_TEXTO)
    c.drawString(x + 60, meio_vertical - 5, nome_grupo.upper())
    c.restoreState()

    c.saveState()
    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(COR_TEXTO)
    c.drawCentredString(largura_pagina / 2, meio_vertical - 5, f"{titulo_pagina} – {data}")
    c.restoreState()

    if atleta is not None:
        x_direita_texto = x + w - 56
        c.saveState()
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(COR_TEXTO)
        c.drawRightString(x_direita_texto, meio_vertical + 6, atleta.nome)
        c.setFont("Helvetica", 9)
        c.drawRightString(x_direita_texto, meio_vertical - 10, f"{atleta.lateralidade}   {atleta.posicao}")
        c.restoreState()
        desenhar_figura(c, icone_avatar(), x + w - 46, y_cartao + 6, 40, 40)

    selo_cognito(c, largura_pagina - 4, altura_pagina - 4)

    return y_cartao - GAP


def rodape(c: Canvas, *, largura_pagina: float, data_emissao: str | None = None) -> None:
    """Rodapé fixo nas 4 páginas com a data de emissão do PDF (hoje) — diferente
    da data que aparece no cabeçalho, que é a data da sessão registrada no CSV.

    `data_emissao=None` calcula a data de hoje aqui mesmo — usado quando uma
    página é desenhada isoladamente (teste manual, por exemplo). `pdf/report.py`
    sempre passa um valor explícito, calculado uma única vez, para garantir que
    as várias páginas do mesmo PDF tragam a mesma data mesmo se a geração
    atravessar a virada da meia-noite.

    Desenhado bem próximo à borda inferior da página (y=12): a página com menos
    espaço livre (Comparação atleta grupo) ainda deixa ~33pt entre o fim do
    último cartão e a borda, então não precisou reduzir nenhum cartão para abrir
    espaço — ver docs/context/06-decisoes.md.
    """
    if data_emissao is None:
        data_emissao = date.today().strftime("%d/%m/%Y")
    c.saveState()
    c.setFont("Helvetica", 8)
    c.setFillColor(COR_RODAPE)
    c.drawCentredString(largura_pagina / 2, 12, f"Relatório emitido em {data_emissao}")
    c.restoreState()
