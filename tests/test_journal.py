from datetime import date

import pytest

from lib import journal, storage


def test_journal_path_format(tmp_telos_home):
    p = journal.journal_path(date(2026, 4, 20))
    assert p.name == "2026-04-20.md"
    assert p.parent.name == "journal"


def test_append_block_writes_to_file(tmp_telos_home):
    journal.append_block(date(2026, 4, 20), "brief", "3 do / 2 avoid / 1 surprise")
    content = storage.read_text("journal/2026-04-20.md")
    assert "[brief]" in content
    assert "3 do" in content


def test_append_multiple_blocks_preserves_order(tmp_telos_home):
    d = date(2026, 4, 20)
    journal.append_block(d, "brief", "morning")
    journal.append_block(d, "session", "did stuff")
    journal.append_block(d, "reflect", "evening thoughts")
    content = storage.read_text("journal/2026-04-20.md")
    assert content.index("[brief]") < content.index("[session]")
    assert content.index("[session]") < content.index("[reflect]")


def test_has_block_detects_presence(tmp_telos_home):
    d = date(2026, 4, 20)
    assert not journal.has_block(d, "brief")
    journal.append_block(d, "brief", "x")
    assert journal.has_block(d, "brief")
    assert not journal.has_block(d, "reflect")


def test_has_block_returns_false_if_file_missing(tmp_telos_home):
    assert not journal.has_block(date(2026, 1, 1), "brief")


def test_recent_journals_returns_newest_first(tmp_telos_home):
    journal.append_block(date(2026, 4, 18), "brief", "A")
    journal.append_block(date(2026, 4, 19), "brief", "B")
    journal.append_block(date(2026, 4, 20), "brief", "C")
    recent = journal.recent_journals(n=3)
    assert len(recent) == 3
    assert "C" in recent[0]
    assert "A" in recent[2]


def test_recent_journals_caps_at_available(tmp_telos_home):
    journal.append_block(date(2026, 4, 20), "brief", "only")
    recent = journal.recent_journals(n=5)
    assert len(recent) == 1
