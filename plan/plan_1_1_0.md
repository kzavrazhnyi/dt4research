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