"""
FastAPI backend for dt4research cybernetic control system (Бекенд FastAPI для кібернетичної системи керування).
Implements the control loop: Manager Goal → Agent Analysis → State Update → Feedback (Реалізує цикл: Ціль менеджера → Аналіз агента → Оновлення стану → Зворотний зв'язок).
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
import uvicorn

from app.models import SystemState, KeyComponent, Resource, MechanismInput, ComponentType, ResourceType
from app.agent_logic import run_mock_analysis


# Initialize FastAPI app (Ініціалізація застосунку FastAPI)
app = FastAPI(title="dt4research - Cybernetic Control System", version="0.1.0")

# Templates and static files (Шаблони та статичні файли)
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Global system state (in-memory database) — Глобальний стан системи (in-memory база)
current_state = SystemState(
    components=[
        KeyComponent(id="comp-strategy", name=ComponentType.STRATEGY, status="Активна"),
        KeyComponent(id="comp-structure", name=ComponentType.STRUCTURE, status="Стабільна"),
        KeyComponent(id="comp-processes", name=ComponentType.PROCESSES, status="В роботі"),
        KeyComponent(id="comp-culture", name=ComponentType.CULTURE, status="Належний стан"),
        KeyComponent(id="comp-resources", name=ComponentType.RESOURCES, status="Доступні"),
    ],
    resources=[
        Resource(id="res-comm", name="Канали комунікації", type=ResourceType.COMMUNICATION, value=65.0),
        Resource(id="res-edu", name="Програми навчання", type=ResourceType.EDUCATIONAL, value=55.0),
        Resource(id="res-fin", name="Капітал та інвестиції", type=ResourceType.FINANCIAL, value=70.0),
        Resource(id="res-info", name="Інформаційні системи", type=ResourceType.INFORMATIONAL, value=60.0),
        Resource(id="res-oper", name="Операційні процеси", type=ResourceType.OPERATIONAL, value=75.0),
        Resource(id="res-org", name="Організаційна структура", type=ResourceType.ORGANIZATIONAL, value=65.0),
        Resource(id="res-risk", name="Управління ризиками", type=ResourceType.RISK, value=50.0),
        Resource(id="res-strat", name="Стратегічне планування", type=ResourceType.STRATEGIC, value=68.0),
        Resource(id="res-tech", name="Технологічні рішення", type=ResourceType.TECHNOLOGICAL, value=62.0),
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
async def apply_mechanism(input_data: MechanismInput) -> SystemState:
    """
    Main cybernetic control endpoint (Головний ендпоінт кібернетичного керування).
    Receives goal from manager, triggers agent analysis, updates system state (Отримує ціль, запускає аналіз агента, оновлює стан).
    """
    global current_state
    
    # Step 1: Get input
    goal = input_data.target_goal
    
    # Step 2: Run agent analysis
    new_state = run_mock_analysis(goal, current_state)
    
    # Step 3: Update global state (simulate updating Memory from ai_agent_runtime.png)
    current_state = new_state
    
    return current_state


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)



