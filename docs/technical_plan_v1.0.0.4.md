# dt4research — Technical Plan (v1.0.0.4)

Status: Delivered (Stage 3: Persistence) — updated with v1.2.0 diagnostics (health checks & masking)

## 1. Architecture Overview

- Backend: FastAPI + Pydantic (typing-first, validation)
- Agent: rule-based engine (`app/agent_logic.py`) with environment-configurable coefficients (python-dotenv)
- Persistence: SQLite + SQLModel; repository pattern; ready to switch to PostgreSQL
- Migrations: Alembic prepared in dependencies (migration scripts to be added later)
- Frontend: HTML + JS (Cytoscape.js), bilingual UI (EN default, UA toggle)
- Logging: console (dev) or JSON (prod) via `LOG_FORMAT`
- CORS: open by default (restrict in production)

### Runtime control loop

![AI Agent runtime](../plan/ai_agent_runtime.png)

- Manager goal → Agent analysis → State update → Feedback
- Agent emits deltas per resource; backend persists new state and writes a history record

### DT model (reference)

- Final English map:

![DT model — English](../plan/dt_model_final_english.png)

- Model with sublevels:

![DT model — sublevels](../plan/dt_model_with_sublevels.png)

## 2. Data Model

### Pydantic (API)
- `SystemState` = `List[KeyComponent]` + `List[Resource]`
- `MechanismInput` `{ target_goal: str(min_length=3) }`
- `MechanismResponse` `{ newState: SystemState, explanation: str, explanation_details: {ResourceType:int} }`
- `ResourceType` (EN string enum): Communication, Educational, Financial, Informational, Operational, Organizational, Risk, Strategic, Technological

### SQLModel (DB)
- `ComponentRow(id:str PK, name:str, status:str)`
- `ResourceRow(id:str PK, name:str, type:ResourceType, value:float)`
- `AgentRunRow(id:int PK, timestamp:utc, input_goal:str, applied_rules_explanation:json, snapshot_state:json)`

## 3. Persistence Layer

Files:
- `app/db.py`: engine, `create_db_and_tables()`, `get_session()`
- `app/db_models.py`: SQLModel tables
- `app/repository.py`: `read_system_state()`, `write_system_state()`, `seed_initial_state()`, `add_agent_run()`, `list_agent_runs()`
- `app/initial_state.py`: `INITIAL_STATE` seed

Flow:
1. App startup → create tables → `seed_initial_state` when empty
2. GET state → read from DB
3. POST apply → read current → run agent → write new state → persist history → return explanation

## 4. Environment & Config

`.env` (optional; defaults applied):
- `DATABASE_URL` (локально `sqlite:///./data.db`; замаскований у діагностиці)
- `RABBITMQ_URL` (рядок CloudAMQP/локального брокера; замаскований у діагностиці)
- `LOG_FORMAT` = `console` | `json`
- `LOG_LEVEL` = `INFO`
- Rule coefficients (examples):
  - `RULE_ECO_TECH`(20), `RULE_ECO_EDU`(15), `RULE_ECO_RISK`(10)
  - `RULE_CUSTOMER_COMM`(15), `RULE_CUSTOMER_INFO`(10), `RULE_CUSTOMER_OPER`(10)
  - `RULE_INNOV_TECH`(25), `RULE_INNOV_STRAT`(15), `RULE_INNOV_FIN`(10)
  - `RULE_PARTNERS_ORG`(20), `RULE_PARTNERS_COMM`(10)
  - `RULE_RISK_RISK`(20), `RULE_RISK_OPER`(10)
  - `RULE_EDU_EDU`(20), `RULE_EDU_ORG`(10)
  - `RULE_DEFAULT_TECH`(5), `RULE_DEFAULT_STRAT`(5), `RULE_DEFAULT_FIN`(5)

## 5. Frontend (EN/UA)

- Language select in header (localStorage `dt4researchLanguage`), EN default
- Dynamic translation of:
  - Graph node labels (components/resources)
  - Details panel & tooltips
  - Controls (labels, placeholders, buttons)
- Client logs (`[UI]`) for key actions (language change, fetch, apply, tooltips)

## 6. Logging

- Dev: human-readable console format
- Prod: JSON structured logs (level/name/message/time)

## 7. Testing

- `tests/test_api.py` – schema, bounds, venv heuristic
- `tests/test_persistence.py` – DB persistence and history endpoint

Run:
```powershell
./venv/Scripts/python.exe -m pytest -q
```

## 8. Next Steps (v1.0.0.4+)

- Add Alembic migration scripts (baseline, repeatable seeds)
- Introduce `GET /api/v1/agent-runs/{id}` for detailed snapshot retrieval (optional)
- Restrict CORS and add request logging middleware in prod profile
- Add caching for `read_system_state()` (if needed under load)



## 9. Additions in v1.2.0
- Health checks for DB and RabbitMQ with mandatory credential masking
- Shared URL masking helper reused by diagnostics and `/settings`
- Settings page outlines environment variables with masked connection strings
- README documents git workflow expectations (version-control hygiene)
