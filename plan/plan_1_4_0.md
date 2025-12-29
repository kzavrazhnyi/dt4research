# Scientific Simulation & Metrics (v1.4.0)

## English Version

### Overview

Version 1.4.0 implements the mathematical model from the `ai_agents_nervous_system` article, adding scientific metrics calculation and simulation capabilities to the dt4research cybernetic control system. This version enables automated scenario generation, time series data collection, and scientific analysis of system behavior.

### Goals

1. Implement three key cybernetic state indices: S (Sustainability), C (Cybernetic Control), and A (Adaptability)
2. Create an automated simulation engine for generating time series data
3. Provide scientific analytics visualization with charts and before/after comparisons
4. Enable hypothesis testing and validation of the mathematical model

### Mathematical Formulas

#### S Index (Sustainability Index)

Formula: \( S = \frac{R_{eco} + R_{soc}}{2} \times (1 - W) \)

Where:
- \( R_{eco} \): Ecological/Technological resource level (normalized 0-1)
- \( R_{soc} \): Social/Cultural resource level (normalized 0-1)
- \( W \): Waste/Entropy level (normalized 0-1)

**Implementation Notes:**
- \( R_{eco} \) is extracted from `TECHNOLOGICAL` resources in the system state
- \( R_{soc} \) combines `EDUCATIONAL` resources and `CULTURE` component status
- \( W \) is calculated as the inverse of process efficiency (from `PROCESSES` component status)

**Interpretation:**
- Higher S index indicates better sustainability and resource efficiency
- Values range from 0.0 to 1.0

#### C Index (Cybernetic Control Index)

Formula: \( C = 1 - \frac{N_{alerts}}{N_{ops}} \)

Where:
- \( N_{alerts} \): Number of incidents/alerts
- \( N_{ops} \): Total number of operations

**Implementation Notes:**
- Handles division by zero (returns 1.0 when no operations)
- Clamps alert ratio to [0, 1] range
- Operations and alerts are simulated or tracked from system logs

**Interpretation:**
- Higher C index indicates better system control and fewer incidents
- Values range from 0.0 to 1.0
- C = 1.0 means perfect control (no alerts)

#### A Index (Adaptability Index)

Formula: \( A = \frac{T_{adapt}}{T_{market}} \)

Where:
- \( T_{adapt} \): System adaptation time (in days)
- \( T_{market} \): Market change time (in days, external parameter)

**Implementation Notes:**
- \( T_{market} \) is a configurable parameter (default: 30 days)
- \( T_{adapt} \) is measured from the start of adaptation to completion
- Returns 1.0 if \( T_{market} \leq 0 \) (invalid input)
- Returns 0.0 if \( T_{adapt} \leq 0 \) (instant adaptation)

**Interpretation:**
- Lower A index indicates faster adaptation relative to market changes
- A < 1.0 means system adapts faster than market changes
- A > 1.0 means system adapts slower than market changes
- Values are >= 0.0 (no upper bound)

### Implementation Details

#### Data Models

**SimulationMetrics** (`app/models.py`):
- `s_index: float` - Sustainability index
- `c_index: float` - Control index
- `a_index: float` - Adaptability index
- `timestamp: datetime` - Time of measurement

**SystemState** (extended):
- Added optional fields: `s_index`, `c_index`, `a_index`
- These fields store current calculated indices

#### Analytics Module (`app/analytics.py`)

Core calculation functions:
- `calculate_s_index(tech_resource, soc_resource, waste) -> float`
- `calculate_c_index(total_ops, alerts_count) -> float`
- `calculate_a_index(t_adapt, t_market) -> float`

Helper functions for data extraction:
- `extract_tech_resource(state) -> float` - Extracts technological resources
- `extract_soc_resource(state) -> float` - Extracts social/cultural resources
- `extract_waste_from_processes(state) -> float` - Calculates waste from process efficiency
- `calculate_metrics_from_state(state, ...) -> tuple` - Complete metrics calculation

#### Simulation Module (`app/simulation.py`)

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

#### API Endpoints (`app/main.py`)

**POST `/api/v1/simulation/run`**
- Runs simulation with parameters
- Request body: `SimulationRunRequest` (days, intensity, t_market)
- Returns: `List[SimulationMetrics]`

