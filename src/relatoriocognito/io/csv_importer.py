from __future__ import annotations

from pathlib import Path

import pandas as pd

from relatoriocognito.domain.models import Athlete, Trial

COLUNAS_ESPERADAS = (
    "Treino",
    "Jogador",
    "PeEsperado",
    "PeUsado",
    "TempoReacao",
    "ClassificacaoTR",
    "Correto",
    "RespostaCorreta",
    "RespostaDada",
    "Data",
    "Hora",
)

_ENCODINGS = ("utf-8", "cp1252", "latin-1")


class CsvImportError(Exception):
    """Erro ao importar um CSV de atleta — mensagem já pronta para mostrar na GUI."""


def carregar_csv(caminho: Path | str) -> Athlete:
    """Lê um CSV de atleta e retorna um `Athlete` com seus trials.

    `ClassificacaoTR` e `Correto` são passados adiante sem recálculo — ver
    docs/context/02-modelo-dados.md.
    """
    caminho = Path(caminho)
    if not caminho.exists():
        raise CsvImportError(f"Arquivo não encontrado: {caminho}")

    try:
        df = _ler_csv_com_fallback_de_encoding(caminho)
    except pd.errors.EmptyDataError as erro:
        raise CsvImportError(f"O arquivo '{caminho.name}' está vazio.") from erro
    except pd.errors.ParserError as erro:
        raise CsvImportError(
            f"Não foi possível interpretar '{caminho.name}' como CSV: {erro}"
        ) from erro
    except OSError as erro:
        raise CsvImportError(f"Não foi possível abrir '{caminho.name}': {erro}") from erro

    df = _normalizar_colunas(df, caminho)
    df = df.dropna(how="all")

    linhas_validas = [row for _, row in df.iterrows() if _linha_valida(row)]
    if not linhas_validas:
        raise CsvImportError(f"O arquivo '{caminho.name}' não tem nenhuma tentativa válida.")

    jogadores_distintos = {str(row["Jogador"]).strip() for row in linhas_validas}
    if len(jogadores_distintos) > 1:
        raise CsvImportError(
            f"O arquivo '{caminho.name}' parece conter mais de um atleta "
            f"(coluna Jogador varia entre as linhas: {', '.join(sorted(jogadores_distintos))})."
        )

    nome, lateralidade, posicao = _parse_jogador(
        str(linhas_validas[0]["Jogador"]).strip(), caminho
    )
    trials = [_linha_para_trial(row) for row in linhas_validas]
    return Athlete(nome=nome, lateralidade=lateralidade, posicao=posicao, trials=trials)


def _ler_csv_com_fallback_de_encoding(caminho: Path) -> pd.DataFrame:
    ultimo_erro: UnicodeDecodeError | None = None
    for encoding in _ENCODINGS:
        try:
            return pd.read_csv(caminho, encoding=encoding, dtype=str)
        except UnicodeDecodeError as erro:
            ultimo_erro = erro
            continue
    raise CsvImportError(
        f"Não foi possível decodificar '{caminho.name}' (tentou {', '.join(_ENCODINGS)})."
    ) from ultimo_erro


def _normalizar_colunas(df: pd.DataFrame, caminho: Path) -> pd.DataFrame:
    mapa_por_chave = {coluna.casefold(): coluna for coluna in COLUNAS_ESPERADAS}
    renomear = {}
    for coluna_original in df.columns:
        chave = coluna_original.strip().casefold()
        if chave in mapa_por_chave:
            renomear[coluna_original] = mapa_por_chave[chave]
    df = df.rename(columns=renomear)

    faltando = [c for c in COLUNAS_ESPERADAS if c not in df.columns]
    if faltando:
        raise CsvImportError(
            f"O arquivo '{caminho.name}' está sem a(s) coluna(s) obrigatória(s): "
            f"{', '.join(faltando)}."
        )
    return df


def _parse_tempo_reacao(valor: str) -> float:
    """Aceita `.` ou `,` como separador decimal — CSVs reexportados/editados no
    Excel com localidade PT-BR trocam o ponto por vírgula (ex.: `"13,31"`), o que
    quebra `float()` direto."""
    texto = valor.strip()
    try:
        return float(texto)
    except ValueError:
        return float(texto.replace(",", "."))


def _linha_valida(row: pd.Series) -> bool:
    jogador = row.get("Jogador")
    if pd.isna(jogador) or not str(jogador).strip():
        return False
    tempo_reacao = row.get("TempoReacao")
    if pd.isna(tempo_reacao):
        return False
    try:
        _parse_tempo_reacao(str(tempo_reacao))
    except ValueError:
        return False
    return True


def _parse_jogador(valor: str, caminho: Path) -> tuple[str, str, str]:
    partes = [p.strip() for p in valor.split(" - ")]
    if len(partes) != 3 or not all(partes):
        raise CsvImportError(
            f"O campo Jogador '{valor}' em '{caminho.name}' não está no formato "
            f"esperado 'Nome - Lateralidade - Posição'."
        )
    nome, lateralidade, posicao = partes
    return nome, lateralidade, posicao


def _campo(row: pd.Series, coluna: str) -> str:
    valor = row[coluna]
    return "" if pd.isna(valor) else str(valor).strip()


def _linha_para_trial(row: pd.Series) -> Trial:
    return Trial(
        treino=_campo(row, "Treino"),
        pe_esperado=_campo(row, "PeEsperado"),
        pe_usado=_campo(row, "PeUsado"),
        tempo_reacao=_parse_tempo_reacao(_campo(row, "TempoReacao")),
        classificacao_tr=_campo(row, "ClassificacaoTR"),
        correto=_campo(row, "Correto"),
        resposta_correta=_campo(row, "RespostaCorreta"),
        resposta_dada=_campo(row, "RespostaDada"),
        data=_campo(row, "Data"),
        hora=_campo(row, "Hora"),
    )
