"""
SQLModel table definitions (Таблиці SQLModel).
Align with Pydantic models to map DB <-> API state (Узгоджено з Pydantic-моделями для мапінгу БД <-> API).
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from app.models import ResourceType


class ComponentRow(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    status: str


class ResourceRow(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    type: ResourceType
    value: float = Field(default=0.0)


class AgentRunRow(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    input_goal: str
    applied_rules_explanation: str  # JSON string with deltas (JSON-рядок з дельтами)
    snapshot_state: str  # JSON string of SystemState (JSON-рядок стану)


class SimulationMetricRow(SQLModel, table=True):
    """Stores simulation metrics for persistence (Зберігає метрики симуляції для персистентності)."""
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    s_index: float = Field(ge=0, le=1, description="Sustainability index (Індекс сталості)")
    c_index: float = Field(ge=0, le=1, description="Cybernetic Control index (Індекс керованості)")
    a_index: float = Field(ge=0, description="Adaptability index (Індекс адаптивності)")
    simulation_run_id: Optional[str] = Field(default=None, index=True, description="Identifier for simulation run (Ідентифікатор запуску симуляції)")
    use_agent: bool = Field(default=True, description="Whether agent was used in this simulation (Чи використовувався агент у цій симуляції)")
    day: int = Field(ge=0, description="Simulation day (День симуляції)")