**GET `/api/v1/simulation/metrics/current`**
- Returns current system metrics indices
- Calculates from current system state if not stored

**GET `/api/v1/simulation/metrics/history`**
- Returns metrics history from last simulation run
- Returns: `List[SimulationMetrics]`

**GET `/api/v1/simulation/summary`**
- Returns summary statistics (before/after comparison)
- Includes improvements for each index

#### Frontend Visualization

**New Panel: "Scientific Analytics"**
- Tab-based interface: "Simulation" and "Metrics"
- Simulation tab: Controls for running simulations (days, intensity, T_market)
- Metrics tab: Charts and summary table

**Charts (Chart.js):**
- Line chart showing S, C, A indices over time
- Responsive design with proper scaling
- Color-coded datasets for each index

**Summary Table:**
- Before vs After comparison
- Shows initial and final values for each index
- Displays improvement (change) with color coding:
  - Green for positive changes
  - Red for negative changes

### Usage Examples

#### Running a Simulation

```python
from app.simulation import run_simulation

# Run 30-day simulation with high intensity
metrics = run_simulation(days=30, intensity="high", t_market=30.0)

# Access metrics
for metric in metrics:
    print(f"Day {metric.timestamp}: S={metric.s_index:.3f}, C={metric.c_index:.3f}, A={metric.a_index:.3f}")
```

#### Calculating Metrics from State

```python
from app.analytics import calculate_metrics_from_state
from app.repository import read_system_state

state = read_system_state()
s, c, a = calculate_metrics_from_state(
    state,
    total_ops=100,
    alerts_count=5,
    t_adapt=10.0,
    t_market=30.0
)
```

#### API Usage

```bash
# Run simulation
curl -X POST "http://localhost:8000/api/v1/simulation/run" \
  -H "Content-Type: application/json" \
  -d '{"days": 30, "intensity": "high", "t_market": 30.0}'

# Get current metrics
curl "http://localhost:8000/api/v1/simulation/metrics/current"

# Get simulation history
curl "http://localhost:8000/api/v1/simulation/metrics/history"

# Get summary
curl "http://localhost:8000/api/v1/simulation/summary"
```

### Testing

Unit tests are provided in:
- `tests/test_analytics.py` - Tests for index calculations and edge cases
- `tests/test_simulation.py` - Tests for simulation engine

Key test scenarios:
- Basic index calculations with known inputs
- Edge cases (zero operations, zero alerts, invalid inputs)
- Simulation runs with different parameters
- History storage and summary generation

### Interpretation of Results

**S Index Trends:**
- Increasing S: System is becoming more sustainable
- Decreasing S: Resource efficiency is declining or waste is increasing

**C Index Trends:**
- Increasing C: System control is improving (fewer incidents)
- Decreasing C: More incidents relative to operations

**A Index Trends:**
- Decreasing A: System adapts faster (good for dynamic markets)
- Increasing A: System adapts slower (may need optimization)

**Correlation Analysis:**
- Compare agent intervention frequency with A index changes
- Analyze relationship between resource changes and S index
- Study impact of process improvements on all indices

---

## Українська версія

### Огляд

Версія 1.4.0 реалізує математичну модель зі статті `ai_agents_nervous_system`, додаючи обчислення наукових метрик та можливості симуляції до кібернетичної системи керування dt4research. Ця версія дозволяє автоматичну генерацію сценаріїв, збір часових рядів даних та науковий аналіз поведінки системи.

### Цілі

1. Реалізувати три ключові індекси кібернетичного стану: S (Сталість), C (Керованість), та A (Адаптивність)
2. Створити автоматичний рушій симуляції для генерації часових рядів даних
3. Надати візуалізацію наукової аналітики з графіками та порівнянням до/після
4. Увімкнути тестування гіпотез та валідацію математичної моделі

### Математичні формули

#### Індекс S (Індекс сталості)

Формула: \( S = \frac{R_{eco} + R_{soc}}{2} \times (1 - W) \)

Де:
- \( R_{eco} \): Рівень екологічних/технологічних ресурсів (нормалізовано 0-1)
- \( R_{soc} \): Рівень соціальних/культурних ресурсів (нормалізовано 0-1)
- \( W \): Рівень відходів/ентропії (нормалізовано 0-1)

