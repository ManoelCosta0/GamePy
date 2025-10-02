@echo off
echo Iniciando a configuracao do ambiente virtual...

:: 1. Cria o ambiente virtual
python -m venv venv

:: 2. Ativa o ambiente virtual e instala as dependencias
call venv\Scripts\activate.bat
pip install -r requirements.txt

:: 3. Informa o usuario que a configuracao terminou
echo.
echo ===========================================
echo Configuracao concluida!
echo Agora voce pode executar o jogo com:
echo.
echo python src/main.py
echo ===========================================

pause