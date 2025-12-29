"""
Rule-based mock AI agent for resource analysis (Правиловий псевдо-АІ агент для аналізу ресурсів).
Simulates the "Resource Analyst" step in the cybernetic control cycle (Імітує крок "Аналіз ресурсу" у кібернетичному циклі).
Reads growth coefficients from environment (.env) with sane defaults (Зчитує коефіцієнти зростання з оточення (.env) з типовими значеннями).
"""

import copy
import os
from typing import Dict, Tuple, List

from dotenv import load_dotenv
from app.models import SystemState, ResourceType


# Load environment variables (Завантажити змінні оточення)
load_dotenv()


def _get_int_env(name: str, default: int) -> int:
    """Get integer environment variable with default (Отримати ціле значення змінної оточення з типовим значенням)."""
    try:
        return int(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


# Ecology / Recycling rule coefficients (Коефіцієнти для правила Екології / Переробки)
ECO_TECH = _get_int_env("RULE_ECO_TECH", 20)
ECO_EDU = _get_int_env("RULE_ECO_EDU", 15)
ECO_RISK = _get_int_env("RULE_ECO_RISK", 10)

# Customer / Service focus coefficients (Коефіцієнти для правила Клієнт/Сервіс)
CUST_COMM = _get_int_env("RULE_CUSTOMER_COMM", 15)
CUST_INFO = _get_int_env("RULE_CUSTOMER_INFO", 10)
CUST_OPER = _get_int_env("RULE_CUSTOMER_OPER", 10)

# Innovation / Digital transformation coefficients (Коефіцієнти для Інновацій / ЦТ)
INNOV_TECH = _get_int_env("RULE_INNOV_TECH", 25)
INNOV_STRAT = _get_int_env("RULE_INNOV_STRAT", 15)
INNOV_FIN = _get_int_env("RULE_INNOV_FIN", 10)

# Partnerships / Ecosystem coefficients (Коефіцієнти для Партнерств / Екосистеми)
PARTNER_ORG = _get_int_env("RULE_PARTNERS_ORG", 20)
PARTNER_COMM = _get_int_env("RULE_PARTNERS_COMM", 10)

# Risk management / Compliance coefficients (Коефіцієнти для Управління ризиками / Комплаєнсу)
RISK_RISK = _get_int_env("RULE_RISK_RISK", 20)
RISK_OPER = _get_int_env("RULE_RISK_OPER", 10)

# Educational / Knowledge coefficients (Коефіцієнти для Освіти / Знань)
EDU_EDU = _get_int_env("RULE_EDU_EDU", 20)
EDU_ORG = _get_int_env("RULE_EDU_ORG", 10)

# Default rule coefficients (Типові коефіцієнти)
DEF_TECH = _get_int_env("RULE_DEFAULT_TECH", 5)
DEF_STRAT = _get_int_env("RULE_DEFAULT_STRAT", 5)
DEF_FIN = _get_int_env("RULE_DEFAULT_FIN", 5)


def run_mock_analysis(goal: str, current_state: SystemState, capture_logs: bool = False) -> Tuple[SystemState, Dict[str, int], List[str]]:
    """
    Simulate AI agent analysis based on the manager's goal (Симулювати аналіз АІ-агента на основі цілі менеджера).

    Args:
        goal: Strategic goal text from the manager (Текст стратегічної цілі менеджера)
        current_state: Current system state (Поточний стан системи)
        capture_logs: If True, capture log messages instead of printing (Якщо True, зберігати повідомлення логів замість виводу)

    Returns:
        Tuple of (new_state, deltas_by_resource_type, log_messages) where deltas map resource type label to delta
        (Кортеж (новий_стан, дельти_за_типом_ресурсу, повідомлення_логів), де дельти — мапа типу ресурсу до зміни)
    """
    new_state = copy.deepcopy(current_state)
    deltas_by_type: Dict[ResourceType, int] = {}
    log_messages: List[str] = []
    
    def log(msg: str) -> None:
        """Log message to console or capture list (Залогувати повідомлення в консоль або зберегти в список)."""
        if capture_logs:
            log_messages.append(msg)
        else:
            print(msg)
    
    log(f"\n{'='*60}")
    log(f"🤖 AI Агент аналізує ціль: '{goal}'")
    log(f"{'='*60}")

    goal_lower = goal.lower()

    def apply_deltas(local_deltas: Dict[ResourceType, int], message: str) -> None:
        """Apply resource deltas and log message (Застосувати дельти ресурсів і залогувати повідомлення)."""
        nonlocal deltas_by_type
        deltas_by_type = local_deltas
        log(message)
        for r_type, delta in local_deltas.items():
            for resource in new_state.resources:
                if resource.type == r_type:
                    resource.value = min(100, resource.value + delta)
        human_readable = "; ".join(
            f"{r_type.value} (+{delta})" for r_type, delta in local_deltas.items()
        )
        log(f"✅ Updated resources: {human_readable}")

    if "переробк" in goal_lower or "екологі" in goal_lower or "circular" in goal_lower:
        log("📊 Виявлено ключові слова: Переробка, Екологія")
        apply_deltas(
            {
                ResourceType.TECHNOLOGICAL: ECO_TECH,
                ResourceType.EDUCATIONAL: ECO_EDU,
                ResourceType.RISK: ECO_RISK,
            },
            "💡 Recommendation: Increase Technological, Educational, Risk resources (Рекомендація: Збільшити Технологічний, Освітній, Ризиковий ресурси)",
        )
    elif "клієнт" in goal_lower or "сервіс" in goal_lower or "клієнтськ" in goal_lower:
        log("📊 Виявлено ключові слова: Клієнт, Сервіс")
        apply_deltas(
            {
                ResourceType.COMMUNICATION: CUST_COMM,
                ResourceType.INFORMATIONAL: CUST_INFO,
                ResourceType.OPERATIONAL: CUST_OPER,
            },
            "💡 Recommendation: Increase Communication, Informational, Operational resources (Рекомендація: Збільшити Комунікаційний, Інформаційний, Операційний ресурси)",
        )
    elif "інновац" in goal_lower or "цифров" in goal_lower or "автоматизац" in goal_lower:
        log("📊 Виявлено ключові слова: Інновація, Цифрова трансформація")
        apply_deltas(
            {
                ResourceType.TECHNOLOGICAL: INNOV_TECH,
                ResourceType.STRATEGIC: INNOV_STRAT,
                ResourceType.FINANCIAL: INNOV_FIN,
            },
            "💡 Recommendation: Increase Technological, Strategic, Financial resources (Рекомендація: Збільшити Технологічний, Стратегічний, Фінансовий ресурси)",
        )
    elif "партнер" in goal_lower or "екосистем" in goal_lower or "співпрац" in goal_lower:
        log("📊 Виявлено ключові слова: Партнерство, Екосистема")
        apply_deltas(
            {
                ResourceType.ORGANIZATIONAL: PARTNER_ORG,
                ResourceType.COMMUNICATION: PARTNER_COMM,
            },
            "💡 Recommendation: Increase Organizational, Communication resources (Рекомендація: Збільшити Організаційний, Комунікаційний ресурси)",
        )
    elif "ризик" in goal_lower or "безпека" in goal_lower or "комплаєнс" in goal_lower:
        log("📊 Виявлено ключові слова: Ризики, Безпека")
        apply_deltas(
            {
                ResourceType.RISK: RISK_RISK,
                ResourceType.OPERATIONAL: RISK_OPER,
            },
            "💡 Recommendation: Increase Risk and Operational resources (Рекомендація: Збільшити Ризиковий та Операційний ресурси)",
        )
    elif "освят" in goal_lower or "трен" in goal_lower or "знанн" in goal_lower or "навчан" in goal_lower:
        log("📊 Виявлено ключові слова: Освіта, Тренінги")
        apply_deltas(
            {
                ResourceType.EDUCATIONAL: EDU_EDU,
                ResourceType.ORGANIZATIONAL: EDU_ORG,
            },
            "💡 Recommendation: Increase Educational and Organizational resources (Рекомендація: Збільшити Освітній та Організаційний ресурси)",
        )
    else:
        log("📊 Ціль не розпізнано чітко - застосовую базові покращення")
        apply_deltas(
            {
                ResourceType.TECHNOLOGICAL: DEF_TECH,
                ResourceType.STRATEGIC: DEF_STRAT,
                ResourceType.FINANCIAL: DEF_FIN,
            },
            "💡 Recommendation: Even improvement of core resources (Рекомендація: Рівномірне підвищення основних ресурсів)",
        )

    log(f"{'='*60}\n")

    deltas_serialized: Dict[str, int] = {r_type.value: delta for r_type, delta in deltas_by_type.items()}
    return new_state, deltas_serialized, log_messages if capture_logs else []



