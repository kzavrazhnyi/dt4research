"""
Simulation module for generating time series data of scientific metrics (Модуль симуляції для генерації часових рядів наукових метрик).
Implements automated scenario generation and agent response simulation (Реалізує автоматичну генерацію сценаріїв та симуляцію реакції агента).
"""

import random
import copy
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Callable

from app.models import SystemState, SimulationMetrics, SimulationRunRequest
from app.agent_logic import run_mock_analysis
from app.analytics import calculate_metrics_from_state
from app.initial_state import INITIAL_STATE
from app.repository import read_system_state, write_system_state, save_simulation_metric


# In-memory storage for simulation metrics history (In-memory сховище для історії метрик симуляції)
_simulation_history: List[SimulationMetrics] = []
_agent_logs_history: List[str] = []


def clear_simulation_history() -> None:
    """Clear simulation metrics history (Очистити історію метрик симуляції)."""
    global _simulation_history, _agent_logs_history
    _simulation_history = []
    _agent_logs_history = []


def get_simulation_history() -> List[SimulationMetrics]:
    """Get current simulation metrics history (Отримати поточну історію метрик симуляції)."""
    return _simulation_history.copy()


def get_agent_logs_history() -> List[str]:
    """Get agent logs from last simulation (Отримати логи агента з останньої симуляції)."""
    return _agent_logs_history.copy()


def generate_event_goal(intensity: str, day: int) -> str:
    """
    Generate a simulated event/goal based on intensity and day (Згенерувати симульовану подію/ціль на основі інтенсивності та дня).
    
    Args:
        intensity: Event intensity level ("low", "medium", "high") (Рівень інтенсивності подій)
        day: Current simulation day (Поточний день симуляції)
    
    Returns:
        Goal string for agent processing (Рядок цілі для обробки агентом)
    """
    # Event categories based on intensity (Категорії подій на основі інтенсивності)
    if intensity == "low":
        events = [
            "Покращити ефективність процесів",
            "Оптимізувати використання ресурсів",
            "Підвищити якість сервісу",
        ]
        # Lower frequency (Нижча частота)
        if day % 3 != 0:
            return None  # No event this day (Немає події цього дня)
    elif intensity == "medium":
        events = [
            "Інновації в технологіях",
            "Партнерство з клієнтами",
            "Управління ризиками",
            "Освіта та навчання персоналу",
            "Екологічна ефективність",
        ]
        # Medium frequency (Середня частота)
        if day % 2 != 0:
            return None
    else:  # high
        events = [
            "Цифрова трансформація",
            "Екологічна переробка",
            "Клієнтський сервіс",
            "Інновації та автоматизація",
            "Партнерство та екосистема",
            "Ризики та безпека",
            "Освіта та тренінги",
        ]
        # High frequency - event every day (Висока частота - подія кожного дня)
    
    return random.choice(events)


def simulate_operations_and_alerts(
    intensity: str,
    day: int,
    base_ops: int = 100,
    base_alerts: int = 5
) -> Tuple[int, int]:
    """
    Simulate operations and alerts count for a day (Симулювати кількість операцій та алертів за день).
    
    Args:
        intensity: Event intensity level (Рівень інтенсивності подій)
        day: Current simulation day (Поточний день симуляції)
        base_ops: Base number of operations per day (Базова кількість операцій на день)
        base_alerts: Base number of alerts per day (Базова кількість алертів на день)
    
    Returns:
        Tuple of (operations_count, alerts_count) (Кортеж (кількість_операцій, кількість_алертів))
    """
    # Intensity multipliers (Множники інтенсивності)
    intensity_multipliers = {
        "low": (0.5, 0.3),
        "medium": (1.0, 0.7),
        "high": (2.0, 1.5),
    }
    
    ops_mult, alerts_mult = intensity_multipliers.get(intensity, (1.0, 1.0))
    
    # Add some randomness (Додати випадковість)
    ops_variation = random.uniform(0.8, 1.2)
    alerts_variation = random.uniform(0.5, 1.5)
    
    # Calculate operations (Обчислити операції)
    ops = int(base_ops * ops_mult * ops_variation)
    
    # Calculate alerts (Обчислити алерти)
    # Alerts tend to decrease as system improves (Алерти мають тенденцію зменшуватися при покращенні системи)
    # But can spike on certain days (Але можуть різко зрости в певні дні)
    alerts = int(base_alerts * alerts_mult * alerts_variation)
    
    # Occasional spike (Випадковий сплеск)
    if random.random() < 0.1:  # 10% chance (10% ймовірність)
        alerts = int(alerts * random.uniform(2.0, 4.0))
    
    return max(0, ops), max(0, alerts)


