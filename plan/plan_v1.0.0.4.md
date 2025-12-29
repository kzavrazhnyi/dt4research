# Project Plan — Version 1.0.0.4

## English Version

## Stage 3: Providing "Memory" (Persistence)
Goal: Give the system memory by implementing the "Memory" component.

Corresponds to previous item: State Persistence (5).

### 3.1 Database
- SQLite + SQLModel (or SQLAlchemy). Preparation for PostgreSQL in the future.

### 3.2 Migrations
- Alembic for schema management.

### 3.3 Schema
- `components` (id, name, status)
- `resources` (id, name, type, value)
- `agent_runs` (id, timestamp, input_goal, applied_rules_explanation JSON, snapshot_state JSON)

### 3.4 Logic
- `main.py` stops holding global `current_state`.
- Read state from DB before response; write new state after applying agent.
- Endpoint for getting "run history" (pagination).

### Stage 3 Success Criteria
- State persists between restarts.
- Run history available for UI.
- Basic migration and repeatable seed of initial values exist.

---

## Українська версія

# План проєкту — версія 1.0.0.4

## Етап 3: Забезпечення «Пам'яті» (Persistence)
Мета: Дати системі пам'ять, реалізувавши компонент «Memory».

Відповідає попередньому пункту: Збереження стану (5).

### 3.1 База даних
- SQLite + SQLModel (або SQLAlchemy). Підготовка до PostgreSQL у майбутньому.

### 3.2 Міграції
- Alembic для управління схемою.

### 3.3 Схема
- `components` (id, name, status)
- `resources` (id, name, type, value)
- `agent_runs` (id, timestamp, input_goal, applied_rules_explanation JSON, snapshot_state JSON)

### 3.4 Логіка
- `main.py` перестає тримати глобальний `current_state`.
- Читання стану з БД перед відповіддю; запис нового стану після застосування агента.
- Ендпоінт для отримання «історії запусків» (пагінація).

### Критерії успіху Етапу 3
- Стан зберігається між перезапусками.
- Історія запусків доступна для UI.
- Є базова міграція і repeatable seed початкових значень.

