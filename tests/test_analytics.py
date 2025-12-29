"""
Unit tests for analytics module (Юніт-тести для модуля аналітики).
Tests calculation of S, C, A indices (Тестування обчислення індексів S, C, A).
"""

import pytest
from app.analytics import (
    calculate_s_index,
    calculate_c_index,
    calculate_a_index,
    extract_tech_resource,
    extract_soc_resource,
    extract_waste_from_processes,
    calculate_metrics_from_state
)
from app.models import SystemState, KeyComponent, Resource, ComponentType, ResourceType


def test_calculate_s_index_basic():
    """Test basic S index calculation (Тест базового обчислення індексу S)."""
    # S = (R_eco + R_soc) / 2 * (1 - W)
    # With tech=0.8, soc=0.6, waste=0.2
    # S = (0.8 + 0.6) / 2 * (1 - 0.2) = 0.7 * 0.8 = 0.56
    result = calculate_s_index(0.8, 0.6, 0.2)
    assert abs(result - 0.56) < 0.001


def test_calculate_s_index_zero_waste():
    """Test S index with zero waste (Тест індексу S з нульовими відходами)."""
    # S = (0.5 + 0.5) / 2 * (1 - 0) = 0.5 * 1 = 0.5
    result = calculate_s_index(0.5, 0.5, 0.0)
    assert abs(result - 0.5) < 0.001


def test_calculate_s_index_max_waste():
    """Test S index with maximum waste (Тест індексу S з максимальними відходами)."""
    # S = (0.5 + 0.5) / 2 * (1 - 1) = 0.5 * 0 = 0.0
    result = calculate_s_index(0.5, 0.5, 1.0)
    assert abs(result - 0.0) < 0.001


def test_calculate_s_index_clamping():
    """Test S index clamping to [0, 1] range (Тест обмеження індексу S до діапазону [0, 1])."""
    # Test negative waste (should clamp to 0)
    result = calculate_s_index(0.5, 0.5, -0.5)
    assert result >= 0.0
    
    # Test waste > 1 (should clamp to 1)
    result = calculate_s_index(0.5, 0.5, 2.0)
    assert result <= 1.0
    assert result >= 0.0


def test_calculate_c_index_basic():
    """Test basic C index calculation (Тест базового обчислення індексу C)."""
    # C = 1 - (N_alerts / N_ops)
    # With ops=100, alerts=10
    # C = 1 - (10 / 100) = 0.9
    result = calculate_c_index(100, 10)
    assert abs(result - 0.9) < 0.001


def test_calculate_c_index_zero_alerts():
    """Test C index with zero alerts (Тест індексу C з нульовими алертами)."""
    # C = 1 - (0 / 100) = 1.0
    result = calculate_c_index(100, 0)
    assert abs(result - 1.0) < 0.001


def test_calculate_c_index_zero_ops():
    """Test C index with zero operations (Тест індексу C з нульовими операціями)."""
    # Should return 1.0 (perfect control when no operations)
    result = calculate_c_index(0, 0)
    assert result == 1.0


def test_calculate_c_index_all_alerts():
    """Test C index when all operations are alerts (Тест індексу C, коли всі операції - алерти)."""
    # C = 1 - (100 / 100) = 0.0
    result = calculate_c_index(100, 100)
    assert abs(result - 0.0) < 0.001


def test_calculate_c_index_more_alerts_than_ops():
    """Test C index when alerts exceed operations (Тест індексу C, коли алертів більше ніж операцій)."""
    # Should clamp to 0.0
    result = calculate_c_index(50, 100)
    assert result == 0.0


def test_calculate_a_index_basic():
    """Test basic A index calculation (Тест базового обчислення індексу A)."""
    # A = T_adapt / T_market
    # With t_adapt=10, t_market=30
    # A = 10 / 30 = 0.333...
    result = calculate_a_index(10.0, 30.0)
    assert abs(result - 0.333) < 0.01


def test_calculate_a_index_fast_adaptation():
    """Test A index with fast adaptation (Тест індексу A з швидкою адаптацією)."""
    # A = 1 / 30 = 0.033...
    result = calculate_a_index(1.0, 30.0)
    assert result < 0.1


def test_calculate_a_index_slow_adaptation():
    """Test A index with slow adaptation (Тест індексу A з повільною адаптацією)."""
    # A = 60 / 30 = 2.0
    result = calculate_a_index(60.0, 30.0)
    assert abs(result - 2.0) < 0.001


def test_calculate_a_index_zero_adaptation():
    """Test A index with zero adaptation time (Тест індексу A з нульовим часом адаптації)."""
    # Should return 0.0 (instant adaptation)
    result = calculate_a_index(0.0, 30.0)
    assert result == 0.0


