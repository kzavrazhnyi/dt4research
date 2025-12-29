# dt4research — Cybernetic Control System / Кібернетична система керування

**Research Topic / Тема дослідження:** Formation of Management Mechanisms for Digital Transformation of Enterprises / Формування управлінських механізмів цифрової трансформації підприємств

## English Version

### Overview

dt4research is an interactive research platform that simulates organizational resource dynamics through a cybernetic control loop. The platform is designed for scientific research on the formation of management mechanisms for digital transformation of enterprises. The solution combines a FastAPI backend, a rule-based agent, and a Cytoscape.js visualization. The user interface is bilingual: English is the default language, and Ukrainian can be enabled from the UI toggle.

### Quick Start

1. **Activate the virtual environment**
   - PowerShell
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - CMD
     ```batch
     venv\Scripts\activate.bat
     ```
2. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```
3. **Launch the server (recommended scripts)**
   - PowerShell
     ```powershell
     .\start_server.ps1
     ```
   - CMD
     ```batch
     start_server.bat
     ```
   The scripts enforce UTF-8 output, activate `venv`, and start FastAPI with hot reload at `http://127.0.0.1:8000`.

> Manual commands are technically possible, but the project rules require using the provided scripts for consistency.

### Project Structure
```
dt4research/
├── app/
│   ├── main.py          # FastAPI entrypoint & endpoints
│   ├── models.py        # Pydantic schemas
│   ├── agent_logic.py   # Rule-based agent with .env coefficients
│   ├── templates/
│   │   └── index.html   # HTML template (language switcher)
│   └── static/
│       ├── app.js       # Cytoscape + UI logic (bilingual)
│       └── style.css    # UI styling
├── plan/                # Planning docs and diagrams
├── requirements.txt     # Python dependencies
├── start_server.ps1     # PowerShell start script
└── start_server.bat     # CMD start script
```

### Cursor Development Rules
- Always work in the virtual environment `venv/`; activate via PowerShell `./venv/Scripts/Activate.ps1`.
- Always start the server using `start_server.ps1` or `start_server.bat` (do not run `uvicorn` directly).
- PowerShell scripts must enforce UTF-8 output for correct Ukrainian text.
- We work on Windows; do not use shell operator `&&` in scripts/commands.
- Code comments: English first with concise Ukrainian in parentheses.
- Follow PEP 8; add type hints and docstrings.
- UI must be bilingual (EN/UK). Do not hardcode labels in HTML; set them from `app/static/app.js` using locale keys.
- New UI strings: add keys to `locales.en` and `locales.uk` in `app/static/app.js` during development; ensure both are complete before merging.

### API Endpoints
- `GET /` – interactive dashboard
- `GET /api/v1/system-state` – current `SystemState`
- `POST /api/v1/apply-mechanism` – applies agent logic, returns `newState` + explanation details
- `GET /api/v1/agent-runs` – history of agent runs (query: `limit`, `offset`)
- `POST /api/v1/system-reset` – reset to initial state (clears state and history, re-seeds)

### Cybernetic Concept
```
Manager Goal → Agent Analysis → State Update → Feedback Loop
```
- **Resource types (9):** Communication, Educational, Financial, Informational, Operational, Organizational, Risk, Strategic, Technological
- **Key components (5):** Strategy, Structure, Processes, Culture, Resources

### Planning Snapshot
- Current version: 1.4.0 "Scientific Simulation & Metrics"
  - Scientific metrics calculation (S, C, A indices)
  - Simulation engine for time series data generation
  - Analytics visualization with charts and before/after comparisons
  - New API endpoints for simulation and metrics
  - Frontend panel for scientific analytics
- Previous versions:
  - 1.2.0: UI Memory & Feedback, System Reset, Basic Analytics, Health Checks
  - 1.0.0.4: Persistence via SQLite/SQLModel
  - 1.0.0.3: Robust Backend with validation and bilingual UI
  - 1.0.0.2: UI/UX enhancements

