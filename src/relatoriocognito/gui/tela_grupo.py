from __future__ import annotations

from pathlib import Path
from tkinter import filedialog, messagebox
from typing import TYPE_CHECKING

import customtkinter as ctk

if TYPE_CHECKING:
    from relatoriocognito.gui.janela_principal import JanelaPrincipal

_TIPOS_IMAGEM = [("Imagens", "*.png *.jpg *.jpeg"), ("Todos os arquivos", "*.*")]


class TelaGrupo(ctk.CTkFrame):
    """Passo 1: nome do grupo/time + logo (opcional)."""

    def __init__(self, master: ctk.CTk, controlador: "JanelaPrincipal") -> None:
        super().__init__(master, fg_color="transparent")
        self.controlador = controlador

        ctk.CTkLabel(self, text="Novo relatório", font=ctk.CTkFont(size=22, weight="bold")).pack(
            anchor="w", pady=(0, 4)
        )
        ctk.CTkLabel(
            self, text="Informe o nome do grupo/time e, se quiser, o logo.", text_color="gray50"
        ).pack(anchor="w", pady=(0, 24))

        ctk.CTkLabel(self, text="Nome do grupo").pack(anchor="w")
        self.campo_nome = ctk.CTkEntry(self, width=360, placeholder_text="Ex.: Atletico - MG")
        self.campo_nome.pack(anchor="w", pady=(4, 20))
        if controlador.nome_grupo:
            self.campo_nome.insert(0, controlador.nome_grupo)

        ctk.CTkLabel(self, text="Logo do grupo (opcional)").pack(anchor="w")
        linha_logo = ctk.CTkFrame(self, fg_color="transparent")
        linha_logo.pack(anchor="w", pady=(4, 20), fill="x")
        self.rotulo_logo = ctk.CTkLabel(linha_logo, text=self._texto_logo(), text_color="gray50")
        self.rotulo_logo.pack(side="left", padx=(0, 12))
        ctk.CTkButton(linha_logo, text="Escolher imagem…", command=self._escolher_logo, width=160).pack(
            side="left"
        )

        ctk.CTkButton(self, text="Avançar →", command=self._avancar, width=140).pack(
            anchor="e", side="bottom"
        )

    def _texto_logo(self) -> str:
        if self.controlador.caminho_logo:
            return self.controlador.caminho_logo.name
        return "Nenhuma imagem selecionada"

    def _escolher_logo(self) -> None:
        caminho = filedialog.askopenfilename(title="Escolher logo", filetypes=_TIPOS_IMAGEM)
        if caminho:
            self.controlador.caminho_logo = Path(caminho)
            self.rotulo_logo.configure(text=self._texto_logo())

    def _avancar(self) -> None:
        nome = self.campo_nome.get().strip()
        if not nome:
            messagebox.showwarning("Nome do grupo", "Informe o nome do grupo antes de continuar.")
            return
        self.controlador.nome_grupo = nome
        self.controlador.mostrar_tela_selecao_csv()
