"""
Analytics module for calculating scientific metrics indices (Модуль аналітики для обчислення наукових індексів метрик).
Implements formulas from ai_agents_nervous_system article (Реалізує формули зі статті ai_agents_nervous_system).
"""

from typing import Optional
from app.models import SystemState, ResourceType, ComponentType


def calculate_s_index(tech_resource: float, soc_resource: float, waste: float) -> float:
    """
    Calculate Sustainability Index (S) (Обчислити індекс сталості S).
    
    Formula: S = (R_eco + R_soc) / 2 * (1 - W)
    Where:
    - R_eco: Ecological/Technological resource level (Рівень екологічних/технологічних ресурсів)
    - R_soc: Social/Cultural resource level (Рівень соціальних/культурних ресурсів)
    - W: Waste/Entropy level (Рівень відходів/ентропії)
    
    Args:
        tech_resource: Technological resource value normalized to 0-1 (Технологічний ресурс, нормалізований до 0-1)
        soc_resource: Social/Cultural resource value normalized to 0-1 (Соціальний/культурний ресурс, нормалізований до 0-1)
        waste: Waste level normalized to 0-1 (Рівень відходів, нормалізований до 0-1)
    
    Returns:
        Sustainability index in range [0, 1] (Індекс сталості в діапазоні [0, 1])
    """
    # Normalize waste to [0, 1] range (Нормалізувати відходи до діапазону [0, 1])
    waste_clamped = max(0.0, min(1.0, waste))
    
    # Calculate average of resources (Обчислити середнє ресурсів)
    avg_resources = (tech_resource + soc_resource) / 2.0
    
    # Apply waste reduction factor (Застосувати фактор зменшення відходів)
    s_index = avg_resources * (1.0 - waste_clamped)
    
    # Clamp to valid range (Обмежити до валідного діапазону)
    return max(0.0, min(1.0, s_index))


def calculate_c_index(total_ops: int, alerts_count: int) -> float:
    """
    Calculate Cybernetic Control Index (C) (Обчислити індекс керованості C).
    
    Formula: C = 1 - (N_alerts / N_ops)
    Where:
    - N_alerts: Number of incidents/alerts (Кількість інцидентів/алертів)
    - N_ops: Total number of operations (Загальна кількість операцій)
    
    Args:
        total_ops: Total number of operations (Загальна кількість операцій)
        alerts_count: Number of alerts/incidents (Кількість алертів/інцидентів)
    
    Returns:
        Control index in range [0, 1] (Індекс керованості в діапазоні [0, 1])
    """
    # Handle division by zero (Обробка ділення на нуль)
    if total_ops == 0:
        # If no operations, assume perfect control (Якщо немає операцій, припустити ідеальне керування)
        return 1.0
    
    # Ensure non-negative values (Переконатися в невід'ємних значеннях)
    alerts_count = max(0, alerts_count)
    total_ops = max(1, total_ops)  # Prevent division by zero (Запобігти діленню на нуль)
    
    # Calculate alert ratio (Обчислити співвідношення алертів)
    alert_ratio = min(1.0, alerts_count / total_ops)
    
    # Control index is inverse of alert ratio (Індекс керованості - обернене до співвідношення алертів)
    c_index = 1.0 - alert_ratio
    
    # Clamp to valid range (Обмежити до валідного діапазону)
    return max(0.0, min(1.0, c_index))


def calculate_a_index(t_adapt: float, t_market: float) -> float:
    """
    Calculate Adaptability Index (A) (Обчислити індекс адаптивності A).
    
    Formula: A = T_adapt / T_market
    Where:
    - T_adapt: System adaptation time (Час адаптації системи)
    - T_market: Market change time (Час змін на ринку)
    
    Args:
        t_adapt: Adaptation time in days (Час адаптації в днях)
        t_market: Market change time in days (Час змін на ринку в днях)
    
    Returns:
        Adaptability index >= 0 (Індекс адаптивності >= 0)
    """
    # Validate inputs (Валідація вхідних даних)
    if t_market <= 0:
        # Invalid market time, return high adaptability (Невірний час ринку, повернути високу адаптивність)
        return 1.0
    
    if t_adapt <= 0:
        # Instant adaptation (Миттєва адаптація)
        return 0.0
    
    # Calculate adaptability ratio (Обчислити співвідношення адаптивності)
    a_index = t_adapt / t_market
    
    # No upper bound, but ensure non-negative (Немає верхньої межі, але переконатися в невід'ємності)
    return max(0.0, a_index)


def extract_tech_resource(state: SystemState) -> float:
    """
    Extract technological resource level from system state (Витягти рівень технологічного ресурсу зі стану системи).
    
    Args:
        state: Current system state (Поточний стан системи)
    
    Returns:
        Normalized technological resource value [0, 1] (Нормалізоване значення технологічного ресурсу [0, 1])
    """
    tech_resources = [r for r in state.resources if r.type == ResourceType.TECHNOLOGICAL]
    if not tech_resources:
        return 0.0
    
    # Average of all technological resources, normalized to [0, 1] (Середнє всіх технологічних ресурсів, нормалізоване до [0, 1])
    avg_value = sum(r.value for r in tech_resources) / len(tech_resources)
    return avg_value / 100.0


