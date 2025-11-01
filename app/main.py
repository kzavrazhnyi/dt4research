"""
FastAPI backend for dt4research cybernetic control system (Бекенд FastAPI для кібернетичної системи керування).
Implements the control loop: Manager Goal → Agent Analysis → State Update → Feedback (Реалізує цикл: Ціль менеджера → Аналіз агента → Оновлення стану → Зворотний зв'язок).
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import json
import uvicorn

from app.models import SystemState, KeyComponent, Resource, MechanismInput, ComponentType, ResourceType, MechanismResponse
from app.agent_logic import run_mock_analysis
from app.db import create_db_and_tables
from app.repository import read_system_state, write_system_state, seed_initial_state, add_agent_run
from app.initial_state import INITIAL_STATE


# Initialize FastAPI app (Ініціалізація застосунку FastAPI)
app = FastAPI(title="dt4research - Cybernetic Control System", version="0.1.0")


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


@app.get("/api/v1/system-state")
async def get_system_state() -> SystemState:
    """Return current system state (Повернути поточний стан системи)."""
    return read_system_state()


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
    new_state, deltas = run_mock_analysis(goal, current_state)

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


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)



