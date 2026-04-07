@echo off
REM Iniciar servidor de upload do Dashboard Financeiro
REM Este arquivo .bat ativa o virtual environment e roda o servidor

chcp 65001 >nul

cls
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║     📊 DASHBOARD FINANCEIRO - SERVIDOR UPLOAD         ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo ⏳ Iniciando servidor...
echo.

cd /d "%~dp0"

REM Verificar se virtual environment existe
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ ERRO: Virtual environment não encontrado!
    echo Por favor, crie o venv primeiro:
    echo   python -m venv .venv
    pause
    exit /b 1
)

REM Ativar venv
call .venv\Scripts\activate.bat

REM Verificar se Flask está instalado
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Flask não instalado!
    echo Instalando Flask...
    pip install flask
)

echo.
echo ✅ SERVIDOR INICIANDO...
echo.
echo 🌐 Endereço: http://localhost:5000
echo.
echo 📋 PRÓXIMOS PASSOS:
echo   1. Abra dashboard.html no navegador
echo   2. Clique em "📤 Upload Excel"
echo   3. Selecione seu arquivo
echo.
echo ⚠️  NÃO FECHE ESTA JANELA enquanto estiver usando o dashboard!
echo.
echo ────────────────────────────────────────────────────────
echo.

REM Iniciar servidor
python servidor_upload.py

echo.
echo ────────────────────────────────────────────────────────
echo ❌ Servidor encerrado.
echo.
pause

