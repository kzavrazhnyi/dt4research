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

# Stop existing server processes (Зупинити існуючі процеси сервера)
Write-Host "Checking for existing server processes..." -ForegroundColor DarkYellow

# Helper: get process IDs by port (Допоміжна функція: отримати PID за портом)
function Get-PortProcessIds {
    param(
        [Parameter(Mandatory = $true)]
        [int]$Port
    )

    netstat -ano | Select-String ":$Port" | ForEach-Object {
        $line = $_.ToString()
        $segments = ($line -replace '\s+', ' ').Trim().Split(' ')
        if ($segments.Count -gt 0) {
            $pidCandidate = $segments[-1]
            if ($pidCandidate -match '^\d+$') {
                [int]$pidCandidate
            }
        }
    } | Sort-Object -Unique
}

# Helper: stop processes listening on a port (Допоміжна функція: завершити процеси на порту)
function Stop-PortProcesses {
    param(
        [Parameter(Mandatory = $true)]
        [int]$Port,
        [int]$Attempts = 5
    )

    for ($i = 1; $i -le $Attempts; $i++) {
        $portProcesses = Get-PortProcessIds -Port $Port
        if (-not $portProcesses) {
            return $true
        }

        foreach ($processId in $portProcesses) {
            try {
                $processObj = Get-Process -Id $processId -ErrorAction SilentlyContinue
                if ($processObj) {
                    Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
                    Write-Host "  Stopping process $processId (attempt $i)" -ForegroundColor DarkGray
                    try {
                        Wait-Process -Id $processId -Timeout 3 -ErrorAction SilentlyContinue
                    } catch {
                        # Ignore timeout (Ігнорувати перевищення часу)
                    }
                }
            } catch {
                # Process already gone (Процес вже завершений)
            }
        }

        Start-Sleep -Seconds 1
    }

    return -not (Get-PortProcessIds -Port $Port)
}

# Stop Python processes from project venv (Зупинити процеси Python з venv проекту)
$pythonProcesses = Get-Process python* -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*dt4research*" }
if ($pythonProcesses) {
    Write-Host "Found $($pythonProcesses.Count) Python process(es) from project, stopping..." -ForegroundColor Yellow
    $pythonProcesses | ForEach-Object {
        try {
            Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
            Write-Host "  Stopping python PID $($_.Id)" -ForegroundColor DarkGray
            try {
                Wait-Process -Id $_.Id -Timeout 3 -ErrorAction SilentlyContinue
            } catch {}
        } catch {}
    }
    Start-Sleep -Seconds 1
}

if (Stop-PortProcesses -Port 8000) {
    Write-Host "Existing processes stopped." -ForegroundColor Green
} else {
    Write-Host "Warning: some processes still using port 8000 (Увага: деякі процеси досі використовують порт 8000)" -ForegroundColor Red
}

Write-Host ""

# Load .env file if present (Завантажити .env, якщо існує)
$envPath = Join-Path -Path (Get-Location) -ChildPath ".env"
if (Test-Path $envPath) {
    Write-Host "Loading environment from .env (Локальні змінні оточення)" -ForegroundColor DarkCyan
    Get-Content $envPath | ForEach-Object {
        $line = $_.Trim()
        if (-not [string]::IsNullOrWhiteSpace($line) -and -not $line.StartsWith('#') -and $line.Contains('=')) {
            $idx = $line.IndexOf('=')
            $key = $line.Substring(0, $idx).Trim()
            $val = $line.Substring($idx + 1).Trim()
            # Remove surrounding quotes if any (Прибрати лапки навколо значення)
            if (($val.StartsWith('"') -and $val.EndsWith('"')) -or ($val.StartsWith("'") -and $val.EndsWith("'"))) {
                $val = $val.Substring(1, $val.Length - 2)
            }
            [System.Environment]::SetEnvironmentVariable($key, $val)
            Set-Item -Path Env:$key -Value $val | Out-Null
        }
    }
}

# Use Python from virtual environment to run uvicorn
& .\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

if ($LASTEXITCODE -ne 0) {
    Write-Host "Server startup error (Помилка запуску сервера)" -ForegroundColor Red
    exit 1
}
