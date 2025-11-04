import pytest
from fastapi.testclient import TestClient

from app.main import app  # Імпорт вашого головного FastAPI додатку
from app.initial_state import INITIAL_STATE  # Імпорт початкового стану для порівняння
from app.agent_logic import (
    ECO_TECH, ECO_EDU, ECO_RISK,  # Імпорт коефіцієнтів (з .env або дефолтних)
    CUST_COMM, CUST_INFO, CUST_OPER,
)


# Створюємо фікстуру 'client', яка буде скидати стан БД перед кожним тестом
@pytest.fixture(scope="function")
def client():
    """
    Ізольований клієнт для тестування.
    Скидає стан БД до початкового (INITIAL_STATE) перед кожним тестом.
    Це вимагає, щоб ендпоінт POST /api/v1/system-reset (з плану v1.1.0) був реалізований.
    """
    with TestClient(app) as c:
        # 1. Скидаємо стан перед кожним тестом для чистої ізоляції
        response = c.post("/api/v1/system-reset")
        assert response.status_code == 200, "Не вдалося скинути стан БД перед тестом"

        # 2. Перевіряємо, що історія також очищена
        response_hist = c.get("/api/v1/agent-runs")
        assert response_hist.json()["total"] == 0, "Історія не була очищена"

        # 3. Передаємо клієнт у тест
        yield c


# --- Сценарії Тестування ---


def test_scenario_1_get_initial_state(client: TestClient):
    """
    СЦЕНАРІЙ 1: Менеджер відкриває дашборд.
    Перевірка, що GET /api/v1/system-state повертає коректний початковий стан.
    """
    print("\n--- СЦЕНАРІЙ 1: Отримання початкового стану ---")
    response = client.get("/api/v1/system-state")
    assert response.status_code == 200

    data = response.json()
    assert len(data["components"]) == len(INITIAL_STATE.components)
    assert len(data["resources"]) == len(INITIAL_STATE.resources)

    # Порівнюємо значення першого ресурсу з початковим станом
    initial_comm_val = next(r.value for r in INITIAL_STATE.resources if r.type == "Communication")
    current_comm_val = next(r["value"] for r in data["resources"] if r["type"] == "Communication")
    assert current_comm_val == initial_comm_val
    print("✅ Стан відповідає початковому.")


def test_scenario_2_apply_mechanism_invalid_goal(client: TestClient):
    """
    СЦЕНАРІЙ 2: Менеджер надсилає невалідну (занадто коротку) ціль.
    Перевірка валідації Pydantic (min_length=3).
    """
    print("\n--- СЦЕНАРІЙ 2: Невдалий запуск (Валідація) ---")
    response = client.post("/api/v1/apply-mechanism", json={"target_goal": "hi"})

    # Очікуємо 422 Unprocessable Entity
    assert response.status_code == 422
    err = response.json()
    assert isinstance(err, dict) and "detail" in err and isinstance(err["detail"], list)
    assert err["detail"][0]["type"] == "string_too_short"
    assert err["detail"][0]["ctx"]["min_length"] == 3
    print("✅ Система коректно відхилила запит (422).")


def test_scenario_3_cybernetic_loop_happy_path_and_history(client: TestClient):
    """
    СЦЕНАРІЙ 3: Повний кібернетичний цикл (Успішний шлях).
    1. Менеджер ставить ціль "покращити екологію".
    2. Агент застосовує правило 'Ecology'.
    3. Стан в БД оновлюється.
    4. Запис про запуск зберігається в "пам'яті" (історії).
    """
    print("\n--- СЦЕНАРІЙ 3: Успішний кібернетичний цикл ---")

    # --- Крок 1: Отримуємо початковий стан ресурсів ---
    response_before = client.get("/api/v1/system-state")
    state_before = response_before.json()
    tech_before = next(r["value"] for r in state_before["resources"] if r["type"] == "Technological")

    # --- Крок 2: Менеджер ставить ціль ---
    goal = "впровадити екологічні інновації"
    response_apply = client.post("/api/v1/apply-mechanism", json={"target_goal": goal})

    # Перевіряємо відповідь API (v1.0.0.4+)
    assert response_apply.status_code == 200
    data_apply = response_apply.json()

    assert "newState" in data_apply
    assert "explanation" in data_apply
    assert "explanation_details" in data_apply

    # Перевіряємо, що агент застосував правильні дельти (ECO_TECH з .env, 20 за дефолтом)
    assert "Technological" in data_apply["explanation_details"]
    assert data_apply["explanation_details"]["Technological"] == ECO_TECH
    print(f"✅ Агент повернув коректні дельти: {data_apply['explanation']}")

    # --- Крок 3: Перевіряємо, чи стан *реально* зберігся в БД ---
    response_after = client.get("/api/v1/system-state")
    state_after = response_after.json()
    tech_after = next(r["value"] for r in state_after["resources"] if r["type"] == "Technological")

    expected_value = min(100, tech_before + ECO_TECH)  # Логіка "запобіжника" 0-100
    assert tech_after == expected_value
    print(f"✅ Стан в БД оновлено: 'Technological' {tech_before} -> {tech_after}")

    # --- Крок 4: Перевіряємо "пам'ять" (історію запусків) ---
    response_hist = client.get("/api/v1/agent-runs")
    data_hist = response_hist.json()

    assert data_hist["total"] == 1
    assert data_hist["items"][0]["input_goal"] == goal
    assert data_hist["items"][0]["applied_rules_explanation"]["Technological"] == ECO_TECH
    print("✅ Запуск агента успішно збережено в історії.")


