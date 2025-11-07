@echo off
REM Скрипт запуску сервера dt4research
REM Автоматично активує віртуальне середовище та запускає FastAPI сервер

REM Установлюємо UTF-8 кодову сторінку для коректної кирилиці (Windows CMD)
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

echo Запуск dt4research...
echo Перевірка існуючих процесів сервера...

REM Stop processes using port 8000 (Зупинити процеси, які використовують порт 8000)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Зупиняємо процес %%a на порту 8000
    taskkill /F /PID %%a >nul 2>&1
)

timeout /t 2 /nobreak >nul
echo Існуючі процеси зупинено (якщо були).
echo.
echo Активуємо віртуальне середовище...

REM Активуємо віртуальне середовище
call venv\Scripts\activate.bat

if %errorlevel% equ 0 (
    echo Віртуальне середовище активовано
    echo Запускаємо FastAPI сервер...
    echo -----------------------------------------------
    
    REM Запускаємо uvicorn з віртуального середовища
    python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
) else (
    echo Помилка активації віртуального середовища
    exit /b 1
)

