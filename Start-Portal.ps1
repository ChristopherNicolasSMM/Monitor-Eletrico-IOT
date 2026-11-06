# Iniciar Monitor Elétrico IoT com Python 3.11 sem depender de ativação do venv.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'

if (-not (Test-Path $python)) {
    Write-Host 'Criando ambiente virtual com Python 3.11...' -ForegroundColor Cyan
    & py -3.11 -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        throw 'Python 3.11 não foi encontrado. Instale Python 3.11 e execute novamente.'
    }
}
& $python -c 'import sys; assert sys.version_info[:2] == (3, 11), "Ambiente requer Python 3.11"'
if ($LASTEXITCODE -ne 0) { throw 'Ambiente virtual incompatível. Remova .venv e execute novamente.' }

Write-Host 'Instalando/validando dependências...' -ForegroundColor Cyan
& $python -m pip install -r portal/requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Falha na instalação das dependências.' }
Write-Host 'Portal técnico: http://127.0.0.1:8080' -ForegroundColor Green
& $python -m portal.run
