@echo off
REM Script para preparar o projeto para deploy
REM Execute este arquivo para preparar tudo automaticamente

echo.
echo ================================
echo   Preparando para Deploy
echo ================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Use o caminho completo: C:/Users/evand/AppData/Local/Programs/Python/Python314/python.exe
    pause
    exit /b 1
)

REM Verificar se pip está instalado
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] pip nao encontrado!
    pause
    exit /b 1
)

echo [1/5] Criando arquivo Procfile...
echo web: gunicorn run:app > Procfile
echo     OK!

echo.
echo [2/5] Instalando gunicorn...
pip install gunicorn psycopg2-binary
echo     OK!

echo.
echo [3/5] Atualizando requirements.txt...
pip freeze > requirements.txt
echo     OK!

echo.
echo [4/5] Verificando arquivos necessarios...

if not exist ".gitignore" (
    echo Criando .gitignore...
    (
        echo __pycache__/
        echo *.pyc
        echo *.pyo
        echo *.pyd
        echo .Python
        echo env/
        echo venv/
        echo instance/
        echo .env
        echo *.db
        echo *.sqlite
        echo *.sqlite3
        echo .DS_Store
        echo salao.db
    ) > .gitignore
    echo     OK!
) else (
    echo .gitignore ja existe
)

echo.
echo [5/5] Inicializando Git (se necessario)...
git status >nul 2>&1
if errorlevel 1 (
    echo Inicializando repositorio Git...
    git init
    git add .
    git commit -m "Initial commit - Sistema de agendamento para salao"
    echo     OK!
) else (
    echo Git ja inicializado
)

echo.
echo ================================
echo   PREPARACAO CONCLUIDA!
echo ================================
echo.
echo Proximos passos:
echo.
echo 1. Criar repositorio no GitHub:
echo    https://github.com/new
echo.
echo 2. Conectar repositorio:
echo    git remote add origin https://github.com/SEU_USUARIO/salao-agendamento.git
echo    git push -u origin main
echo.
echo 3. Deploy no Render:
echo    - Acesse: https://dashboard.render.com
echo    - Clique em: New +^>Web Service
echo    - Selecione seu repositorio
echo.
echo Leia o arquivo DEPLOY.md para mais detalhes!
echo.
pause
