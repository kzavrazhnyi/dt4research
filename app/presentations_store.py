from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict

# Simple JSON store for presentation links (Просте сховище посилань у JSON)
STORE_PATH = Path(__file__).parent.parent / "presentations.json"


def read_presentations() -> List[Dict[str, str]]:
    if STORE_PATH.exists():
        try:
            return json.loads(STORE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def write_presentations(items: List[Dict[str, str]]) -> None:
    STORE_PATH.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")






















