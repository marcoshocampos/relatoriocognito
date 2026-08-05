from __future__ import annotations

from relatoriocognito.charts import colors


def test_misturar_com_branco_intensidade_zero_e_branco():
    assert colors.misturar_com_branco("#1E5FCC", 0.0) == "#FFFFFF"


def test_misturar_com_branco_intensidade_um_e_a_propria_cor():
    assert colors.misturar_com_branco("#1e5fcc", 1.0) == "#1E5FCC"


def test_misturar_com_branco_fica_entre_a_cor_e_o_branco():
    resultado = colors.misturar_com_branco("#000000", 0.12)
    r, g, b = int(resultado[1:3], 16), int(resultado[3:5], 16), int(resultado[5:7], 16)
    assert 0 < r < 255 and 0 < g < 255 and 0 < b < 255


def test_cor_texto_sobre_fundo_claro_e_escuro():
    assert colors.cor_texto_sobre("#FFFFFF") == colors.GRAFITE
    assert colors.cor_texto_sobre("#000000") == colors.BRANCO


def test_cor_texto_sobre_cor_base_escura_usa_texto_branco():
    # Azul escuro (ex.: cor de time) precisa de texto branco, não preto fixo —
    # regressão do problema que motivou cor_texto_sobre existir (ver
    # docs/context/06-decisoes.md, 03/08/2026).
    assert colors.cor_texto_sobre("#1E5FCC") == colors.BRANCO


def test_cor_texto_sobre_verde_padrao_usa_texto_escuro():
    assert colors.cor_texto_sobre(colors.VERDE) == colors.GRAFITE


def test_escurecer_reduz_cada_canal():
    assert colors.escurecer("#FFFFFF", 0.25) == "#BFBFBF"


def test_paleta_default_reproduz_verde_do_modelo_canva():
    paleta = colors.Paleta()
    assert paleta.base == colors.VERDE
    assert paleta.destaque == colors.VERDE


def test_paleta_destaque_segue_a_cor_base_escolhida():
    paleta = colors.Paleta(base="#1E5FCC")
    assert paleta.destaque == "#1E5FCC"


def test_paleta_referencia_e_fixa_independente_da_cor_base():
    # "Media Grupo" / "Media da posição" precisam continuar neutros mesmo com
    # uma cor base saturada — ver docs/context/06-decisoes.md.
    assert colors.Paleta(base="#1E5FCC").referencia == colors.CINZA_MEDIO
    assert colors.Paleta(base="#FF00FF").referencia == colors.CINZA_MEDIO


def test_paleta_fundo_cartao_deriva_da_cor_base():
    paleta = colors.Paleta(base="#1E5FCC")
    assert paleta.fundo_cartao == colors.misturar_com_branco("#1E5FCC", 0.12)
    assert paleta.fundo_cartao_destaque == colors.misturar_com_branco("#1E5FCC", 0.20)
