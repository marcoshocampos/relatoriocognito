from relatoriocognito.domain import metrics
from relatoriocognito.domain.models import Athlete, Trial


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


def _atleta(nome: str, posicao: str, trials: list[Trial]) -> Athlete:
    return Athlete(nome=nome, lateralidade="Destro", posicao=posicao, trials=trials)


def test_contagem_acertos_erros_conta_por_categoria():
    trials = [_trial(correto="Acertou")] * 3 + [_trial(correto="Errou")] * 2
    assert metrics.contagem_acertos_erros(trials) == {"Acertou": 3, "Errou": 2}


def test_contagem_acertos_erros_lista_vazia():
    assert metrics.contagem_acertos_erros([]) == {"Acertou": 0, "Errou": 0}


def test_taxa_acerto():
    trials = [_trial(correto="Acertou")] * 3 + [_trial(correto="Errou")] * 2
    assert metrics.taxa_acerto(trials) == 60.0


def test_taxa_acerto_lista_vazia_nao_quebra():
    assert metrics.taxa_acerto([]) == 0.0


def test_distribuicao_classificacao_tr_soma_100_e_inclui_perda_de_bola():
    trials = (
        [_trial(classificacao_tr="Ideal")] * 4
        + [_trial(classificacao_tr="Precoce")] * 2
        + [_trial(classificacao_tr="Tardio")] * 1
        + [_trial(classificacao_tr="Perda de bola")] * 3
    )
    dist = metrics.distribuicao_classificacao_tr(trials)
    assert dist["Ideal"] == 40.0
    assert dist["Precoce"] == 20.0
    assert dist["Tardio"] == 10.0
    assert dist["Perda de bola"] == 30.0
    assert sum(dist.values()) == 100.0


def test_distribuicao_classificacao_tr_lista_vazia_nao_quebra():
    dist = metrics.distribuicao_classificacao_tr([])
    assert all(v == 0.0 for v in dist.values())


def test_media_tr_e_pooled_nao_media_das_medias():
    # Atleta A: 1 tentativa (TR=10). Atleta B: 3 tentativas (TR=0).
    # Pooled sobre as 4 tentativas = 10/4 = 2.5. Média das médias seria (10+0)/2 = 5.
    trials_a = [_trial(tempo_reacao=10.0)]
    trials_b = [_trial(tempo_reacao=0.0)] * 3
    assert metrics.media_tr(trials_a + trials_b) == 2.5


def test_media_tr_lista_vazia_nao_quebra():
    assert metrics.media_tr([]) == 0.0


def test_media_tr_por_resultado_separa_acertos_de_erros():
    trials = [
        _trial(correto="Acertou", tempo_reacao=2.0),
        _trial(correto="Acertou", tempo_reacao=3.0),
        _trial(correto="Errou", tempo_reacao=1.0),
    ]
    resultado = metrics.media_tr_por_resultado(trials)
    assert resultado["Acertou"] == 2.5
    assert resultado["Errou"] == 1.0


def test_media_tr_por_resultado_categoria_sem_dado_retorna_zero():
    trials = [_trial(correto="Acertou", tempo_reacao=2.0)]
    resultado = metrics.media_tr_por_resultado(trials)
    assert resultado["Errou"] == 0.0


def test_classificacao_tr_por_resultado_exclui_perda_de_bola():
    # Reproduz os números do modelo de referência (dashboard_individual.png):
    # Acertou = 10 (Ideal) + 10 (Tardio); Errou = 6 (Precoce) + 4 (Ideal).
    trials = (
        [_trial(correto="Acertou", classificacao_tr="Ideal")] * 10
        + [_trial(correto="Acertou", classificacao_tr="Tardio")] * 10
        + [_trial(correto="Errou", classificacao_tr="Precoce")] * 6
        + [_trial(correto="Errou", classificacao_tr="Ideal")] * 4
        + [_trial(correto="Errou", classificacao_tr="Perda de bola")] * 5
    )
    resultado = metrics.classificacao_tr_por_resultado(trials)
    assert resultado["Acertou"] == {"Ideal": 10, "Precoce": 0, "Tardio": 10}
    assert resultado["Errou"] == {"Ideal": 4, "Precoce": 6, "Tardio": 0}
    assert "Perda de bola" not in resultado["Acertou"]
    assert "Perda de bola" not in resultado["Errou"]


def test_acertos_por_decisao_separa_ideal_de_dado():
    trials = [
        _trial(resposta_correta="Chutar ao Gol", resposta_dada="Manter Posse"),
        _trial(resposta_correta="Chutar ao Gol", resposta_dada="Manter Posse"),
        _trial(resposta_correta="Manter Posse", resposta_dada="Manter Posse"),
    ]
    resultado = metrics.acertos_por_decisao(trials)
    assert resultado["Chutar ao Gol"] == (2, 0)
    assert resultado["Manter Posse"] == (1, 3)
    assert resultado["Passe a Esquerda"] == (0, 0)
    assert resultado["Passe a Direita"] == (0, 0)


