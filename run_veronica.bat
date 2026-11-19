@echo off
title VERONICA AI Voice Assistant [MK-IV]
cd /d "%~dp0"

echo ========================================================
echo        STARTING VERONICA TACTICAL AI VOICE ASSISTANT
echo ========================================================
echo.

if exist "myvenv\Scripts\python.exe" (
    echo [INFO] Virtual environment detected. Launching VERONICA...
    myvenv\Scripts\python.exe main.py
) else (
    echo [INFO] Using system Python to launch VERONICA...
    python main.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] An error occurred while running VERONICA.
    pause
)
