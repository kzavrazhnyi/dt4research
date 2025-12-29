"""
Pydantic models for dt4research system state (Моделі Pydantic для стану системи).
Defines the data structure for the cybernetic control cycle (Визначає структуру даних для кібернетичного циклу керування).
"""

from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class ResourceType(str, Enum):
    """Types of resources in the system (Типи ресурсів у системі)."""
    COMMUNICATION = "Communication"
    EDUCATIONAL = "Educational"
    FINANCIAL = "Financial"
    INFORMATIONAL = "Informational"
    OPERATIONAL = "Operational"
    ORGANIZATIONAL = "Organizational"
    RISK = "Risk"
    STRATEGIC = "Strategic"
    TECHNOLOGICAL = "Technological"


class ComponentType(str, Enum):
    """Types of key components in the system (Типи ключових компонентів системи)."""
    STRATEGY = "Strategy"
    STRUCTURE = "Structure"
    PROCESSES = "Processes"
    CULTURE = "Culture"
    RESOURCES = "Resources"


class Resource(BaseModel):
    """Represents a resource in the system (Представляє ресурс у системі)."""
    id: str
    name: str
    type: ResourceType
    value: float = Field(ge=0, le=100, description="Current resource level (0-100) — Поточний рівень ресурсу (0-100)")


class KeyComponent(BaseModel):
    """Represents a key component of the system (Представляє ключовий компонент системи)."""
    id: str
    name: ComponentType
    status: str


class SystemState(BaseModel):
    """Represents the complete state of the system (Представляє повний стан системи)."""
    components: List[KeyComponent]
    resources: List[Resource]
    # Scientific metrics indices (Наукові індекси метрик)
    s_index: Optional[float] = Field(default=None, ge=0, le=1, description="Sustainability index (Індекс сталості)")
    c_index: Optional[float] = Field(default=None, ge=0, le=1, description="Cybernetic Control index (Індекс керованості)")
    a_index: Optional[float] = Field(default=None, ge=0, description="Adaptability index (Індекс адаптивності)")


class MechanismInput(BaseModel):
    """Input from manager for the cybernetic control mechanism (Ввід менеджера для кібернетичного механізму)."""
    target_goal: str = Field(..., min_length=3, description="Strategic goal entered by the manager — Стратегічна ціль, введена менеджером")



class MechanismResponse(BaseModel):
    """Response for apply-mechanism endpoint (Відповідь ендпоінта застосування механізму)."""
    newState: SystemState
    explanation: str
    explanation_details: Optional[Dict[str, int]] = None


class SimulationMetrics(BaseModel):
    """Metrics snapshot for scientific analysis (Знімок метрик для наукового аналізу)."""
    s_index: float = Field(ge=0, le=1, description="Sustainability index (Індекс сталості)")
    c_index: float = Field(ge=0, le=1, description="Cybernetic Control index (Індекс керованості)")
    a_index: float = Field(ge=0, description="Adaptability index (Індекс адаптивності)")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of metrics (Часова мітка метрик)")


class SimulationRunRequest(BaseModel):
    """Request parameters for simulation run (Параметри запиту для запуску симуляції)."""
    days: int = Field(default=30, ge=1, le=365, description="Number of simulation days (Кількість днів симуляції)")
    intensity: str = Field(default="high", description="Event intensity level (Рівень інтенсивності подій)")
    t_market: float = Field(default=30.0, gt=0, description="Market change time in days (Час змін на ринку в днях)")
    use_agent: bool = Field(default=True, description="If True, agent responds to events; if False, entropy degrades resources (Якщо True, агент реагує на події; якщо False, ентропія деградує ресурси)")

