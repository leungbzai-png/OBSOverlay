@echo off
REM ============================================================
REM  OBSOverlay - safe reset / clean
REM ============================================================
REM  This script ONLY touches things created by THIS project:
REM    - the "OBS Overlay.lnk" auto-start entry
REM    - the "OBS Studio.lnk" auto-start entry
REM    - this project's __pycache__ / logs / temp / cache folders
REM    - optionally this project's local config.json (extra confirm)
REM
REM  It NEVER deletes project source folders, parent folders,
REM  the old E:\OBSOverlay folder, or any release folder.
REM  It NEVER kills unrelated processes or uninstalls other apps.
REM ============================================================
setlocal EnableDelayedExpansion
cd /d "%~dp0.."
set PROJECT_DIR=%CD%

echo ============================================================
echo OBSOverlay safe reset
echo Project dir: %PROJECT_DIR%
echo ============================================================
echo.
echo This will remove the following, each with confirmation:
echo   1) Auto-start entry: OBS Overlay.lnk
echo   2) Auto-start entry: OBS Studio.lnk
echo   3) This project's __pycache__ / logs / temp / cache
echo   4) (Optional, separate confirm) local config.json
echo.
echo Before any deletion the target path is shown.
echo If a path cannot be confirmed as belonging to this project, it is skipped.
echo.
set /p GO=Type YES to begin, anything else to cancel:
if /i not "%GO%"=="YES" (
    echo Cancelled. Nothing was changed.
    pause
    exit /b 0
)

echo.
echo --- [1/4] OBSOverlay auto-start entry ---
set LNK1=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\OBS Overlay.lnk
echo Target: %LNK1%
if exist "%LNK1%" (
    set /p C1=Type YES to delete this entry:
    if /i "!C1!"=="YES" ( del "%LNK1%" & echo   Removed. ) else ( echo   Skipped. )
) else (
    echo   Not present. Skipped.
)

echo.
echo --- [2/4] OBS Studio auto-start entry ---
set LNK2=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\OBS Studio.lnk
echo Target: %LNK2%
if exist "%LNK2%" (
    set /p C2=Type YES to delete this entry:
    if /i "!C2!"=="YES" ( del "%LNK2%" & echo   Removed. ) else ( echo   Skipped. )
) else (
    echo   Not present. Skipped.
)

echo.
echo --- [3/4] Project temp / cache / logs ---
for %%D in ("%PROJECT_DIR%\src\__pycache__" "%PROJECT_DIR%\logs" "%PROJECT_DIR%\temp" "%PROJECT_DIR%\cache") do (
    if exist "%%~D" (
        echo Target: %%~D
        set /p C3=Type YES to delete this folder:
        if /i "!C3!"=="YES" ( rd /s /q "%%~D" & echo   Removed. ) else ( echo   Skipped. )
    )
)

echo.
echo --- [4/4] Local config.json (contains your OBS password) ---
set CFG=%PROJECT_DIR%\config.json
echo Target: %CFG%
if exist "%CFG%" (
    echo WARNING: deleting config.json removes your saved OBS WebSocket settings.
    set /p C4=Type DELETE to remove config.json, anything else to keep it:
    if /i "!C4!"=="DELETE" ( del "%CFG%" & echo   config.json removed. ) else ( echo   Kept config.json. )
) else (
    echo   Not present. Skipped.
)

echo.
echo ============================================================
echo Reset complete.
echo Tip: if the overlay is still running, right-click the tray icon - Quit.
echo ============================================================
pause
