"""
Pydantic models for dt4research system state (Моделі Pydantic для стану системи).
Defines the data structure for the cybernetic control cycle (Визначає структуру даних для кібернетичного циклу керування).
"""

from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class ResourceType(str, Enum):
    """Types of resources in the system (Типи ресурсів у системі)."""
    COMMUNICATION = "Комунікаційний"
    EDUCATIONAL = "Освітній"
    FINANCIAL = "Фінансовий"
    INFORMATIONAL = "Інформаційний"
    OPERATIONAL = "Операційний"
    ORGANIZATIONAL = "Організаційний"
    RISK = "Ризиковий"
    STRATEGIC = "Стратегічний"
    TECHNOLOGICAL = "Технологічний"


class ComponentType(str, Enum):
    """Types of key components in the system (Типи ключових компонентів системи)."""
    STRATEGY = "Стратегія"
    STRUCTURE = "Структура"
    PROCESSES = "Процеси"
    CULTURE = "Культура"
    RESOURCES = "Ресурси"


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


class MechanismInput(BaseModel):
    """Input from manager for the cybernetic control mechanism (Ввід менеджера для кібернетичного механізму)."""
    target_goal: str = Field(..., description="Strategic goal entered by the manager — Стратегічна ціль, введена менеджером")



