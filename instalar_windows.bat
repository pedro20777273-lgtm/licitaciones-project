@echo off
chcp 65001 >nul
title HOLOGIC IBERIA — Instalación

echo.
echo ==========================================
echo  HOLOGIC IBERIA — Instalador
echo ==========================================
echo.

REM ── Comprobar Python ──────────────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python no encontrado.
    echo.
    echo  Instala Python desde:
    echo    https://www.python.org/downloads/
    echo.
    echo  IMPORTANTE: marca la casilla
    echo    "Add Python to PATH"  al instalar.
    echo.
    pause
    start https://www.python.org/downloads/
    exit /b 1
)

for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo  Python encontrado: %%v
echo.

REM ── Instalar dependencias ─────────────────────────────────────────────────
echo  Instalando dependencias (puede tardar 2-3 minutos)...
echo.
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo.
    echo  ERROR al instalar dependencias.
    echo  Prueba ejecutar como Administrador.
    pause
    exit /b 1
)

echo.
echo  ✔  Dependencias instaladas correctamente.
echo.

REM ── Crear acceso directo en el escritorio ─────────────────────────────────
echo  Creando acceso directo en el escritorio...

set SCRIPT_DIR=%~dp0
set LANZADOR=%SCRIPT_DIR%lanzar.vbs

REM Create VBScript launcher (no CMD window)
(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo WshShell.CurrentDirectory = "%SCRIPT_DIR%"
echo WshShell.Run "python launcher.py", 0, False
) > "%LANZADOR%"

REM Create desktop shortcut
set DESKTOP=%USERPROFILE%\Desktop
powershell -Command ^
  "$ws = New-Object -ComObject WScript.Shell; ^
   $s = $ws.CreateShortcut('%DESKTOP%\Licitaciones Hologic.lnk'); ^
   $s.TargetPath = '%LANZADOR%'; ^
   $s.WorkingDirectory = '%SCRIPT_DIR%'; ^
   $s.Description = 'Procesador de Licitaciones Hologic Iberia'; ^
   $s.Save()"

echo  ✔  Acceso directo creado en el escritorio.
echo.
echo ==========================================
echo  Instalación completada.
echo  Abre "Licitaciones Hologic" en el escritorio.
echo ==========================================
echo.
pause
