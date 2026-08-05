from __future__ import annotations

from pathlib import Path
from tkinter import filedialog, messagebox
from typing import TYPE_CHECKING

import customtkinter as ctk

from relatoriocognito.charts.colors import Paleta
from relatoriocognito.domain.models import Group
from relatoriocognito.io.csv_importer import CsvImportError, carregar_csv
from relatoriocognito.pdf.report import gerar_relatorio_pdf

if TYPE_CHECKING:
    from relatoriocognito.gui.janela_principal import JanelaPrincipal


class TelaGerar(ctk.CTkFrame):
    """Passo 3: ler os CSVs, montar o grupo e gerar/salvar o PDF."""

    def __init__(self, master: ctk.CTk, controlador: "JanelaPrincipal") -> None:
        super().__init__(master, fg_color="transparent")
        self.controlador = controlador

        ctk.CTkLabel(self, text="Gerar relatório", font=ctk.CTkFont(size=22, weight="bold")).pack(
            anchor="w", pady=(0, 4)
        )
        ctk.CTkLabel(self, text="Confira os dados antes de gerar o PDF.", text_color="gray50").pack(
            anchor="w", pady=(0, 20)
        )

        resumo = (
            f"Grupo: {controlador.nome_grupo}\n"
            f"Logo: {controlador.caminho_logo.name if controlador.caminho_logo else 'nenhum'}\n"
            f"Atletas selecionados: {len(controlador.caminhos_csv)}"
        )
        ctk.CTkLabel(self, text=resumo, justify="left").pack(anchor="w", pady=(0, 24))

        self.rotulo_status = ctk.CTkLabel(self, text="", text_color="gray50")
        self.rotulo_status.pack(anchor="w", pady=(0, 12))

        self.botao_gerar = ctk.CTkButton(
            self, text="Gerar e salvar PDF", command=self._gerar, width=200, height=40
        )
        self.botao_gerar.pack(anchor="w")

        linha_botoes = ctk.CTkFrame(self, fg_color="transparent")
        linha_botoes.pack(fill="x", side="bottom", pady=(16, 0))
        ctk.CTkButton(
            linha_botoes,
            text="← Voltar",
            command=controlador.mostrar_tela_selecao_csv,
            width=120,
            fg_color="gray40",
            hover_color="gray30",
        ).pack(side="left")

    def _gerar(self) -> None:
        self.botao_gerar.configure(state="disabled")
        self.rotulo_status.configure(text="Lendo CSVs…", text_color="gray50")
        self.update_idletasks()

        atletas = []
        for caminho in self.controlador.caminhos_csv:
            try:
                atletas.append(carregar_csv(caminho))
            except CsvImportError as erro:
                messagebox.showerror("Erro ao ler CSV", str(erro))
                self.rotulo_status.configure(text="")
                self.botao_gerar.configure(state="normal")
                return

        destino = filedialog.asksaveasfilename(
            title="Salvar relatório",
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            initialfile=f"relatorio_{self.controlador.nome_grupo}.pdf",
        )
        if not destino:
            self.rotulo_status.configure(text="")
            self.botao_gerar.configure(state="normal")
            return

        self.rotulo_status.configure(text="Gerando PDF…")
        self.update_idletasks()

        grupo = Group(nome=self.controlador.nome_grupo, athletes=atletas)
        paleta = Paleta(base=self.controlador.cor_base)
        try:
            gerar_relatorio_pdf(grupo, self.controlador.caminho_logo, Path(destino), paleta=paleta)
        except Exception as erro:
            messagebox.showerror("Erro ao gerar PDF", f"Não foi possível gerar o relatório:\n{erro}")
            self.rotulo_status.configure(text="")
            self.botao_gerar.configure(state="normal")
            return

        self.rotulo_status.configure(text="Relatório gerado com sucesso!", text_color="green")
        messagebox.showinfo("Sucesso", f"Relatório salvo em:\n{destino}")
        self.botao_gerar.configure(state="normal")
