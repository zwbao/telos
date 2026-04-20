---
name: briefing-daily
description: Use on first /telos of the day, when today's journal has no [brief] block yet, or when a session starts after 6am with no brief. Produces the morning brief that frames the day through the polestar.
---

# Briefing Daily

Produce today's brief. Every brief MUST: (a) restate the polestar in one line, (b) self-score yesterday's alignment 1-5, (c) give 3 to do, 2 to avoid, 1 surprise, all framed by the polestar.

## Read

1. `~/.claude/telos/profile.md` — get polestar
2. `~/.claude/telos/journal/YYYY-MM-DD.md` for last 3 days — get recent entries
3. Today's date + day-of-week

## Output Format

Write to today's journal as `[brief]` block AND echo to user:

```
🌅 早间 brief — 2026-04-20

**北极星**: <one-line restatement>

**昨日对齐**: X/5 — <one sentence assessment>

**今日做 (3)**:
1. <item, ≤ 15 字> — 为什么对齐: <6 字>
2. ...
3. ...

**今日避 (2)**:
1. <item> — 为什么不对齐: <6 字>
2. ...

**今日惊喜 (1)**:
<an unusual suggestion — ≤ 30 字 — still aligned but outside the obvious ruts>
```

## Write

Call `lib/journal.py::append_block(today, "brief", body)`.

## Hand-off

Return control to user. Next decision-shaped prompt will trigger `deciding-with-telos`.

## Red Flags

| Thought | Reality |
|---|---|
| "User wants generic productivity tips" | If the brief could be for anyone, it's a failure. Every item must cite the polestar. |
| "Yesterday had nothing notable, skip the score" | Score anyway. The ritual is the point. |
| "Surprise must be fun/creative" | Surprise means *outside the usual ruts*, not amusement. 'Call your estranged sister' counts. |
| "Let me ask user what they want to do today" | The brief proposes; user pushes back if wrong. Don't make user do the proposing work. |