def test_calculate_a_index_invalid_market_time():
    """Test A index with invalid market time (Тест індексу A з невалідним часом ринку)."""
    # Should return 1.0 (high adaptability when market time is invalid)
    result = calculate_a_index(10.0, 0.0)
    assert result == 1.0


def test_extract_tech_resource():
    """Test extraction of technological resource (Тест витягування технологічного ресурсу)."""
    state = SystemState(
        components=[],
        resources=[
            Resource(id="tech1", name="Tech 1", type=ResourceType.TECHNOLOGICAL, value=80.0),
            Resource(id="tech2", name="Tech 2", type=ResourceType.TECHNOLOGICAL, value=60.0),
        ]
    )
    result = extract_tech_resource(state)
    # Average: (80 + 60) / 2 / 100 = 0.7
    assert abs(result - 0.7) < 0.001


def test_extract_tech_resource_missing():
    """Test extraction when no technological resource exists (Тест витягування, коли немає технологічного ресурсу)."""
    state = SystemState(
        components=[],
        resources=[
            Resource(id="other", name="Other", type=ResourceType.FINANCIAL, value=50.0),
        ]
    )
    result = extract_tech_resource(state)
    assert result == 0.0


def test_extract_soc_resource():
    """Test extraction of social/cultural resource (Тест витягування соціального/культурного ресурсу)."""
    state = SystemState(
        components=[
            KeyComponent(id="culture", name=ComponentType.CULTURE, status="Healthy"),
        ],
        resources=[
            Resource(id="edu", name="Education", type=ResourceType.EDUCATIONAL, value=70.0),
        ]
    )
    result = extract_soc_resource(state)
    # Should combine educational (70) and culture (80 for "Healthy") = (70 + 80) / 2 / 100 = 0.75
    assert abs(result - 0.75) < 0.01


def test_extract_waste_from_processes():
    """Test extraction of waste from operational resources (Тест витягування відходів з операційних ресурсів)."""
    state = SystemState(
        components=[],
        resources=[
            Resource(id="oper1", name="Operational 1", type=ResourceType.OPERATIONAL, value=80.0),
        ]
    )
    result = extract_waste_from_processes(state)
    # Operational value = 80, efficiency = 0.8, waste = 1 - 0.8 = 0.2
    assert abs(result - 0.2) < 0.01


def test_extract_waste_from_processes_multiple():
    """Test waste calculation with multiple operational resources (Тест обчислення відходів з кількома операційними ресурсами)."""
    state = SystemState(
        components=[],
        resources=[
            Resource(id="oper1", name="Operational 1", type=ResourceType.OPERATIONAL, value=60.0),
            Resource(id="oper2", name="Operational 2", type=ResourceType.OPERATIONAL, value=80.0),
        ]
    )
    result = extract_waste_from_processes(state)
    # Average operational = (60 + 80) / 2 = 70, efficiency = 0.7, waste = 0.3
    assert abs(result - 0.3) < 0.01


def test_extract_waste_from_processes_no_operational():
    """Test waste calculation when no operational resources exist (Тест обчислення відходів, коли немає операційних ресурсів)."""
    state = SystemState(
        components=[],
        resources=[
            Resource(id="tech", name="Tech", type=ResourceType.TECHNOLOGICAL, value=50.0),
        ]
    )
    result = extract_waste_from_processes(state)
    # Should return default 0.5
    assert result == 0.5


def test_calculate_metrics_from_state():
    """Test complete metrics calculation from state (Тест повного обчислення метрик зі стану)."""
    state = SystemState(
        components=[
            KeyComponent(id="processes", name=ComponentType.PROCESSES, status="Good"),
            KeyComponent(id="culture", name=ComponentType.CULTURE, status="Healthy"),
        ],
        resources=[
            Resource(id="tech", name="Tech", type=ResourceType.TECHNOLOGICAL, value=80.0),
            Resource(id="edu", name="Education", type=ResourceType.EDUCATIONAL, value=60.0),
        ]
    )
    
    s, c, a = calculate_metrics_from_state(
        state,
        total_ops=100,
        alerts_count=5,
        t_adapt=10.0,
        t_market=30.0
    )
    
    # All indices should be valid
    assert 0.0 <= s <= 1.0
    assert 0.0 <= c <= 1.0
    assert a >= 0.0


def test_calculate_metrics_from_state_edge_cases():
    """Test metrics calculation with edge cases (Тест обчислення метрик з граничними випадками)."""
    state = SystemState(
        components=[],
        resources=[]
    )
    
    # Test with zero operations
    s, c, a = calculate_metrics_from_state(
        state,
        total_ops=0,
        alerts_count=0,
        t_adapt=1.0,
        t_market=30.0
    )
    
    # C should be 1.0 (perfect control with no operations)
    assert c == 1.0
    assert s >= 0.0
    assert a >= 0.0

