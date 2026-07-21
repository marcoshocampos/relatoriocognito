from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Trial:
    """Uma linha do CSV: uma tentativa/trial de um atleta.

    `classificacao_tr` e `correto` vêm prontos da ferramenta de origem e nunca
    são recalculados — ver docs/context/02-modelo-dados.md.
    """

    treino: str
    pe_esperado: str
    pe_usado: str
    tempo_reacao: float
    classificacao_tr: str
    correto: str
    resposta_correta: str
    resposta_dada: str
    data: str
    hora: str


@dataclass
class Athlete:
    """Um atleta selecionado para o relatório (= um CSV).

    `lateralidade` e `posicao` vêm do campo `Jogador` do CSV
    (`"Nome - Lateralidade - Posição"`).
    """

    nome: str
    lateralidade: str
    posicao: str
    trials: list[Trial] = field(default_factory=list)


@dataclass
class Group:
    """Grupo formado manualmente pelo usuário para um relatório."""

    nome: str
    athletes: list[Athlete] = field(default_factory=list)
