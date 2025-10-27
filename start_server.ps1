# Скрипт запуску сервера dt4research
# Автоматично активує віртуальне середовище та запускає FastAPI сервер

# Встановлюємо UTF-8 кодування для правильного відображення українських символів
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "🚀 Запуск dt4research..." -ForegroundColor Cyan
Write-Host "📦 Запускаємо FastAPI сервер через віртуальне середовище..." -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan

# Використовуємо Python з віртуального середовища для запуску uvicorn
& .\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Помилка запуску сервера" -ForegroundColor Red
    exit 1
}
