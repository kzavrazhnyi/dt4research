# Script to start dt4research server
# Automatically starts FastAPI server using venv Python

# Set UTF-8 encoding for proper Unicode output
[Console]::InputEncoding  = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding           = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'

# Ensure Python uses UTF-8 for stdio
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUTF8 = '1'

# Set console code page to UTF-8
try { chcp 65001 | Out-Null } catch {}

Write-Host "Starting dt4research..." -ForegroundColor Cyan
Write-Host "Starting FastAPI server via virtual environment..." -ForegroundColor Yellow
Write-Host "-----------------------------------------------" -ForegroundColor Cyan

# Use Python from virtual environment to run uvicorn
& .\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

if ($LASTEXITCODE -ne 0) {
    Write-Host "Помилка запуску сервера" -ForegroundColor Red
    exit 1
}