def apply_entropy_degradation(state: SystemState, intensity: str, log_callback: Optional[Callable[[str], None]] = None) -> SystemState:
    """
    Apply entropy degradation to resources when agent is not active (Застосувати деградацію ентропії до ресурсів, коли агент неактивний).
    
    Without agent intervention, resources naturally degrade due to entropy (Без втручання агента ресурси природно деградують через ентропію).
    
    Args:
        state: Current system state (Поточний стан системи)
        intensity: Event intensity level (affects degradation rate) (Рівень інтенсивності подій (впливає на швидкість деградації))
        log_callback: Optional callback to log degradation details (Опціональний callback для логування деталей деградації)
    
    Returns:
        New state with degraded resources (Новий стан з деградованими ресурсами)
    """
    new_state = copy.deepcopy(state)
    
    # Degradation rate based on intensity (Швидкість деградації на основі інтенсивності)
    degradation_rates = {
        "low": 0.5,    # 0.5% per day (0.5% на день)
        "medium": 1.0,  # 1.0% per day (1.0% на день)
        "high": 2.0,    # 2.0% per day (2.0% на день)
    }
    
    degradation = degradation_rates.get(intensity, 1.0)
    
    degraded_resources = []
    
    # Apply degradation to all resources (Застосувати деградацію до всіх ресурсів)
    for resource in new_state.resources:
        old_value = resource.value
        # Degrade resource value (Деградувати значення ресурсу)
        resource.value = max(0.0, resource.value - degradation)
        if old_value != resource.value:
            degraded_resources.append((resource.type.value, old_value, resource.value))
    
    # Log degradation details if callback provided (Залогувати деталі деградації, якщо надано callback)
    if log_callback:
        if degraded_resources:
            log_callback(f"⚠️ Entropy degradation applied: -{degradation}% to all resources")
            log_callback(f"📉 Resources degraded ({len(degraded_resources)} total):")
            # Show all resources with changes (Показати всі ресурси зі змінами)
            for res_type, old_val, new_val in degraded_resources:
                change = new_val - old_val
                percentage = (new_val / old_val * 100) if old_val > 0 else 0
                log_callback(f"   • {res_type}: {old_val:.1f} → {new_val:.1f} ({change:+.1f}, {percentage:.1f}% of original)")
            
            # Show most affected resources (Показати найбільш постраждалі ресурси)
            if len(degraded_resources) > 3:
                sorted_by_impact = sorted(degraded_resources, key=lambda x: x[1] - x[2], reverse=True)
                log_callback(f"🔴 Most affected resources:")
                for res_type, old_val, new_val in sorted_by_impact[:3]:
                    impact = old_val - new_val
                    log_callback(f"   • {res_type}: lost {impact:.1f} points (from {old_val:.1f} to {new_val:.1f})")
        else:
            log_callback(f"⚠️ Entropy degradation: -{degradation}% (all resources already at minimum 0.0)")
            log_callback(f"   System has reached minimum resource levels - no further degradation possible")
    
    return new_state


