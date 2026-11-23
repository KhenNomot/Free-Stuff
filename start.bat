@echo off
title FreeShits Server
cd /d "%~dp0"

echo ====================================================
echo Starting FreeShits Server on http://127.0.0.1:8000
echo ====================================================

if not exist ".venv\Scripts\python.exe" (
    echo Error: Virtual environment .venv not found!
    pause
    exit /b 1
)

.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload

pause
