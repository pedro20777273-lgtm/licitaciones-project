@echo off
chcp 65001 >nul
title HOLOGIC IBERIA — Instalación
cd /d "%~dp0"

echo.
echo  ==========================================
echo   HOLOGIC IBERIA — Instalacion automatica
echo  ==========================================
echo.

REM ── 1. Buscar Python ──────────────────────────────────────────────────────
set PYTHON=
for %%p in (python.exe py.exe) do (
    if not defined PYTHON (
        where %%p >nul 2>&1 && set "PYTHON=%%p"
    )
)

if not defined PYTHON goto :INSTALAR_PYTHON
%PYTHON% --version >nul 2>&1 && goto :PYTHON_OK

:INSTALAR_PYTHON
echo  Descargando Python 3.12...

REM Escribir script PS1 a disco (evita problemas con ^ en lineas largas)
(
echo [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
echo $url = 'https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe'
echo $out = "$env:TEMP\py_setup.exe"
echo Invoke-WebRequest -Uri $url -OutFile $out -UseBasicParsing
) > "%TEMP%\dl_python.ps1"

powershell -NoProfile -ExecutionPolicy Bypass -File "%TEMP%\dl_python.ps1"
del "%TEMP%\dl_python.ps1" >nul 2>&1

if not exist "%TEMP%\py_setup.exe" (
    echo.
    echo  ERROR: No se pudo descargar Python.
    echo  Descargalo manualmente de: https://www.python.org/downloads/
    echo  Marca "Add Python to PATH" y vuelve a ejecutar SETUP.bat
    pause & exit /b 1
)

echo  Instalando Python, espera...
"%TEMP%\py_setup.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1 Include_tcltk=1
del "%TEMP%\py_setup.exe" >nul 2>&1
timeout /t 5 >nul

REM Recargar PATH
(
echo $u = [Environment]::GetEnvironmentVariable('PATH','User')
echo $m = [Environment]::GetEnvironmentVariable('PATH','Machine')
echo [Environment]::SetEnvironmentVariable('PATH', "$u;$m", 'Process')
) > "%TEMP%\reload_path.ps1"
for /f "delims=" %%i in ('powershell -NoProfile -ExecutionPolicy Bypass -Command "[Environment]::GetEnvironmentVariable(\"PATH\",\"User\")"') do set "PATH=%%i;%PATH%"
del "%TEMP%\reload_path.ps1" >nul 2>&1

set PYTHON=python
%PYTHON% --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  Python instalado. Cierra esta ventana y haz doble clic en SETUP.bat de nuevo.
    pause & exit /b 0
)

:PYTHON_OK
for /f "tokens=*" %%v in ('%PYTHON% --version 2^>^&1') do echo  OK  %%v

REM ── 2. Crear .env ─────────────────────────────────────────────────────────
if not exist ".env" (
    echo  Configurando credenciales...
    (
    echo $b64 = 'QU5USFJPUElDX0FQSV9LRVk9c2stYW50LWFwaTAzLUlvM0IwcWZGZ2hLUlJMeW53WGRXM3dXUjdtVF9UZVVHZ1BvNWl4c25fV1ptWDV6NmxoZzBXVmRXanI3Z0hPXzdjazRtY1pjdkRJbXBsUmlnVjlWWXR3LWZWZW1JUUFBCkdNQUlMX1VTRVI9bW9yb250YXA0QGdtYWlsLmNvbQpHTUFJTF9BUFBfUEFTU1dPUkQ9cHdvYnd0YXNucHhwa3dhaw=='
    echo $txt = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($b64))
    echo [IO.File]::WriteAllText('.env', $txt)
    ) > "%TEMP%\mk_env.ps1"
    powershell -NoProfile -ExecutionPolicy Bypass -File "%TEMP%\mk_env.ps1"
    del "%TEMP%\mk_env.ps1" >nul 2>&1
    echo  OK  Credenciales configuradas
)

REM ── 3. Carpetas ───────────────────────────────────────────────────────────
if not exist "output"                  mkdir output
if not exist "templates\declaraciones" mkdir templates\declaraciones
if not exist "templates\excel"         mkdir templates\excel

REM ── 4. Dependencias ───────────────────────────────────────────────────────
echo  Instalando dependencias (puede tardar 3-4 min la primera vez)...
%PYTHON% -m pip install --upgrade pip -q
%PYTHON% -m pip install -r requirements.txt -q
if errorlevel 1 (
    echo.
    echo  Reintentando con mas detalle...
    %PYTHON% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo  ERROR: fallo la instalacion de dependencias.
        pause & exit /b 1
    )
)
echo  OK  Dependencias instaladas

REM ── 5. Acceso directo ─────────────────────────────────────────────────────
set "HERE=%~dp0"
(
echo Set sh = CreateObject("WScript.Shell"^)
echo sh.CurrentDirectory = "%HERE%"
echo sh.Run "python launcher.py", 0, False
) > "%HERE%lanzar.vbs"

(
echo $ws = New-Object -ComObject WScript.Shell
echo $sc = $ws.CreateShortcut("$env:USERPROFILE\Desktop\Licitaciones Hologic.lnk"^)
echo $sc.TargetPath = 'wscript.exe'
echo $sc.Arguments = '"%HERE%lanzar.vbs"'
echo $sc.WorkingDirectory = '%HERE%'
echo $sc.Description = 'Procesador Licitaciones Hologic Iberia'
echo $sc.Save(^)
) > "%TEMP%\mk_sc.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "%TEMP%\mk_sc.ps1"
del "%TEMP%\mk_sc.ps1" >nul 2>&1
echo  OK  Icono creado en el escritorio

echo.
echo  ==========================================
echo   Instalacion completada. Abriendo app...
echo  ==========================================
echo.
timeout /t 2 >nul
start "" %PYTHON% launcher.py
