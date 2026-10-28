import zipfile

import pytest

from relatoriocognito.domain.models import Athlete, Group, Trial
from relatoriocognito.pdf import report


def _trial(**overrides) -> Trial:
    dados = dict(
        treino="Treino",
        pe_esperado="Esquerdo",
        pe_usado="Esquerdo",
        tempo_reacao=2.0,
        classificacao_tr="Ideal",
        correto="Acertou",
        resposta_correta="Chutar ao Gol",
        resposta_dada="Chutar ao Gol",
        data="10/03/2025",
        hora="09:30",
    )
    dados.update(overrides)
    return Trial(**dados)


def _atleta(nome: str, posicao: str = "Zagueiro") -> Athlete:
    return Athlete(nome=nome, lateralidade="Destro", posicao=posicao, trials=[_trial()] * 3)


# --- Nome do arquivo dentro do ZIP -----------------------------------------


def test_nome_do_arquivo_usa_o_nome_do_atleta():
    assert report._nome_unico_no_zip("Ana", {}) == "relatorio_Ana.pdf"


def test_nome_do_arquivo_troca_caracteres_invalidos_no_windows():
    # O nome vem do campo `Jogador` do CSV, que é texto livre.
    nome = report._nome_unico_no_zip('Ana/Maria:Silva', {})
    assert nome == "relatorio_Ana-Maria-Silva.pdf"
    assert not any(c in nome for c in '<>:"/\\|?*')


def test_nome_do_arquivo_com_nome_vazio_nao_gera_arquivo_sem_nome():
    assert report._nome_unico_no_zip("   ", {}) == "relatorio_atleta.pdf"


def test_nomes_repetidos_ganham_sufixo_para_nao_se_sobrescrever():
    usados: dict[str, int] = {}
    assert report._nome_unico_no_zip("Ana", usados) == "relatorio_Ana.pdf"
    assert report._nome_unico_no_zip("Ana", usados) == "relatorio_Ana_2.pdf"
    assert report._nome_unico_no_zip("Ana", usados) == "relatorio_Ana_3.pdf"


def test_nomes_repetidos_ignoram_diferenca_de_maiuscula():
    # Windows não diferencia maiúscula em nome de arquivo: "ANA" e "Ana" no mesmo
    # ZIP viram conflito ao extrair.
    usados: dict[str, int] = {}
    report._nome_unico_no_zip("Ana", usados)
    assert report._nome_unico_no_zip("ANA", usados) == "relatorio_ANA_2.pdf"


# --- Geração do lote --------------------------------------------------------


def test_zip_tem_um_pdf_de_4_paginas_por_atleta(tmp_path):
    grupo = Group(nome="Time", athletes=[_atleta("Ana"), _atleta("Miguel", "Atacante")])
    destino = tmp_path / "relatorios.zip"

    nomes = report.gerar_relatorios_zip(grupo, None, destino)

    assert nomes == ["relatorio_Ana.pdf", "relatorio_Miguel.pdf"]
    with zipfile.ZipFile(destino) as arquivo_zip:
        assert arquivo_zip.namelist() == nomes
        for nome in nomes:
            conteudo = arquivo_zip.read(nome)
            assert conteudo.startswith(b"%PDF")
            # 4 páginas: a de grupo + as 3 do atleta.
            assert conteudo.count(b"/Type /Page\n") == 4


def test_progresso_e_reportado_para_cada_atleta(tmp_path):
    grupo = Group(nome="Time", athletes=[_atleta("Ana"), _atleta("Miguel")])
    eventos = []

    report.gerar_relatorios_zip(
        grupo, None, tmp_path / "r.zip", progresso=lambda *args: eventos.append(args)
    )

    assert eventos == [(1, 2, "Ana"), (2, 2, "Miguel")]


def test_grupo_sem_atleta_nao_gera_zip_vazio_em_silencio(tmp_path):
    with pytest.raises(ValueError):
        report.gerar_relatorios_zip(Group(nome="Time", athletes=[]), None, tmp_path / "r.zip")


def test_pdf_do_atleta_tem_as_quatro_paginas():
    grupo = Group(nome="Time", athletes=[_atleta("Ana")])
    conteudo = report.gerar_pdf_do_atleta(grupo, grupo.athletes[0], None)
    assert conteudo.startswith(b"%PDF")
    assert conteudo.count(b"/Type /Page\n") == 4
