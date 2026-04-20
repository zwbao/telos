#!/usr/bin/env python3
"""UserPromptSubmit hook: silently inject polestar context on decision-shaped prompts."""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib import observations, profile  # noqa: E402

DECISION_PATTERNS = [
    r"要不要",
    r"该不该",
    r"应不应该",
    r"选哪",
    r"should i",
    r"\bvs\.?\b",
    r"哪个更",
]
DECISION_RE = re.compile("|".join(DECISION_PATTERNS), re.IGNORECASE)

MIN_PROMPT_LEN_FOR_HINT = 80


def should_inject(prompt: str) -> tuple[bool, bool]:
    """Return (inject, is_decision). Inject if decision OR long enough."""
    is_decision = bool(DECISION_RE.search(prompt))
    long_enough = len(prompt) >= MIN_PROMPT_LEN_FOR_HINT
    return (is_decision or long_enough, is_decision)


def main() -> None:
    try:
        try:
            ev = json.loads(sys.stdin.read() or "{}")
        except json.JSONDecodeError:
            print("")
            return

        prompt = ev.get("prompt", "") or ""
        prof = profile.read_profile()
        polestar_text = profile.polestar(prof)

        inject, is_decision = should_inject(prompt)

        observations.log({
            "mode": "hook_prompt_submit",
            "matched": inject,
            "is_decision": is_decision,
            "prompt_len": len(prompt),
            "profile_present": prof is not None,
        })

        if not inject or not polestar_text:
            print("")
            return

        if is_decision:
            ctx = (
                f"用户北极星: {polestar_text}\n"
                f"[HARD-GATE] 若此 prompt 是决策，遵守 deciding-with-telos: "
                f"引用北极星原文 → 枚举 ≥2 选项的对齐/不对齐 → 可追溯推荐。"
            )
        else:
            ctx = (
                f"用户北极星: {polestar_text}\n"
                f"回答时可酌情考虑此北极星是否相关。"
            )

        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": ctx,
            }
        }, ensure_ascii=False))
    except Exception as e:
        observations.log({"mode": "hook_error", "hook": "user_prompt_submit", "error": str(e)})
        sys.exit(0)


if __name__ == "__main__":
    main()
