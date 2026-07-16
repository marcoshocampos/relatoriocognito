# Gera o .exe único do relatoriocognito via PyInstaller.
# Uso: pwsh ./scripts/build_exe.ps1

$ErrorActionPreference = "Stop"

uv run pyinstaller `
    --name relatoriocognito `
    --onefile `
    --windowed `
    --add-data "src/relatoriocognito/resources;relatoriocognito/resources" `
    src/relatoriocognito/__main__.py

Write-Host "Build concluído: dist/relatoriocognito.exe"
