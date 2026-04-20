import pytest

from lib import profile, storage


SAMPLE = """# Profile

## 北极星
Build things that outlive me; pursue truth over comfort; keep 5 people close.

## 命盘
INTJ, 1996 年冬月生。

## 五个核心价值
1. 诚实
2. 好奇
3. 自由
4. 责任
5. 美

## 十年图景
Running a sustainable org that matters; still married; still writing.

## 调整历史
"""


def test_read_profile_returns_none_if_missing(tmp_telos_home):
    assert profile.read_profile() is None


def test_read_profile_parses_sections(tmp_telos_home):
    storage.write_text("profile.md", SAMPLE)
    p = profile.read_profile()
    assert p is not None
    assert "outlive me" in p["北极星"]
    assert "INTJ" in p["命盘"]
    assert len(p["五个核心价值"].splitlines()) >= 5


def test_polestar_extracts_paragraph(tmp_telos_home):
    storage.write_text("profile.md", SAMPLE)
    p = profile.read_profile()
    ps = profile.polestar(p)
    assert "outlive me" in ps
    assert "##" not in ps  # no markdown headers


def test_write_profile_roundtrip(tmp_telos_home):
    data = {
        "北极星": "short polestar text",
        "命盘": "",
        "五个核心价值": "1. a\n2. b\n3. c\n4. d\n5. e",
        "十年图景": "a vision",
        "调整历史": "",
    }
    profile.write_profile(data)
    read_back = profile.read_profile()
    assert read_back["北极星"] == "short polestar text"
    assert "1. a" in read_back["五个核心价值"]


def test_append_tiaozheng_lishi(tmp_telos_home):
    storage.write_text("profile.md", SAMPLE)
    profile.append_调整历史("reason: Q1 reflection", old_polestar="X", new_polestar="Y")
    p = profile.read_profile()
    assert "Q1 reflection" in p["调整历史"]
    assert "X → Y" in p["调整历史"]


def test_polestar_none_if_empty_section(tmp_telos_home):
    storage.write_text("profile.md", "# Profile\n\n## 北极星\n\n## 命盘\n")
    p = profile.read_profile()
    assert profile.polestar(p) == ""