### Configuration (.env)
Supported environment variables (optional; sensible defaults are used):
- `LOG_FORMAT` = `console` | `json`
- `LOG_LEVEL` = `INFO` (typical values: DEBUG, INFO, WARNING, ERROR)
- Rule coefficients (example defaults in parentheses):
  - `RULE_ECO_TECH` (20), `RULE_ECO_EDU` (15), `RULE_ECO_RISK` (10)
  - `RULE_CUSTOMER_COMM` (15), `RULE_CUSTOMER_INFO` (10), `RULE_CUSTOMER_OPER` (10)
  - `RULE_INNOV_TECH` (25), `RULE_INNOV_STRAT` (15), `RULE_INNOV_FIN` (10)
  - `RULE_PARTNERS_ORG` (20), `RULE_PARTNERS_COMM` (10)
  - `RULE_RISK_RISK` (20), `RULE_RISK_OPER` (10)
  - `RULE_EDU_EDU` (20), `RULE_EDU_ORG` (10)
  - `RULE_DEFAULT_TECH` (5), `RULE_DEFAULT_STRAT` (5), `RULE_DEFAULT_FIN` (5)

### Internationalization
- English is the default UI language; Ukrainian can be selected from the page header.
- Graph node labels, details panel, tooltips and controls update instantly on language change.

#### Localization Policy (i18n/l10n)
- Supported languages: English (EN) and Ukrainian (UK). EN is the source-of-truth for new strings.
- Development workflow:
  - Implement new UI text in EN first and add string keys to `locales.en` in `app/static/app.js`.
  - Add corresponding keys to `locales.uk` immediately (may temporarily mirror EN during prototyping).
  - Before merging to `main`, ensure UK translations are complete and verified in UI.
- Do not hardcode user-facing text in `index.html`. Use element IDs and set labels from `app.js` based on the current locale.
- Scope of localization: history block title, analytics block title, indices labels, reset button label, confirm/toast messages, and any new UI labels.
- Testing: verify both EN/UK via the language switch; missing keys must fall back to EN and be logged during development.

### UI Additions in v1.1.0
- History block (Run History / Історія запусків): shows timestamp, input goal, explanation for last N runs.
- Analytics block (Key Indices / Ключові індекси):
  - Adaptiveness A = (Technological + Strategic + Informational) / 3
  - Sustainability S = (Technological + Educational + Risk) / 3
  - Displayed with mini-bars (0–100).

### Testing
Run tests from `venv`:
```powershell
./venv/Scripts/python.exe -m pytest -q
```

### Technology Stack
- Backend: FastAPI, Uvicorn, Pydantic
- Frontend: Cytoscape.js, vanilla JavaScript
- Storage: In-memory (designed for SQLite/PostgreSQL transition)

