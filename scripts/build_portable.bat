@echo off
REM ============================================================
REM  OBSOverlay - build the portable edition (OBSOverlay.exe + zips)
REM  - Installs/checks deps + PyInstaller
REM  - Builds a windowed (no-console) onefile OBSOverlay.exe
REM  - Assembles a portable folder and zips it
REM  - Builds a source zip via "git archive HEAD"
REM
REM  Output goes OUTSIDE the repo, to:
REM    E:\Backup\Releases\OBSOverlay\%VER%\   (VER set below)
REM  Run the SOURCE-zip step AFTER committing so it captures the tagged code.
REM ============================================================
setlocal
cd /d "%~dp0.."
echo Project dir: %CD%
echo.

set VER=v0.2.1
set RELROOT=E:\Backup\Releases\OBSOverlay\%VER%
set PORTNAME=OBSOverlay-%VER%-portable
set PORTDIR=%RELROOT%\%PORTNAME%
set PORTZIP=%RELROOT%\%PORTNAME%.zip
set SRCZIP=%RELROOT%\OBSOverlay-%VER%-source.zip

REM ---- 1. Python ----
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found on PATH. Install Python 3 and retry.
    pause
    exit /b 1
)

REM ---- 2. Dependencies + PyInstaller ----
echo Installing/checking runtime dependencies...
python -m pip install -r requirements.txt
echo Installing/checking PyInstaller...
python -m pip install pyinstaller

REM ---- 3. Clean previous build/dist ----
echo Cleaning build / dist ...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM ---- 4. Build OBSOverlay.exe (onefile, windowed = no console) ----
echo Building OBSOverlay.exe ...
python -m PyInstaller --noconfirm --clean --onefile --windowed ^
    --name OBSOverlay ^
    --hidden-import pystray._win32 ^
    --distpath dist --workpath build --specpath build ^
    src\obs_overlay.pyw
if not exist "dist\OBSOverlay.exe" (
    echo [ERROR] Build failed: dist\OBSOverlay.exe not found.
    pause
    exit /b 1
)
echo Built: dist\OBSOverlay.exe

REM ---- 5. Assemble portable folder ----
echo Assembling portable folder: %PORTDIR%
if exist "%PORTDIR%" rmdir /s /q "%PORTDIR%"
mkdir "%PORTDIR%"
copy /y "dist\OBSOverlay.exe" "%PORTDIR%\OBSOverlay.exe" >nul
copy /y "config.example.json" "%PORTDIR%\config.example.json" >nul
copy /y "README.md" "%PORTDIR%\README.md" >nul
copy /y "LICENSE" "%PORTDIR%\LICENSE" >nul
xcopy /e /i /y /q "docs" "%PORTDIR%\docs" >nul
xcopy /e /i /y /q "scripts" "%PORTDIR%\scripts" >nul
mkdir "%PORTDIR%\logs" 2>nul
mkdir "%PORTDIR%\cache" 2>nul
mkdir "%PORTDIR%\data" 2>nul

REM ---- 6. Portable zip ----
echo Creating portable zip: %PORTZIP%
if exist "%PORTZIP%" del /q "%PORTZIP%"
powershell -NoProfile -Command "Compress-Archive -Path '%PORTDIR%\*' -DestinationPath '%PORTZIP%' -Force"

REM ---- 7. Source zip (git tracked files only) ----
echo Creating source zip: %SRCZIP%
git archive --format=zip -o "%SRCZIP%" HEAD
if errorlevel 1 (
    echo [WARN] git archive failed - commit your changes, then re-run this step.
)

echo.
echo ============================================
echo Portable build complete.
echo   EXE:          dist\OBSOverlay.exe
echo   Portable dir: %PORTDIR%
echo   Portable zip: %PORTZIP%
echo   Source zip:   %SRCZIP%
echo ============================================
echo.
echo Reminder: config.json is NEVER bundled. Users create it on first launch.
pause
