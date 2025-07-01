@echo off
echo ========================================
echo    Sistema de Controle de Docagem
echo ========================================
echo.
echo Instalando dependencias...
pip install -r requirements.txt
echo.
echo Iniciando servidor...
echo.
echo Descubra seu IP executando 'ipconfig' em outro terminal
echo.
python controle.py
pause 