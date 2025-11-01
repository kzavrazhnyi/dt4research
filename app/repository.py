"""
Repository layer for persistence operations (Репозиторій для операцій збереження).
"""

import json
from typing import List, Tuple

from sqlmodel import select

from app.db import get_session, create_db_and_tables
from app.db_models import ComponentRow, ResourceRow, AgentRunRow
from app.models import SystemState, KeyComponent, Resource
from app.initial_state import INITIAL_STATE


def ensure_db_initialized() -> None:
    """Create tables and seed initial data if needed (Ініціалізувати БД та seed)."""
    create_db_and_tables()
    seed_initial_state(INITIAL_STATE)


def read_system_state() -> SystemState:
    """Read current state from the database (Прочитати поточний стан із БД)."""
    ensure_db_initialized()
    with get_session() as session:
        components_rows = session.exec(select(ComponentRow)).all()
        resources_rows = session.exec(select(ResourceRow)).all()

    components = [
        KeyComponent(id=row.id, name=row.name, status=row.status) for row in components_rows
    ]
    resources = [
        Resource(id=row.id, name=row.name, type=row.type, value=row.value) for row in resources_rows
    ]
    return SystemState(components=components, resources=resources)


def write_system_state(new_state: SystemState) -> None:
    """Overwrite system state in the database (Перезаписати стан системи у БД)."""
    with get_session() as session:
        # Update or insert components
        for comp in new_state.components:
            existing = session.get(ComponentRow, comp.id)
            if existing is None:
                session.add(ComponentRow(id=comp.id, name=comp.name, status=comp.status))
            else:
                existing.name = comp.name
                existing.status = comp.status
        # Update or insert resources
        for res in new_state.resources:
            existing = session.get(ResourceRow, res.id)
            if existing is None:
                session.add(
                    ResourceRow(id=res.id, name=res.name, type=res.type, value=res.value)
                )
            else:
                existing.name = res.name
                existing.type = res.type
                existing.value = res.value
        session.commit()


def seed_initial_state(initial_state: SystemState) -> None:
    """Insert initial state if tables are empty (Додати початковий стан, якщо таблиці порожні)."""
    with get_session() as session:
        has_components = session.exec(select(ComponentRow).limit(1)).first() is not None
        has_resources = session.exec(select(ResourceRow).limit(1)).first() is not None
        if has_components and has_resources:
            return
    write_system_state(initial_state)


def add_agent_run(goal: str, deltas: dict, snapshot: SystemState) -> int:
    """Persist agent run (Зберегти запуск агента)."""
    with get_session() as session:
        row = AgentRunRow(
            input_goal=goal,
            applied_rules_explanation=json.dumps(deltas, ensure_ascii=False),
            snapshot_state=snapshot.model_dump_json()
        )
        session.add(row)
        session.commit()
        session.refresh(row)
        return int(row.id)  # type: ignore


def list_agent_runs(limit: int = 20, offset: int = 0) -> Tuple[int, List[AgentRunRow]]:
    """List agent runs with pagination (Список запусків агента з пагінацією)."""
    with get_session() as session:
        total_list = session.exec(select(AgentRunRow)).all()
        total = len(total_list)
        runs = session.exec(
            select(AgentRunRow).order_by(AgentRunRow.timestamp.desc()).offset(offset).limit(limit)
        ).all()
        return total, runs


