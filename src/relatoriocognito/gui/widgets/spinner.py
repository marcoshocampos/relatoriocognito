"""Indicador circular de carregamento.

O CustomTkinter não traz um spinner redondo pronto (só `CTkProgressBar`, que é
uma barra), então é um arco desenhado em canvas girando via `after` — sem
dependência nova e sem depender de glifo de fonte (um "◐" animado ficaria à
mercê da fonte instalada).
"""

from __future__ import annotations

import customtkinter as ctk


def _cor_do_tema(componente: str, propriedade: str) -> str:
    """Resolve uma cor do tema atual para um valor único.

    O tema guarda `[claro, escuro]` para a maioria das cores; o canvas do Tk
    precisa de uma string só, e não acompanha troca de aparência sozinho.
    """
    valor = ctk.ThemeManager.theme[componente][propriedade]
    if isinstance(valor, (list, tuple)):
        return valor[1] if ctk.get_appearance_mode() == "Dark" else valor[0]
    return valor


class SpinnerCircular(ctk.CTkCanvas):
    """Arco girando, para sinalizar trabalho em andamento sem prever duração.

    Só anima enquanto o laço de eventos do Tk estiver livre — quem chama precisa
    rodar o trabalho pesado em outra thread, senão o spinner congela junto com o
    resto da janela (foi exatamente o caso da geração do PDF, ver
    `gui/tela_gerar.py`).
    """

    def __init__(
        self,
        master,
        *,
        tamanho: int = 22,
        espessura: int = 3,
        cor: str | None = None,
        cor_fundo: str | None = None,
    ) -> None:
        super().__init__(
            master,
            width=tamanho,
            height=tamanho,
            highlightthickness=0,
            borderwidth=0,
            bg=cor_fundo or _cor_do_tema("CTk", "fg_color"),
        )
        cor_arco = cor or _cor_do_tema("CTkButton", "fg_color")
        margem = espessura
        caixa = (margem, margem, tamanho - margem, tamanho - margem)

        # Círculo de fundo fraco: sem ele o arco sozinho parece um traço solto.
        self.create_oval(*caixa, outline=_cor_do_tema("CTkFrame", "fg_color"), width=espessura)
        self._arco = self.create_arc(
            *caixa, start=0, extent=100, style="arc", outline=cor_arco, width=espessura
        )

        self._angulo = 0
        self._rodando = False
        self._job: str | None = None

    def iniciar(self) -> None:
        if self._rodando:
            return
        self._rodando = True
        self._animar()

    def parar(self) -> None:
        self._rodando = False
        if self._job is not None:
            self.after_cancel(self._job)
            self._job = None

    def _animar(self) -> None:
        if not self._rodando:
            return
        self._angulo = (self._angulo - 11) % 360
        self.itemconfigure(self._arco, start=self._angulo)
        self._job = self.after(30, self._animar)
