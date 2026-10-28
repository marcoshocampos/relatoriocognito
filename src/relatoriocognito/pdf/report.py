from __future__ import annotations

import datetime
import io
import zipfile
from collections.abc import Callable
from pathlib import Path

from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen.canvas import Canvas

from relatoriocognito.charts.colors import Paleta
from relatoriocognito.domain.models import Athlete, Group
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

# Caracteres que o Windows não aceita em nome de arquivo. O nome do atleta vem do
# campo `Jogador` do CSV, que é texto livre — não dá para confiar que seja
# sempre um primeiro nome limpo.
_CARACTERES_INVALIDOS = '<>:"/\\|?*'


def gerar_relatorios_zip(
    group: Group,
    caminho_logo: str | Path | None,
    caminho_zip: str | Path,
    *,
    paleta: Paleta = Paleta(),
    progresso: Callable[[int, int, str], None] | None = None,
) -> list[str]:
    """Gera **um PDF por atleta** e junta todos num ZIP. Retorna os nomes dentro do ZIP.

    Cada PDF tem 4 páginas: a página de grupo ("Dashboard Overview", igual em
    todos) + as 3 páginas daquele atleta. As métricas de grupo e de posição
    continuam calculadas sobre o grupo inteiro carregado na sessão — o que muda é
    só o empacotamento, para o cliente poder entregar a cada jogador só o
    relatório dele.

    `progresso(indice, total, nome_do_atleta)` é chamado antes de cada PDF. Como
    isso costuma rodar numa thread de trabalho (ver `gui/tela_gerar.py`), a
    função passada **não pode mexer em widget** — deve só guardar o estado.
    """
    if not group.athletes:
        raise ValueError("O grupo precisa de pelo menos um atleta para gerar o relatório.")

    data = _data_do_relatorio(group)
    # Calculada uma única vez para todos os PDFs: mesmo que a geração atravesse a
    # virada da meia-noite, todo o lote mostra a mesma data de emissão.
    data_emissao = datetime.date.today().strftime("%d/%m/%Y")

    nomes_gerados: list[str] = []
    usados: dict[str, int] = {}
    total = len(group.athletes)

    with zipfile.ZipFile(caminho_zip, "w", zipfile.ZIP_DEFLATED) as arquivo_zip:
        for indice, atleta in enumerate(group.athletes, start=1):
            if progresso is not None:
                progresso(indice, total, atleta.nome)

            nome_arquivo = _nome_unico_no_zip(atleta.nome, usados)
            conteudo = gerar_pdf_do_atleta(
                group, atleta, caminho_logo, paleta=paleta, data=data, data_emissao=data_emissao
            )
            arquivo_zip.writestr(nome_arquivo, conteudo)
            nomes_gerados.append(nome_arquivo)

    return nomes_gerados


def gerar_pdf_do_atleta(
    group: Group,
    atleta: Athlete,
    caminho_logo: str | Path | None,
    *,
    paleta: Paleta = Paleta(),
    data: str | None = None,
    data_emissao: str | None = None,
) -> bytes:
    """As 4 páginas de um atleta, em memória (sem passar por arquivo temporário).

    `data`/`data_emissao` vêm de fora quando o lote inteiro precisa das mesmas
    datas; sozinhos, são derivados aqui (útil para gerar um relatório avulso).
    """
    if data is None:
        data = _data_do_relatorio(group)
    if data_emissao is None:
        data_emissao = datetime.date.today().strftime("%d/%m/%Y")

    largura_pagina, altura_pagina = TAMANHO_PAGINA
    buffer = io.BytesIO()
    c = Canvas(buffer, pagesize=TAMANHO_PAGINA)

    for desenhar_pagina in (
        _pagina_grupo,
        layout_individual.desenhar,
        layout_acoes_pe.desenhar,
        layout_comparacao_grupo.desenhar,
    ):
        desenhar_pagina(
            c, group, atleta, caminho_logo, data,
            largura_pagina=largura_pagina, altura_pagina=altura_pagina,
            paleta=paleta, data_emissao=data_emissao,
        )
        c.showPage()

    c.save()
    return buffer.getvalue()


def _pagina_grupo(c: Canvas, group: Group, atleta: Athlete, *args, **kwargs) -> None:
    """Adapta a página de grupo à mesma assinatura das páginas de atleta, para
    todas caberem na mesma sequência acima. Ela não usa `atleta` — é idêntica em
    todos os PDFs do lote."""
    layout_grupo.desenhar(c, group, *args, **kwargs)


def _nome_unico_no_zip(nome_atleta: str, usados: dict[str, int]) -> str:
    """`relatorio_<atleta>.pdf`, com sufixo numérico se dois atletas do grupo
    tiverem o mesmo nome (senão um sobrescreveria o outro dentro do ZIP)."""
    base = "".join("-" if caractere in _CARACTERES_INVALIDOS else caractere for caractere in nome_atleta)
    base = base.strip().strip(".") or "atleta"

    chave = base.casefold()
    usados[chave] = usados.get(chave, 0) + 1
    ocorrencia = usados[chave]
    sufixo = "" if ocorrencia == 1 else f"_{ocorrencia}"
    return f"relatorio_{base}{sufixo}.pdf"


def _data_do_relatorio(group: Group) -> str:
    """Usa a Data (do CSV) da primeira tentativa encontrada — não a data de hoje,
    que pode ser bem posterior à sessão de teste em si. Cai para hoje só se, por
    algum motivo, nenhuma tentativa tiver Data preenchida."""
    for atleta in group.athletes:
        for trial in atleta.trials:
            if trial.data:
                return trial.data
    return datetime.date.today().strftime("%d/%m/%Y")
