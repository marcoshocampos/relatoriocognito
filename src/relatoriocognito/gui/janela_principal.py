from __future__ import annotations

from pathlib import Path
from typing import Callable

import customtkinter as ctk

from relatoriocognito.charts.colors import COR_BASE_PADRAO


class JanelaPrincipal(ctk.CTk):
    """Janela única que troca de tela (wizard de 3 passos). Guarda o estado
    compartilhado entre telas — sem lógica de cálculo, só orquestração."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Relatório Cognito")
        self.geometry("780x580")
        self.minsize(680, 480)

        self.nome_grupo: str = ""
        self.caminho_logo: Path | None = None
        self.caminhos_csv: list[Path] = []
        self.cor_base: str = COR_BASE_PADRAO

        self._tela_atual: ctk.CTkFrame | None = None
        self.mostrar_tela_grupo()

    def _trocar_tela(self, construtor_tela: Callable[[ctk.CTk, "JanelaPrincipal"], ctk.CTkFrame]) -> None:
        if self._tela_atual is not None:
            self._tela_atual.destroy()
        self._tela_atual = construtor_tela(self, self)
        self._tela_atual.pack(fill="both", expand=True, padx=28, pady=24)

    def mostrar_tela_grupo(self) -> None:
        from relatoriocognito.gui.tela_grupo import TelaGrupo

        self._trocar_tela(TelaGrupo)

    def mostrar_tela_selecao_csv(self) -> None:
        from relatoriocognito.gui.tela_selecao_csv import TelaSelecaoCsv

        self._trocar_tela(TelaSelecaoCsv)

    def mostrar_tela_gerar(self) -> None:
        from relatoriocognito.gui.tela_gerar import TelaGerar

        self._trocar_tela(TelaGerar)


def executar() -> None:
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    janela = JanelaPrincipal()
    janela.mainloop()
