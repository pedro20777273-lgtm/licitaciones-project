@echo off
chcp 65001 >nul
cd /d "%~dp0"
python launcher.py
if errorlevel 1 (
    echo.
    echo  Error al iniciar. Asegúrate de haber ejecutado instalar_windows.bat primero.
    pause
)
