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