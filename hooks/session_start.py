#!/usr/bin/env python3
"""SessionStart hook: inject polestar paragraph into CC session context."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import observations, profile  # noqa: E402


def main() -> None:
    try:
        try:
            _ = json.loads(sys.stdin.read() or "{}")
        except json.JSONDecodeError:
            pass  # continue anyway; hook should succeed with no input

        prof = profile.read_profile()
        polestar_text = profile.polestar(prof)

        observations.log({
            "mode": "hook_session_start",
            "profile_present": prof is not None,
        })

        if not polestar_text:
            print("")
            return

        context = (
            f"用户的北极星（telos）: {polestar_text}\n"
            f"本 session 中，涉及人生决策/方向的提问需引用此北极星。"
        )
        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context,
            }
        }
        print(json.dumps(output, ensure_ascii=False))
    except Exception as e:
        observations.log({"mode": "hook_error", "hook": "session_start", "error": str(e)})
        sys.exit(0)


if __name__ == "__main__":
    main()
