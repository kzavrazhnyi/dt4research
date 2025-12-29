# Plan: Manager Cockpit v1.1.0 (Stage 2)

## Scope

Implement: (1) UI memory & immediate feedback; (2) Scenario reset API + UI; (3) Basic analytics (nVPA indices) in sidebar.

## Files to change

- app/templates/index.html
- app/static/style.css
- app/static/app.js
- app/main.py
- (reuse) app/repository.py, app/initial_state.py

## UI changes (index.html)

- Under `.details` add history block:
- <div class="history"><h3>Історія Запусків</h3><ul id="historyList"></ul></div>
- In sidebar add analytics block:
- <div class="analytics"><h3>Ключові Індекси</h3><div id="analyticsContent">...</div></div>
- In `.control-panel` add reset button:
- <button id="resetButton" class="reset-btn">Скинути стан</button>

## Styles (style.css)

- Add `.history`, `.history h3`, `.history ul`, `.history li` basic layout; scrollable list with subtle borders.
- Add `.reset-btn` prominent red style with hover state.
- Add `.analytics` container and mini-bar styles (e.g., `.bar`, `.bar-fill`) for A% and S indices.
- Add lightweight toast styles (e.g., `#toast` fixed bottom-right, fade-in/out).

## Frontend logic (app.js)

- Create async `loadAgentHistory()`:
- fetch('/api/v1/agent-runs?limit=10') → JSON → render `<li>` entries with `timestamp`, `input_goal`, `applied_rules_explanation` into `#historyList`.
- On DOMContentLoaded end: call `loadAgentHistory()`.
- In existing `applyButton` click handler, inside `if (response.ok) { const data = await response.json(); ... }`:
- Show `data.explanation` via toast.
- Call `loadAgentHistory()` to refresh list immediately.
- Add `resetButton` handler with confirm():
- If confirmed, POST '/api/v1/system-reset'. On success: call `updateMainGraph()` and `loadAgentHistory()`.
- In `updateMainGraph()` after fetching system state:
- Compute indices:
  - Adaptiveness A% = (Technological + Strategic + Informational)/3
  - Sustainability S = (Technological + Educational + Risk)/3
- Render A and S values (0–100) with mini-bars into `#analyticsContent`.
- Add small `showToast(message)` utility that creates/removes a toast element.

## Backend API (app/main.py)

- Add POST `/api/v1/system-reset`:
- Use `repository` to clear `ResourceRow`, `ComponentRow`, `AgentRunRow`.
- Call `repository.seed_initial_state(INITIAL_STATE)`.
- Return 200 with the initial system state (same shape as GET /api/v1/system-state).
- Keep compatibility with existing models.

## Validation & Compatibility

- Ensure names of resources match UI lookup (Technological/Стратегічний/Інформаційний/Освітній/Ризиковий). If localized, map by `type` keys defined in `models.py`.
- Preserve existing endpoints and event wiring.
- Do not change server startup scripts; continue using `start_server.ps1`/`.bat`.

---

## Українська версія

# План: Менеджерський Кокпіт v1.1.0 (Етап 2)

## Обсяг робіт

Реалізувати: (1) Пам'ять UI та миттєвий зворотний зв'язок; (2) API скидання сценарію + UI; (3) Базова аналітика (індекси nVPA) у бічній панелі.

## Файли для зміни

- app/templates/index.html
- app/static/style.css
- app/static/app.js
- app/main.py
- (використати) app/repository.py, app/initial_state.py

## Зміни UI (index.html)

- Під `.details` додати блок історії:
- <div class="history"><h3>Історія Запусків</h3><ul id="historyList"></ul></div>
- У бічній панелі додати блок аналітики:
- <div class="analytics"><h3>Ключові Індекси</h3><div id="analyticsContent">...</div></div>
- У `.control-panel` додати кнопку скидання:
- <button id="resetButton" class="reset-btn">Скинути стан</button>

## Стилі (style.css)

- Додати `.history`, `.history h3`, `.history ul`, `.history li` базовий макет; прокручуваний список з тонкими рамками.
- Додати `.reset-btn` помітний червоний стиль зі станом наведення.
- Додати контейнер `.analytics` та стилі міні-барів (напр., `.bar`, `.bar-fill`) для індексів A% та S.
- Додати легкі стилі тостів (напр., `#toast` фіксований внизу справа, з'явлення/зникнення).

## Логіка фронтенду (app.js)

- Створити асинхронну `loadAgentHistory()`:
- fetch('/api/v1/agent-runs?limit=10') → JSON → відображення записів `<li>` з `timestamp`, `input_goal`, `applied_rules_explanation` у `#historyList`.
- На кінці DOMContentLoaded: викликати `loadAgentHistory()`.
- У наявному обробнику кліку `applyButton`, всередині `if (response.ok) { const data = await response.json(); ... }`:
- Показати `data.explanation` через тост.
- Викликати `loadAgentHistory()` для миттєвого оновлення списку.
- Додати обробник `resetButton` з confirm():
- Якщо підтверджено, POST '/api/v1/system-reset'. При успіху: викликати `updateMainGraph()` та `loadAgentHistory()`.
- У `updateMainGraph()` після отримання стану системи:
- Обчислити індекси:
  - Адаптивність A% = (Технологічний + Стратегічний + Інформаційний)/3
  - Сталість S = (Технологічний + Освітній + Ризиковий)/3
- Відобразити значення A та S (0–100) з міні-барами у `#analyticsContent`.
- Додати невелику утиліту `showToast(message)`, яка створює/видаляє елемент тосту.

## Backend API (app/main.py)

- Додати POST `/api/v1/system-reset`:
- Використати `repository` для очищення `ResourceRow`, `ComponentRow`, `AgentRunRow`.
- Викликати `repository.seed_initial_state(INITIAL_STATE)`.
- Повернути 200 з початковим станом системи (такий самий формат, як GET /api/v1/system-state).
- Зберегти сумісність з наявними моделями.

## Валідація та сумісність

- Переконатися, що назви ресурсів відповідають пошуку UI (Technological/Стратегічний/Інформаційний/Освітній/Ризиковий). Якщо локалізовано, зіставляти за ключами `type`, визначеними в `models.py`.
- Зберегти наявні ендпоінти та підключення подій.
- Не змінювати скрипти запуску сервера; продовжувати використовувати `start_server.ps1`/`.bat`.