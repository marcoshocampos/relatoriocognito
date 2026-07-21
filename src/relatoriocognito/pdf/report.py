from __future__ import annotations

import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen.canvas import Canvas

from relatoriocognito.domain.models import Group
from relatoriocognito.pdf import layout_acoes_pe, layout_comparacao_grupo, layout_grupo, layout_individual

TAMANHO_PAGINA = landscape(A4)


def gerar_relatorio_pdf(
    group: Group,
    caminho_logo: str | Path | None,
    caminho_saida: str | Path,
) -> None:
    """Monta o PDF completo: 1 página de grupo + 3 páginas por atleta do grupo."""
    if not group.athletes:
        raise ValueError("O grupo precisa de pelo menos um atleta para gerar o relatório.")

    largura_pagina, altura_pagina = TAMANHO_PAGINA
    c = Canvas(str(caminho_saida), pagesize=TAMANHO_PAGINA)
    data = _data_do_relatorio(group)

    layout_grupo.desenhar(
        c, group, caminho_logo, data, largura_pagina=largura_pagina, altura_pagina=altura_pagina
    )
    c.showPage()

    for atleta in group.athletes:
        layout_individual.desenhar(
            c, group, atleta, caminho_logo, data, largura_pagina=largura_pagina, altura_pagina=altura_pagina
        )
        c.showPage()
        layout_acoes_pe.desenhar(
            c, group, atleta, caminho_logo, data, largura_pagina=largura_pagina, altura_pagina=altura_pagina
        )
        c.showPage()
        layout_comparacao_grupo.desenhar(
            c, group, atleta, caminho_logo, data, largura_pagina=largura_pagina, altura_pagina=altura_pagina
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
