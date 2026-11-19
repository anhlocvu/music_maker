@echo off
setlocal EnableExtensions

set "REPO_DIR=%~dp0"
if "%REPO_DIR:~-1%"=="\" set "REPO_DIR=%REPO_DIR:~0,-1%"
set "PLUGIN_DIR=%REPO_DIR%\music_maker_plugin"
set "REQ_FILE=%REPO_DIR%\requirements.txt"
set "PYPROJECT_FILE=%REPO_DIR%\pyproject.toml"
set "NO_PAUSE=0"
if /I "%~1"=="--no-pause" set "NO_PAUSE=1"

echo ==================================================
echo   Cai dat Global Antigravity Plugin: music-maker
echo ==================================================
echo.

set "AGY_CMD="
where agy >nul 2>&1
if not errorlevel 1 set "AGY_CMD=agy"
if not defined AGY_CMD if exist "%LOCALAPPDATA%\agy\bin\agy.exe" set "AGY_CMD=%LOCALAPPDATA%\agy\bin\agy.exe"

if not defined AGY_CMD (
    echo [LOI] Khong tim thay Antigravity CLI ^(agy.exe^).
    echo Vui long cai Antigravity CLI hoac them thu muc chua agy.exe vao PATH.
    call :maybe_pause
    exit /b 1
)

echo [1/3] Kiem tra cau truc plugin bang Antigravity CLI...
"%AGY_CMD%" plugin validate "%PLUGIN_DIR%" --strict
if errorlevel 1 (
    echo [LOI] Plugin khong dat kiem tra validate.
    call :maybe_pause
    exit /b 1
)
echo.

echo [2/3] Cai dat plugin toan cuc qua Antigravity CLI...
"%AGY_CMD%" plugin install "%PLUGIN_DIR%"
if errorlevel 1 (
    echo [THONG BAO] Thu go ban cu va cai lai ban moi...
    "%AGY_CMD%" plugin uninstall music-maker-plugin >nul 2>&1
    "%AGY_CMD%" plugin uninstall music_maker_plugin >nul 2>&1
    "%AGY_CMD%" plugin install "%PLUGIN_DIR%"
    if errorlevel 1 (
        echo [LOI] Khong the cai dat plugin bang Antigravity CLI.
        call :maybe_pause
        exit /b 1
    )
)
"%AGY_CMD%" plugin enable music-maker-plugin >nul 2>&1
if errorlevel 1 "%AGY_CMD%" plugin enable music_maker_plugin >nul 2>&1
echo.

echo [3/3] Cai dat thu vien Python trong requirements.txt...
call :install_python_deps
echo.

echo [HOAN TAT] Danh sach plugin hien tai:
"%AGY_CMD%" plugin list
echo.
call :maybe_pause
exit /b 0

:install_python_deps
where uv >nul 2>&1
if not errorlevel 1 (
    if not exist "%PYPROJECT_FILE%" (
        uv init --bare --no-readme --no-pin-python --vcs none "%REPO_DIR%"
        if errorlevel 1 exit /b %errorlevel%
    )
    uv add --project "%REPO_DIR%" -r "%REQ_FILE%"
    exit /b %errorlevel%
)
where py >nul 2>&1
if not errorlevel 1 (
    py -m pip install -r "%REQ_FILE%"
    exit /b %errorlevel%
)
where python >nul 2>&1
if not errorlevel 1 (
    python -m pip install -r "%REQ_FILE%"
    exit /b %errorlevel%
)
echo [CANH BAO] Khong tim thay uv / py / python. Vui long cai thu cong:
echo   uv add -r "%REQ_FILE%"
echo   hoac: pip install -r "%REQ_FILE%"
exit /b 0

:maybe_pause
if "%NO_PAUSE%"=="0" pause
exit /b 0
