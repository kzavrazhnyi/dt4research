# dt4research — Technical Plan (v1.4.0)

**Research Topic:** Formation of Management Mechanisms for Digital Transformation of Enterprises

Status: Delivered (Stage 4: Scientific Simulation & Metrics) — updated with v1.4.0 simulation engine and analytics

## 1. Architecture Overview
- Backend: FastAPI + Pydantic
- Agent: rule-based (`app/agent_logic.py`) with .env coefficients
- Persistence: SQLite + SQLModel; repository pattern; PostgreSQL-ready
- Migrations: Alembic (deps ready)
- Frontend: Cytoscape.js; bilingual UI (EN default, UA toggle)
- Logging: console or JSON via `LOG_FORMAT`
- CORS: open by default
- Analytics: Scientific metrics calculation (`app/analytics.py`)
- Simulation: Time series simulation engine (`app/simulation.py`)

### Runtime control loop
![AI Agent runtime](../plan/ai_agent_runtime.png)

Manager goal → Agent analysis → State update → Feedback.
Agent emits deltas per resource; backend persists state and writes history.

### DT model (reference)
![DT model — English](../plan/dt_model_final_english.png)
![DT model — sublevels](../plan/dt_model_with_sublevels.png)

## 2. Data Model
### Pydantic (API)
- SystemState = List[KeyComponent] + List[Resource]
  - Extended with optional fields: `s_index`, `c_index`, `a_index` (float)
- MechanismInput { target_goal: str(min_length=3) }
- MechanismResponse { newState, explanation, explanation_details }
- ResourceType (EN strings): Communication, Educational, Financial, Informational, Operational, Organizational, Risk, Strategic, Technological
- SimulationMetrics { s_index: float, c_index: float, a_index: float, timestamp: datetime }
- SimulationRunRequest { days: int, intensity: str, t_market: float }

### SQLModel (DB)
- ComponentRow(id, name, status)
- ResourceRow(id, name, type, value)
- AgentRunRow(id, timestamp, input_goal, applied_rules_explanation JSON, snapshot_state JSON)

## 3. Persistence Layer
Files: `app/db.py`, `app/db_models.py`, `app/repository.py`, `app/initial_state.py`.
Flow: startup → create tables + seed; GET → read DB; POST apply → read → run agent → persist state + history → return.

## 4. Scientific Metrics (v1.4.0)

### Mathematical Formulas

#### S Index (Sustainability Index)
Formula: \( S = \frac{R_{eco} + R_{soc}}{2} \times (1 - W) \)

Where:
- \( R_{eco} \): Ecological/Technological resource level (normalized 0-1)
- \( R_{soc} \): Social/Cultural resource level (normalized 0-1)
- \( W \): Waste/Entropy level (normalized 0-1)

**Implementation:**
- \( R_{eco} \) extracted from `TECHNOLOGICAL` resources
- \( R_{soc} \) combines `EDUCATIONAL` resources and `CULTURE` component status
- \( W \) calculated as inverse of process efficiency (from `PROCESSES` component status)
- Values range from 0.0 to 1.0

#### C Index (Cybernetic Control Index)
Formula: \( C = 1 - \frac{N_{alerts}}{N_{ops}} \)

Where:
- \( N_{alerts} \): Number of incidents/alerts
- \( N_{ops} \): Total number of operations

**Implementation:**
- Handles division by zero (returns 1.0 when no operations)
- Clamps alert ratio to [0, 1] range
- Values range from 0.0 to 1.0 (C = 1.0 means perfect control)

#### A Index (Adaptability Index)
Formula: \( A = \frac{T_{adapt}}{T_{market}} \)

Where:
- \( T_{adapt} \): System adaptation time (in days)
- \( T_{market} \): Market change time (in days, external parameter, default: 30)

**Implementation:**
- Returns 1.0 if \( T_{market} \leq 0 \) (invalid input)
- Returns 0.0 if \( T_{adapt} \leq 0 \) (instant adaptation)
- Values >= 0.0 (no upper bound)
- A < 1.0 means system adapts faster than market changes

### Analytics Module (`app/analytics.py`)

Core calculation functions:
- `calculate_s_index(tech_resource, soc_resource, waste) -> float`
- `calculate_c_index(total_ops, alerts_count) -> float`
- `calculate_a_index(t_adapt, t_market) -> float`

