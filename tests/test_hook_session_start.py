import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "session_start.py"
PYTHON = sys.executable  # use the same interpreter running the tests


def _run_hook(input_json: dict, home: Path) -> dict:
    result = subprocess.run(
        [PYTHON, str(HOOK)],
        input=json.dumps(input_json).encode(),
        capture_output=True,
        env={"HOME": str(home), "PATH": "/usr/bin:/bin"},
        timeout=5,
    )
    assert result.returncode == 0, f"hook failed: {result.stderr.decode()}"
    out = result.stdout.decode().strip()
    return json.loads(out) if out else {}


def test_session_start_with_no_profile_emits_empty(tmp_telos_home):
    home = tmp_telos_home.parent.parent  # up from .claude/telos to home
    out = _run_hook({"hook_event_name": "SessionStart"}, home)
    # Should be empty output or lack additionalContext
    assert out == {} or "additionalContext" not in out.get("hookSpecificOutput", {})


def test_session_start_with_profile_injects_polestar(tmp_telos_home):
    tmp_telos_home.mkdir(parents=True, exist_ok=True)
    (tmp_telos_home / "profile.md").write_text(
        "# Profile\n\n## 北极星\nbuild things that outlive me\n\n## 命盘\n\n",
        encoding="utf-8",
    )
    home = tmp_telos_home.parent.parent
    out = _run_hook({"hook_event_name": "SessionStart"}, home)
    ctx = out.get("hookSpecificOutput", {}).get("additionalContext", "")
    assert "outlive me" in ctx
    assert "北极星" in ctx


def test_session_start_never_fails_on_bad_input(tmp_telos_home):
    home = tmp_telos_home.parent.parent
    result = subprocess.run(
        [PYTHON, str(HOOK)],
        input=b"not json",
        capture_output=True,
        env={"HOME": str(home), "PATH": "/usr/bin:/bin"},
        timeout=5,
    )
    assert result.returncode == 0  # fail open
