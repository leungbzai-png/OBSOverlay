@echo off
REM ============================================================
REM  OBSOverlay - install auto-start at Windows logon
REM  Creates a shortcut "OBS Overlay.lnk" in the user Startup folder.
REM ============================================================
setlocal
cd /d "%~dp0.."
echo Project dir: %CD%
echo.

REM If auto-detect fails, remove REM and set your pythonw.exe path:
REM set PYTHONW=C:\Python312\pythonw.exe

if not defined PYTHONW (
    for /f "delims=" %%i in ('where pythonw 2^>nul') do set PYTHONW=%%i
)

if not defined PYTHONW (
    echo [ERROR] pythonw.exe not found.
    echo Edit this bat, uncomment the PYTHONW line, set your pythonw.exe path.
    pause
    exit /b 1
)

set SCRIPT=%CD%\src\obs_overlay.pyw
set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set SHORTCUT=%STARTUP%\OBS Overlay.lnk

if not exist "%SCRIPT%" (
    echo [ERROR] %SCRIPT% not found.
    pause
    exit /b 1
)

echo The following auto-start entry will be created:
echo   Name:     OBS Overlay
echo   Python:   %PYTHONW%
echo   Script:   %SCRIPT%
echo   Shortcut: %SHORTCUT%
echo.
set /p CONFIRM=Type YES to create this startup entry, anything else to cancel:
if /i not "%CONFIRM%"=="YES" (
    echo Cancelled. Nothing was written.
    pause
    exit /b 0
)

powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%SHORTCUT%'); $s.TargetPath='%PYTHONW%'; $s.Arguments='\"%SCRIPT%\"'; $s.WorkingDirectory='%CD%'; $s.WindowStyle=7; $s.Save()"

echo.
echo ============================================
echo Startup shortcut created.
echo ============================================
echo.
echo Tip: make sure you created config.json first (see USER_GUIDE.md).
echo Starting now, check the system tray...
start "" "%PYTHONW%" "%SCRIPT%"
echo.
pause
