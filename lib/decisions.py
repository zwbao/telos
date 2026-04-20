"""Decision snapshots: polestar quote, options, recommendation, outcome."""

import re
from datetime import date, datetime
from pathlib import Path

from . import storage


def slug(question: str, max_len: int = 50) -> str:
    """Lowercase, replace non-word with hyphen, trim."""
    s = question.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"[\s_]+", "-", s)
    s = s.strip("-")
    return s[:max_len].rstrip("-")


def decision_path(d: date, question: str) -> Path:
    return storage.data_root() / "decisions" / f"{d.isoformat()}-{slug(question)}.md"


def write_decision(
    d: date,
    question: str,
    polestar_quote: str,
    options: list[dict],
    recommendation: str,
    reasoning: str,
) -> Path:
    """Write a decision snapshot file. Returns the path."""
    lines = [
        f"# Decision — {d.isoformat()}",
        "",
        f"**Question:** {question}",
        "",
        "## Polestar",
        f"> {polestar_quote}",
        "",
        "## Options",
    ]
    for opt in options:
        lines.extend([
            f"### {opt['name']}",
            f"- **Pro (aligned):** {opt['pro']}",
            f"- **Con (misaligned):** {opt['con']}",
            "",
        ])
    lines.extend([
        "## Recommendation",
        f"Recommendation: {recommendation}",
        "",
        "## Reasoning",
        reasoning,
        "",
    ])
    rel = f"decisions/{d.isoformat()}-{slug(question)}.md"
    storage.write_text(rel, "\n".join(lines) + "\n")
    return storage.data_root() / rel


def list_decisions() -> list[Path]:
    """Return all decision files, newest first."""
    decisions_dir = storage.data_root() / "decisions"
    if not decisions_dir.exists():
        return []
    return sorted(decisions_dir.glob("*.md"), reverse=True)


def append_outcome(path: Path, outcome_text: str) -> None:
    """Append [outcome]...[/outcome] block to a decision file."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    block = f"\n## Outcome\n[outcome] {ts}\n{outcome_text.strip()}\n[/outcome]\n"
    with path.open("a", encoding="utf-8") as f:
        f.write(block)