def test_scenario_4_state_clamping_at_100(client: TestClient):
    """
    СЦЕНАРІЙ 4: Перевірка "запобіжника" (0-100).
    Ресурс не може перевищити 100, навіть якщо агент цього хоче.
    """
    print("\n--- СЦЕНАРІЙ 4: Тестування обмеження 'max 100' ---")
    goal = "покращити сервіс"  # Запускає CUST_COMM (15)

    # "Накачуємо" ресурс Communication до ~90
    for _ in range(2):  # (Початкове значення 65 -> 80 -> 95)
        client.post("/api/v1/apply-mechanism", json={"target_goal": goal})

    # Перевіряємо, що він < 100
    state_before = client.get("/api/v1/system-state").json()
    comm_before = next(r["value"] for r in state_before["resources"] if r["type"] == "Communication")
    assert comm_before == 65 + CUST_COMM + CUST_COMM  # 65 + 15 + 15 = 95
    print(f"✅ Ресурс 'Communication' доведений до {comm_before}")

    # Останній запуск (95 + 15 = 110, але має бути 100)
    client.post("/api/v1/apply-mechanism", json={"target_goal": goal})

    # Перевіряємо, що значення "застрягло" на 100
    state_after = client.get("/api/v1/system-state").json()
    comm_after = next(r["value"] for r in state_after["resources"] if r["type"] == "Communication")

    assert comm_after == 100
    print(f"✅ Ресурс 'Communication' коректно обмежений на 100 (було {comm_before}).")


def test_scenario_5_system_reset_after_changes(client: TestClient):
    """
    СЦЕНАРІЙ 5: Скидання сценарію (Функція v1.1.0).
    Менеджер працює з системою, а потім натискає "Скинути стан".
    """
    print("\n--- СЦЕНАРІЙ 5: Перевірка скидання системи ---")

    # --- Крок 1: Змінюємо стан ---
    client.post("/api/v1/apply-mechanism", json={"target_goal": "інновації"})
    response_mid = client.get("/api/v1/system-state")
    state_mid = response_mid.json()

    # Переконуємось, що стан відрізняється від початкового
    initial_tech_val = next(r.value for r in INITIAL_STATE.resources if r.type == "Technological")
    current_tech_val = next(r["value"] for r in state_mid["resources"] if r["type"] == "Technological")
    assert current_tech_val != initial_tech_val
    print("✅ Стан успішно змінено.")

    # Переконуємось, що історія НЕ порожня
    response_hist_mid = client.get("/api/v1/agent-runs")
    assert response_hist_mid.json()["total"] > 0
    print("✅ Історія містить записи.")

    # --- Крок 2: Викликаємо скидання (тестуємо сам ендпоінт) ---
    response_reset = client.post("/api/v1/system-reset")
    assert response_reset.status_code == 200
    state_reset_data = response_reset.json()

    # Перевіряємо, що ендпоінт повернув початковий стан
    reset_tech_val = next(r["value"] for r in state_reset_data["resources"] if r["type"] == "Technological")
    assert reset_tech_val == initial_tech_val
    print("✅ Ендпоінт скидання повернув початковий стан.")

    # --- Крок 3: Перевіряємо, що стан в БД *дійсно* скинуто ---
    response_after = client.get("/api/v1/system-state")
    state_after = response_after.json()
    after_tech_val = next(r["value"] for r in state_after["resources"] if r["type"] == "Technological")
    assert after_tech_val == initial_tech_val
    print("✅ Стан в БД успішно скинуто до початкового.")

    # --- Крок 4: Перевіряємо, що історія очищена ---
    response_hist_after = client.get("/api/v1/agent-runs")
    assert response_hist_after.json()["total"] == 0
    print("✅ Історію запусків успішно очищено.")



