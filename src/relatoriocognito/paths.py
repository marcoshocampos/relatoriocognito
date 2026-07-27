from __future__ import annotations

import sys
from pathlib import Path


def caminho_recurso(nome_arquivo: str) -> Path:
    """Resolve um arquivo em resources/, rodando tanto do código-fonte quanto do
    .exe empacotado — o PyInstaller extrai os dados de `--add-data` para
    `sys._MEIPASS` em tempo de execução (ver scripts/build_exe.ps1)."""
    base = getattr(sys, "_MEIPASS", None)
    if base is not None:
        return Path(base) / "relatoriocognito" / "resources" / nome_arquivo
    return Path(__file__).resolve().parent / "resources" / nome_arquivo
