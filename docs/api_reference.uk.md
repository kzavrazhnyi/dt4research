# dt4research — Довідник API (v1.4.0)

Базовий URL: `http://127.0.0.1:8000`

Автентифікація: не потрібна (dev)
Content-Type: `application/json`

## GET /
Повертає SPA-дашборд (граф Cytoscape.js, перемикач мови).

## GET /settings
Повертає сторінку налаштувань (огляд середовища, замасковані URL підключень).

## GET /api/v1/system-state
Повертає поточний стан системи з БД.

Відповідь 200:
```json
{
  "components": [{ "id": "comp-strategy", "name": "Strategy", "status": "Active" }],
  "resources": [{ "id": "res-tech", "name": "Technology Solutions", "type": "Technological", "value": 62.0 }]
}
```

## POST /api/v1/apply-mechanism
Запускає агента для вказаної цілі, зберігає новий стан і запис історії.

Тіло запиту:
```json
{ "target_goal": "Покращити сервіс для клієнтів" }
```

Відповідь 200:
```json
{
  "newState": { /* SystemState */ },
  "explanation": "Communication +15; Informational +10; Operational +10",
  "explanation_details": { "Communication": 15, "Informational": 10, "Operational": 10 }
}
```

Помилки: 422 при валідації ("target_goal" `min_length=3`).

## GET /api/v1/agent-runs
Історія запусків з пагінацією.

Параметри: `limit` (int, 20 за замовчуванням), `offset` (int, 0 за замовчуванням).

Відповідь 200:
```json
{
  "total": 3,
  "limit": 20,
  "offset": 0,
  "items": [{
    "id": 1,
    "timestamp": "2025-10-30T12:00:00Z",
    "input_goal": "Покращити сервіс для клієнтів",
    "applied_rules_explanation": {"Communication": 15, "Informational": 10, "Operational": 10}
  }]
}
```

## POST /api/v1/system-reset
Скидає симуляцію до початкового стану. Усередині очищує `ResourceRow`, `ComponentRow`, `AgentRunRow`, після чого повторно застосовує `INITIAL_STATE`.

- Тіло запиту: відсутнє.
- Відповідь 200:
```json
{
  "components": [{ "id": "comp-strategy", "name": "Strategy", "status": "Active" }],
  "resources": [{ "id": "res-tech", "name": "Technology Solutions", "type": "Technological", "value": 62.0 }]
}
```

## GET /api/v1/health/db
Перевірка стану БД. Встановлює підключення через репозиторій і повертає замаскований URL (облікові дані замінено на `***`).

Відповідь 200:
```json
{
  "ok": true,
  "status": "connected",
  "url": "postgresql://***@host.example/neondb?sslmode=require",
  "driver": "postgresql"
}
```

У разі помилки повертається замаскований URL та санітайзоване повідомлення.

## GET /api/v1/health/rabbit
Перевірка RabbitMQ/CloudAMQP. Рядок підключення завжди маскується.

Відповідь 200:
```json
{
  "ok": true,
  "status": "connected",
  "url": "amqps://***@duck.lmq.cloudamqp.com/tcflaeri",
  "driver": "pika"
}
```

Помилки також повертають замаскований URL.

## Моделі (Pydantic)
- `MechanismInput`: `{ "target_goal": "string (min 3)" }`
- `MechanismResponse`: `{ "newState": SystemState, "explanation": string, "explanation_details": {ResourceType:number} }`
- `SystemState`: `{ "components": [...], "resources": [...] }`
- `ResourceType` (EN): Communication, Educational, Financial, Informational, Operational, Organizational, Risk, Strategic, Technological

## Нотатки
- Ендпоінти здоровʼя маскують облікові дані між `//` та `@`.
- Формат логування керується `LOG_FORMAT` (`console` | `json`).
- Коефіцієнти правил конфігуруються через `.env`; дефолти застосовуються автоматично, якщо змінні відсутні.
