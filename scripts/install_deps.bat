@echo off
REM ============================================================
REM  OBSOverlay - install Python dependencies
REM ============================================================
setlocal
cd /d "%~dp0.."
echo Project dir: %CD%
echo.
echo This will install Python packages from requirements.txt:
type requirements.txt
echo.
set /p CONFIRM=Type YES to install, anything else to cancel:
if /i not "%CONFIRM%"=="YES" (
    echo Cancelled.
    pause
    exit /b 0
)

echo.
echo Installing dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] pip install failed. Is Python installed and on PATH?
    pause
    exit /b 1
)

echo.
echo Done!
pause
