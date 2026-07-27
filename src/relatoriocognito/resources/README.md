# resources

Assets estáticos embutidos no `.exe` via PyInstaller (`--add-data`, ver
`scripts/build_exe.ps1`) — não confundir com `docs/reference/` (material de
referência para desenvolvimento, não embutido no executável).

- `par_de_pes.png` — imagem decorativa da página "Ações por pé" (`pdf/layout_acoes_pe.py`).

Ainda faltando: o arquivo do selo "Cognito" em alta resolução/vetor (ver
`docs/context/07-pontos-em-aberto.md`, item 12) e o ícone do app. Até lá,
`pdf/layout_helpers.py` desenha um selo placeholder vetorialmente, sem
depender de nenhum arquivo aqui.

Caminhos aqui são resolvidos com `relatoriocognito.paths.caminho_recurso`, que
funciona tanto rodando do código-fonte quanto do `.exe` empacotado.
