import json
from pathlib import Path
import os

LOGS_DIR = Path(os.getenv("LOGS_DIR", "logs")).resolve()
LOGS_DIR.mkdir(parents=True, exist_ok=True)
CHECKPOINT = LOGS_DIR / "checkpoint.json"

def save_state(state):
    with open(CHECKPOINT, "w", encoding="utf8") as f:
        json.dump(state, f, indent=4, ensure_ascii=False)

def load_state():
    if os.path.exists(CHECKPOINT):
        with open(CHECKPOINT, "r", encoding="utf8") as f:
            return json.load(f)
    return None