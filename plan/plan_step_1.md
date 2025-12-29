# Plan for Creating dt4research (Stage 1: Simulation Prototype)

## English Version

## 1. Project Setup and Dependencies

**Create structure:**

```
dt4research/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── agent_logic.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── app.js
│       └── style.css
├── requirements.txt
└── .gitignore
```

**requirements.txt:**

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.4.0
jinja2>=3.1.0
```

**Activate venv and install:**

```powershell
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Data Models (app/models.py)

**ResourceType Enum** — 9 types according to plan:

- Communication, Educational, Financial, Informational, Operational, Organizational, Risk, Strategic, Technological

**ComponentType Enum** — key components:

- Strategy, Structure, Processes, Culture, Resources

**Pydantic models:**

- `Resource`: id, name, type (ResourceType), value (float, 0-100)
- `KeyComponent`: id, name (ComponentType), status (str)
- `SystemState`: components (List[KeyComponent]), resources (List[Resource])
- `MechanismInput`: target_goal (str)

**Model note:** Component "Resources" is included in `KeyComponent` for conceptual completeness, but on the main graph all 9 specific resources are displayed as separate nodes (flat graph). This ensures simplicity and clarity of visualization of changes.

## 3. FastAPI Backend (app/main.py)

**Global variable `current_state`** — initialize with hardcoded initial data (5 components + 9 resources with values ~50-70).

**Jinja2 and StaticFiles:**

- `Jinja2Templates(directory="app/templates")`
- `app.mount("/static", StaticFiles(directory="app/static"), name="static")`

**Endpoints:**

- `GET /` → renders `index.html`
- `GET /api/v1/system-state` → returns current `current_state` as JSON
- `POST /api/v1/apply-mechanism` → accepts `MechanismInput`, calls `agent_logic.run_mock_analysis()`, updates global state, returns new state

## 4. Agent Logic (app/agent_logic.py)

**Function `run_mock_analysis(goal: str, current_state: SystemState) -> SystemState`:**

- Create deep copy of state
- Use `print()` for logging agent "thoughts"
- Rule-based logic (examples):
  - If "recycling" or "ecology" in goal → +20 to Technological, +15 to Educational, +10 to Risk
  - If "client" or "service" → +15 to Communication, +10 to Informational, +10 to Operational
  - If "innovation" or "digital" → +25 to Technological, +15 to Strategic
  - If "partner" or "ecosystem" → +20 to Organizational, +10 to Communication
- Limit resource values to range 0-100
- Return modified state

## 5. Frontend HTML (app/templates/index.html) — Hybrid Approach

**Structure:**

- Header: "dt4research — Cybernetic Model of Digital Transformation"
- **Manager Impact Panel** (class `controls`):
  - `<input id="goalInput" placeholder="Enter strategic goal...">`
  - `<button id="applyButton">Run Agent</button>`
- **Main Visualization** (Main View):
  - `<div id="cy-graph-main"></div>` (80% screen height)
- **Detailed Visualization** (Detail View, initially hidden):
  - `<div id="cy-graph-detail" style="display: none;"></div>`
  - `<button id="backButton" style="display: none;">← Back to Overview</button>`
- Connect Cytoscape.js from CDN
- Connect `/static/app.js` and `/static/style.css`

**Switching logic:**

- Main graph displays flat graph (5 components + 9 resources as separate nodes)
- On click on "Resources" node, user transitions to detailed view
- In detailed view "Resources" becomes compound node (parent node), and 9 resources — child nodes with grid layout
- "Back" button returns to main overview

## 6. Client Logic (app/static/app.js) — Hybrid Approach

**Two Cytoscape instances:**

1. `cy_main` — for main graph (container: `#cy-graph-main`)
2. `cy_detail` — for detailed graph (container: `#cy-graph-detail`)

**Styles for cy_main:**

- Components — blue squares (`shape: 'square'`)
- Resources — green circles (`shape: 'ellipse'`), size depends on `value`
- Edges — dashed/solid according to dt_model.png

**Styles for cy_detail:**

- Parent node "Resources" — light gray with border
- Child resources — green circles with labels `"Name (value)"`

**Function `updateMainGraph()`:**

- `fetch('/api/v1/system-state')`
- Clear `cy_main.elements().remove()`
- Add 5 components (including "Resources")
- Add 9 resources as separate nodes (flat graph)
- Add edges according to model (Strategy→Processes, Strategy→Structure, Structure→Processes, Processes→Culture, Culture→Resources, each resource→Processes/Culture, etc.)
- Apply `layout({ name: 'breadthfirst', directed: true })`
- Call `updateDetailGraph(state)` to synchronize data

**Function `updateDetailGraph(state)`:**

- Clear `cy_detail.elements().remove()`
- Find component "Resources" in `state.components`
- Add it as parent node
- Add 9 resources as child nodes with `parent: 'resources'` and labels with `value`
- Apply `layout({ name: 'grid', rows: 3, cols: 3 })`

**View switching functions:**

`showMainGraph()`:

- Show `#cy-graph-main` and `.controls`
- Hide `#cy-graph-detail` and `#backButton`

