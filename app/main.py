"""
FastAPI backend for dt4research cybernetic control system (Бекенд FastAPI для кібернетичної системи керування).
Implements the control loop: Manager Goal → Agent Analysis → State Update → Feedback (Реалізує цикл: Ціль менеджера → Аналіз агента → Оновлення стану → Зворотний зв'язок).
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import queue
import threading
import logging
import os
import json
import re  # For URL masking (Для маскування URL)
import uvicorn
from pathlib import Path
from datetime import datetime
from typing import List, Optional

from app.models import SystemState, KeyComponent, Resource, MechanismInput, ComponentType, ResourceType, MechanismResponse, SimulationMetrics, SimulationRunRequest
from app.agent_logic import run_mock_analysis
from app.db import create_db_and_tables
from app.repository import read_system_state, write_system_state, seed_initial_state, add_agent_run, clear_state_and_runs
from app.initial_state import INITIAL_STATE
from app.presentations_store import read_presentations, write_presentations
from app.simulation import run_simulation, get_simulation_history, get_simulation_summary, get_agent_logs_history
from app.analytics import calculate_metrics_from_state
from app.repository import get_simulation_metrics_by_run_id, get_latest_simulation_run_id, get_all_simulation_metrics
from fastapi.responses import Response
import csv
import io
# Universal URL credentials masker (Універсальна утиліта маскування облікових даних у URL)
def _mask_url_credentials(url: str) -> str:
    """
    Mask credentials in URL by replacing everything between '//' and '@' with '***'
    (Маскує облікові дані у URL, замінюючи все між '//' та '@' на '***').
    Handles cases where '@' may appear in password (Обробляє випадки, коли '@' може бути в паролі).
    Example: "postgres://user:pass@host.com" -> "postgres://***@host.com"
    """
    try:
        # Find the position of '//' and the last '@'
        # (Знайти позицію '//' та останній '@')
        start = url.find("//")
        if start == -1:
            return url  # No protocol prefix found (Не знайдено префікс протоколу)

        end = url.rfind("@")  # <-- Key fix: find last @ (Ключове виправлення: знайти останній @)
        if end == -1 or end < start:
            return url  # No '@' found after protocol (Не знайдено '@' після протоколу)

        # Rebuild the string: protocol + '***' + host part
        # (Перебудувати рядок: протокол + '***' + хост)
        return f"{url[:start+2]}***@{url[end+1:]}"
    except Exception as e:
        # Simplified fallback logic (Спрощена запасна логіка)
        logging.getLogger(__name__).warning("URL masking failed: %s", e)
        if "@" in url:
            return f"***@{url.split('@')[-1]}"
        return "URL [masking failed]"


# Initialize FastAPI app (Ініціалізація застосунку FastAPI)
app = FastAPI(title="dt4research - Cybernetic Control System", version="1.4.0")


# Configure CORS (Налаштування CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consider restricting in production (Розглянути обмеження у продакшені)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _configure_logging() -> None:
    """Configure logging depending on environment (Налаштувати логування залежно від оточення)."""
    log_format = os.getenv("LOG_FORMAT", "console").lower()
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.getLogger().handlers.clear()

    if log_format == "json":
        class JsonFormatter(logging.Formatter):
            def format(self, record: logging.LogRecord) -> str:
                payload = {
                    "level": record.levelname,
                    "name": record.name,
                    "message": record.getMessage(),
                    "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
                }
                return json.dumps(payload, ensure_ascii=False)

        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        logging.basicConfig(level=level, handlers=[handler])
    else:
        logging.basicConfig(
            level=level,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%H:%M:%S",
        )


_configure_logging()

# Templates and static files (Шаблони та статичні файли)
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/docs", StaticFiles(directory="docs"), name="docs")
app.mount("/plan", StaticFiles(directory="plan"), name="plan")

# Optional mount for local presentation static build (Опційне підключення локальної статичної презентації)
_local_prez_path = (Path(__file__).parent.parent / "research/03_presentations/adaptive_enterprise_slidev/dist").resolve()
_local_prez_url = "/presentations/local/adaptive_enterprise"
if _local_prez_path.exists():
    app.mount(_local_prez_url, StaticFiles(directory=str(_local_prez_path), html=True), name="presentations_local")


# Initial state used for seeding the database (Початковий стан для заповнення БД)
_initial_state = INITIAL_STATE


@app.on_event("startup")
def _startup_seed() -> None:
    """Create tables and seed initial data if needed (Створити таблиці та початкові дані)."""
    create_db_and_tables()
    seed_initial_state(_initial_state)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main HTML page (Віддавати головну HTML-сторінку)."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    """Render settings page (Віддати сторінку налаштувань)."""
    return templates.TemplateResponse("settings.html", {"request": request})

@app.get("/presentations", response_class=HTMLResponse)
async def presentations_page(request: Request):
    """List presentations with descriptions (Список презентацій із описами)."""
    items = read_presentations()
    local_available = _local_prez_path.exists()
    local_url = _local_prez_url if local_available else None
    return templates.TemplateResponse("presentations.html", {"request": request, "items": items, "local_available": local_available, "local_url": local_url})

@app.post("/presentations/add", response_class=HTMLResponse)
async def presentations_add(request: Request, title: str = Form(...), url: str = Form(...), description: str = Form("")):
    """
    Append a presentation link to JSON store (Додати посилання на презентацію у JSON).
    """
    items = read_presentations()
    items.append({"title": title.strip(), "url": url.strip(), "description": description.strip()})
    write_presentations(items)
    return templates.TemplateResponse("presentations.html", {"request": request, "items": items})

@app.get("/api/v1/system-state")
async def get_system_state() -> SystemState:
    """Return current system state (Повернути поточний стан системи)."""
    return read_system_state()


@app.get("/api/v1/health/db")
async def health_db():
    """
    Database health check (Перевірка підключення до БД).
    Always returns masked URL (Завжди повертає замаскований URL).
    """
    # Get URL and driver hint (Отримати URL та тип драйвера)
    from app.db import DATABASE_URL  # type: ignore
    # Get original URL from environment (not from db.py which might be modified)
    # (Отримати оригінальний URL з оточення, не з db.py, який може бути модифікований)
    import os
    original_url = os.getenv("DATABASE_URL", DATABASE_URL)
    masked_url = _mask_url_credentials(original_url)
    # Ensure masking is correct - if URL still contains anything between // and @, force mask
    # (Переконатися, що маскування правильне - якщо URL все ще містить щось між // та @, примусити маскування)
    if "//" in masked_url and "@" in masked_url:
        start = masked_url.find("//")
        end = masked_url.find("@")
        if start != -1 and end != -1 and end > start + 2:
            between = masked_url[start+2:end]
            if between != "***":
                # Force correct masking (Примусити правильне маскування)
                masked_url = f"{masked_url[:start+2]}***@{masked_url[end+1:]}"
    driver = "postgresql" if "postgresql" in original_url else "sqlite"

    try:
        # Trigger real connection via repository (Спробувати реальне підключення через репозиторій)
        from app.repository import read_system_state  # type: ignore
        read_system_state()
        return {"ok": True, "status": "connected", "url": masked_url, "driver": driver}
    except Exception as exc:
        # Mask any URLs in error message (Маскувати будь-які URL у повідомленні про помилку)
        error_msg = str(exc)
        error_msg = _mask_url_credentials(error_msg) if "//" in error_msg and "@" in error_msg else error_msg
        logging.getLogger(__name__).warning("DB health check failed: %s", exc)
        return {"ok": False, "status": "failed", "error": error_msg, "url": masked_url, "driver": driver}


@app.get("/api/v1/health/rabbit")
async def health_rabbit():
    """
    RabbitMQ health check (Перевірка підключення RabbitMQ/CloudAMQP).
    Always returns masked URL (Завжди повертає замаскований URL).
    """
    import os
    import logging as _logging
    import pika  # type: ignore

    masked_url = "N/A"
    try:
        # Build masked URL from env (Сформувати замаскований URL із оточення)
        real_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/%2F")
        # Always mask the URL (Завжди маскувати URL)
        masked_url = _mask_url_credentials(real_url)
        # Ensure masking was applied (Переконатися, що маскування застосовано)
        if masked_url == real_url and "//" in real_url and "@" in real_url:
            # Force masking if it didn't work (Примусити маскування, якщо не спрацювало)
            _logging.getLogger(__name__).error("URL masking failed for RabbitMQ, forcing mask")
            # Use rfind as fallback (Використати rfind як резервний варіант)
            start = real_url.find("//")
            end = real_url.rfind("@")
            if start != -1 and end != -1 and end > start:
                masked_url = f"{real_url[:start+2]}***@{real_url[end+1:]}"

        # Connect with real parameters (Підключення з реальними параметрами)
        try:
            from app.consumer import get_rabbit_params  # type: ignore
            params = get_rabbit_params()
        except Exception:
            params = pika.URLParameters(real_url)

        connection = pika.BlockingConnection(params)
        connection.close()

        return {"ok": True, "status": "connected", "url": masked_url, "driver": "pika"}
    except Exception as exc:
        # Mask any URLs in error message (Маскувати будь-які URL у повідомленні про помилку)
        error_msg = str(exc)
        error_msg = _mask_url_credentials(error_msg) if "//" in error_msg and "@" in error_msg else error_msg
        _logging.getLogger(__name__).warning("RabbitMQ health check failed: %s", exc)
        return {"ok": False, "status": "failed", "error": error_msg, "url": masked_url}


@app.post("/api/v1/apply-mechanism")
async def apply_mechanism(input_data: MechanismInput) -> MechanismResponse:
    """
    Main cybernetic control endpoint (Головний ендпоінт кібернетичного керування).
    Receives goal from manager, triggers agent analysis, updates system state (Отримує ціль, запускає аналіз агента, оновлює стан).
    """
    # Step 1: Get input
    goal = input_data.target_goal

    # Step 2: Read current state from DB and run agent analysis
    current_state = read_system_state()
    new_state, deltas, _ = run_mock_analysis(goal, current_state, capture_logs=False)

    # Step 3: Persist new state and the run history
    write_system_state(new_state)

    # Build explanation string (Сформувати текст пояснення)
    if deltas:
        parts = [f"{resource} +{delta}" for resource, delta in deltas.items()]
        explanation = "; ".join(parts)
    else:
        explanation = "Без змін"

    # Store agent run (Зберегти запуск агента)
    try:
        add_agent_run(goal, deltas, new_state)
    except Exception as exc:  # pragma: no cover
        logging.getLogger(__name__).warning("Failed to store agent run: %s", exc)

    return MechanismResponse(newState=new_state, explanation=explanation, explanation_details=deltas)


@app.get("/api/v1/agent-runs")
async def get_agent_runs(limit: int = 20, offset: int = 0):
    """Return paginated agent run history (Повернути історію запусків із пагінацією)."""
    from app.repository import list_agent_runs  # local import to avoid circular

    total, runs = list_agent_runs(limit=limit, offset=offset)
    items = [
        {
            "id": r.id,
            "timestamp": r.timestamp.isoformat() + "Z",
            "input_goal": r.input_goal,
            "applied_rules_explanation": json.loads(r.applied_rules_explanation),
        }
        for r in runs
    ]
    return {"total": total, "items": items, "limit": limit, "offset": offset}


@app.post("/api/v1/system-reset")
async def system_reset() -> SystemState:
    """Reset simulation to initial state (Скинути симуляцію до початкового стану)."""
    # Clear all tables (Очистити всі таблиці)
    clear_state_and_runs()
    # Seed initial state (Заповнити початковим станом)
    seed_initial_state(_initial_state)
    # Return initial state (Повернути початковий стан)
    return read_system_state()


@app.post("/api/v1/simulation/run", response_model=List[SimulationMetrics])
async def run_simulation_endpoint(request: SimulationRunRequest) -> List[SimulationMetrics]:
    """
    Run automated simulation and return time series of metrics (Запустити автоматичну симуляцію та повернути часовий ряд метрик).
    
    Args:
        request: Simulation parameters (Параметри симуляції)
    
    Returns:
        List of SimulationMetrics for each simulation step (Список SimulationMetrics для кожного кроку)
    """
    metrics_history = run_simulation(
        days=request.days,
        intensity=request.intensity,
        t_market=request.t_market,
        use_agent=request.use_agent
    )
    return metrics_history


@app.post("/api/v1/simulation/run-stream")
async def run_simulation_stream_endpoint(request: SimulationRunRequest):
    """
    Run simulation with real-time log streaming via Server-Sent Events (Запустити симуляцію з потоковою передачею логів через Server-Sent Events).
    
    Args:
        request: Simulation parameters (Параметри симуляції)
    
    Returns:
        StreamingResponse with SSE events (StreamingResponse з SSE подіями)
    """
    import queue
    
    log_queue = queue.Queue()
    metrics_result = []
    
    def log_callback(log_line: str):
        """Callback to send logs to queue (Callback для відправки логів у чергу)."""
        log_queue.put(log_line)
    
    async def generate():
        """Generate SSE events (Генерувати SSE події)."""
        # Start simulation in background thread (Запустити симуляцію у фоновому потоці)
        def run_sim():
            try:
                result = run_simulation(
                    days=request.days,
                    intensity=request.intensity,
                    t_market=request.t_market,
                    use_agent=request.use_agent,
                    log_callback=log_callback
                )
                metrics_result.extend(result)
                log_queue.put(None)  # Signal completion (Сигнал завершення)
            except Exception as e:
                log_queue.put(f"ERROR: {str(e)}")
                log_queue.put(None)
        
        sim_thread = threading.Thread(target=run_sim)
        sim_thread.start()
        
        # Stream logs as they arrive (Потоково передавати логи, коли вони надходять)
        while True:
            try:
                log_line = log_queue.get(timeout=0.1)
                if log_line is None:
                    # Simulation completed (Симуляція завершена)
                    yield f"data: {json.dumps({'type': 'complete', 'metrics_count': len(metrics_result)})}\n\n"
                    break
                else:
                    # Send log line (Відправити рядок логу)
                    yield f"data: {json.dumps({'type': 'log', 'message': log_line})}\n\n"
            except queue.Empty:
                # Check if thread is still alive (Перевірити, чи потік ще живий)
                if not sim_thread.is_alive():
                    break
                await asyncio.sleep(0.05)
        
        sim_thread.join()
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.get("/api/v1/simulation/metrics/current")
async def get_current_metrics():
    """
    Get current system metrics indices (Отримати поточні індекси метрик системи).
    
    Returns:
        Dictionary with current S, C, A indices (Словник з поточними індексами S, C, A)
    """
    state = read_system_state()
    
    # If indices are already calculated, return them (Якщо індекси вже обчислені, повернути їх)
    if state.s_index is not None and state.c_index is not None and state.a_index is not None:
        return {
            "s_index": state.s_index,
            "c_index": state.c_index,
            "a_index": state.a_index,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    
    # Otherwise calculate from current state (Інакше обчислити з поточного стану)
    # Use default operational data (Використати типові операційні дані)
    s_index, c_index, a_index = calculate_metrics_from_state(
        state,
        total_ops=100,
        alerts_count=5,
        t_adapt=10.0,
        t_market=30.0
    )
    
    return {
        "s_index": s_index,
        "c_index": c_index,
        "a_index": a_index,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/api/v1/simulation/metrics/history", response_model=List[SimulationMetrics])
async def get_metrics_history():
    """
    Get simulation metrics history (Отримати історію метрик симуляції).
    
    Returns:
        List of SimulationMetrics from last simulation run (Список SimulationMetrics з останнього запуску симуляції)
    """
    return get_simulation_history()


@app.get("/api/v1/simulation/summary")
async def get_simulation_summary_endpoint():
    """
    Get summary statistics from last simulation (Отримати зведену статистику з останньої симуляції).
    
    Returns:
        Dictionary with before/after comparison (Словник з порівнянням до/після)
    """
    history = get_simulation_history()
    return get_simulation_summary(history)


@app.get("/api/v1/simulation/agent-logs")
async def get_agent_logs():
    """
    Get agent logs from last simulation (Отримати логи агента з останньої симуляції).
    
    Returns:
        List of log messages (Список повідомлень логів)
    """
    return {"logs": get_agent_logs_history()}


@app.get("/api/v1/simulation/export/csv")
async def export_simulation_csv(run_id: Optional[str] = None):
    """
    Export simulation metrics to CSV file (Експортувати метрики симуляції у CSV файл).
    
    Args:
        run_id: Optional simulation run ID. If not provided, exports latest run (Опціональний ID запуску симуляції. Якщо не надано, експортує останній запуск)
    
    Returns:
        CSV file with simulation metrics (CSV файл з метриками симуляції)
    """
    if run_id:
        metrics = get_simulation_metrics_by_run_id(run_id)
    else:
        # Get latest run ID (Отримати ID останнього запуску)
        latest_run_id = get_latest_simulation_run_id()
        if latest_run_id:
            metrics = get_simulation_metrics_by_run_id(latest_run_id)
        else:
            # Fallback to in-memory history (Резервний варіант - історія в пам'яті)
            metrics = get_simulation_history()
    
    if not metrics:
        return Response(
            content="No simulation data available (Немає доступних даних симуляції)",
            status_code=404,
            media_type="text/plain"
        )
    
    # Create CSV in memory (Створити CSV в пам'яті)
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header (Записати заголовок)
    writer.writerow(["Day", "Timestamp", "S_Index", "C_Index", "A_Index"])
    
    # Write data (Записати дані)
    for i, metric in enumerate(metrics):
        writer.writerow([
            i,
            metric.timestamp.isoformat(),
            f"{metric.s_index:.6f}",
            f"{metric.c_index:.6f}",
            f"{metric.a_index:.6f}"
        ])
    
    # Return CSV file (Повернути CSV файл)
    csv_content = output.getvalue()
    output.close()
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=simulation_results_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    )

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)



