import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "user_prompt_submit.py"
PYTHON = sys.executable


def _run(input_json: dict, home: Path) -> dict:
    result = subprocess.run(
        [PYTHON, str(HOOK)],
        input=json.dumps(input_json).encode(),
        capture_output=True,
        env={"HOME": str(home), "PATH": "/usr/bin:/bin"},
        timeout=5,
    )
    assert result.returncode == 0
    out = result.stdout.decode().strip()
    return json.loads(out) if out else {}


def _write_profile(home_telos: Path):
    home_telos.mkdir(parents=True, exist_ok=True)
    (home_telos / "profile.md").write_text(
        "# Profile\n\n## 北极星\nbuild things that outlive me\n\n",
        encoding="utf-8",
    )


def test_short_prompt_does_not_inject(tmp_telos_home):
    _write_profile(tmp_telos_home)
    home = tmp_telos_home.parent.parent
    out = _run({"hook_event_name": "UserPromptSubmit", "prompt": "hi"}, home)
    assert "additionalContext" not in out.get("hookSpecificOutput", {})


def test_decision_prompt_injects_hint(tmp_telos_home):
    _write_profile(tmp_telos_home)
    home = tmp_telos_home.parent.parent
    prompt = "我应不应该接这个 offer？薪水不错但是需要搬家。"
    out = _run({"hook_event_name": "UserPromptSubmit", "prompt": prompt}, home)
    ctx = out.get("hookSpecificOutput", {}).get("additionalContext", "")
    assert "outlive me" in ctx
    assert "HARD-GATE" in ctx or "deciding-with-telos" in ctx


def test_long_non_decision_prompt_injects_hint(tmp_telos_home):
    _write_profile(tmp_telos_home)
    home = tmp_telos_home.parent.parent
    prompt = "x" * 200  # long enough to trigger
    out = _run({"hook_event_name": "UserPromptSubmit", "prompt": prompt}, home)
    ctx = out.get("hookSpecificOutput", {}).get("additionalContext", "")
    assert "outlive me" in ctx


def test_no_profile_no_inject(tmp_telos_home):
    home = tmp_telos_home.parent.parent
    out = _run({"hook_event_name": "UserPromptSubmit", "prompt": "要不要接 offer"}, home)
    assert "additionalContext" not in out.get("hookSpecificOutput", {})


def test_bad_input_fails_open(tmp_telos_home):
    home = tmp_telos_home.parent.parent
    result = subprocess.run(
        [PYTHON, str(HOOK)],
        input=b"garbage",
        capture_output=True,
        env={"HOME": str(home), "PATH": "/usr/bin:/bin"},
        timeout=5,
    )
    assert result.returncode == 0
