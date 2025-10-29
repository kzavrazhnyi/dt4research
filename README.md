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
- Current baseline: 1.0.0.2 (UI/UX enhancements)
- Upcoming stages: 1.0.0.3 “Robust Backend”, 1.0.0.4 “Persistence” (`plan/` directory)

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
- Актуальна база: 1.0.0.2 (покращення UI/UX)
- Наступні етапи: 1.0.0.3 «Надійний бекенд», 1.0.0.4 «Персистентність» (`plan/`)

### Технології
- Бекенд: FastAPI, Uvicorn, Pydantic
- Фронтенд: Cytoscape.js, нативний JavaScript
- Дані: In-memory (готовий перехід до SQLite/PostgreSQL)

### Ліцензія
Проєкт поширюється на умовах MIT License — дивіться `LICENSE`.