def extract_soc_resource(state: SystemState) -> float:
    """
    Extract social/cultural resource level from system state (Витягти рівень соціального/культурного ресурсу зі стану системи).
    
    Uses EDUCATIONAL resource and CULTURE component status (Використовує освітній ресурс та статус компонента культури).
    
    Args:
        state: Current system state (Поточний стан системи)
    
    Returns:
        Normalized social/cultural resource value [0, 1] (Нормалізоване значення соціального/культурного ресурсу [0, 1])
    """
    # Get educational resources (Отримати освітні ресурси)
    edu_resources = [r for r in state.resources if r.type == ResourceType.EDUCATIONAL]
    
    # Get culture component status (Отримати статус компонента культури)
    culture_components = [c for c in state.components if c.name == ComponentType.CULTURE]
    
    edu_value = 0.0
    if edu_resources:
        edu_value = sum(r.value for r in edu_resources) / len(edu_resources)
    
    # Map culture status to numeric value (Маппінг статусу культури до числового значення)
    culture_value = 50.0  # Default (За замовчуванням)
    if culture_components:
        status = culture_components[0].status.lower()
        if "healthy" in status or "active" in status:
            culture_value = 80.0
        elif "stable" in status:
            culture_value = 60.0
        elif "progress" in status or "improving" in status:
            culture_value = 70.0
        else:
            culture_value = 40.0
    
    # Average of educational and culture, normalized to [0, 1] (Середнє освітнього та культури, нормалізоване до [0, 1])
    combined_value = (edu_value + culture_value) / 2.0
    return combined_value / 100.0


def extract_waste_from_processes(state: SystemState) -> float:
    """
    Extract waste/entropy level from operational resource value (Витягти рівень відходів/ентропії зі значення операційного ресурсу).
    
    Waste is dynamically calculated based on OPERATIONAL resource: waste = 1.0 - (operational_value / 100.0)
    This creates inverse correlation: as operational resource decreases, waste increases (Відходи динамічно обчислюються на основі операційного ресурсу: waste = 1.0 - (operational_value / 100.0). Це створює обернену кореляцію: коли операційний ресурс знижується, відходи зростають).
    
    Args:
        state: Current system state (Поточний стан системи)
    
    Returns:
        Normalized waste level [0, 1] (Нормалізований рівень відходів [0, 1])
    """
    # Get operational resources (Отримати операційні ресурси)
    operational_resources = [r for r in state.resources if r.type == ResourceType.OPERATIONAL]
    
    if not operational_resources:
        return 0.5  # Default waste if no operational resources (Типові відходи, якщо немає операційних ресурсів)
    
    # Calculate average operational resource value (Обчислити середнє значення операційного ресурсу)
    avg_operational = sum(r.value for r in operational_resources) / len(operational_resources)
    
    # Waste is inverse of operational efficiency (Відходи - обернене до операційної ефективності)
    # Formula: waste = 1.0 - (operational_value / 100.0) (Формула: waste = 1.0 - (operational_value / 100.0))
    efficiency = avg_operational / 100.0
    waste = 1.0 - efficiency
    
    # Clamp to valid range (Обмежити до валідного діапазону)
    return max(0.0, min(1.0, waste))


def calculate_metrics_from_state(
    state: SystemState,
    total_ops: int = 0,
    alerts_count: int = 0,
    t_adapt: Optional[float] = None,
    t_market: float = 30.0
) -> tuple[float, float, float]:
    """
    Calculate all three indices (S, C, A) from system state and operational data (Обчислити всі три індекси (S, C, A) зі стану системи та операційних даних).
    
    Args:
        state: Current system state (Поточний стан системи)
        total_ops: Total number of operations (Загальна кількість операцій)
        alerts_count: Number of alerts/incidents (Кількість алертів/інцидентів)
        t_adapt: Adaptation time in days, if None uses default (Час адаптації в днях, якщо None - використовує типове значення)
        t_market: Market change time in days (Час змін на ринку в днях)
    
    Returns:
        Tuple of (s_index, c_index, a_index) (Кортеж (s_index, c_index, a_index))
    """
    # Extract resources for S index (Витягти ресурси для індексу S)
    tech_resource = extract_tech_resource(state)
    soc_resource = extract_soc_resource(state)
    waste = extract_waste_from_processes(state)
    
    # Calculate S index (Обчислити індекс S)
    s_index = calculate_s_index(tech_resource, soc_resource, waste)
    
    # Calculate C index (Обчислити індекс C)
    c_index = calculate_c_index(total_ops, alerts_count)
    
    # Calculate A index (Обчислити індекс A)
    if t_adapt is None:
        # Default: assume adaptation takes 1 day per operation (За замовчуванням: припустити, що адаптація займає 1 день на операцію)
        t_adapt = max(1.0, total_ops * 0.1)  # Scale down for realistic values (Масштабувати для реалістичних значень)
    
    a_index = calculate_a_index(t_adapt, t_market)
    
    return s_index, c_index, a_index

