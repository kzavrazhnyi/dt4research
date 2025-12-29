"""
Initial in-memory system state (Початковий стан системи).
Used for seeding the DB on first run (Використовується для початкового заповнення БД).
"""

from app.models import SystemState, KeyComponent, Resource, ComponentType, ResourceType


INITIAL_STATE = SystemState(
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
    ],
    s_index=None,
    c_index=None,
    a_index=None
)





