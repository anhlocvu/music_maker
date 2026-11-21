@echo off
setlocal EnableExtensions

set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
for %%I in ("%SCRIPT_DIR%\..") do set "REPO_DIR=%%~fI"
set "PY_SCRIPT=%SCRIPT_DIR%\generate_midi_map.py"
set "NO_PAUSE=0"
if /I "%~1"=="--no-pause" set "NO_PAUSE=1"

echo ==================================================
echo   Tao Ban Do MIDI (music_maker_plugin/midi_map.md)
echo ==================================================
echo.

where uv >nul 2>&1
if not errorlevel 1 (
    uv run --project "%REPO_DIR%" --with mido python "%PY_SCRIPT%"
    goto :done
)

where py >nul 2>&1
if not errorlevel 1 (
    py "%PY_SCRIPT%"
    goto :done
)

where python >nul 2>&1
if not errorlevel 1 (
    python "%PY_SCRIPT%"
    goto :done
)

echo [LOI] Khong tim thay uv, py hoac python.
if "%NO_PAUSE%"=="0" pause
exit /b 1

:done
set "EXIT_CODE=%errorlevel%"
echo.
if not "%EXIT_CODE%"=="0" goto :failed
echo [HOAN TAT] Da cap nhat music_maker_plugin\midi_map.md
if "%NO_PAUSE%"=="0" pause
exit /b 0

:failed
echo [LOI] Tao midi_map.md that bai - ma loi %EXIT_CODE%.
if "%NO_PAUSE%"=="0" pause
exit /b %EXIT_CODE%
