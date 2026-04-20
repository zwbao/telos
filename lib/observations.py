"""JSONL experiment logger. Best-effort; never raises."""

import json
from datetime import datetime, timezone

from . import storage

LOG_PATH = "observations.jsonl"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def log(event_dict: dict) -> None:
    """Append event as one JSON line. Swallow all errors."""
    try:
        event = {"ts": now_iso(), **event_dict}
        storage.append_text(LOG_PATH, json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        pass  # fail open; observation logging must never break the hook


def read_since(cutoff_iso: str) -> list[dict]:
    """Return events with ts > cutoff_iso. Returns [] if file missing."""
    content = storage.read_text(LOG_PATH)
    if content is None:
        return []
    events = []
    for line in content.strip().splitlines():
        try:
            rec = json.loads(line)
            if rec.get("ts", "") > cutoff_iso:
                events.append(rec)
        except json.JSONDecodeError:
            continue
    return events
