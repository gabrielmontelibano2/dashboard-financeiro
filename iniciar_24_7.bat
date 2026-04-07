@echo off
REM Inicia o Dashboard Financeiro 24/7
REM Reinicia automaticamente se falhar

setlocal enabledelayedexpansion

:start
echo.
echo ============================================
echo DASHBOARD FINANCEIRO - SERVIDOR 24/7
echo ============================================
echo.
echo [%date% %time%] Iniciando servidor...
echo.

cd /d "c:\Users\GabrielOliveiraDeFar\OneDrive - Argus Solutions\Gabriel\analise-contas"

".venv\Scripts\python.exe" servidor_dash.py

echo.
echo [%date% %time%] Servidor foi interrompido!
echo Reiniciando em 5 segundos...
echo.

timeout /t 5 /nobreak

goto start
