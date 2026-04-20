import json
import time

import pytest

from lib import observations, storage


def test_log_appends_jsonl(tmp_telos_home):
    observations.log({"mode": "hook_session_start", "profile_present": True})
    content = storage.read_text("observations.jsonl")
    assert content is not None
    line = content.strip().splitlines()[0]
    rec = json.loads(line)
    assert rec["mode"] == "hook_session_start"
    assert rec["profile_present"] is True
    assert "ts" in rec


def test_log_multiple_events(tmp_telos_home):
    observations.log({"mode": "a"})
    observations.log({"mode": "b"})
    observations.log({"mode": "c"})
    content = storage.read_text("observations.jsonl")
    lines = content.strip().splitlines()
    assert len(lines) == 3
    modes = [json.loads(l)["mode"] for l in lines]
    assert modes == ["a", "b", "c"]


def test_log_fails_open_on_error(tmp_telos_home, monkeypatch):
    """If logging fails, it must not raise."""
    def broken(*a, **kw):
        raise OSError("disk full")
    monkeypatch.setattr(storage, "append_text", broken)
    # Should NOT raise
    observations.log({"mode": "test"})


def test_read_since_filters_by_timestamp(tmp_telos_home):
    observations.log({"mode": "old"})
    time.sleep(0.01)
    cutoff = observations.now_iso()
    time.sleep(0.01)
    observations.log({"mode": "new"})
    recent = observations.read_since(cutoff)
    modes = [r["mode"] for r in recent]
    assert "new" in modes
    assert "old" not in modes


def test_read_since_returns_empty_if_no_file(tmp_telos_home):
    assert observations.read_since("2020-01-01T00:00:00") == []
