from datetime import datetime
from pathlib import Path
import os

LOGS_DIR = Path(os.getenv("LOGS_DIR", "logs")).resolve()
LOGS_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOGS_DIR / "audit.log"

def log_transition(state_name):
    with open(LOG_FILE, "a", encoding="utf8") as file:
        file.write(
            f"{datetime.now()} -> Estado: {state_name}\n"
        )