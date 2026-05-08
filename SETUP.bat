@echo off
chcp 65001 >nul
title HOLOGIC IBERIA — Instalación automática
cd /d "%~dp0"

echo.
echo  ==========================================
echo   HOLOGIC IBERIA — Procesador Licitaciones
echo   Configuración automática completa
echo  ==========================================
echo.

REM ── 1. Comprobar o instalar Python ────────────────────────────────────────
python --version >nul 2>&1
if not errorlevel 1 goto :PYTHON_OK

py --version >nul 2>&1
if not errorlevel 1 goto :PYTHON_OK

echo  Descargando Python 3.12 (puede tardar 1-2 min)...
powershell -NoProfile -Command "& { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe' -OutFile '%TEMP%\py_setup.exe' -UseBasicParsing }"

if not exist "%TEMP%\py_setup.exe" (
    echo.
    echo  ERROR: Sin conexión a internet o descarga fallida.
    echo  Instala Python manualmente: https://www.python.org/downloads/
    echo  Marca "Add Python to PATH" al instalar y vuelve a ejecutar este archivo.
    pause & exit /b 1
)

echo  Instalando Python...
"%TEMP%\py_setup.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1 Include_tcltk=1
del /f "%TEMP%\py_setup.exe" >nul 2>&1

REM Recargar PATH
for /f "delims=" %%i in ('powershell -NoProfile -Command "[Environment]::GetEnvironmentVariable(\"PATH\",\"User\")"') do set "PATH=%%i;%PATH%"
timeout /t 2 >nul

python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  Python instalado. Cierra esta ventana y vuelve a abrirla.
    pause & exit /b 0
)

:PYTHON_OK
for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo  OK  %%v

REM ── 2. Crear .env con credenciales ────────────────────────────────────────
if not exist ".env" (
    echo  Configurando credenciales...
    powershell -NoProfile -Command ^
        "[IO.File]::WriteAllText('.env', [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('QU5USFJPUElDX0FQSV9LRVk9c2stYW50LWFwaTAzLUlvM0IwcWZGZ2hLUlJMeW53WGRXM3dXUjdtVF9UZVVHZ1BvNWl4c25fV1ptWDV6NmxoZzBXVmRXanI3Z0hPXzdjazRtY1pjdkRJbXBsUmlnVjlWWXR3LWZWZW1JUUFBCkdNQUlMX1VTRVI9bW9yb250YXA0QGdtYWlsLmNvbQpHTUFJTF9BUFBfUEFTU1dPUkQ9cHdvYnd0YXNucHhwa3dhaw==')))"
    echo  OK  Credenciales configuradas
)

REM ── 3. Crear carpetas necesarias ──────────────────────────────────────────
if not exist "output"                   mkdir output
if not exist "templates\declaraciones"  mkdir templates\declaraciones
if not exist "templates\excel"          mkdir templates\excel

REM ── 4. Instalar dependencias Python ───────────────────────────────────────
echo  Instalando dependencias (primera vez tarda 2-3 min)...
python -m pip install --upgrade pip --quiet 2>nul
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo  Reintentando...
    python -m pip install -r requirements.txt
    if errorlevel 1 ( echo  ERROR en dependencias & pause & exit /b 1 )
)
echo  OK  Dependencias instaladas

REM ── 5. Crear acceso directo en escritorio ────────────────────────────────
set "HERE=%~dp0"
set "VBS=%HERE%lanzar.vbs"

(
    echo Set sh = CreateObject^("WScript.Shell"^)
    echo sh.CurrentDirectory = "%HERE%"
    echo sh.Run "python launcher.py", 0, False
) > "%VBS%"

powershell -NoProfile -Command ^
    "$ws=New-Object -ComObject WScript.Shell; ^
     $sc=$ws.CreateShortcut('%USERPROFILE%\Desktop\Licitaciones Hologic.lnk'); ^
     $sc.TargetPath='wscript.exe'; ^
     $sc.Arguments='\"%VBS%\"'; ^
     $sc.WorkingDirectory='%HERE%'; ^
     $sc.Description='Procesador de Licitaciones Hologic Iberia'; ^
     $sc.Save()" >nul 2>&1
echo  OK  Acceso directo creado en el escritorio

echo.
echo  ==========================================
echo   Instalacion completada. Abriendo app...
echo  ==========================================
echo.
timeout /t 2 >nul
start "" python "%HERE%launcher.py"