`showDetailGraph()`:

- Hide `#cy-graph-main` and `.controls`
- Show `#cy-graph-detail` and `#backButton`
- Redraw detailed graph layout

**Event handlers:**

- **"Run Agent" button** (`#applyButton`):
  - Get `goal` from `#goalInput.value`
  - `fetch('/api/v1/apply-mechanism', { method: 'POST', body: JSON.stringify({ target_goal: goal }), headers: { 'Content-Type': 'application/json' } })`
  - After successful response call `updateMainGraph()` (this will update both graphs)

- **Click on "Resources" node** in `cy_main`:
  - `cy_main.on('tap', 'node[name="Resources"]', () => showDetailGraph())`

- **"Back" button** (`#backButton`):
  - Call `showMainGraph()`

**Startup:**

- Call `updateMainGraph()` on `DOMContentLoaded`
- Call `showMainGraph()` for initial state

## 7. Styles (app/static/style.css)

- Modern, clean UI with base palette (blue/green/gray)
- `#cy-graph-main, #cy-graph-detail`: `width: 100%; height: 80vh; border: 1px solid #ccc;`
- Control panel (`.controls`): flexbox centering, padding, shadows for buttons
- `#backButton`: positioning in upper left corner, styled as secondary button
- Responsiveness for desktops

## 8. .gitignore

```
.venv/
venv/
__pycache__/
*.pyc
.env
```

## Success Criteria (Definition of Done)

✅ Project runs: `uvicorn app.main:app --reload`

✅ Browser (`http://127.0.0.1:8000`) shows interactive graph

✅ Graph visualizes initial state (5 components + 9 resources)

✅ Manager enters goal in text field

✅ "Run Agent" button sends POST request

✅ Terminal logs agent "thoughts"

✅ System state updates on backend

✅ Graph automatically updates, displaying new resource values (visually — changed node sizes)

✅ Cybernetic loop closed: Goal → Analysis → Change → Feedback

---

## Українська версія

# План створення dt4research (Етап 1: Прототип Симуляції)

## 1. Налаштування проєкту та залежностей

**Створити структуру:**

```
dt4research/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── agent_logic.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── app.js
│       └── style.css
├── requirements.txt
└── .gitignore
```

**requirements.txt:**

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.4.0
jinja2>=3.1.0
```

**Активація venv та інсталяція:**

```powershell
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Моделі даних (app/models.py)

**ResourceType Enum** — 9 типів згідно з планом:

- Комунікаційний, Освітній, Фінансовий, Інформаційний, Операційний, Організаційний, Ризиковий, Стратегічний, Технологічний

**ComponentType Enum** — ключові компоненти:

- Стратегія, Структура, Процеси, Культура, Ресурси

**Pydantic моделі:**

- `Resource`: id, name, type (ResourceType), value (float, 0-100)
- `KeyComponent`: id, name (ComponentType), status (str)
- `SystemState`: components (List[KeyComponent]), resources (List[Resource])
- `MechanismInput`: target_goal (str)

**Примітка щодо моделі:** Компонент "Ресурси" включено в `KeyComponent` для концептуальної повноти, але на головному графі всі 9 конкретних ресурсів відображаються як окремі вузли (плаский граф). Це забезпечує простоту та чіткість візуалізації змін.

## 3. FastAPI бекенд (app/main.py)

**Глобальна змінна `current_state`** — ініціалізувати з hardcoded початковими даними (5 компонентів + 9 ресурсів зі значеннями ~50-70).

**Jinja2 та StaticFiles:**

- `Jinja2Templates(directory="app/templates")`
- `app.mount("/static", StaticFiles(directory="app/static"), name="static")`

**Ендпоінти:**

- `GET /` → рендерить `index.html`
- `GET /api/v1/system-state` → повертає поточний `current_state` як JSON
- `POST /api/v1/apply-mechanism` → приймає `MechanismInput`, викликає `agent_logic.run_mock_analysis()`, оновлює глобальний стан, повертає новий стан

## 4. Логіка агента (app/agent_logic.py)

**Функція `run_mock_analysis(goal: str, current_state: SystemState) -> SystemState`:**

- Створити deep copy стану
- Використати `print()` для логування "думок" агента
- Rule-based логіка (приклади):
  - Якщо "переробк" або "екологі" в цілі → +20 до Технологічний, +15 до Освітній, +10 до Ризиковий
  - Якщо "клієнт" або "сервіс" → +15 до Комунікаційний, +10 до Інформаційний, +10 до Операційний
  - Якщо "інновац" або "цифров" → +25 до Технологічний, +15 до Стратегічний
  - Якщо "партнер" або "екосистем" → +20 до Організаційний, +10 до Комунікаційний
- Обмежити значення ресурсів діапазоном 0-100
- Повернути модифікований стан

## 5. Фронтенд HTML (app/templates/index.html) — Гібридний підхід

**Структура:**

- Заголовок: "dt4research — Кібернетична Модель Цифрової Трансформації"
- **Панель Впливу Менеджера** (клас `controls`):
  - `<input id="goalInput" placeholder="Введіть стратегічну ціль...">`
  - `<button id="applyButton">Запустити Агента</button>`