**Примітки реалізації:**
- \( R_{eco} \) витягується з ресурсів типу `TECHNOLOGICAL` у стані системи
- \( R_{soc} \) поєднує ресурси типу `EDUCATIONAL` та статус компонента `CULTURE`
- \( W \) обчислюється як обернене до ефективності процесів (зі статусу компонента `PROCESSES`)

**Інтерпретація:**
- Вищий індекс S вказує на кращу сталість та ефективність ресурсів
- Значення в діапазоні від 0.0 до 1.0

#### Індекс C (Індекс керованості)

Формула: \( C = 1 - \frac{N_{alerts}}{N_{ops}} \)

Де:
- \( N_{alerts} \): Кількість інцидентів/алертів
- \( N_{ops} \): Загальна кількість операцій

**Примітки реалізації:**
- Обробляє ділення на нуль (повертає 1.0, коли немає операцій)
- Обмежує співвідношення алертів до діапазону [0, 1]
- Операції та алерти симулюються або відстежуються з логів системи

**Інтерпретація:**
- Вищий індекс C вказує на краще керування системою та менше інцидентів
- Значення в діапазоні від 0.0 до 1.0
- C = 1.0 означає ідеальне керування (немає алертів)

#### Індекс A (Індекс адаптивності)

Формула: \( A = \frac{T_{adapt}}{T_{market}} \)

Де:
- \( T_{adapt} \): Час адаптації системи (в днях)
- \( T_{market} \): Час змін на ринку (в днях, зовнішній параметр)

**Примітки реалізації:**
- \( T_{market} \) - конфігурований параметр (за замовчуванням: 30 днів)
- \( T_{adapt} \) вимірюється від початку адаптації до завершення
- Повертає 1.0, якщо \( T_{market} \leq 0 \) (невалідний ввід)
- Повертає 0.0, якщо \( T_{adapt} \leq 0 \) (миттєва адаптація)

**Інтерпретація:**
- Нижчий індекс A вказує на швидшу адаптацію відносно змін ринку
- A < 1.0 означає, що система адаптується швидше за зміни ринку
- A > 1.0 означає, що система адаптується повільніше за зміни ринку
- Значення >= 0.0 (немає верхньої межі)

### Деталі реалізації

#### Моделі даних

**SimulationMetrics** (`app/models.py`):
- `s_index: float` - Індекс сталості
- `c_index: float` - Індекс керованості
- `a_index: float` - Індекс адаптивності
- `timestamp: datetime` - Часова мітка вимірювання

**SystemState** (розширено):
- Додано опціональні поля: `s_index`, `c_index`, `a_index`
- Ці поля зберігають поточні обчислені індекси

#### Модуль аналітики (`app/analytics.py`)

Основні функції обчислення:
- `calculate_s_index(tech_resource, soc_resource, waste) -> float`
- `calculate_c_index(total_ops, alerts_count) -> float`
- `calculate_a_index(t_adapt, t_market) -> float`

Допоміжні функції для витягування даних:
- `extract_tech_resource(state) -> float` - Витягує технологічні ресурси
- `extract_soc_resource(state) -> float` - Витягує соціальні/культурні ресурси
- `extract_waste_from_processes(state) -> float` - Обчислює відходи з ефективності процесів
- `calculate_metrics_from_state(state, ...) -> tuple` - Повне обчислення метрик

#### Модуль симуляції (`app/simulation.py`)

**Основна функція:**
- `run_simulation(days, intensity, t_market, initial_state) -> List[SimulationMetrics]`

**Процес симуляції:**
1. Ініціалізувати початковий стан системи (з бази даних або наданий стан)
2. Для кожного дня симуляції:
   - Згенерувати події на основі рівня інтенсивності
   - Симулювати операції та алерти
   - Запустити реакцію агента, якщо подія відбулася
   - Оновити накопичувальну статистику (total_ops, total_alerts, t_adapt)
   - Обчислити індекси S, C, A
   - Зберегти знімок метрик
3. Повернути часовий ряд метрик

**Генерація подій:**
- Рівні інтенсивності: "low", "medium", "high"
- Low: Події кожні 3 дні, прості цілі
- Medium: Події кожні 2 дні, помірна різноманітність
- High: Події кожного дня, різноманітні сценарії

