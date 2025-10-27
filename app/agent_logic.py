"""
Rule-based mock AI agent for resource analysis.
Simulates the "Resource Analyst" step in the cybernetic control cycle.
"""

import copy
from app.models import SystemState


def run_mock_analysis(goal: str, current_state: SystemState) -> SystemState:
    """
    Simulate AI agent analysis based on the manager's goal.
    
    Args:
        goal: Strategic goal text from the manager
        current_state: Current system state
        
    Returns:
        Modified system state after agent's recommendations
    """
    # Create deep copy to avoid mutations
    new_state = copy.deepcopy(current_state)
    
    # Log agent "thoughts"
    print(f"\n{'='*60}")
    print(f"🤖 AI Агент аналізує ціль: '{goal}'")
    print(f"{'='*60}")
    
    goal_lower = goal.lower()
    
    # Rule 1: Circular economy / recycling
    if "переробк" in goal_lower or "екологі" in goal_lower or "circular" in goal_lower:
        print("📊 Виявлено ключові слова: Переробка, Екологія")
        print("💡 Рекомендація: Збільшити Технологічний, Освітній, Ризиковий ресурси")
        
        for resource in new_state.resources:
            if resource.type.value == "Технологічний":
                resource.value = min(100, resource.value + 20)
            elif resource.type.value == "Освітній":
                resource.value = min(100, resource.value + 15)
            elif resource.type.value == "Ризиковий":
                resource.value = min(100, resource.value + 10)
        
        print(f"✅ Оновлено: Технологічний (+20), Освітній (+15), Ризиковий (+10)")
    
    # Rule 2: Customer / service focus
    elif "клієнт" in goal_lower or "сервіс" in goal_lower or "клієнтськ" in goal_lower:
        print("📊 Виявлено ключові слова: Клієнт, Сервіс")
        print("💡 Рекомендація: Збільшити Комунікаційний, Інформаційний, Операційний ресурси")
        
        for resource in new_state.resources:
            if resource.type.value == "Комунікаційний":
                resource.value = min(100, resource.value + 15)
            elif resource.type.value == "Інформаційний":
                resource.value = min(100, resource.value + 10)
            elif resource.type.value == "Операційний":
                resource.value = min(100, resource.value + 10)
        
        print(f"✅ Оновлено: Комунікаційний (+15), Інформаційний (+10), Операційний (+10)")
    
    # Rule 3: Innovation / digital transformation
    elif "інновац" in goal_lower or "цифров" in goal_lower or "автоматизац" in goal_lower:
        print("📊 Виявлено ключові слова: Інновація, Цифрова трансформація")
        print("💡 Рекомендація: Збільшити Технологічний, Стратегічний, Фінансовий ресурси")
        
        for resource in new_state.resources:
            if resource.type.value == "Технологічний":
                resource.value = min(100, resource.value + 25)
            elif resource.type.value == "Стратегічний":
                resource.value = min(100, resource.value + 15)
            elif resource.type.value == "Фінансовий":
                resource.value = min(100, resource.value + 10)
        
        print(f"✅ Оновлено: Технологічний (+25), Стратегічний (+15), Фінансовий (+10)")
    
    # Rule 4: Partnerships / ecosystem
    elif "партнер" in goal_lower or "екосистем" in goal_lower or "співпрац" in goal_lower:
        print("📊 Виявлено ключові слова: Партнерство, Екосистема")
        print("💡 Рекомендація: Збільшити Організаційний, Комунікаційний ресурси")
        
        for resource in new_state.resources:
            if resource.type.value == "Організаційний":
                resource.value = min(100, resource.value + 20)
            elif resource.type.value == "Комунікаційний":
                resource.value = min(100, resource.value + 10)
        
        print(f"✅ Оновлено: Організаційний (+20), Комунікаційний (+10)")
    
    # Rule 5: Risk management / compliance
    elif "ризик" in goal_lower or "безпека" in goal_lower or "комплаєнс" in goal_lower:
        print("📊 Виявлено ключові слова: Ризики, Безпека")
        print("💡 Рекомендація: Збільшити Ризиковий, Операційний ресурси")
        
        for resource in new_state.resources:
            if resource.type.value == "Ризиковий":
                resource.value = min(100, resource.value + 20)
            elif resource.type.value == "Операційний":
                resource.value = min(100, resource.value + 10)
        
        print(f"✅ Оновлено: Ризиковий (+20), Операційний (+10)")
    
    # Rule 6: Educational / knowledge
    elif "освят" in goal_lower or "трен" in goal_lower or "знанн" in goal_lower or "навчан" in goal_lower:
        print("📊 Виявлено ключові слова: Освіта, Тренінги")
        print("💡 Рекомендація: Збільшити Освітній, Організаційний ресурси")
        
        for resource in new_state.resources:
            if resource.type.value == "Освітній":
                resource.value = min(100, resource.value + 20)
            elif resource.type.value == "Організаційний":
                resource.value = min(100, resource.value + 10)
        
        print(f"✅ Оновлено: Освітній (+20), Організаційний (+10)")
    
    # Default: general strategy
    else:
        print("📊 Ціль не розпізнано чітко - застосовую базові покращення")
        print("💡 Рекомендація: Рівномірне підвищення основних ресурсів")
        
        for resource in new_state.resources:
            if resource.type.value in ["Технологічний", "Стратегічний", "Фінансовий"]:
                resource.value = min(100, resource.value + 5)
        
        print(f"✅ Оновлено: Технологічний (+5), Стратегічний (+5), Фінансовий (+5)")
    
    print(f"{'='*60}\n")
    
    return new_state



