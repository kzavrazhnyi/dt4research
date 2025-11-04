# dt4research — API Reference (v1.1.0)

Base URL: `http://127.0.0.1:8000`

Authentication: not required (dev)
Content-Type: `application/json`

## GET /
Serves the SPA dashboard (Cytoscape.js graph, language switch)

## GET /api/v1/system-state
Returns current system state from DB.

Response 200:
```json
{
  "components": [{ "id": "comp-strategy", "name": "Strategy", "status": "Active" }],
  "resources": [{ "id": "res-tech", "name": "Technology Solutions", "type": "Technological", "value": 62.0 }]
}
```

## POST /api/v1/apply-mechanism
Runs agent for provided goal, persists new state, writes history.

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

Errors: 422 on validation (min_length=3).

## GET /api/v1/agent-runs
Paginated history of agent runs.

Query: `limit` (int, default 20), `offset` (int, default 0)

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
    "applied_rules_explanation": {"Communication": 15}
  }]
}
```

## POST /api/v1/system-reset
Resets the simulation to its initial state. Internally clears `ResourceRow`, `ComponentRow`, and `AgentRunRow`, then re-seeds `INITIAL_STATE`.

- Request body: none
- Response 200:
```json
{
  "components": [{ "id": "comp-strategy", "name": "Strategy", "status": "Active" }],
  "resources": [{ "id": "res-tech", "name": "Technology Solutions", "type": "Technological", "value": 62.0 }]
}
```

## Models (Pydantic)
- `MechanismInput`: `{ "target_goal": "string (min 3)" }`
- `MechanismResponse`: `{ "newState": SystemState, "explanation": string, "explanation_details": {ResourceType:number} }`
- `SystemState`: `{ "components": [...], "resources": [...] }`
- `ResourceType` enum (EN): Communication, Educational, Financial, Informational, Operational, Organizational, Risk, Strategic, Technological



