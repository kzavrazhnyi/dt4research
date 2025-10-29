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


# Global system state (in-memory database) — Глобальний стан системи (in-memory база)
current_state = SystemState(
    components=[
        KeyComponent(id="comp-strategy", name=ComponentType.STRATEGY, status="Active"),
        KeyComponent(id="comp-structure", name=ComponentType.STRUCTURE, status="Stable"),
        KeyComponent(id="comp-processes", name=ComponentType.PROCESSES, status="In Progress"),
        KeyComponent(id="comp-culture", name=ComponentType.CULTURE, status="Healthy"),
        KeyComponent(id="comp-resources", name=ComponentType.RESOURCES, status="Available"),
    ],
    resources=[
        Resource(id="res-comm", name="Communication Channels", type=ResourceType.COMMUNICATION, value=65.0),
        Resource(id="res-edu", name="Learning Programs", type=ResourceType.EDUCATIONAL, value=55.0),
        Resource(id="res-fin", name="Capital and Investments", type=ResourceType.FINANCIAL, value=70.0),
        Resource(id="res-info", name="Information Systems", type=ResourceType.INFORMATIONAL, value=60.0),
        Resource(id="res-oper", name="Operational Processes", type=ResourceType.OPERATIONAL, value=75.0),
        Resource(id="res-org", name="Organizational Structure", type=ResourceType.ORGANIZATIONAL, value=65.0),
        Resource(id="res-risk", name="Risk Management", type=ResourceType.RISK, value=50.0),
        Resource(id="res-strat", name="Strategic Planning", type=ResourceType.STRATEGIC, value=68.0),
        Resource(id="res-tech", name="Technology Solutions", type=ResourceType.TECHNOLOGICAL, value=62.0),
    ]
)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main HTML page (Віддавати головну HTML-сторінку)."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/v1/system-state")
async def get_system_state() -> SystemState:
    """Return current system state (Повернути поточний стан системи)."""
    return current_state


@app.post("/api/v1/apply-mechanism")
async def apply_mechanism(input_data: MechanismInput) -> MechanismResponse:
    """
    Main cybernetic control endpoint (Головний ендпоінт кібернетичного керування).
    Receives goal from manager, triggers agent analysis, updates system state (Отримує ціль, запускає аналіз агента, оновлює стан).
    """
    global current_state
    
    # Step 1: Get input
    goal = input_data.target_goal
    
    # Step 2: Run agent analysis
    new_state, deltas = run_mock_analysis(goal, current_state)
    
    # Step 3: Update global state (simulate updating Memory from ai_agent_runtime.png)
    current_state = new_state

    # Build explanation string (Сформувати текст пояснення)
    if deltas:
        parts = [f"{resource} +{delta}" for resource, delta in deltas.items()]
        explanation = "; ".join(parts)
    else:
        explanation = "Без змін"

    return MechanismResponse(newState=current_state, explanation=explanation, explanation_details=deltas)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)