Helper functions:
- `extract_tech_resource(state) -> float` - Extracts technological resources
- `extract_soc_resource(state) -> float` - Extracts social/cultural resources
- `extract_waste_from_processes(state) -> float` - Calculates waste from process efficiency
- `calculate_metrics_from_state(state, total_ops, alerts_count, t_adapt, t_market) -> tuple` - Complete metrics calculation

## 5. Simulation Engine (v1.4.0)

### Simulation Module (`app/simulation.py`)

**Main Function:**
- `run_simulation(days, intensity, t_market, initial_state) -> List[SimulationMetrics]`

**Simulation Process:**
1. Initialize starting system state (from database or provided state)
2. For each simulation day:
   - Generate events based on intensity level
   - Simulate operations and alerts
   - Trigger agent response if event occurred
   - Update cumulative statistics (total_ops, total_alerts, t_adapt)
   - Calculate S, C, A indices
   - Store metrics snapshot
3. Return time series of metrics

**Event Generation:**
- Intensity levels: "low", "medium", "high"
- Low: Events every 3 days, simple goals
- Medium: Events every 2 days, moderate variety
- High: Events every day, diverse scenarios

**In-Memory Storage:**
- Global list `_simulation_history` stores metrics
- Functions: `get_simulation_history()`, `clear_simulation_history()`
- `get_simulation_summary()` generates before/after comparison

## 6. Environment & Config
`.env` (optional; defaults exist):
- `DATABASE_URL` (defaults to `sqlite:///./data.db` locally; masked in diagnostics)
- `RABBITMQ_URL` (CloudAMQP/local broker; masked in diagnostics)
- `LOG_FORMAT` (`console` | `json`)
- `LOG_LEVEL` (`INFO` default)
- `RULE_*` coefficients

## 7. Frontend (EN/UA)
Language switch; translates graph labels, details, tooltips, controls; console logs `[UI]`.

**New Panel: "Scientific Analytics" (v1.4.0)**
- Tab-based interface: "Simulation" and "Metrics"
- Simulation tab: Controls for running simulations (days, intensity, T_market)
- Metrics tab: Charts and summary table
- Charts (Chart.js): Line chart showing S, C, A indices over time
- Summary Table: Before vs After comparison with color-coded improvements

## 8. API Endpoints

### Core Endpoints
- `GET /api/v1/state` - Get current system state
- `POST /api/v1/apply` - Apply mechanism (agent analysis)
- `GET /api/v1/agent-runs` - List agent run history

### Health Endpoints (v1.2.0)
- `GET /api/v1/health/db` - Database health check
- `GET /api/v1/health/rabbit` - RabbitMQ health check

### Simulation Endpoints (v1.4.0)
- `POST /api/v1/simulation/run` - Run simulation with parameters
  - Request body: `SimulationRunRequest` (days, intensity, t_market)
  - Returns: `List[SimulationMetrics]`
- `GET /api/v1/simulation/metrics/current` - Get current system metrics indices
  - Calculates from current system state if not stored
- `GET /api/v1/simulation/metrics/history` - Get metrics history from last simulation run
  - Returns: `List[SimulationMetrics]`
- `GET /api/v1/simulation/summary` - Get summary statistics (before/after comparison)
  - Includes improvements for each index

## 9. Testing
`tests/test_api.py`, `tests/test_persistence.py`, `tests/test_analytics.py`, `tests/test_simulation.py`; run: `./venv/Scripts/python.exe -m pytest -q`.

Key test scenarios:
- Basic index calculations with known inputs
- Edge cases (zero operations, zero alerts, invalid inputs)
- Simulation runs with different parameters
- History storage and summary generation

## 10. Next steps
- Alembic migrations (baseline + seeds)
- `GET /api/v1/agent-runs/{id}` (optional)
- Restrict CORS in prod; request logging middleware
- Persist simulation history to database
- Add export functionality for simulation data

## 11. Version History

### v1.2.0
- Health endpoints: `GET /api/v1/health/db`, `GET /api/v1/health/rabbit`
- URL masking utility shared across diagnostics and settings page (credentials replaced with `***`)
- `/settings` page surfaces environment hints with masked connection strings
- README codifies git version-control hygiene for contributors

### v1.4.0
- Scientific metrics calculation (S, C, A indices)
- Simulation engine for time series data generation
- Analytics visualization with charts and before/after comparisons
- Hypothesis testing and validation of mathematical model
- New API endpoints for simulation and metrics
- Frontend panel for scientific analytics