def test_taxa_acerto_por_resposta_condiciona_em_resposta_correta():
    trials = [
        _trial(resposta_correta="Chutar ao Gol", correto="Acertou"),
        _trial(resposta_correta="Chutar ao Gol", correto="Errou"),
        _trial(resposta_correta="Manter Posse", correto="Acertou"),
    ]
    resultado = metrics.taxa_acerto_por_resposta(trials)
    assert resultado["Chutar ao Gol"] == 50.0
    assert resultado["Manter Posse"] == 100.0
    assert resultado["Passe a Esquerda"] == 0.0


def test_distribuicao_pe_usado():
    trials = [_trial(pe_usado="Esquerdo")] * 3 + [_trial(pe_usado="Direito")] * 1
    assert metrics.distribuicao_pe_usado(trials) == {"Esquerdo": 3, "Direito": 1}


def test_media_tr_por_pe():
    trials = [
        _trial(pe_usado="Esquerdo", tempo_reacao=2.0),
        _trial(pe_usado="Esquerdo", tempo_reacao=4.0),
        _trial(pe_usado="Direito", tempo_reacao=3.0),
    ]
    resultado = metrics.media_tr_por_pe(trials)
    assert resultado["Esquerdo"] == 3.0
    assert resultado["Direito"] == 3.0


def test_acertos_por_pe_reproduz_modelo_de_referencia():
    # acoes_por_pe.png: Acertou = Esquerdo 13 + Direito 7; Errou = Esquerdo 6 + Direito 4.
    trials = (
        [_trial(correto="Acertou", pe_usado="Esquerdo")] * 13
        + [_trial(correto="Acertou", pe_usado="Direito")] * 7
        + [_trial(correto="Errou", pe_usado="Esquerdo")] * 6
        + [_trial(correto="Errou", pe_usado="Direito")] * 4
    )
    resultado = metrics.acertos_por_pe(trials)
    assert resultado["Acertou"] == {"Esquerdo": 13, "Direito": 7}
    assert resultado["Errou"] == {"Esquerdo": 6, "Direito": 4}


def test_trials_do_grupo_achata_todos_os_atletas():
    a1 = _atleta("Caio", "Meio Campista", [_trial()] * 2)
    a2 = _atleta("Bruno", "Atacante", [_trial()] * 3)
    assert len(metrics.trials_do_grupo([a1, a2])) == 5


def test_trials_por_posicao_exclui_o_proprio_atleta():
    caio = _atleta("Caio", "Meio Campista", [_trial()] * 2)
    bruno = _atleta("Bruno", "Meio Campista", [_trial()] * 3)
    ana = _atleta("Ana", "Atacante", [_trial()] * 4)
    trials = metrics.trials_por_posicao([caio, bruno, ana], "Meio Campista", excluir_atleta=caio)
    assert len(trials) == 3  # só os de Bruno, Caio excluído, Ana é outra posição


def test_media_acertos_por_atleta_e_media_das_contagens():
    a1 = _atleta("Caio", "Meio Campista", [_trial(correto="Acertou")] * 3)
    a2 = _atleta("Bruno", "Atacante", [_trial(correto="Acertou")] * 5)
    assert metrics.media_acertos_por_atleta([a1, a2]) == 4.0


def test_media_acertos_por_atleta_lista_vazia_nao_quebra():
    assert metrics.media_acertos_por_atleta([]) == 0.0


def test_acertos_por_posicao_exclui_o_proprio_atleta_e_marca_posicao_sem_atleta():
    caio = _atleta("Caio", "Meio Campista", [_trial(correto="Acertou")] * 20)
    bruno = _atleta("Bruno", "Meio Campista", [_trial(correto="Acertou")] * 10)
    ana = _atleta("Ana", "Atacante", [_trial(correto="Acertou")] * 6)

    resultado = metrics.acertos_por_posicao([caio, bruno, ana], caio)

    # Meio Campista exclui Caio (o próprio atleta): só sobra Bruno (10).
    assert resultado["Meio Campista"] == 10.0
    assert resultado["Atacante"] == 6.0
    # Posições sem nenhum atleta no grupo ficam sem dado (item 9).
    assert resultado["Zagueiro"] is None
    assert resultado["Volante"] is None
    assert resultado["Lateral Direito"] is None
    assert resultado["Lateral Esquerdo"] is None


def test_acertos_por_posicao_ignora_diferenca_de_maiuscula_da_posicao():
    # Regressão: o CSV real usa "Meio campista" (minúsculo), mas POSICOES usa
    # "Meio Campista" — comparação sensível a maiúscula fazia o atleta "sumir"
    # do gráfico "Acertos por posição" (descoberto gerando um PDF de teste real).
    caio = _atleta("Caio", "Meio campista", [_trial(correto="Acertou")] * 20)
    ana = _atleta("Ana", "meio campista", [_trial(correto="Acertou")] * 10)

    resultado = metrics.acertos_por_posicao([caio, ana], caio)

    assert resultado["Meio Campista"] == 10.0


def test_trials_por_posicao_ignora_diferenca_de_maiuscula():
    caio = _atleta("Caio", "Meio campista", [_trial()] * 2)
    ana = _atleta("Ana", "MEIO CAMPISTA", [_trial()] * 3)

    trials = metrics.trials_por_posicao([caio, ana], "Meio campista", excluir_atleta=caio)

    assert len(trials) == 3  # Ana é encontrada mesmo com grafia diferente
