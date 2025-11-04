# dt4research — Cybernetic Control System / Кібернетична система керування

## English Version

### Overview

dt4research is an interactive research platform that simulates organizational resource dynamics through a cybernetic control loop. The solution combines a FastAPI backend, a rule-based agent, and a Cytoscape.js visualization. The user interface is bilingual: English is the default language, and Ukrainian can be enabled from the UI toggle.

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

### Cybernetic Concept
```
Manager Goal → Agent Analysis → State Update → Feedback Loop
```
- **Resource types (9):** Communication, Educational, Financial, Informational, Operational, Organizational, Risk, Strategic, Technological
- **Key components (5):** Strategy, Structure, Processes, Culture, Resources

### Planning Snapshot
- Completed: 1.0.0.3 “Robust Backend”
  - Input validation (`min_length` on mechanism input)
  - Environment-based coefficients via `.env` (defaults applied if missing)
  - API response returns `newState`, `explanation`, `explanation_details`
  - CORS enabled; standardized logging (console or JSON via `LOG_FORMAT`)
  - Test suite with `pytest` (3 tests) running under `venv`
  - Bilingual UI with runtime language toggle
- Previous baseline: 1.0.0.2 (UI/UX enhancements)
- Next stage: 1.0.0.4 “Persistence” (`plan/` directory)

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

### Testing
Run tests from `venv`:
```powershell
./venv/Scripts/python.exe -m pytest -q
```

### Technology Stack
- Backend: FastAPI, Uvicorn, Pydantic
- Frontend: Cytoscape.js, vanilla JavaScript
- Storage: In-memory (designed for SQLite/PostgreSQL transition)

### License
MIT License — see `LICENSE`.

---

## Українська версія

### Огляд

dt4research — це інтерактивна платформа для дослідження, що моделює динаміку ресурсів організації через кібернетичний цикл управління. Рішення складається з FastAPI бекенду, правилового агента та візуалізації Cytoscape.js. Інтерфейс двомовний: англійська використовується за замовчуванням, перемикач дозволяє увімкнути українську.

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

### Кібернетична концепція
```
Менеджерська ціль → Аналіз агента → Оновлення стану → Зворотний зв'язок
```
- **Типи ресурсів (9):** Комунікаційний, Освітній, Фінансовий, Інформаційний, Операційний, Організаційний, Ризиковий, Стратегічний, Технологічний
- **Ключові компоненти (5):** Стратегія, Структура, Процеси, Культура, Ресурси

### План розвитку
- Виконано: 1.0.0.3 «Надійний бекенд»
  - Валідація вводу (`min_length` для цілі механізму)
  - Коефіцієнти з `.env` (із дефолтами за відсутності файлу)
  - Відповідь API містить `newState`, `explanation`, `explanation_details`
  - Увімкнено CORS; стандартизоване логування (`LOG_FORMAT=console|json`)
  - Набір тестів `pytest` (3 тести) у `venv`
  - Двомовний UI з перемикачем мови
- Попередня база: 1.0.0.2 (поліпшення UI/UX)
- Наступний етап: 1.0.0.4 «Персистентність» (`plan/`)

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

### Тестування
Запуск тестів із `venv`:
```powershell
./venv/Scripts/python.exe -m pytest -q
```

### Технології
- Бекенд: FastAPI, Uvicorn, Pydantic
- Фронтенд: Cytoscape.js, нативний JavaScript
- Дані: In-memory (готовий перехід до SQLite/PostgreSQL)

### Ліцензія
Проєкт поширюється на умовах MIT License — дивіться `LICENSE`.

