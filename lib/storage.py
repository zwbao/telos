"""Filesystem primitives for telos data at ~/.claude/telos/."""

import os
from pathlib import Path


def data_root() -> Path:
    """Return ~/.claude/telos/, creating it if missing."""
    root = Path(os.environ["HOME"]) / ".claude" / "telos"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _resolve(rel_path: str) -> Path:
    return data_root() / rel_path


def read_text(rel_path: str) -> str | None:
    """Return file content, or None if missing."""
    p = _resolve(rel_path)
    if not p.exists():
        return None
    return p.read_text(encoding="utf-8")


def write_text(rel_path: str, content: str) -> None:
    """Atomic write: write to .tmp then rename."""
    p = _resolve(rel_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, p)


def append_text(rel_path: str, content: str) -> None:
    """Append content; create file + parents if missing."""
    p = _resolve(rel_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(content)
