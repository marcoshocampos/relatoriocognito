from __future__ import annotations

from collections import Counter
from collections.abc import Sequence

from relatoriocognito.domain.models import Athlete, Trial

RESPOSTA_CATEGORIAS = ("Chutar ao Gol", "Manter Posse", "Passe a Esquerda", "Passe a Direita")
CLASSIFICACAO_TR_CATEGORIAS = ("Ideal", "Precoce", "Tardio", "Perda de bola")
PES = ("Esquerdo", "Direito")
POSICOES = (
    "Zagueiro",
    "Meio Campista",
    "Atacante",
    "Volante",
    "Lateral Direito",
    "Lateral Esquerdo",
)


# --- Métricas sobre uma lista de tentativas (atleta isolado ou grupo já achatado) ---


def contagem_acertos_erros(trials: Sequence[Trial]) -> dict[str, int]:
    contagem = Counter(t.correto for t in trials)
    return {"Acertou": contagem["Acertou"], "Errou": contagem["Errou"]}


def taxa_acerto(trials: Sequence[Trial]) -> float:
    if not trials:
        return 0.0
    acertos = contagem_acertos_erros(trials)["Acertou"]
    return 100 * acertos / len(trials)


def distribuicao_classificacao_tr(trials: Sequence[Trial]) -> dict[str, float]:
    total = len(trials)
    if total == 0:
        return {cat: 0.0 for cat in CLASSIFICACAO_TR_CATEGORIAS}
    contagem = Counter(t.classificacao_tr for t in trials)
    return {cat: 100 * contagem[cat] / total for cat in CLASSIFICACAO_TR_CATEGORIAS}


def media_tr(trials: Sequence[Trial]) -> float:
    if not trials:
        return 0.0
    return sum(t.tempo_reacao for t in trials) / len(trials)


def media_tr_por_resultado(trials: Sequence[Trial]) -> dict[str, float]:
    """TR médio condicionado a Correto=Acertou vs Errou.

    Leitura adotada para o par "2.5s/1.8s" do modelo de referência — ver
    docs/context/03-metricas.md e item 1 de docs/context/07-pontos-em-aberto.md.
    Isolada para facilitar ajuste caso a leitura precise mudar.
    """
    resultado: dict[str, float] = {}
    for chave in ("Acertou", "Errou"):
        subset = [t.tempo_reacao for t in trials if t.correto == chave]
        resultado[chave] = sum(subset) / len(subset) if subset else 0.0
    return resultado


def classificacao_tr_por_resultado(trials: Sequence[Trial]) -> dict[str, dict[str, int]]:
    """Cruzamento Correto x ClassificacaoTR, excluindo 'Perda de bola' (item 5)."""
    categorias = [c for c in CLASSIFICACAO_TR_CATEGORIAS if c != "Perda de bola"]
    contagens = {"Acertou": Counter(), "Errou": Counter()}
    for t in trials:
        if t.classificacao_tr == "Perda de bola":
            continue
        if t.correto in contagens:
            contagens[t.correto][t.classificacao_tr] += 1
    return {
        resultado_key: {cat: contagem[cat] for cat in categorias}
        for resultado_key, contagem in contagens.items()
    }


def acertos_por_decisao(athletes: Sequence[Athlete]) -> dict[str, tuple[float, float]]:
    """Por categoria de resposta: média por atleta de (RespostaCorreta, RespostaDada).

    Cada contagem é dividida pelo número de atletas do grupo (total/atletas, não
    percentual) — mesma convenção de docs/context/07-pontos-em-aberto.md item 14.
    """
    trials = trials_do_grupo(athletes)
    ideal = Counter(t.resposta_correta for t in trials)
    dado = Counter(t.resposta_dada for t in trials)
    n = len(athletes) or 1
    return {cat: (ideal[cat] / n, dado[cat] / n) for cat in RESPOSTA_CATEGORIAS}


