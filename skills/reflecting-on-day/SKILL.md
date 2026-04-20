---
name: reflecting-on-day
description: Use at session end via Stop hook (when last session of day — heuristic: after 9pm or no further session within 2h), OR when user runs /telos after today's brief already exists. Socratic three-question reflection that closes the day's loop.
---

# Reflecting On Day

Ask three questions, one at a time. Capture answers. Append to today's journal as `[reflect]` block.

## The Three Questions

1. **"今天什么对齐了？"** (What aligned today with the polestar?)
2. **"今天什么没对齐？"** (What didn't?)
3. **"明天想带走一件什么事？"** (One thing to carry forward.)

Wait for each answer before asking the next.

## Additional: decision outcome check

If `~/.claude/telos/decisions/YYYY-MM-DD-*.md` exists for today, ask: "今天做的决定（<slug>），有结果了吗？" If yes, invoke `lib/decisions.py::append_outcome(path, outcome_text)`.

## Write

Call `lib/journal.py::append_block(today, "reflect", body)` with all three answers.

## Hand-off

- If today is Sunday: chain into `checking-in-weekly`.
- Else: return control.

## Red Flags

| Thought | Reality |
|---|---|
| "User is tired, shorten to one question" | Three IS the discipline. Don't cut. |
| "Generate the answers yourself from journal" | No. Answers are user-owned. You only ask. |
| "Wrap it up with motivational advice" | No motivational anything. The Socratic ask is enough. |
