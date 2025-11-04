"""
Test configuration to ensure project root is importable (Конфіг для тестів, щоб корінь проєкту підтягувався в імпорти).
"""

import os
import sys


def _ensure_project_root_on_path() -> None:
    """Prepend project root to sys.path (Додати корінь проєкту в sys.path)."""
    tests_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(tests_dir, os.pardir))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


_ensure_project_root_on_path()




