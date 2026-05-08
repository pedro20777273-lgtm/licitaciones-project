@echo off
chcp 65001 >nul
title HOLOGIC IBERIA — Instalación automática
cd /d "%~dp0"

echo.
echo  ==========================================
echo   HOLOGIC IBERIA — Procesador Licitaciones
echo   Instalación automática
echo  ==========================================
echo.

REM ── ¿Ya está Python instalado? ────────────────────────────────────────────
python --version >nul 2>&1
if not errorlevel 1 goto :python_ok

py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON=py
    goto :python_ok
)

echo  Python no encontrado. Descargando e instalando...
echo  (Esto puede tardar 2-3 minutos, no cierres la ventana)
echo.

REM Descargar Python 3.12 con PowerShell
powershell -Command "& { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe' -OutFile '%TEMP%\python_installer.exe' }"

if not exist "%TEMP%\python_installer.exe" (
    echo.
    echo  ERROR: No se pudo descargar Python.
    echo  Comprueba tu conexión a internet.
    echo  O instálalo manualmente desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo  Instalando Python 3.12...
"%TEMP%\python_installer.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1 Include_tcltk=1

REM Refrescar PATH en esta sesión
for /f "tokens=*" %%i in ('powershell -NoProfile -Command "[System.Environment]::GetEnvironmentVariable(\"PATH\",\"User\")"') do set PATH=%%i;%PATH%

REM Dar tiempo a que el instalador termine
timeout /t 3 >nul

python --version >nul 2>&1
if errorlevel 1 (
    REM Cerrar y pedir que reabran
    echo.
    echo  ✔  Python instalado. Cierra esta ventana y
    echo     vuelve a hacer doble clic en este archivo.
    echo.
    pause
    exit /b 0
)

:python_ok
for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo  ✔  %%v encontrado
echo.

REM ── Verificar .env ────────────────────────────────────────────────────────
if not exist ".env" (
    echo  AVISO: No se encontró el archivo .env con las credenciales.
    echo  Asegúrate de que el archivo .env esté en la misma carpeta que este script.
    echo  Debería contener:
    echo    ANTHROPIC_API_KEY=sk-ant-...
    echo    GMAIL_USER=morontap4@gmail.com
    echo    GMAIL_APP_PASSWORD=...
    echo.
    pause
    exit /b 1
)
echo  ✔  .env encontrado

REM ── Instalar dependencias ─────────────────────────────────────────────────
echo  Instalando dependencias Python...
echo  (Primera vez tarda 2-3 minutos)
echo.
python -m pip install --upgrade pip --quiet 2>nul
python -m pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo.
    echo  Reintentando sin --quiet para ver el error...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo  ERROR instalando dependencias.
        pause
        exit /b 1
    )
)
echo  ✔  Dependencias instaladas
echo.

REM ── Crear carpetas necesarias ─────────────────────────────────────────────
if not exist "output" mkdir output
if not exist "templates\declaraciones" mkdir templates\declaraciones
if not exist "templates\excel" mkdir templates\excel

REM ── Crear lanzador VBS (sin ventana CMD) ──────────────────────────────────
set SCRIPT_DIR=%~dp0
set VBS_PATH=%SCRIPT_DIR%lanzar.vbs

(
    echo Set oShell = CreateObject^("WScript.Shell"^)
    echo oShell.CurrentDirectory = "%SCRIPT_DIR%"
    echo oShell.Run "python launcher.py", 0, False
) > "%VBS_PATH%"

REM ── Acceso directo en escritorio ──────────────────────────────────────────
set DESKTOP=%USERPROFILE%\Desktop

powershell -NoProfile -Command ^
    "$ws = New-Object -ComObject WScript.Shell; ^
     $sc = $ws.CreateShortcut('%DESKTOP%\Licitaciones Hologic.lnk'); ^
     $sc.TargetPath = 'wscript.exe'; ^
     $sc.Arguments = '\"%VBS_PATH%\"'; ^
     $sc.WorkingDirectory = '%SCRIPT_DIR%'; ^
     $sc.Description = 'Procesador de Licitaciones Hologic Iberia'; ^
     $sc.WindowStyle = 1; ^
     $sc.Save()" >nul 2>&1

echo  ✔  Acceso directo creado en el escritorio
echo.
echo  ==========================================
echo   ✔  Instalación completada
echo  ==========================================
echo.
echo  Abriendo la aplicación ahora...
timeout /t 2 >nul

start "" python launcher.py

echo.
echo  Si la ventana no apareció, haz doble clic en:
echo  "Licitaciones Hologic" en el escritorio.
echo.
pause
