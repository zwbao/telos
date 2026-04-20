# Scenario: Sunday Weekly Check-In

**Precondition:**
- `~/.claude/telos/profile.md` exists.
- Today is Sunday.
- This week's journal files have no `[weekly]` block.

**User types:** `/telos`

**Expected Claude behavior:**

1. `/telos` smart router detects: profile exists, today is Sunday, no weekly block this week. Routes to `checking-in-weekly`.
2. Claude asks Q1: "1-10，这周感觉多有意义？"
3. User answers with a number.
4. Claude asks Q2: "一句话为什么？"
5. User answers with one sentence.
6. Claude writes to TWO locations:
   a. `~/.claude/telos/journal/<sunday>.md` appends `[weekly]` block via `lib/journal.py::append_block(..., "weekly", body)`.
   b. `~/.claude/telos/weekly.md` appends one line: `YYYY-MM-DD | score/10 | reason`.

**Post-conditions:**
- Today's journal has a `[weekly]` block.
- `~/.claude/telos/weekly.md` has one more line than before.

**Manual verification:**
```bash
grep '\[weekly\]' ~/.claude/telos/journal/$(date +%Y-%m-%d).md
tail -1 ~/.claude/telos/weekly.md
```

**Drift signal (informational, not automated in V0):**
If last 3 lines of `weekly.md` all have scores ≤ 3/10, Claude should mention it verbally: "看起来连续三周都在 3 分以下，可能需要 /telos-setup 重校准。"
