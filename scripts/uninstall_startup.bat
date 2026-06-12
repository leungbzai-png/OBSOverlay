@echo off
REM ============================================================
REM  OBSOverlay - remove the auto-start entry created by this project
REM  Only deletes "OBS Overlay.lnk" (created by install_startup.bat).
REM ============================================================
setlocal
set SHORTCUT=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\OBS Overlay.lnk

echo This will remove the OBSOverlay auto-start entry:
echo   %SHORTCUT%
echo.
if not exist "%SHORTCUT%" (
    echo No startup shortcut found. Nothing to do.
    pause
    exit /b 0
)

set /p CONFIRM=Type YES to remove it, anything else to cancel:
if /i not "%CONFIRM%"=="YES" (
    echo Cancelled.
    pause
    exit /b 0
)

del "%SHORTCUT%"
echo Startup shortcut removed.
echo.
echo Tip: if the program is running, right-click the tray icon - Quit.
pause
