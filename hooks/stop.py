#!/usr/bin/env python3
"""Stop hook: append heuristic session summary to today's journal."""

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import journal, observations  # noqa: E402

MAX_CONTENT_CHARS = 150  # per message
MAX_TOTAL_CHARS = 500


def summarize(messages: list[dict]) -> str:
    """Heuristic: first user prompt + last assistant response, truncated."""
    if not messages:
        return "(empty session)"
    first_user = next(
        (m for m in messages if m.get("role") == "user"),
        None,
    )
    last_asst = next(
        (m for m in reversed(messages) if m.get("role") == "assistant"),
        None,
    )
    parts = []
    if first_user:
        content = str(first_user.get("content", ""))[:MAX_CONTENT_CHARS]
        parts.append(f"User: {content}")
    if last_asst:
        content = str(last_asst.get("content", ""))[:MAX_CONTENT_CHARS]
        parts.append(f"Asst: {content}")
    summary = "\n".join(parts)
    return summary[:MAX_TOTAL_CHARS]


def main() -> None:
    try:
        try:
            ev = json.loads(sys.stdin.read() or "{}")
        except json.JSONDecodeError:
            observations.log({"mode": "hook_stop", "error": "bad_input"})
            sys.exit(0)

        messages = ev.get("messages", [])
        summary = summarize(messages)
        today = date.today()
        journal.append_block(today, "session", summary)

        observations.log({
            "mode": "hook_stop",
            "message_count": len(messages),
            "summary_chars": len(summary),
        })
    except Exception as e:
        observations.log({"mode": "hook_error", "hook": "stop", "error": str(e)})
        sys.exit(0)


if __name__ == "__main__":
    main()
