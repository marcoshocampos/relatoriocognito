from __future__ import annotations

from pathlib import Path
from tkinter import filedialog, messagebox
from typing import TYPE_CHECKING

import customtkinter as ctk

if TYPE_CHECKING:
    from relatoriocognito.gui.janela_principal import JanelaPrincipal

_TIPOS_CSV = [("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]


class TelaSelecaoCsv(ctk.CTkFrame):
    """Passo 2: selecionar um CSV por atleta que vai entrar no relatório."""

    def __init__(self, master: ctk.CTk, controlador: "JanelaPrincipal") -> None:
        super().__init__(master, fg_color="transparent")
        self.controlador = controlador

        ctk.CTkLabel(self, text="Atletas do relatório", font=ctk.CTkFont(size=22, weight="bold")).pack(
            anchor="w", pady=(0, 4)
        )
        ctk.CTkLabel(
            self,
            text="Selecione um arquivo CSV para cada atleta que vai entrar no relatório.",
            text_color="gray50",
        ).pack(anchor="w", pady=(0, 16))

        self.lista_frame = ctk.CTkScrollableFrame(self, width=500, height=260)
        self.lista_frame.pack(fill="both", expand=True, pady=(0, 16))

        ctk.CTkButton(self, text="Adicionar CSVs…", command=self._adicionar, width=160).pack(anchor="w")

        linha_botoes = ctk.CTkFrame(self, fg_color="transparent")
        linha_botoes.pack(fill="x", side="bottom", pady=(16, 0))
        ctk.CTkButton(
            linha_botoes,
            text="← Voltar",
            command=controlador.mostrar_tela_grupo,
            width=120,
            fg_color="gray40",
            hover_color="gray30",
        ).pack(side="left")
        ctk.CTkButton(linha_botoes, text="Avançar →", command=self._avancar, width=140).pack(side="right")

        self._redesenhar_lista()

    def _adicionar(self) -> None:
        caminhos = filedialog.askopenfilenames(title="Selecionar CSVs dos atletas", filetypes=_TIPOS_CSV)
        for caminho in caminhos:
            caminho_path = Path(caminho)
            if caminho_path not in self.controlador.caminhos_csv:
                self.controlador.caminhos_csv.append(caminho_path)
        self._redesenhar_lista()

    def _remover(self, caminho: Path) -> None:
        self.controlador.caminhos_csv.remove(caminho)
        self._redesenhar_lista()

    def _redesenhar_lista(self) -> None:
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        if not self.controlador.caminhos_csv:
            ctk.CTkLabel(self.lista_frame, text="Nenhum CSV selecionado ainda.", text_color="gray50").pack(
                anchor="w", pady=8
            )
            return

        for caminho in self.controlador.caminhos_csv:
            linha = ctk.CTkFrame(self.lista_frame, fg_color="transparent")
            linha.pack(fill="x", pady=4)
            ctk.CTkLabel(linha, text=caminho.name).pack(side="left", padx=(0, 8))
            ctk.CTkButton(
                linha,
                text="Remover",
                width=80,
                height=24,
                fg_color="gray40",
                hover_color="#B23B3B",
                command=lambda c=caminho: self._remover(c),
            ).pack(side="right")

    def _avancar(self) -> None:
        if not self.controlador.caminhos_csv:
            messagebox.showwarning("Atletas", "Selecione pelo menos um CSV antes de continuar.")
            return
        self.controlador.mostrar_tela_gerar()
