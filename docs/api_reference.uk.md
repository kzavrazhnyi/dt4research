# dt4research — Довідник API (v1.1.0)

Базовий URL: `http://127.0.0.1:8000`

Автентифікація: не потрібна (dev)
Content-Type: `application/json`

## GET /
Повертає UI (Cytoscape.js граф, перемикач мови)

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
Запускає агента для вказаної цілі, зберігає новий стан і історію.

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

Помилки: 422 при валідації (min_length=3).

## GET /api/v1/agent-runs
Історія запусків з пагінацією.

Параметри: `limit` (int, 20 за замовчуванням), `offset` (int, 0 за замовчуванням)

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
    "applied_rules_explanation": {"Communication": 15}
  }]
}
```

## POST /api/v1/system-reset
Скидає симуляцію до початкового стану. Усередині очищує `ResourceRow`, `ComponentRow`, `AgentRunRow`, після чого викликає `INITIAL_STATE` для повторного заповнення.

- Тіло запиту: відсутнє
- Відповідь 200:
```json
{
  "components": [{ "id": "comp-strategy", "name": "Strategy", "status": "Active" }],
  "resources": [{ "id": "res-tech", "name": "Technology Solutions", "type": "Technological", "value": 62.0 }]
}
```

## Моделі (Pydantic)
- `MechanismInput`: `{ "target_goal": "string (min 3)" }`
- `MechanismResponse`: `{ "newState": SystemState, "explanation": string, "explanation_details": {ResourceType:number} }`
- `SystemState`: `{ "components": [...], "resources": [...] }`
- `ResourceType` (EN): Communication, Educational, Financial, Informational, Operational, Organizational, Risk, Strategic, Technological