def run_simulation(
    days: int = 30,
    intensity: str = "high",
    t_market: float = 30.0,
    initial_state: Optional[SystemState] = None,
    use_agent: bool = True,
    log_callback: Optional[Callable[[str], None]] = None
) -> List[SimulationMetrics]:
    """
    Run automated simulation and generate time series of metrics (Запустити автоматичну симуляцію та згенерувати часовий ряд метрик).
    
    Args:
        days: Number of simulation days (Кількість днів симуляції)
        intensity: Event intensity level ("low", "medium", "high") (Рівень інтенсивності подій)
        t_market: Market change time in days (Час змін на ринку в днях)
        initial_state: Starting system state, if None uses current DB state (Початковий стан системи, якщо None - використовує поточний стан БД)
        use_agent: If True, agent responds to events; if False, entropy degrades resources (Якщо True, агент реагує на події; якщо False, ентропія деградує ресурси)
        log_callback: Optional callback function to send logs in real-time (Опціональна функція зворотного виклику для відправки логів в реальному часі)
    
    Returns:
        List of SimulationMetrics for each simulation step (Список SimulationMetrics для кожного кроку симуляції)
    """
    global _simulation_history
    
    # Clear previous history (Очистити попередню історію)
    clear_simulation_history()
    global _agent_logs_history
    _agent_logs_history = []
    
    # Initialize starting state (Ініціалізувати початковий стан)
    if initial_state is None:
        current_state = read_system_state()
    else:
        current_state = copy.deepcopy(initial_state)
    
    # Reset to initial state for clean simulation (Скинути до початкового стану для чистої симуляції)
    simulation_state = copy.deepcopy(INITIAL_STATE)
    write_system_state(simulation_state)
    
    # Generate unique simulation run ID (Згенерувати унікальний ID запуску симуляції)
    simulation_run_id = str(uuid.uuid4())
    
    # Track cumulative statistics (Відстежувати накопичувальну статистику)
    total_ops = 0
    total_alerts = 0
    adaptation_start_day: Optional[int] = None
    agent_actions_count = 0
    
    metrics_history: List[SimulationMetrics] = []
    
    # Send initial message if callback provided (Відправити початкове повідомлення, якщо надано callback)
    if log_callback:
        log_callback(f"Starting simulation: {days} days, intensity: {intensity}, use_agent: {use_agent}")
        log_callback(f"Market change time (T_market): {t_market} days")
        log_callback("=" * 60)
    
    # Record initial metrics (Записати початкові метрики)
    initial_metrics = calculate_metrics_from_state(
        simulation_state,
        total_ops=0,
        alerts_count=0,
        t_adapt=1.0,
        t_market=t_market
    )
    initial_metric = SimulationMetrics(
        s_index=initial_metrics[0],
        c_index=initial_metrics[1],
        a_index=initial_metrics[2],
        timestamp=datetime.utcnow()
    )
    metrics_history.append(initial_metric)
    # Save to database (Зберегти в базу даних)
    save_simulation_metric(initial_metric, simulation_run_id, use_agent, day=0)
    
    # Run simulation for each day (Запустити симуляцію для кожного дня)
    for day in range(1, days + 1):
        # Send day info if callback provided (Відправити інформацію про день, якщо надано callback)
        if log_callback:
            log_callback(f"\n{'='*60}")
            log_callback(f"Day {day}/{days}")
            log_callback(f"{'='*60}")
        
        # Generate event/goal for this day (Згенерувати подію/ціль для цього дня)
        event_goal = generate_event_goal(intensity, day)
        
        # Simulate operations and alerts (Симулювати операції та алерти)
        daily_ops, daily_alerts = simulate_operations_and_alerts(intensity, day)
        total_ops += daily_ops
        total_alerts += daily_alerts
        
        if log_callback:
            log_callback(f"📊 Operations: {daily_ops}, Alerts: {daily_alerts}")
        
        # Apply agent response or entropy degradation (Застосувати реакцію агента або деградацію ентропії)
        if use_agent:
            # With agent: respond to events (З агентом: реагувати на події)
            if event_goal:
                # Mark adaptation start if not already started (Позначити початок адаптації, якщо ще не почалася)
                if adaptation_start_day is None:
                    adaptation_start_day = day
                
                # Run agent analysis (Запустити аналіз агента)
                new_state, deltas, agent_logs = run_mock_analysis(event_goal, simulation_state, capture_logs=True)
                simulation_state = new_state
                write_system_state(simulation_state)
                agent_actions_count += 1
                # Store agent logs (Зберегти логи агента)
                if agent_logs:
                    _agent_logs_history.extend(agent_logs)
                    # Send logs in real-time if callback provided (Відправити логи в реальному часі, якщо надано callback)
                    if log_callback:
                        for log_line in agent_logs:
                            log_callback(log_line)
            else:
                if log_callback:
                    log_callback("ℹ️ No event this day")
        else:
            # Without agent: entropy degrades resources (Без агента: ентропія деградують ресурси)
            if log_callback:
                log_callback("⚠️ Control Group: No agent intervention - entropy degradation active")
                # Show summary of current resource levels before degradation (Показати зведення поточних рівнів ресурсів до деградації)
                total_resources = len(simulation_state.resources)
                avg_value = sum(r.value for r in simulation_state.resources) / total_resources if total_resources > 0 else 0
                min_value = min((r.value for r in simulation_state.resources), default=0)
                max_value = max((r.value for r in simulation_state.resources), default=0)
                log_callback(f"📊 Resource state before degradation:")
                log_callback(f"   • Total resources: {total_resources}")
                log_callback(f"   • Average value: {avg_value:.1f}")
                log_callback(f"   • Range: {min_value:.1f} - {max_value:.1f}")
            simulation_state = apply_entropy_degradation(simulation_state, intensity, log_callback)
            write_system_state(simulation_state)
            if log_callback:
                # Show summary after degradation (Показати зведення після деградації)
                total_resources_after = len(simulation_state.resources)
                avg_value_after = sum(r.value for r in simulation_state.resources) / total_resources_after if total_resources_after > 0 else 0
                min_value_after = min((r.value for r in simulation_state.resources), default=0)
                max_value_after = max((r.value for r in simulation_state.resources), default=0)
                log_callback(f"📊 Resource state after degradation:")
                log_callback(f"   • Average value: {avg_value_after:.1f} (change: {avg_value_after - avg_value:+.1f})")
                log_callback(f"   • Range: {min_value_after:.1f} - {max_value_after:.1f}")
        
        # Calculate adaptation time (Обчислити час адаптації)
        if adaptation_start_day is not None:
            t_adapt = float(day - adaptation_start_day + 1)
        else:
            t_adapt = 1.0  # No adaptation yet (Адаптації ще немає)
        
        # Calculate current metrics (Обчислити поточні метрики)
        s_index, c_index, a_index = calculate_metrics_from_state(
            simulation_state,
            total_ops=total_ops,
            alerts_count=total_alerts,
            t_adapt=t_adapt,
            t_market=t_market
        )
        
        # Update state with calculated indices (Оновити стан з обчисленими індексами)
        simulation_state.s_index = s_index
        simulation_state.c_index = c_index
        simulation_state.a_index = a_index
        
        # Log metrics if callback provided (Залогувати метрики, якщо надано callback)
        if log_callback:
            log_callback(f"📈 Calculated Metrics:")
            log_callback(f"   • S Index (Sustainability): {s_index:.3f}")
            log_callback(f"   • C Index (Control): {c_index:.3f}")
            log_callback(f"   • A Index (Adaptability): {a_index:.3f}")
            log_callback(f"📊 Cumulative Stats: Total Ops={total_ops}, Total Alerts={total_alerts}, T_adapt={t_adapt:.1f} days")
        
        # Record metrics for this day (Записати метрики для цього дня)
        metrics = SimulationMetrics(
            s_index=s_index,
            c_index=c_index,
            a_index=a_index,
            timestamp=datetime.utcnow() + timedelta(days=day)
        )
        metrics_history.append(metrics)
        # Save to database (Зберегти в базу даних)
        save_simulation_metric(metrics, simulation_run_id, use_agent, day=day)
    
    # Store in global history (Зберегти в глобальній історії)
    _simulation_history = metrics_history
    # Agent logs are already stored in _agent_logs_history during simulation (Логи агента вже збережені в _agent_logs_history під час симуляції)
    
    # Send completion message if callback provided (Відправити повідомлення про завершення, якщо надано callback)
    if log_callback:
        log_callback("=" * 60)
        log_callback(f"Simulation completed: {len(metrics_history)} data points collected")
        log_callback(f"Agent actions: {agent_actions_count}")
    
    # Restore original state (Відновити оригінальний стан)
    write_system_state(current_state)
    
    return metrics_history


def get_simulation_summary(metrics_history: List[SimulationMetrics]) -> Dict:
    """
    Generate summary statistics from simulation results (Згенерувати зведену статистику з результатів симуляції).
    
    Args:
        metrics_history: List of metrics from simulation (Список метрик з симуляції)
    
    Returns:
        Dictionary with before/after comparison and statistics (Словник з порівнянням до/після та статистикою)
    """
    if not metrics_history:
        return {
            "before": {"s_index": 0.0, "c_index": 0.0, "a_index": 0.0},
            "after": {"s_index": 0.0, "c_index": 0.0, "a_index": 0.0},
            "improvements": {"s_index": 0.0, "c_index": 0.0, "a_index": 0.0},
        }
    
    initial = metrics_history[0]
    final = metrics_history[-1]
    
    return {
        "before": {
            "s_index": initial.s_index,
            "c_index": initial.c_index,
            "a_index": initial.a_index,
        },
        "after": {
            "s_index": final.s_index,
            "c_index": final.c_index,
            "a_index": final.a_index,
        },
        "improvements": {
            "s_index": final.s_index - initial.s_index,
            "c_index": final.c_index - initial.c_index,
            "a_index": final.a_index - initial.a_index,
        },
        "total_steps": len(metrics_history),
    }

