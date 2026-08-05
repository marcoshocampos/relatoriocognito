"""Paleta do relatório.

A base veio de amostragem de pixel das imagens em docs/reference/modelo-canva/.
Desde 26/07/2026 a cor de destaque deixou de ser fixa: o usuário escolhe a "cor
base" do time na tela 1 do wizard, porque os times que recebem o relatório se
incomodam quando a cor exibida é da paleta de um rival (ver docs/context/06-decisoes.md).

Divisão adotada:

- **Cor base** (escolhida) — tudo que é destaque/atleta/dado real do grupo. Toma o
  lugar que o verde ocupava.
- **Neutros** (fixos) — séries de referência (média do grupo, média da posição,
  série "Ideal"), que existem para serem lidas como pano de fundo do dado real.
- **Semânticas** (fixas) — vermelho/amarelo/laranja. São convenção de leitura
  ("errou", "precoce", "tardio"); derivá-las da cor base tiraria o significado.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

# --- Semânticas: fixas, não respondem à cor base ---
VERMELHO = "#FF3131"
AMARELO = "#FFDE59"
LARANJA = "#FF914D"

# --- Neutros ---
CINZA_MEDIO = "#A6A6A6"
CINZA_CLARO = "#D9D9D9"
PRETO = "#000000"
BRANCO = "#FFFFFF"
GRAFITE = "#1A1A1A"

# Verde do modelo Canva — hoje é só o valor padrão do seletor de cor, não mais
# uma constante usada direto pelos gráficos.
VERDE = "#7ED957"
COR_BASE_PADRAO = VERDE

# Proporção da cor base nos fundos de cartão. O usuário pediu "alpha de 20% ou
# menos"; 12% para o cartão comum e 20% para o de destaque (que antes era
# lavanda fixa) mantém o texto escuro legível mesmo com cor base saturada.
_INTENSIDADE_FUNDO = 0.12
_INTENSIDADE_FUNDO_DESTAQUE = 0.20


def _para_rgb(cor: str) -> tuple[int, int, int]:
    valor = cor.lstrip("#")
    if len(valor) != 6:
        raise ValueError(f"Cor hexadecimal inválida: {cor!r} (esperado formato #RRGGBB)")
    return int(valor[0:2], 16), int(valor[2:4], 16), int(valor[4:6], 16)


def _para_hex(rgb: Iterable[float]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*(max(0, min(255, round(canal))) for canal in rgb))


def misturar_com_branco(cor: str, intensidade: float) -> str:
    """Achata `cor` sobre branco na proporção `intensidade` (0 = branco, 1 = a cor).

    Gera uma cor sólida em vez de usar alpha de verdade: transparência em PDF
    depende do suporte do leitor e costuma se perder na impressão, enquanto a
    cor pré-misturada tem o mesmo resultado visual em qualquer visualizador.
    """
    return _para_hex(255 + (canal - 255) * intensidade for canal in _para_rgb(cor))


def _luminancia(cor: str) -> float:
    """Luminância relativa (0 = preto, 1 = branco), fórmula sRGB da WCAG."""
    def canal_linear(valor: int) -> float:
        proporcao = valor / 255
        return proporcao / 12.92 if proporcao <= 0.03928 else ((proporcao + 0.055) / 1.055) ** 2.4

    r, g, b = (canal_linear(c) for c in _para_rgb(cor))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def cor_texto_sobre(fundo: str) -> str:
    """Preto ou branco, o que tiver mais contraste sobre `fundo`.

    Necessário porque a cor base agora é livre: os badges de valor da página
    individual pintam o fundo com ela, e um azul-marinho escolhido pelo usuário
    deixaria o texto escuro ilegível.
    """
    return GRAFITE if _luminancia(fundo) > 0.45 else BRANCO


def escurecer(cor: str, intensidade: float = 0.25) -> str:
    """Versão mais escura da cor — usada onde a cor base precisa aparecer sobre o
    próprio fundo tingido dela (ex.: título de cartão, texto de destaque)."""
    return _para_hex(canal * (1 - intensidade) for canal in _para_rgb(cor))


@dataclass(frozen=True)
class Paleta:
    """Cores do relatório derivadas da cor base escolhida pelo usuário.

    Instanciada uma vez por relatório na GUI e repassada para `pdf/` e `charts/`.
    O default reproduz o visual do modelo Canva, então gerar sem escolher cor
    nenhuma continua funcionando como antes.
    """

    base: str = COR_BASE_PADRAO

    @property
    def destaque(self) -> str:
        """Atleta, acertos, dado real do grupo — o que antes era verde."""
        return self.base

    @property
    def referencia(self) -> str:
        """Séries de comparação (média do grupo, média da posição, "Ideal")."""
        return CINZA_MEDIO

    @property
    def fundo_cartao(self) -> str:
        return misturar_com_branco(self.base, _INTENSIDADE_FUNDO)

    @property
    def fundo_cartao_destaque(self) -> str:
        return misturar_com_branco(self.base, _INTENSIDADE_FUNDO_DESTAQUE)

    @property
    def texto_sobre_destaque(self) -> str:
        return cor_texto_sobre(self.base)

    @property
    def destaque_escuro(self) -> str:
        """Para texto na cor base sobre fundo claro — a cor base pura pode ser
        clara demais para ler (o verde padrão, por exemplo)."""
        return escurecer(self.base, 0.3)
