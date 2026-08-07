from __future__ import annotations

import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen.canvas import Canvas

from relatoriocognito.charts.colors import Paleta
from relatoriocognito.domain.models import Group
from relatoriocognito.pdf import layout_acoes_pe, layout_comparacao_grupo, layout_grupo, layout_individual

# Página 16:9, mantendo a altura da A4 paisagem e alargando a largura
# (841.89 -> 1058.27pt). O relatório é um painel para ver na tela, não um
# documento para imprimir, e a proporção 16:9 é a mesma do modelo Canva de
# referência. Manter a altura preserva todo o ajuste vertical dos cartões, e a
# largura extra vai direto para os gráficos, que se dividem por
# `distribuir_colunas` (proporcional à largura da página). Ver
# docs/context/06-decisoes.md.
_ALTURA_A4_PAISAGEM = landscape(A4)[1]
TAMANHO_PAGINA = (_ALTURA_A4_PAISAGEM * 16 / 9, _ALTURA_A4_PAISAGEM)


def gerar_relatorio_pdf(
    group: Group,
    caminho_logo: str | Path | None,
    caminho_saida: str | Path,
    *,
    paleta: Paleta = Paleta(),
) -> None:
    """Monta o PDF completo: 1 página de grupo + 3 páginas por atleta do grupo.

    `paleta` carrega a cor base escolhida pelo time na GUI (tela 1) — sem
    escolha nenhuma, usa o verde do modelo Canva original (ver
    `charts.colors.Paleta`).
    """
    if not group.athletes:
        raise ValueError("O grupo precisa de pelo menos um atleta para gerar o relatório.")

    largura_pagina, altura_pagina = TAMANHO_PAGINA
    c = Canvas(str(caminho_saida), pagesize=TAMANHO_PAGINA)
    data = _data_do_relatorio(group)
    # Calculada uma única vez para todas as páginas: mesmo que a geração do PDF
    # atravesse a virada da meia-noite, todo o relatório mostra a mesma data de
    # emissão no rodapé.
    data_emissao = datetime.date.today().strftime("%d/%m/%Y")

    layout_grupo.desenhar(
        c, group, caminho_logo, data,
        largura_pagina=largura_pagina, altura_pagina=altura_pagina,
        paleta=paleta, data_emissao=data_emissao,
    )
    c.showPage()

    for atleta in group.athletes:
        layout_individual.desenhar(
            c, group, atleta, caminho_logo, data,
            largura_pagina=largura_pagina, altura_pagina=altura_pagina,
            paleta=paleta, data_emissao=data_emissao,
        )
        c.showPage()
        layout_acoes_pe.desenhar(
            c, group, atleta, caminho_logo, data,
            largura_pagina=largura_pagina, altura_pagina=altura_pagina,
            paleta=paleta, data_emissao=data_emissao,
        )
        c.showPage()
        layout_comparacao_grupo.desenhar(
            c, group, atleta, caminho_logo, data,
            largura_pagina=largura_pagina, altura_pagina=altura_pagina,
            paleta=paleta, data_emissao=data_emissao,
        )
        c.showPage()

    c.save()


def _data_do_relatorio(group: Group) -> str:
    """Usa a Data (do CSV) da primeira tentativa encontrada — não a data de hoje,
    que pode ser bem posterior à sessão de teste em si. Cai para hoje só se, por
    algum motivo, nenhuma tentativa tiver Data preenchida."""
    for atleta in group.athletes:
        for trial in atleta.trials:
            if trial.data:
                return trial.data
    return datetime.date.today().strftime("%d/%m/%Y")
