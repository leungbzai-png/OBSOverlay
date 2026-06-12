@echo off
REM ============================================================
REM  OBSOverlay - remove the OBS Studio auto-start entry
REM  created by this project. Only deletes "OBS Studio.lnk".
REM ============================================================
setlocal
set SHORTCUT=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\OBS Studio.lnk

echo This will remove the OBS Studio auto-start entry:
echo   %SHORTCUT%
echo.
if not exist "%SHORTCUT%" (
    echo No OBS startup shortcut found. Nothing to do.
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
echo OBS startup shortcut removed.
pause
