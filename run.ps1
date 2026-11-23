# FreeShits manual run script for PowerShell
Set-Location -Path $PSScriptRoot

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "Starting FreeShits Server on http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Cyan

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "Error: Virtual environment .venv not found!" -ForegroundColor Red
    pause
    exit 1
}

& ".\.venv\Scripts\python.exe" -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
