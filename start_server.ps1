# Script to start dt4research server (Скрипт запуску сервера dt4research)
# Automatically starts FastAPI server using venv Python (Автоматично запускає FastAPI сервер через Python з venv)

# Set UTF-8 encoding for proper Ukrainian symbols (Встановлюємо UTF-8 для коректних українських символів)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "🚀 Запуск dt4research..." -ForegroundColor Cyan
Write-Host "📦 Запускаємо FastAPI сервер через віртуальне середовище..." -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan

# Use Python from virtual environment to run uvicorn (Використати Python з віртуального середовища для uvicorn)
& .\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Помилка запуску сервера" -ForegroundColor Red
    exit 1
}
