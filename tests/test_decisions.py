from datetime import date

import pytest

from lib import decisions, storage


def test_slug_sanitizes_input():
    assert decisions.slug("Should I take the offer?") == "should-i-take-the-offer"
    assert len(decisions.slug("x" * 100)) <= 50


def test_slug_handles_chinese_input():
    # Non-ASCII shouldn't crash; result should contain something recognizable
    s = decisions.slug("要不要接这个 offer")
    assert len(s) > 0


def test_write_decision_creates_file(tmp_telos_home):
    path = decisions.write_decision(
        d=date(2026, 4, 20),
        question="Should I take the offer?",
        polestar_quote="Build things that outlive me",
        options=[
            {"name": "take", "pro": "money", "con": "eats time"},
            {"name": "skip", "pro": "focus", "con": "lose option"},
        ],
        recommendation="skip",
        reasoning="Focus beats breadth at this stage.",
    )
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "Should I take" in content
    assert "outlive me" in content
    assert "Recommendation: skip" in content


def test_list_decisions_returns_all_newest_first(tmp_telos_home):
    decisions.write_decision(
        d=date(2026, 4, 18),
        question="q1", polestar_quote="p", options=[{"name": "a", "pro": "x", "con": "y"}],
        recommendation="a", reasoning="r",
    )
    decisions.write_decision(
        d=date(2026, 4, 20),
        question="q2", polestar_quote="p", options=[{"name": "b", "pro": "x", "con": "y"}],
        recommendation="b", reasoning="r",
    )
    lst = decisions.list_decisions()
    assert len(lst) == 2
    assert "2026-04-20" in lst[0].name


def test_append_outcome_adds_block(tmp_telos_home):
    path = decisions.write_decision(
        d=date(2026, 4, 20),
        question="q", polestar_quote="p",
        options=[{"name": "a", "pro": "x", "con": "y"}],
        recommendation="a", reasoning="r",
    )
    decisions.append_outcome(path, "I followed the recommendation. It worked out.")
    content = path.read_text(encoding="utf-8")
    assert "[outcome]" in content
    assert "worked out" in content
