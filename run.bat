@echo off
title SoundPress Launcher
cd /d "%~dp0"

if exist "dist\SoundPress.exe" (
    echo Starting SoundPress (Standalone Windows App)...
    start "" "dist\SoundPress.exe"
    exit /b 0
)

if exist "dist\ShotgunKeyboard-Windows-x64.exe" (
    echo Starting SoundPress...
    start "" "dist\ShotgunKeyboard-Windows-x64.exe"
    exit /b 0
)

where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo Starting SoundPress with Python...
    start "" pythonw app.py
    exit /b 0
)

echo Neither dist\SoundPress.exe nor Python was found.
echo Please run: powershell -ExecutionPolicy Bypass -File .\download-windows-binary.ps1
pause
