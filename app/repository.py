"""
Repository layer for persistence operations (Репозиторій для операцій збереження).
"""

import json
from typing import List, Tuple, Optional

from sqlmodel import select, delete

from app.db import get_session, create_db_and_tables
from app.db_models import ComponentRow, ResourceRow, AgentRunRow, SimulationMetricRow
from app.models import SystemState, KeyComponent, Resource, SimulationMetrics
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



def clear_state_and_runs() -> None:
    """Clear components, resources, and agent runs (Очистити компоненти, ресурси та запуски агента)."""
    with get_session() as session:
        # Delete in dependency-safe order (Видалення у безпечному порядку залежностей)
        session.exec(delete(SimulationMetricRow))
        session.exec(delete(AgentRunRow))
        session.exec(delete(ResourceRow))
        session.exec(delete(ComponentRow))
        session.commit()


def save_simulation_metric(
    metric: SimulationMetrics,
    simulation_run_id: str,
    use_agent: bool,
    day: int
) -> int:
    """Save simulation metric to database (Зберегти метрику симуляції в базу даних)."""
    with get_session() as session:
        row = SimulationMetricRow(
            timestamp=metric.timestamp,
            s_index=metric.s_index,
            c_index=metric.c_index,
            a_index=metric.a_index,
            simulation_run_id=simulation_run_id,
            use_agent=use_agent,
            day=day
        )
        session.add(row)
        session.commit()
        session.refresh(row)
        return int(row.id)  # type: ignore


def get_simulation_metrics_by_run_id(simulation_run_id: str) -> List[SimulationMetrics]:
    """Get all metrics for a specific simulation run (Отримати всі метрики для конкретного запуску симуляції)."""
    with get_session() as session:
        rows = session.exec(
            select(SimulationMetricRow)
            .where(SimulationMetricRow.simulation_run_id == simulation_run_id)
            .order_by(SimulationMetricRow.day)
        ).all()
        
        return [
            SimulationMetrics(
                s_index=row.s_index,
                c_index=row.c_index,
                a_index=row.a_index,
                timestamp=row.timestamp
            )
            for row in rows
        ]


def get_latest_simulation_run_id() -> Optional[str]:
    """Get the latest simulation run ID (Отримати ID останнього запуску симуляції)."""
    with get_session() as session:
        latest = session.exec(
            select(SimulationMetricRow)
            .order_by(SimulationMetricRow.timestamp.desc())
            .limit(1)
        ).first()
        return latest.simulation_run_id if latest else None


def get_all_simulation_metrics(limit: int = 1000) -> List[SimulationMetricRow]:
    """Get all simulation metrics (Отримати всі метрики симуляції)."""
    with get_session() as session:
        return session.exec(
            select(SimulationMetricRow)
            .order_by(SimulationMetricRow.timestamp.desc())
            .limit(limit)
        ).all()

