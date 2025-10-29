"""
API tests for dt4research (Тести API для dt4research).
"""

import sys
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_system_state_schema():
    """GET /api/v1/system-state returns expected schema (повертає очікувану схему)."""
    resp = client.get("/api/v1/system-state")
    assert resp.status_code == 200
    data = resp.json()
    assert "components" in data
    assert "resources" in data
    assert isinstance(data["components"], list)
    assert isinstance(data["resources"], list)


def test_apply_mechanism_updates_values_within_bounds():
    """POST /api/v1/apply-mechanism updates resource values within 0..100 (оновлює значення в межах 0..100)."""
    payload = {"target_goal": "Покращити обслуговування клієнтів"}
    resp = client.post("/api/v1/apply-mechanism", json=payload)
    assert resp.status_code == 200
    data = resp.json()

    # Response contains newState and explanation (Містить newState та explanation)
    assert "newState" in data
    assert "explanation" in data

    state = data["newState"]
    assert "resources" in state
    for r in state["resources"]:
        assert 0 <= float(r["value"]) <= 100


def test_running_inside_venv():
    """Ensure tests run inside virtual environment (Переконатися, що тести запускаються у віртуальному середовищі)."""
    # Heuristic: path should include 'venv' directory on Windows (Евристика: шлях містить 'venv')
    exe_path = sys.executable.lower()
    assert "venv" in exe_path



