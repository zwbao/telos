from pathlib import Path

import pytest

from lib import storage


def test_data_root_creates_dir(tmp_telos_home):
    root = storage.data_root()
    assert root.exists()
    assert root.is_dir()
    assert str(root).endswith(".claude/telos")


def test_read_text_returns_none_for_missing(tmp_telos_home):
    assert storage.read_text("nope.md") is None


def test_write_text_and_read_text_roundtrip(tmp_telos_home):
    storage.write_text("profile.md", "hello\n")
    assert storage.read_text("profile.md") == "hello\n"


def test_write_text_creates_parent_dirs(tmp_telos_home):
    storage.write_text("journal/2026-04-20.md", "entry\n")
    assert (tmp_telos_home / "journal" / "2026-04-20.md").exists()


def test_write_text_is_atomic(tmp_telos_home):
    # Write twice; second should fully replace
    storage.write_text("x.md", "first")
    storage.write_text("x.md", "second")
    assert storage.read_text("x.md") == "second"


def test_append_text_creates_if_missing(tmp_telos_home):
    storage.append_text("log.md", "line1\n")
    storage.append_text("log.md", "line2\n")
    assert storage.read_text("log.md") == "line1\nline2\n"
