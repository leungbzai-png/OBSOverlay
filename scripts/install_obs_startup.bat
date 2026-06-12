@echo off
REM ============================================================
REM  OBSOverlay - install OBS Studio auto-start at Windows logon
REM  Creates a shortcut "OBS Studio.lnk" in the user Startup folder.
REM  Does NOT hardcode any install path; auto-detects common ones
REM  and otherwise asks you for the full path to obs64.exe.
REM ============================================================
setlocal
echo Locating obs64.exe ...
echo.

set OBS_EXE=
if exist "C:\Program Files\obs-studio\bin\64bit\obs64.exe" set OBS_EXE=C:\Program Files\obs-studio\bin\64bit\obs64.exe
if not defined OBS_EXE if exist "C:\Program Files (x86)\obs-studio\bin\64bit\obs64.exe" set OBS_EXE=C:\Program Files (x86)\obs-studio\bin\64bit\obs64.exe

if not defined OBS_EXE (
    echo Could not auto-detect OBS in the common install folders.
    echo Please paste the FULL path to obs64.exe
    echo   example: D:\OBS\obs-studio\bin\64bit\obs64.exe
    set /p OBS_EXE=obs64.exe path:
)

if not defined OBS_EXE (
    echo [ERROR] No path provided. Nothing was written.
    pause
    exit /b 1
)

if not exist "%OBS_EXE%" (
    echo [ERROR] File not found: %OBS_EXE%
    echo Nothing was written.
    pause
    exit /b 1
)

set OBS_DIR=
for %%I in ("%OBS_EXE%") do set OBS_DIR=%%~dpI

set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set SHORTCUT=%STARTUP%\OBS Studio.lnk

echo.
echo The following auto-start entry will be created:
echo   Name:     OBS Studio
echo   OBS exe:  %OBS_EXE%
echo   Shortcut: %SHORTCUT%
echo.
set /p CONFIRM=Type YES to create this startup entry, anything else to cancel:
if /i not "%CONFIRM%"=="YES" (
    echo Cancelled. Nothing was written.
    pause
    exit /b 0
)

powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%SHORTCUT%'); $s.TargetPath='%OBS_EXE%'; $s.Arguments='--minimize-to-tray --disable-shutdown-check'; $s.WorkingDirectory='%OBS_DIR%'; $s.Save()"

echo.
echo ============================================
echo OBS startup shortcut created.
echo ============================================
echo.
echo Next: in OBS - File - Settings - General - System Tray
echo   [x] Enable system tray icon
echo   [x] Minimize to system tray instead of taskbar
echo   [x] Always minimize to system tray instead of task bar
echo.
pause