**In-Memory сховище:**
- Глобальний список `_simulation_history` зберігає метрики
- Функції: `get_simulation_history()`, `clear_simulation_history()`
- `get_simulation_summary()` генерує порівняння до/після

#### API ендпоінти (`app/main.py`)

**POST `/api/v1/simulation/run`**
- Запускає симуляцію з параметрами
- Тіло запиту: `SimulationRunRequest` (days, intensity, t_market)
- Повертає: `List[SimulationMetrics]`

**GET `/api/v1/simulation/metrics/current`**
- Повертає поточні індекси метрик системи
- Обчислює з поточного стану системи, якщо не збережено

**GET `/api/v1/simulation/metrics/history`**
- Повертає історію метрик з останнього запуску симуляції
- Повертає: `List[SimulationMetrics]`

**GET `/api/v1/simulation/summary`**
- Повертає зведену статистику (порівняння до/після)
- Включає покращення для кожного індексу

#### Візуалізація на фронтенді

**Нова панель: "Наукова аналітика"**
- Інтерфейс на вкладках: "Simulation" та "Metrics"
- Вкладка симуляції: Елементи керування для запуску симуляцій (дні, інтенсивність, T_market)
- Вкладка метрик: Графіки та таблиця зведення

**Графіки (Chart.js):**
- Лінійний графік, що показує індекси S, C, A у часі
- Адаптивний дизайн з правильним масштабуванням
- Набори даних з кольоровим кодуванням для кожного індексу

**Таблиця зведення:**
- Порівняння до/після
- Показує початкові та фінальні значення для кожного індексу
- Відображає покращення (зміну) з кольоровим кодуванням:
  - Зелений для позитивних змін
  - Червоний для негативних змін

### Приклади використання

#### Запуск симуляції

```python
from app.simulation import run_simulation

# Запустити 30-денну симуляцію з високою інтенсивністю
metrics = run_simulation(days=30, intensity="high", t_market=30.0)

# Доступ до метрик
for metric in metrics:
    print(f"День {metric.timestamp}: S={metric.s_index:.3f}, C={metric.c_index:.3f}, A={metric.a_index:.3f}")
```

#### Обчислення метрик зі стану

```python
from app.analytics import calculate_metrics_from_state
from app.repository import read_system_state

state = read_system_state()
s, c, a = calculate_metrics_from_state(
    state,
    total_ops=100,
    alerts_count=5,
    t_adapt=10.0,
    t_market=30.0
)
```

#### Використання API

```bash
# Запустити симуляцію
curl -X POST "http://localhost:8000/api/v1/simulation/run" \
  -H "Content-Type: application/json" \
  -d '{"days": 30, "intensity": "high", "t_market": 30.0}'

# Отримати поточні метрики
curl "http://localhost:8000/api/v1/simulation/metrics/current"

# Отримати історію симуляції
curl "http://localhost:8000/api/v1/simulation/metrics/history"

# Отримати зведення
curl "http://localhost:8000/api/v1/simulation/summary"
```

### Тестування

Юніт-тести надано в:
- `tests/test_analytics.py` - Тести для обчислення індексів та граничних випадків
- `tests/test_simulation.py` - Тести для рушія симуляції

Ключові сценарії тестування:
- Базові обчислення індексів з відомими входами
- Граничні випадки (нуль операцій, нуль алертів, невалідні входи)
- Запуски симуляції з різними параметрами
- Збереження історії та генерація зведення

### Інтерпретація результатів

**Тренди індексу S:**
- Зростання S: Система стає більш сталою
- Зменшення S: Ефективність ресурсів знижується або відходи зростають

**Тренди індексу C:**
- Зростання C: Керування системою покращується (менше інцидентів)
- Зменшення C: Більше інцидентів відносно операцій

**Тренди індексу A:**
- Зменшення A: Система адаптується швидше (добре для динамічних ринків)
- Зростання A: Система адаптується повільніше (може потребувати оптимізації)

**Аналіз кореляції:**
- Порівняти частоту втручань агента зі змінами індексу A
- Аналізувати зв'язок між змінами ресурсів та індексом S
- Досліджувати вплив покращень процесів на всі індекси




