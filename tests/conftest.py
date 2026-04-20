import os
import sys
from pathlib import Path

import pytest

# Make lib importable from tests
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture
def tmp_telos_home(tmp_path, monkeypatch):
    """Redirect ~/.claude/telos/ to a tmp dir for each test."""
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setenv("HOME", str(fake_home))
    # Also patch any cached paths if needed
    return fake_home / ".claude" / "telos"
