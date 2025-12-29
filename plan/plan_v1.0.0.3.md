# Project Plan — Version 1.0.0.3

## English Version

## Stage 2: Strengthening the "Nervous System" (Robust Backend)
Goal: Reliable, tested, configurable agent logic.

Corresponds to previous items: Backend (3), Agent Logic (4), Configuration (6), Testing (7), Security (8).

### 2.1 Input Validation
- In `models.py` add `min_length` (e.g., 3) to `MechanismInput.target_goal`.

### 2.2 Configuration via .env
- Add `python-dotenv`.
- Extract growth coefficients from `agent_logic.py` to `.env` (e.g., `TECH_INCREASE=20`, `EDU_INCREASE=15`, etc.).
- Read values in `agent_logic.py` with defaults.

### 2.3 API Feedback
- `POST /api/v1/apply-mechanism` returns object:

```json
{
  "newState": SystemState,
  "explanation": "Applied rule 'Ecology': Technological +20, Educational +15, Risk +10"
}
```

- `agent_logic.run_mock_analysis()` also returns explanation structure (rule id, deltas by resources).
- This feeds "Run History" in UI.

### 2.4 Tests
- `tests/test_api.py` (pytest + FastAPI TestClient):
  - GET `/api/v1/system-state` responds with schema.
  - POST `/api/v1/apply-mechanism` changes values of expected resources within 0–100.
  - Check run in venv (verify path `sys.executable`).

### 2.5 Environment / Security
- Add CORS (FastAPI middleware) for potential separate frontend.
- Standardized logging (JSON handler in prod, readable in dev).

### Stage 2 Success Criteria
- Configuration with .env for coefficients works.
- API returns explanation of changes.
- Basic test suite exists, passing in venv.
- CORS enabled and configured.

---

## Українська версія

# План проєкту — версія 1.0.0.3

## Етап 2: Посилення «Нервової Системи» (Robust Backend)
Мета: Надійна, тестована, конфігуровна логіка агента.

Відповідає попереднім пунктам: Backend (3), Логіка агента (4), Конфігурація (6), Тестування (7), Безпека (8).

### 2.1 Валідація вводу
- У `models.py` додати `min_length` (напр. 3) до `MechanismInput.target_goal`.

### 2.2 Конфігурація через .env
- Додати `python-dotenv`.
- Винести коефіцієнти зростання з `agent_logic.py` у `.env` (напр. `TECH_INCREASE=20`, `EDU_INCREASE=15` тощо).
- Зчитувати значення у `agent_logic.py` з дефолтами.

### 2.3 Зворотний зв'язок API
- `POST /api/v1/apply-mechanism` повертає об’єкт:

```json
{
  "newState": SystemState,
  "explanation": "Застосовано правило 'Екологія': Технологічний +20, Освітній +15, Ризиковий +10"
}
```

- `agent_logic.run_mock_analysis()` повертає також структуру пояснення (rule id, дельти по ресурсах).
- Це живить «Історію запусків» у UI.

### 2.4 Тести
- `tests/test_api.py` (pytest + FastAPI TestClient):
  - GET `/api/v1/system-state` відповідає схемі.
  - POST `/api/v1/apply-mechanism` змінює значення очікуваних ресурсів у межах 0–100.
  - Перевірка запуску у venv (перевірити шлях `sys.executable`).

### 2.5 Оточення / Безпека
- Додати CORS (FastAPI middleware) для потенційного відокремленого фронтенду.
- Стандартизоване логування (JSON-хендлер у проді, читабельний у dev).

### Критерії успіху Етапу 2
- Працює конфігурація з .env для коефіцієнтів.
- API повертає пояснення змін.
- Є базовий набір тестів, що проходять у venv.
- CORS увімкнений і налаштований.