-### Version Video Presentations (Newest first)
PDF: Smart data with Cursor AI — [Download](/plan/Smart%20data%20with%20Cursor%20AI.%20Розумні%20дані%20з%20Cursor%20AI.pdf)
- dt4research 1.1.0 — Smart data with Cursor AI: [YouTube](https://www.youtube.com/watch?v=DL6YPSd6ppk)
- dt4research 1.0.0.4 — Smart data with Cursor AI and management mechanisms: [YouTube](https://www.youtube.com/watch?v=z7zIV4yAKOw)
- dt4research 1.0.0.3 — Smart data with Cursor AI and management mechanisms: [YouTube](https://www.youtube.com/watch?v=mZISM3IhgOw)
- dt4research 1.0.0.2 — Smart data with Cursor AI and management mechanisms: [YouTube](https://www.youtube.com/watch?v=HrORYhMlNfU)
- dt4research 1.0.0.1 — Smart data with Cursor AI and management mechanisms: [YouTube](https://www.youtube.com/watch?v=cal_GzkN1HM)
- 0 — Smart data with Cursor AI. Get started: [YouTube](https://www.youtube.com/watch?v=6xtUx7HiTqQ)

### License
MIT License — see `LICENSE`.

---

## Українська версія

### Огляд

dt4research — це інтерактивна платформа для дослідження, що моделює динаміку ресурсів організації через кібернетичний цикл управління. Платформа призначена для наукового дослідження з формування управлінських механізмів цифрової трансформації підприємств. Рішення складається з FastAPI бекенду, правилового агента та візуалізації Cytoscape.js. Інтерфейс двомовний: англійська використовується за замовчуванням, перемикач дозволяє увімкнути українську.

### Швидкий старт
1. **Активуйте віртуальне середовище**
   - PowerShell
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - CMD
     ```batch
     venv\Scripts\activate.bat
     ```
2. **Встановіть залежності**
   ```powershell
   pip install -r requirements.txt
   ```
3. **Запустіть сервер (рекомендовані скрипти)**
   - PowerShell
     ```powershell
     .\start_server.ps1
     ```
   - CMD
     ```batch
     start_server.bat
     ```
   Скрипти встановлюють UTF-8, активують `venv` і запускають FastAPI з hot reload на `http://127.0.0.1:8000`.

> Ручний запуск можливий, але правила проєкту вимагають використовувати підготовлені скрипти для уніфікованого процесу.

### Структура проєкту
```
dt4research/
├── app/
│   ├── main.py          # Бекенд FastAPI та ендпоінти
│   ├── models.py        # Pydantic-схеми
│   ├── agent_logic.py   # Логіка агента з коефіцієнтами з .env
│   ├── templates/
│   │   └── index.html   # Головний шаблон (перемикач мов)
│   └── static/
│       ├── app.js       # Клієнтська логіка Cytoscape.js (двомовна)
│       └── style.css    # Оформлення інтерфейсу
├── plan/                # Документація та діаграми
├── requirements.txt     # Python-залежності
├── start_server.ps1     # PowerShell-скрипт запуску
└── start_server.bat     # Скрипт запуску для CMD
```

### API-ендпоінти
- `GET /` — веб-інтерфейс з інтерактивним графом
- `GET /api/v1/system-state` — отримати поточний `SystemState`
- `POST /api/v1/apply-mechanism` — застосувати логіку агента та отримати `newState` з поясненням
- `GET /api/v1/agent-runs` — історія запусків агента (параметри: `limit`, `offset`)
- `POST /api/v1/system-reset` — скидання до початкового стану (очищує стан і історію, перевисіває)

### Кібернетична концепція
```
Менеджерська ціль → Аналіз агента → Оновлення стану → Зворотний зв'язок
```
- **Типи ресурсів (9):** Комунікаційний, Освітній, Фінансовий, Інформаційний, Операційний, Організаційний, Ризиковий, Стратегічний, Технологічний
- **Ключові компоненти (5):** Стратегія, Структура, Процеси, Культура, Ресурси

### План розвитку
- Поточна версія: 1.4.0 «Наукова симуляція та метрики»
  - Обчислення наукових метрик (індекси S, C, A)
  - Рушій симуляції для генерації часових рядів даних
  - Візуалізація аналітики з графіками та порівнянням до/після
  - Нові API ендпоінти для симуляції та метрик
  - Панель фронтенду для наукової аналітики
- Попередні версії:
  - 1.2.0: Пам'ять і зворотний зв'язок у UI, скидання системи, базова аналітика, health checks
  - 1.0.0.4: Персистентність на SQLite/SQLModel
  - 1.0.0.3: Надійний бекенд з валідацією та двомовним UI
  - 1.0.0.2: Поліпшення UI/UX

### Налаштування (.env)
Підтримувані змінні середовища (опційно; є адекватні значення за замовчуванням):
- `LOG_FORMAT` = `console` | `json`
- `LOG_LEVEL` = `INFO` (типові: DEBUG, INFO, WARNING, ERROR)
- Коефіцієнти правил (типові значення в дужках):
  - `RULE_ECO_TECH` (20), `RULE_ECO_EDU` (15), `RULE_ECO_RISK` (10)
  - `RULE_CUSTOMER_COMM` (15), `RULE_CUSTOMER_INFO` (10), `RULE_CUSTOMER_OPER` (10)
  - `RULE_INNOV_TECH` (25), `RULE_INNOV_STRAT` (15), `RULE_INNOV_FIN` (10)
  - `RULE_PARTNERS_ORG` (20), `RULE_PARTNERS_COMM` (10)
  - `RULE_RISK_RISK` (20), `RULE_RISK_OPER` (10)
  - `RULE_EDU_EDU` (20), `RULE_EDU_ORG` (10)
  - `RULE_DEFAULT_TECH` (5), `RULE_DEFAULT_STRAT` (5), `RULE_DEFAULT_FIN` (5)

### Локалізація
- Англійська — основна мова інтерфейсу; українська обирається у шапці сторінки.
- Підписи вузлів графа, панель деталей, тултіпи та елементи керування оновлюються миттєво при зміні мови.

#### Правила локалізації (i18n/l10n)
- Підтримувані мови: Англійська (EN) та Українська (UK). EN — джерело правди для нових рядків.
- Робочий процес:
  - Спочатку додаємо новий текст UI англійською та ключ у `locales.en` (`app/static/app.js`).
  - Одразу створюємо відповідний ключ у `locales.uk` (на етапі прототипу допускається тимчасовий текст EN).
  - Перед злиттям у `main` обов’язково завершуємо переклад UK і перевіряємо в UI.
- Не хардкодити тексти інтерфейсу у `index.html`. Використовувати ідентифікатори елементів і встановлювати тексти з `app.js` згідно з поточною мовою.
- Обов’язково локалізуємо: заголовок історії, заголовок аналітики, підписи індексів, підпис кнопки скидання, повідомлення підтвердження та тости, а також усі нові написи UI.
- Тестування: перевіряти EN/UK через перемикач; відсутні ключі мають тимчасово підставляти EN та бути виправлені до релізу.

### UI-доповнення у v1.1.0
- Блок історії (Run History / Історія запусків): показує час, ціль і пояснення останніх запусків.
- Блок аналітики (Key Indices / Ключові індекси):
  - A = (Technological + Strategic + Informational) / 3
  - S = (Technological + Educational + Risk) / 3
  - Відображаються міні-барами (0–100).

### Тестування
Запуск тестів із `venv`:
```powershell
./venv/Scripts/python.exe -m pytest -q
```

### Технології
- Бекенд: FastAPI, Uvicorn, Pydantic
- Фронтенд: Cytoscape.js, нативний JavaScript
- Дані: In-memory (готовий перехід до SQLite/PostgreSQL)

### Відеопрезентації версій (Найновіші спочатку)
PDF: Smart data with Cursor AI / Розумні дані з Cursor AI — [Завантажити](/plan/Smart%20data%20with%20Cursor%20AI.%20Розумні%20дані%20з%20Cursor%20AI.pdf)
- (dt4research 1.1.0) Smart data with Cursor AI / Розумні дані з Cursor AI: [YouTube](https://www.youtube.com/watch?v=DL6YPSd6ppk)
- (dt4research 1.0.0.4) Розумні дані з Cursor AI та формування управлінських механізмів цифрової трансформації підприємств: [YouTube](https://www.youtube.com/watch?v=z7zIV4yAKOw)
- (dt4research 1.0.0.3) Розумні дані з Cursor AI та формування управлінських механізмів цифрової трансформації підприємств: [YouTube](https://www.youtube.com/watch?v=mZISM3IhgOw)
- (dt4research 1.0.0.2) Розумні дані з Cursor AI та формування управлінських механізмів цифрової трансформації підприємств: [YouTube](https://www.youtube.com/watch?v=HrORYhMlNfU)
- (dt4research 1.0.0.1) Розумні дані з Cursor AI та формування управлінських механізмів цифрової трансформації підприємств: [YouTube](https://www.youtube.com/watch?v=cal_GzkN1HM)
- 0 — Розумні дані з Cursor AI. Початок: [YouTube](https://www.youtube.com/watch?v=6xtUx7HiTqQ)

### Ліцензія
Проєкт поширюється на умовах MIT License — дивіться `LICENSE`.

