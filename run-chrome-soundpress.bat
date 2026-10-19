@echo off
title SoundPress Chrome Companion
cd /d "%~dp0"

echo ========================================================
echo   SoundPress Chrome-Bound Companion
echo   - Active ONLY when Google Chrome is the focused window
echo   - Works on address bar, search, new tabs, and all pages
echo   - Automatically EXITS when Google Chrome is closed
echo ========================================================
echo.

python soundpress_chrome.py
