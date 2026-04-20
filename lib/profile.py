"""Profile (polestar + 命盘 + values + vision + 调整历史) read/write."""

import re
from datetime import datetime

from . import storage

PROFILE_PATH = "profile.md"
SECTIONS = ["北极星", "命盘", "五个核心价值", "十年图景", "调整历史"]


def read_profile() -> dict | None:
    """Parse profile.md into {section: body}. Return None if missing."""
    raw = storage.read_text(PROFILE_PATH)
    if raw is None:
        return None
    result = {s: "" for s in SECTIONS}
    parts = re.split(r"^## (.+)$", raw, flags=re.MULTILINE)
    # parts = [preamble, header1, body1, header2, body2, ...]
    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        if header in result:
            result[header] = body
    return result


def write_profile(data: dict) -> None:
    """Serialize profile dict to markdown and write."""
    lines = ["# Profile", ""]
    for section in SECTIONS:
        lines.append(f"## {section}")
        body = data.get(section, "").strip()
        if body:
            lines.append(body)
        lines.append("")
    storage.write_text(PROFILE_PATH, "\n".join(lines) + "\n")


def polestar(profile_dict: dict | None) -> str:
    """Extract the 北极星 paragraph, or empty string."""
    if profile_dict is None:
        return ""
    return profile_dict.get("北极星", "").strip()


def append_调整历史(reason: str, old_polestar: str, new_polestar: str) -> None:
    """Append an entry to 调整历史 section, then rewrite polestar."""
    data = read_profile()
    if data is None:
        raise FileNotFoundError("profile.md does not exist")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"- {ts}: {reason}\n  {old_polestar} → {new_polestar}"
    existing = data.get("调整历史", "").strip()
    data["调整历史"] = (existing + "\n" + entry).strip() if existing else entry
    data["北极星"] = new_polestar
    write_profile(data)