def taxa_acerto_por_resposta(trials: Sequence[Trial]) -> dict[str, float]:
    """% de Correto=Acertou entre as tentativas cuja RespostaCorreta era cada categoria."""
    resultado: dict[str, float] = {}
    for cat in RESPOSTA_CATEGORIAS:
        subset = [t for t in trials if t.resposta_correta == cat]
        if not subset:
            resultado[cat] = 0.0
            continue
        acertos = sum(1 for t in subset if t.correto == "Acertou")
        resultado[cat] = 100 * acertos / len(subset)
    return resultado


def distribuicao_pe_usado(trials: Sequence[Trial]) -> dict[str, int]:
    contagem = Counter(t.pe_usado for t in trials)
    return {pe: contagem[pe] for pe in PES}


def media_tr_por_pe(trials: Sequence[Trial]) -> dict[str, float]:
    resultado: dict[str, float] = {}
    for pe in PES:
        subset = [t.tempo_reacao for t in trials if t.pe_usado == pe]
        resultado[pe] = sum(subset) / len(subset) if subset else 0.0
    return resultado


def acertos_por_pe(trials: Sequence[Trial]) -> dict[str, dict[str, int]]:
    """Cruzamento Correto x PeUsado, para as barras empilhadas 'Acertos por pé usado'."""
    contagens = {"Acertou": Counter(), "Errou": Counter()}
    for t in trials:
        if t.correto in contagens:
            contagens[t.correto][t.pe_usado] += 1
    return {
        resultado_key: {pe: contagem[pe] for pe in PES}
        for resultado_key, contagem in contagens.items()
    }


# --- Métricas que precisam da estrutura por atleta (não dá para achatar) ---


def trials_do_grupo(athletes: Sequence[Athlete]) -> list[Trial]:
    trials: list[Trial] = []
    for atleta in athletes:
        trials.extend(atleta.trials)
    return trials


def _mesma_posicao(valor: str, posicao: str) -> bool:
    """Comparação case-insensitive — o CSV real usa 'Meio campista', enquanto o
    modelo visual/POSICOES usa 'Meio Campista'; não hardcodar grafia exata (mesma
    cautela já aplicada a nomes de coluna em io/csv_importer.py)."""
    return valor.strip().casefold() == posicao.strip().casefold()


def trials_por_posicao(
    athletes: Sequence[Athlete], posicao: str, excluir_atleta: Athlete | None = None
) -> list[Trial]:
    """Tentativas de todos os atletas do grupo numa posição, exceto `excluir_atleta`."""
    trials: list[Trial] = []
    for atleta in athletes:
        if not _mesma_posicao(atleta.posicao, posicao) or atleta is excluir_atleta:
            continue
        trials.extend(atleta.trials)
    return trials


def media_acertos_por_atleta(athletes: Sequence[Athlete]) -> float:
    """Média, entre os atletas, da contagem de tentativas Correto=Acertou de cada um.

    Contagem bruta, não porcentagem — ver item 14 de docs/context/07-pontos-em-aberto.md.
    """
    if not athletes:
        return 0.0
    contagens = [contagem_acertos_erros(a.trials)["Acertou"] for a in athletes]
    return sum(contagens) / len(contagens)


def acertos_por_posicao(athletes: Sequence[Athlete]) -> dict[str, float | None]:
    """Média da contagem de Acertou por posição, entre os atletas do grupo.

    Contagem bruta, não porcentagem (item 14). A média inclui **todos** os atletas
    carregados na posição, inclusive aquele que é o foco do relatório — assim a
    barra de média existe em qualquer posição com dado, mesmo quando o atleta é o
    único da posição dele (aí as duas barras ficam iguais por definição). Difere de
    `trials_por_posicao`, que exclui o próprio atleta porque lá a comparação é
    "eu x os outros". Posição sem nenhum atleta no grupo retorna `None` (item 9) —
    o chamador não deve travar a geração do relatório por causa disso.
    """
    resultado: dict[str, float | None] = {}
    for posicao in POSICOES:
        contagens = [
            contagem_acertos_erros(a.trials)["Acertou"]
            for a in athletes
            if _mesma_posicao(a.posicao, posicao)
        ]
        resultado[posicao] = sum(contagens) / len(contagens) if contagens else None
    return resultado
