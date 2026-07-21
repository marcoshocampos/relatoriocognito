from pathlib import Path

import pytest

from relatoriocognito.io.csv_importer import CsvImportError, carregar_csv

FIXTURE_REAL = Path(__file__).parent.parent / "fixtures" / "sample_csvs" / "Geral_10_3_2025.csv"

CABECALHO = (
    "Treino,Jogador,PeEsperado,PeUsado,TempoReacao,ClassificacaoTR,Correto,"
    "RespostaCorreta,RespostaDada,Data,Hora"
)


def _escrever_csv(tmp_path: Path, linhas: list[str], encoding: str = "utf-8", nome: str = "atleta.csv") -> Path:
    caminho = tmp_path / nome
    conteudo = "\r\n".join([CABECALHO, *linhas]) + "\r\n"
    caminho.write_bytes(conteudo.encode(encoding))
    return caminho


def _linha(
    treino="Treino1",
    jogador="Caio - Canhoto - Meio campista",
    pe_esperado="Esquerdo",
    pe_usado="Esquerdo",
    tempo_reacao="13.31",
    classificacao_tr="Precoce",
    correto="Errou",
    resposta_correta="Chutar ao Gol",
    resposta_dada="Manter Posse",
    data="10/03/2025",
    hora="09:30",
) -> str:
    return ",".join(
        [
            treino,
            jogador,
            pe_esperado,
            pe_usado,
            tempo_reacao,
            classificacao_tr,
            correto,
            resposta_correta,
            resposta_dada,
            data,
            hora,
        ]
    )


def test_carrega_fixture_real():
    atleta = carregar_csv(FIXTURE_REAL)
    assert atleta.nome == "Caio"
    assert atleta.lateralidade == "Canhoto"
    assert atleta.posicao == "Meio campista"
    assert len(atleta.trials) == 15
    assert all(t.correto == "Errou" for t in atleta.trials)
    assert atleta.trials[0].tempo_reacao == 13.31
    assert atleta.trials[1].tempo_reacao == 16.0  # "16" sem casas decimais


def test_fallback_de_encoding_latin1(tmp_path):
    # "José" só é válido em UTF-8 se o arquivo inteiro for UTF-8; gravamos como
    # latin-1 (não é UTF-8 válido para o é) para forçar o fallback de decodificação.
    caminho = _escrever_csv(
        tmp_path,
        [_linha(jogador="José - Destro - Zagueiro")],
        encoding="latin-1",
    )
    atleta = carregar_csv(caminho)
    assert atleta.nome == "José"
    assert atleta.posicao == "Zagueiro"


def test_normaliza_colunas_case_insensitive(tmp_path):
    cabecalho_minusculo = (
        "treino,jogador,peesperado,peusado,temporeacao,classificacaotr,correto,"
        "respostacorreta,respostadada,data,hora"
    )
    conteudo = cabecalho_minusculo + "\r\n" + _linha() + "\r\n"
    caminho = tmp_path / "atleta.csv"
    caminho.write_bytes(conteudo.encode("utf-8"))
    atleta = carregar_csv(caminho)
    assert atleta.nome == "Caio"
    assert len(atleta.trials) == 1


def test_descarta_linha_vazia_final(tmp_path):
    caminho = _escrever_csv(tmp_path, [_linha(), ""])
    atleta = carregar_csv(caminho)
    assert len(atleta.trials) == 1


def test_coluna_obrigatoria_faltando_gera_erro_claro(tmp_path):
    cabecalho_sem_hora = (
        "Treino,Jogador,PeEsperado,PeUsado,TempoReacao,ClassificacaoTR,Correto,"
        "RespostaCorreta,RespostaDada,Data"
    )
    conteudo = cabecalho_sem_hora + "\r\n" + "Treino1,Caio - Canhoto - Meio campista,Esquerdo,Esquerdo,13.31,Precoce,Errou,Chutar ao Gol,Manter Posse,10/03/2025\r\n"
    caminho = tmp_path / "atleta.csv"
    caminho.write_bytes(conteudo.encode("utf-8"))
    with pytest.raises(CsvImportError, match="Hora"):
        carregar_csv(caminho)


def test_mais_de_um_atleta_no_mesmo_csv_gera_erro(tmp_path):
    caminho = _escrever_csv(
        tmp_path,
        [
            _linha(jogador="Caio - Canhoto - Meio campista"),
            _linha(jogador="Bruno - Destro - Atacante"),
        ],
    )
    with pytest.raises(CsvImportError, match="mais de um atleta"):
        carregar_csv(caminho)


def test_campo_jogador_mal_formado_gera_erro(tmp_path):
    caminho = _escrever_csv(tmp_path, [_linha(jogador="SoNome")])
    with pytest.raises(CsvImportError, match="Jogador"):
        carregar_csv(caminho)


def test_arquivo_inexistente_gera_erro_claro(tmp_path):
    with pytest.raises(CsvImportError, match="não encontrado"):
        carregar_csv(tmp_path / "nao_existe.csv")


def test_arquivo_vazio_gera_erro_claro(tmp_path):
    caminho = tmp_path / "vazio.csv"
    caminho.write_bytes(b"")
    with pytest.raises(CsvImportError):
        carregar_csv(caminho)
