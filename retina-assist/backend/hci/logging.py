import json
from pathlib import Path
from datetime import datetime, timezone

LOG_PATH = Path("research/interaction_events.jsonl")

def log_event(event: dict):
    """
    Local research event log. Do not place patient identifiers or PHI here.
    Replace with an approved secure store before any real clinical study.
    """
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        **event,
        "logged_at": datetime.now(timezone.utc).isoformat(),
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")
