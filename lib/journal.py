"""Daily journal: append-only blocks, queried by kind."""

from datetime import date, datetime
from pathlib import Path

from . import storage

VALID_KINDS = {"brief", "session", "reflect", "weekly", "analysis", "manual"}


def journal_path(d: date) -> Path:
    return storage.data_root() / "journal" / f"{d.isoformat()}.md"


def _rel_path(d: date) -> str:
    return f"journal/{d.isoformat()}.md"


def append_block(d: date, kind: str, body: str) -> None:
    """Append a [kind]...[/kind] block with timestamp."""
    if kind not in VALID_KINDS:
        raise ValueError(f"invalid kind: {kind}")
    ts = datetime.now().strftime("%H:%M")
    block = f"\n[{kind}] {ts}\n{body.strip()}\n[/{kind}]\n"
    storage.append_text(_rel_path(d), block)


def has_block(d: date, kind: str) -> bool:
    content = storage.read_text(_rel_path(d))
    if content is None:
        return False
    return f"[{kind}]" in content


def recent_journals(n: int = 3) -> list[str]:
    """Return last n days' journal contents, newest first."""
    journal_dir = storage.data_root() / "journal"
    if not journal_dir.exists():
        return []
    files = sorted(journal_dir.glob("*.md"), reverse=True)[:n]
    return [f.read_text(encoding="utf-8") for f in files]
