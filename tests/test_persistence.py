"""
Persistence and history tests for dt4research (Тести персистентності та історії запусків).
"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def _resource_value(state: dict, resource_id: str) -> float:
    for r in state["resources"]:
        if r["id"] == resource_id:
            return float(r["value"])
    raise AssertionError(f"Resource {resource_id} not found in state")


def test_persistence_and_history_endpoint():
    # Read initial state
    resp = client.get("/api/v1/system-state")
    assert resp.status_code == 200
    state_before = resp.json()

    before_comm = _resource_value(state_before, "res-comm")

    # Apply a goal that triggers Communication/Informational/Operational
    payload = {"target_goal": "Покращити сервіс для клієнтів"}
    resp_apply = client.post("/api/v1/apply-mechanism", json=payload)
    assert resp_apply.status_code == 200
    apply_data = resp_apply.json()
    assert "newState" in apply_data
    assert "explanation_details" in apply_data

    # Check persisted state reflects the change
    resp_after = client.get("/api/v1/system-state")
    assert resp_after.status_code == 200
    state_after = resp_after.json()
    after_comm = _resource_value(state_after, "res-comm")
    assert after_comm >= before_comm

    # History endpoint should contain at least one item
    resp_history = client.get("/api/v1/agent-runs?limit=5&offset=0")
    assert resp_history.status_code == 200
    hist = resp_history.json()
    assert isinstance(hist.get("items"), list)
    assert hist.get("total", 0) >= 1
    if hist["items"]:
        first = hist["items"][0]
        assert "input_goal" in first
        assert "applied_rules_explanation" in first
        # Expect English keys for explanation (ResourceType values)
        # Presence check is sufficient
        assert isinstance(first["applied_rules_explanation"], dict)





