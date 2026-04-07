#!/usr/bin/env pwsh
# Iniciar servidor de upload do Dashboard Financeiro
# Script PowerShell para iniciar o servidor Flask

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     📊 DASHBOARD FINANCEIRO - SERVIDOR UPLOAD         ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Obter o diretório do script
$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Set-Location $scriptPath

# Verificar se virtual environment existe
if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "❌ ERRO: Virtual environment não encontrado!" -ForegroundColor Red
    Write-Host "Por favor, crie o venv primeiro:" -ForegroundColor Yellow
    Write-Host "  python -m venv .venv"
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host "⏳ Iniciando servidor..." -ForegroundColor Yellow
Write-Host ""

# Ativar venv
& ".venv\Scripts\Activate.ps1"

# Verificar se Flask está instalado
try {
    python -c "import flask" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Flask não instalado"
    }
} catch {
    Write-Host "❌ ERRO: Flask não instalado!" -ForegroundColor Red
    Write-Host "Instalando Flask..." -ForegroundColor Yellow
    pip install flask
}

Write-Host ""
Write-Host "✅ SERVIDOR INICIANDO..." -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Endereço: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 PRÓXIMOS PASSOS:" -ForegroundColor Cyan
Write-Host "  1. Abra dashboard.html no navegador" -ForegroundColor White
Write-Host "  2. Clique em '📤 Upload Excel'" -ForegroundColor White
Write-Host "  3. Selecione seu arquivo" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  NÃO FECHE ESTA JANELA enquanto estiver usando o dashboard!" -ForegroundColor Yellow
Write-Host ""
Write-Host "────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

# Iniciar servidor
python servidor_upload.py

Write-Host ""
Write-Host "────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host "❌ Servidor encerrado." -ForegroundColor Red
Write-Host ""
Read-Host "Pressione Enter para sair"
