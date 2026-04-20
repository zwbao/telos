---
name: checking-in-weekly
description: Use on Sunday evening, OR when reflecting-on-day detects 7+ days since last weekly checkin. Captures the week's meaning score + one-sentence reason.
---

# Checking In Weekly

Ask exactly two questions, capture the answer, mirror to two files.

## Ask

1. **"1-10，这周感觉多有意义？"** (1-10, how meaningful did this week feel?)
2. **"一句话为什么？"** (One sentence why.)

## Write

1. Append `[weekly]` block to today's journal via `lib/journal.py::append_block(today, "weekly", f"{score}/10 — {reason}")`.
2. Append one line to `~/.claude/telos/weekly.md` (via `lib/storage.py::append_text`):
   ```
   2026-04-20 | 7/10 | 推进了三个事，但 Q4 焦虑仍在。
   ```

## Hand-off

If last 3 weekly scores are all ≤ 3: this is a drift signal. In V0, just note it to the user verbally. (V1 will invoke `observing-drift` here automatically.)

## Red Flags

| Thought | Reality |
|---|---|
| "Let me analyze what happened this week" | That's `analyzing-observations` (V1). Here, just capture score + sentence. |
| "Score feels arbitrary" | It is. And it becomes meaningful in aggregate. Don't refuse to ask. |
| "Give a motivational reframe if score is low" | No. Low scores are data. Let them be data. |
