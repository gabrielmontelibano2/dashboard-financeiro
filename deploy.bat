@echo off
REM Script para publicar Dashboard Financeiro no GitHub
REM Execute este script após criar repositório em https://github.com/new

echo =====================================
echo Dashboard Financeiro - GitHub Setup
echo =====================================
echo.
echo [1/5] Configurando Git...
git config user.name "gabriel019pira"
git config user.email "gabriel019pira@gmail.com"

echo.
echo [2/5] Adicionando arquivos...
git add dashboard.html
git add servidor_dash.py
git add requirements.txt
git add .gitignore
git add README.md
git add GITHUB_SETUP.md

echo.
echo [3/5] Fazendo commit...
git commit -m "Inicializar Dashboard Financeiro"

echo.
echo [4/5] Adicionando repositório remoto...
echo Digite o URL do seu repositório GitHub:
echo Exemplo: https://github.com/gabriel019pira/dashboard-financeiro.git
set /p github_url="URL: "

git remote add origin %github_url%

echo.
echo [5/5] Enviando para GitHub...
git branch -M main
git push -u origin main

echo.
echo =====================================
echo Sucesso! Deploy completo!
echo =====================================
echo.
echo Seu dashboard está em:
echo https://gabriel019pira.github.io/dashboard-financeiro
echo.
pause
