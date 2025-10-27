"""
Pydantic models for dt4research system state.
Defines the data structure for the cybernetic control cycle.
"""

from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class ResourceType(str, Enum):
    """Types of resources in the system."""
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
    """Types of key components in the system."""
    STRATEGY = "Стратегія"
    STRUCTURE = "Структура"
    PROCESSES = "Процеси"
    CULTURE = "Культура"
    RESOURCES = "Ресурси"


class Resource(BaseModel):
    """Represents a resource in the system."""
    id: str
    name: str
    type: ResourceType
    value: float = Field(ge=0, le=100, description="Current resource level (0-100)")


class KeyComponent(BaseModel):
    """Represents a key component of the system."""
    id: str
    name: ComponentType
    status: str


class SystemState(BaseModel):
    """Represents the complete state of the system."""
    components: List[KeyComponent]
    resources: List[Resource]


class MechanismInput(BaseModel):
    """Input from manager for the cybernetic control mechanism."""
    target_goal: str = Field(..., description="Strategic goal entered by the manager")



