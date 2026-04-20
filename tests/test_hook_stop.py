import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "stop.py"
PYTHON = sys.executable


def _run(input_json: dict, home: Path) -> int:
    result = subprocess.run(
        [PYTHON, str(HOOK)],
        input=json.dumps(input_json).encode(),
        capture_output=True,
        env={"HOME": str(home), "PATH": "/usr/bin:/bin"},
        timeout=5,
    )
    return result.returncode


def test_stop_appends_session_block_to_today_journal(tmp_telos_home):
    home = tmp_telos_home.parent.parent
    ev = {
        "hook_event_name": "Stop",
        "messages": [
            {"role": "user", "content": "fix the bug in x.py"},
            {"role": "assistant", "content": "Fixed. Tests pass."},
        ],
    }
    assert _run(ev, home) == 0
    today = date.today().isoformat()
    journal_file = tmp_telos_home / "journal" / f"{today}.md"
    assert journal_file.exists()
    content = journal_file.read_text(encoding="utf-8")
    assert "[session]" in content
    assert "fix the bug" in content or "Fixed" in content


def test_stop_with_no_messages_still_logs(tmp_telos_home):
    home = tmp_telos_home.parent.parent
    assert _run({"hook_event_name": "Stop"}, home) == 0
    obs_file = tmp_telos_home / "observations.jsonl"
    assert obs_file.exists()


def test_stop_bad_input_fails_open(tmp_telos_home):
    home = tmp_telos_home.parent.parent
    result = subprocess.run(
        [PYTHON, str(HOOK)],
        input=b"not json",
        capture_output=True,
        env={"HOME": str(home), "PATH": "/usr/bin:/bin"},
        timeout=5,
    )
    assert result.returncode == 0


def test_stop_truncates_long_content(tmp_telos_home):
    home = tmp_telos_home.parent.parent
    ev = {
        "hook_event_name": "Stop",
        "messages": [
            {"role": "user", "content": "x" * 5000},
            {"role": "assistant", "content": "y" * 5000},
        ],
    }
    assert _run(ev, home) == 0
    today = date.today().isoformat()
    content = (tmp_telos_home / "journal" / f"{today}.md").read_text(encoding="utf-8")
    # Should be truncated, not contain 5000 of anything
    assert content.count("x") < 1000
