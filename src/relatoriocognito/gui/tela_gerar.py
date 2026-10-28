from __future__ import annotations

import os
import subprocess
import sys
import threading
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import TYPE_CHECKING

import customtkinter as ctk

from relatoriocognito.charts.colors import Paleta
from relatoriocognito.domain.models import Group
from relatoriocognito.gui.widgets.spinner import SpinnerCircular
from relatoriocognito.io.csv_importer import CsvImportError, carregar_csv
from relatoriocognito.pdf.report import gerar_relatorios_zip

if TYPE_CHECKING:
    from relatoriocognito.gui.janela_principal import JanelaPrincipal

_INTERVALO_VERIFICACAO_MS = 100
# Plural: a saída é um ZIP com um PDF por atleta, não um arquivo só.
_TEXTO_BOTAO = "Gerar e salvar relatórios"


def abrir_arquivo(caminho: Path) -> None:
    """Abre o arquivo no leitor padrão do sistema.

    Falha em silêncio de propósito: o PDF já foi gerado e salvo com sucesso: se o
    sistema não conseguir abrir (sem leitor de PDF associado, por exemplo), isso
    não torna a geração um erro, e a tela já mostra onde o arquivo está.
    """
    try:
        if sys.platform == "win32":
            os.startfile(caminho)  # type: ignore[attr-defined]  # só existe no Windows
        elif sys.platform == "darwin":
            subprocess.run(["open", str(caminho)], check=False)
        else:
            subprocess.run(["xdg-open", str(caminho)], check=False)
    except OSError:
        pass


class TelaGerar(ctk.CTkFrame):
    """Passo 3: ler os CSVs, montar o grupo e gerar/salvar o PDF."""

    def __init__(self, master: ctk.CTk, controlador: "JanelaPrincipal") -> None:
        super().__init__(master, fg_color="transparent")
        self.controlador = controlador
        self._erro_geracao: Exception | None = None
        self._progresso: tuple[int, int, str] | None = None
        self._nomes_gerados: list[str] = []

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

        linha_gerar = ctk.CTkFrame(self, fg_color="transparent")
        linha_gerar.pack(anchor="w", fill="x")
        self.botao_gerar = ctk.CTkButton(
            linha_gerar, text=_TEXTO_BOTAO, command=self._gerar, width=200, height=40
        )
        self.botao_gerar.pack(side="left")
        # Fica ao lado do botão (e não dentro dele): sobrepor um canvas no
        # CTkButton exigiria mexer na estrutura interna do widget, e o botão em si
        # já sinaliza o estado ficando desabilitado com o texto "Gerando PDF…".
        self.spinner = SpinnerCircular(linha_gerar)

        linha_botoes = ctk.CTkFrame(self, fg_color="transparent")
        linha_botoes.pack(fill="x", side="bottom", pady=(16, 0))
        self.botao_voltar = ctk.CTkButton(
            linha_botoes,
            text="← Voltar",
            command=controlador.mostrar_tela_selecao_csv,
            width=120,
            fg_color="gray40",
            hover_color="gray30",
        )
        self.botao_voltar.pack(side="left")

    # --- Estado visual ---------------------------------------------------

    def _travar_para_gerar(self) -> None:
        self.botao_gerar.configure(state="disabled", text="Gerando PDF…")
        # "Voltar" também sai de cena: destruir esta tela no meio da geração
        # deixaria o acompanhamento da thread mexendo em widget já destruído.
        self.botao_voltar.configure(state="disabled")
        self.spinner.pack(side="left", padx=(12, 0))
        self.spinner.iniciar()

    def _destravar(self) -> None:
        self.spinner.parar()
        self.spinner.pack_forget()
        self.botao_gerar.configure(state="normal", text=_TEXTO_BOTAO)
        self.botao_voltar.configure(state="normal")

    # --- Fluxo -----------------------------------------------------------

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

        # Um PDF por atleta, reunidos num ZIP — ver docs/context/06-decisoes.md.
        destino = filedialog.asksaveasfilename(
            title="Salvar relatórios",
            defaultextension=".zip",
            filetypes=[("Arquivo ZIP", "*.zip")],
            initialfile=f"relatorios_{self.controlador.nome_grupo}.zip",
        )
        if not destino:
            self.rotulo_status.configure(text="")
            self.botao_gerar.configure(state="normal")
            return

        self.rotulo_status.configure(text="Gerando PDFs…")
        self._travar_para_gerar()

        grupo = Group(nome=self.controlador.nome_grupo, athletes=atletas)
        paleta = Paleta(base=self.controlador.cor_base)
        caminho_destino = Path(destino)

        # A geração roda fora da thread da interface porque desenhar os gráficos
        # leva alguns segundos: no mesmo thread, o laço de eventos do Tk fica
        # parado, a janela congela e o spinner nem chega a girar.
        self._erro_geracao = None
        self._progresso = None
        self._nomes_gerados = []
        thread = threading.Thread(
            target=self._gerar_em_background,
            args=(grupo, paleta, caminho_destino),
            daemon=True,
        )
        thread.start()
        self._acompanhar(thread, caminho_destino)

    def _gerar_em_background(self, grupo: Group, paleta: Paleta, destino: Path) -> None:
        """Roda na thread de trabalho — não pode tocar em widget nenhum daqui.
        O resultado volta por `self._erro_geracao` / `self._progresso`, lidos pelo
        `_acompanhar` já na thread da interface."""
        try:
            self._nomes_gerados = gerar_relatorios_zip(
                grupo,
                self.controlador.caminho_logo,
                destino,
                paleta=paleta,
                progresso=self._registrar_progresso,
            )
        except Exception as erro:  # noqa: BLE001 - qualquer falha vira mensagem na tela
            self._erro_geracao = erro

    def _registrar_progresso(self, indice: int, total: int, nome_atleta: str) -> None:
        """Chamado da thread de trabalho: só guarda o estado, sem tocar em widget
        (quem escreve na tela é o `_acompanhar`)."""
        self._progresso = (indice, total, nome_atleta)

    def _acompanhar(self, thread: threading.Thread, destino: Path) -> None:
        """Verifica periodicamente se a thread terminou, já de volta na thread da
        interface (é `after` quem chama), onde mexer em widget é seguro."""
        if thread.is_alive():
            if self._progresso is not None:
                indice, total, nome_atleta = self._progresso
                self.rotulo_status.configure(text=f"Gerando PDF {indice} de {total} — {nome_atleta}…")
            self.after(_INTERVALO_VERIFICACAO_MS, lambda: self._acompanhar(thread, destino))
            return

        self._destravar()

        if self._erro_geracao is not None:
            messagebox.showerror(
                "Erro ao gerar relatórios",
                f"Não foi possível gerar os relatórios:\n{self._erro_geracao}",
            )
            self.rotulo_status.configure(text="")
            return

        quantidade = len(self._nomes_gerados)
        plural = "s" if quantidade != 1 else ""
        self.rotulo_status.configure(
            text=f"{quantidade} relatório{plural} gerado{plural} com sucesso!\n{destino}",
            text_color="green",
        )
        # Sem messagebox de sucesso: o próprio ZIP abrindo já é o retorno, e um
        # modal só criaria um passo a mais para o usuário fechar antes de vê-lo.
        abrir_arquivo(destino)
