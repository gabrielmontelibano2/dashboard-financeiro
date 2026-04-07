@echo off
REM Agendar Dashboard para iniciar automaticamente

setlocal

set "PROJECTDIR=c:\Users\GabrielOliveiraDeFar\OneDrive - Argus Solutions\Gabriel\analise-contas"
set "SCRIPTPATH=%PROJECTDIR%\iniciar_24_7.ps1"
set "TASKNAME=Dashboard-Financeiro-24-7"

echo.
echo ============================================
echo Agendando Dashboard para iniciar auto
echo ============================================
echo.

REM Deletar tarefa anterior se existir
schtasks /delete /tn "%TASKNAME%" /f >nul 2>&1

REM Criar nova tarefa
schtasks /create /tn "%TASKNAME%" ^
    /tr "powershell -ExecutionPolicy Bypass -File \"%SCRIPTPATH%\"" ^
    /sc onlogon ^
    /ru "%USERNAME%" ^
    /f

if %errorlevel% equ 0 (
    echo [OK] Tarefa agendada com sucesso!
    echo.
    echo Dashboard vai iniciar automaticamente quando você fizer login.
    echo.
) else (
    echo [ERRO] Falha ao agendar. Experimente rodar como Administrador.
)

pause