- **Головна Візуалізація** (Main View):
  - `<div id="cy-graph-main"></div>` (80% висоти екрану)
- **Детальна Візуалізація** (Detail View, спочатку прихована):
  - `<div id="cy-graph-detail" style="display: none;"></div>`
  - `<button id="backButton" style="display: none;">← Назад до огляду</button>`
- Підключити Cytoscape.js з CDN
- Підключити `/static/app.js` та `/static/style.css`

**Логіка перемикання:**

- На головному графі відображається плаский граф (5 компонентів + 9 ресурсів як окремі вузли)
- При кліку на вузол "Ресурси" користувач переходить до детального вигляду
- В детальному вигляді "Ресурси" стає compound node (батьківським вузлом), а 9 ресурсів — дочірніми вузлами з grid layout
- Кнопка "Назад" повертає до головного огляду

## 6. Клієнтська логіка (app/static/app.js) — Гібридний підхід

**Дві інстанції Cytoscape:**

1. `cy_main` — для головного графу (контейнер: `#cy-graph-main`)
2. `cy_detail` — для детального графу (контейнер: `#cy-graph-detail`)

**Стилі для cy_main:**

- Components — блакитні квадрати (`shape: 'square'`)
- Resources — зелені кола (`shape: 'ellipse'`), розмір залежить від `value`
- Edges — пунктирні/суцільні згідно з dt_model.png

**Стилі для cy_detail:**

- Батьківський вузол "Ресурси" — світло-сірий з рамкою
- Дочірні ресурси — зелені кола з підписами `"Назва (значення)"`

**Функція `updateMainGraph()`:**

- `fetch('/api/v1/system-state')`
- Очистити `cy_main.elements().remove()`
- Додати 5 компонентів (включно з "Ресурси")
- Додати 9 ресурсів як окремі вузли (плаский граф)
- Додати ребра згідно з моделлю (Стратегія→Процеси, Стратегія→Структура, Структура→Процеси, Процеси→Культура, Культура→Ресурси, кожен ресурс→Процеси/Культура тощо)
- Застосувати `layout({ name: 'breadthfirst', directed: true })`
- Викликати `updateDetailGraph(state)` для синхронізації даних

**Функція `updateDetailGraph(state)`:**

- Очистити `cy_detail.elements().remove()`
- Знайти компонент "Ресурси" в `state.components`
- Додати його як батьківський вузол
- Додати 9 ресурсів як дочірні вузли з `parent: 'resources'` та підписами з `value`
- Застосувати `layout({ name: 'grid', rows: 3, cols: 3 })`

**Функції перемикання вигляду:**

`showMainGraph()`:

- Показати `#cy-graph-main` та `.controls`
- Приховати `#cy-graph-detail` та `#backButton`

`showDetailGraph()`:

- Приховати `#cy-graph-main` та `.controls`
- Показати `#cy-graph-detail` та `#backButton`
- Перемалювати layout детального графу

**Обробники подій:**

- **Кнопка "Запустити Агента"** (`#applyButton`):
  - Отримати `goal` з `#goalInput.value`
  - `fetch('/api/v1/apply-mechanism', { method: 'POST', body: JSON.stringify({ target_goal: goal }), headers: { 'Content-Type': 'application/json' } })`
  - Після успішної відповіді викликати `updateMainGraph()` (це оновить обидва графи)

- **Клік на вузол "Ресурси"** в `cy_main`:
  - `cy_main.on('tap', 'node[name="Ресурси"]', () => showDetailGraph())`

- **Кнопка "Назад"** (`#backButton`):
  - Викликати `showMainGraph()`

**Запуск:**

- Викликати `updateMainGraph()` при `DOMContentLoaded`
- Викликати `showMainGraph()` для початкового стану

## 7. Стилі (app/static/style.css)

- Сучасний, чистий UI з базовою палітрою (блакитний/зелений/сірий)
- `#cy-graph-main, #cy-graph-detail`: `width: 100%; height: 80vh; border: 1px solid #ccc;`
- Панель управління (`.controls`): flexbox-центрування, padding, тіні для кнопок
- `#backButton`: позиціонування у верхньому лівому куті, стилізація як secondary button
- Респонсивність для десктопів

## 8. .gitignore

```
.venv/
venv/
__pycache__/
*.pyc
.env
```

## Критерії успіху (Definition of Done)

✅ Проєкт запускається: `uvicorn app.main:app --reload`

✅ Браузер (`http://127.0.0.1:8000`) показує інтерактивний граф

✅ Граф візуалізує початковий стан (5 компонентів + 9 ресурсів)

✅ Менеджер вводить ціль у текстове поле

✅ Кнопка "Запустити Агента" надсилає POST запит

✅ Термінал логує "думки" агента

✅ Стан системи оновлюється на бекенді

✅ Граф автоматично оновлюється, відображаючи нові значення ресурсів (візуально — змінений розмір вузлів)

✅ Кібернетичний цикл замкнено: Ціль → Аналіз → Зміна → Зворотний зв'язок