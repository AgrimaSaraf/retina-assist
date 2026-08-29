import json, os
from datetime import datetime, timezone
from pathlib import Path

def write_event(event: dict) -> None:
    path = Path(os.getenv("EVENT_LOG_PATH", "research_events/events.jsonl"))
    path.parent.mkdir(parents=True, exist_ok=True)
    record = dict(event)
    record["timestamp_iso"] = record.get("timestamp_iso") or datetime.now(timezone.utc).isoformat()
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
