# dt4research — API Reference (v1.4.0)

Base URL: `http://127.0.0.1:8000`

Authentication: not required (dev)
Content-Type: `application/json`

## GET /
Serves the SPA dashboard (Cytoscape.js graph, language switch).

## GET /settings
Serves the settings UI (environment overview, masked connection URLs).

## GET /api/v1/system-state
Returns the current system state from the database.

Response 200:
```json
{
  "components": [{ "id": "comp-strategy", "name": "Strategy", "status": "Active" }],
  "resources": [{ "id": "res-tech", "name": "Technology Solutions", "type": "Technological", "value": 62.0 }]
}
```

## POST /api/v1/apply-mechanism
Runs the agent for the provided goal, persists the new state, and writes a history entry.

Request body:
```json
{ "target_goal": "Improve customer service" }
```

Response 200:
```json
{
  "newState": { /* SystemState */ },
  "explanation": "Communication +15; Informational +10; Operational +10",
  "explanation_details": { "Communication": 15, "Informational": 10, "Operational": 10 }
}
```

Errors: 422 on validation failure ("target_goal" `min_length=3`).

## GET /api/v1/agent-runs
Paginated history of agent runs.

Query: `limit` (int, default 20), `offset` (int, default 0).

Response 200:
```json
{
  "total": 3,
  "limit": 20,
  "offset": 0,
  "items": [{
    "id": 1,
    "timestamp": "2025-10-30T12:00:00Z",
    "input_goal": "Improve customer service",
    "applied_rules_explanation": {"Communication": 15, "Informational": 10, "Operational": 10}
  }]
}
```

## POST /api/v1/system-reset
Resets the simulation to its initial state. Internally clears `ResourceRow`, `ComponentRow`, and `AgentRunRow`, then re-seeds `INITIAL_STATE`.

- Request body: none.
- Response 200:
```json
{
  "components": [{ "id": "comp-strategy", "name": "Strategy", "status": "Active" }],
  "resources": [{ "id": "res-tech", "name": "Technology Solutions", "type": "Technological", "value": 62.0 }]
}
```

## GET /api/v1/health/db
Database health check. Establishes a connection through the repository and returns a masked URL (credentials replaced with `***`).

Response 200:
```json
{
  "ok": true,
  "status": "connected",
  "url": "postgresql://***@host.example/neondb?sslmode=require",
  "driver": "postgresql"
}
```

Failure responses include the masked URL and a sanitized error message.

## GET /api/v1/health/rabbit
RabbitMQ/CloudAMQP health check. Connection URLs are always masked.

Response 200:
```json
{
  "ok": true,
  "status": "connected",
  "url": "amqps://***@duck.lmq.cloudamqp.com/tcflaeri",
  "driver": "pika"
}
```

Failure responses mask any URLs inside the error payload.

## Models (Pydantic)
- `MechanismInput`: `{ "target_goal": "string (min 3)" }`
- `MechanismResponse`: `{ "newState": SystemState, "explanation": string, "explanation_details": {ResourceType:number} }`
- `SystemState`: `{ "components": [...], "resources": [...] }`
- `ResourceType` enum (EN): Communication, Educational, Financial, Informational, Operational, Organizational, Risk, Strategic, Technological

## Notes
- Health endpoints mask credentials between `//` and `@` before returning URLs.
- Logging format controlled via `LOG_FORMAT` (`console` | `json`).
- Rule coefficients configurable via `.env`; defaults are applied when variables are absent.
