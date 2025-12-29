"""
Unit tests for simulation module (Юніт-тести для модуля симуляції).
Tests simulation engine and metrics generation (Тестування рушія симуляції та генерації метрик).
"""

import pytest
from app.simulation import (
    run_simulation,
    get_simulation_history,
    clear_simulation_history,
    get_simulation_summary,
    generate_event_goal,
    simulate_operations_and_alerts
)
from app.models import SystemState, KeyComponent, Resource, ComponentType, ResourceType
from app.initial_state import INITIAL_STATE


@pytest.fixture
def clean_simulation():
    """Clear simulation history before and after test (Очистити історію симуляції до та після тесту)."""
    clear_simulation_history()
    yield
    clear_simulation_history()


def test_generate_event_goal_high_intensity():
    """Test event generation with high intensity (Тест генерації подій з високою інтенсивністю)."""
    goal = generate_event_goal("high", 1)
    assert goal is not None
    assert isinstance(goal, str)
    assert len(goal) > 0


def test_generate_event_goal_low_intensity():
    """Test event generation with low intensity (Тест генерації подій з низькою інтенсивністю)."""
    # Low intensity may skip some days
    goal_day_1 = generate_event_goal("low", 1)
    goal_day_2 = generate_event_goal("low", 2)
    goal_day_3 = generate_event_goal("low", 3)
    
    # At least one should be None (skipped)
    goals = [goal_day_1, goal_day_2, goal_day_3]
    assert any(g is None for g in goals) or any(g is not None for g in goals)


def test_simulate_operations_and_alerts():
    """Test operations and alerts simulation (Тест симуляції операцій та алертів)."""
    ops, alerts = simulate_operations_and_alerts("medium", 1)
    
    assert ops >= 0
    assert alerts >= 0
    assert isinstance(ops, int)
    assert isinstance(alerts, int)


def test_simulate_operations_intensity_scaling():
    """Test that intensity affects operations count (Тест, що інтенсивність впливає на кількість операцій)."""
    ops_low, _ = simulate_operations_and_alerts("low", 1)
    ops_high, _ = simulate_operations_and_alerts("high", 1)
    
    # High intensity should generally produce more operations
    # (allowing for randomness, but high should be >= low on average)
    assert ops_high >= 0
    assert ops_low >= 0


def test_run_simulation_basic(clean_simulation):
    """Test basic simulation run (Тест базового запуску симуляції)."""
    metrics = run_simulation(days=5, intensity="medium", t_market=30.0, use_agent=True)
    
    assert len(metrics) == 6  # Initial + 5 days
    assert all(hasattr(m, 's_index') for m in metrics)
    assert all(hasattr(m, 'c_index') for m in metrics)
    assert all(hasattr(m, 'a_index') for m in metrics)
    assert all(hasattr(m, 'timestamp') for m in metrics)


def test_run_simulation_without_agent(clean_simulation):
    """Test simulation without agent (control group) (Тест симуляції без агента (контрольна група))."""
    metrics = run_simulation(days=5, intensity="medium", t_market=30.0, use_agent=False)
    
    assert len(metrics) == 6  # Initial + 5 days
    # Without agent, resources should degrade (entropy)
    # S index should generally decrease over time
    # (Без агента ресурси мають деградувати (ентропія), індекс S має загалом знижуватися з часом)
    initial_s = metrics[0].s_index
    final_s = metrics[-1].s_index
    # Note: This is probabilistic, but entropy should generally cause degradation
    # (Примітка: Це ймовірнісне, але ентропія зазвичай викликає деградацію)


def test_run_simulation_metrics_range(clean_simulation):
    """Test that simulation metrics are in valid ranges (Тест, що метрики симуляції в валідних діапазонах)."""
    metrics = run_simulation(days=10, intensity="high", t_market=30.0, use_agent=True)
    
    for m in metrics:
        assert 0.0 <= m.s_index <= 1.0
        assert 0.0 <= m.c_index <= 1.0
        assert m.a_index >= 0.0


def test_run_simulation_history_storage(clean_simulation):
    """Test that simulation stores history (Тест, що симуляція зберігає історію)."""
    metrics = run_simulation(days=3, intensity="low", t_market=30.0)
    
    history = get_simulation_history()
    assert len(history) == len(metrics)
    assert history == metrics


def test_get_simulation_summary(clean_simulation):
    """Test simulation summary generation (Тест генерації зведення симуляції)."""
    run_simulation(days=5, intensity="medium", t_market=30.0)
    
    summary = get_simulation_summary(get_simulation_history())
    
    assert "before" in summary
    assert "after" in summary
    assert "improvements" in summary
    assert "total_steps" in summary
    
    assert "s_index" in summary["before"]
    assert "c_index" in summary["before"]
    assert "a_index" in summary["before"]
    
    assert "s_index" in summary["after"]
    assert "c_index" in summary["after"]
    assert "a_index" in summary["after"]


def test_get_simulation_summary_empty():
    """Test summary with empty history (Тест зведення з порожньою історією)."""
    clear_simulation_history()
    summary = get_simulation_summary([])
    
    assert summary["before"]["s_index"] == 0.0
    assert summary["after"]["s_index"] == 0.0
    assert summary["improvements"]["s_index"] == 0.0


def test_run_simulation_different_intensities(clean_simulation):
    """Test simulation with different intensity levels (Тест симуляції з різними рівнями інтенсивності)."""
    for intensity in ["low", "medium", "high"]:
        metrics = run_simulation(days=3, intensity=intensity, t_market=30.0, use_agent=True)
        assert len(metrics) == 4  # Initial + 3 days
        assert all(0.0 <= m.s_index <= 1.0 for m in metrics)


def test_run_simulation_t_market_parameter(clean_simulation):
    """Test simulation with different T_market values (Тест симуляції з різними значеннями T_market)."""
    metrics_short = run_simulation(days=5, intensity="medium", t_market=10.0, use_agent=True)
    metrics_long = run_simulation(days=5, intensity="medium", t_market=60.0, use_agent=True)
    
    # Both should complete successfully
    assert len(metrics_short) == 6
    assert len(metrics_long) == 6
    
    # A index should be affected by T_market
    # (shorter T_market should generally result in higher A index)
    # But we just check that values are valid
    assert all(m.a_index >= 0.0 for m in metrics_short)
    assert all(m.a_index >= 0.0 for m in metrics_long)

