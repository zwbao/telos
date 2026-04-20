# Scenario: Onboarding First Run

**Precondition:** `~/.claude/telos/profile.md` does not exist.

**User types:** `/telos`

**Expected Claude behavior:**

1. `using-telos` auto-triggers. Detects missing profile. Hands off to `setting-polestar`.
2. `setting-polestar` asks Q1: birth info (optional).
3. User answers (or skips).
4. Q2: MBTI / 人类图 / 星座 (optional). User answers.
5. Q3: 5 core values, no explanation. User answers.
6. Q4: 10-year vision, one paragraph. User answers.
7. Q5: one existential sore-spot, one sentence. User answers.
8. Claude synthesizes a ≤ 300-char polestar paragraph. Shows it to user. Asks: "does this ring true?"
9. If user accepts: writes `~/.claude/telos/profile.md` via `lib/profile.py::write_profile`.
10. Hands off to `briefing-daily` for immediate first brief.

**Post-conditions:**
- `~/.claude/telos/profile.md` exists with all 5 sections populated.
- `~/.claude/telos/journal/<today>.md` exists with a `[brief]` block.
- `~/.claude/telos/observations.jsonl` has entries for hook_session_start and any skill invocations.

**Manual verification commands:**
```bash
cat ~/.claude/telos/profile.md | head -30
cat ~/.claude/telos/journal/$(date +%Y-%m-%d).md
wc -l ~/.claude/telos/observations.jsonl
```
