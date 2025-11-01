# dt4research — API Reference (v1.0.0.4)

Base URL: `http://127.0.0.1:8000`

Authentication: not required (dev mode)

Content-Type: `application/json`

## GET /
- Description: Serve the SPA dashboard (Cytoscape.js graph, language switch)
- Response: HTML

## GET /api/v1/system-state
- Description: Return the current system state from DB
- Response 200
```json
{
  "components": [
    { "id": "comp-strategy", "name": "Strategy", "status": "Active" }
  ],
  "resources": [
    { "id": "res-tech", "name": "Technology Solutions", "type": "Technological", "value": 62.0 }
  ]
}
```

## POST /api/v1/apply-mechanism
- Description: Run the agent for a provided goal, persist new state, write history
- Request body
```json
{ "target_goal": "Improve customer service" }
```
- Response 200
```json
{
  "newState": { /* SystemState after applying rules */ },
  "explanation": "Communication +15; Informational +10; Operational +10",
  "explanation_details": {
    "Communication": 15,
    "Informational": 10,
    "Operational": 10
  }
}
```
- Errors
  - 422 Unprocessable Entity (validation error: "target_goal" min_length=3)

## GET /api/v1/agent-runs
- Description: Paginated history of agent runs
- Query params
  - `limit` (int, default 20)
  - `offset` (int, default 0)
- Response 200
```json
{
  "total": 3,
  "limit": 20,
  "offset": 0,
  "items": [
    {
      "id": 1,
      "timestamp": "2025-10-30T12:00:00Z",
      "input_goal": "Improve customer service",
      "applied_rules_explanation": {
        "Communication": 15,
        "Informational": 10,
        "Operational": 10
      }
    }
  ]
}
```

## Models (Pydantic)
- `MechanismInput`
```json
{ "target_goal": "string (min 3)" }
```
- `MechanismResponse`
```json
{
  "newState": { /* SystemState */ },
  "explanation": "string",
  "explanation_details": { "ResourceType": number }
}
```
- `SystemState`
```json
{
  "components": [{ "id": "string", "name": "string", "status": "string" }],
  "resources": [{ "id": "string", "name": "string", "type": "ResourceType", "value": 0.0 }]
}
```
- `ResourceType` enum (EN strings): Communication, Educational, Financial, Informational, Operational, Organizational, Risk, Strategic, Technological

## Notes
- Logging format controlled via `LOG_FORMAT` (`console` | `json`)
- Coefficients for rules configured via `.env` with safe defaults



