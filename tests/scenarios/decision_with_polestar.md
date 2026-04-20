# Scenario: Decision With Polestar

**Precondition:** `~/.claude/telos/profile.md` exists with a non-empty 北极星 section.

**User types:** `/telos 我应不应该接这个外部顾问的 offer？薪水是当前的 1.5 倍但会挤占主业时间。`

**Expected Claude behavior:**

1. UserPromptSubmit hook detects decision language (`应不应该`), injects polestar context.
2. `using-telos` routes to `deciding-with-telos` (HARD-GATE).
3. Claude executes the four-step gate **in order**:
   a. Quotes polestar paragraph verbatim in a blockquote.
   b. Restates decision in one sentence.
   c. Enumerates ≥ 2 options with aligned pro / misaligned con for each.
   d. Gives recommendation with reasoning traceable to polestar values.
4. Writes snapshot to `~/.claude/telos/decisions/YYYY-MM-DD-<slug>.md` via `lib/decisions.py::write_decision`.
5. Reminds user: "when the outcome is known, run `/telos` and I'll append it."

**Failure modes to watch for:**
- Claude gives the recommendation BEFORE quoting polestar → HARD-GATE violation, skill broken.
- Claude paraphrases polestar → violation, must quote verbatim.
- Claude only lists one option → violation, must enumerate ≥ 2.

**Post-conditions:**
- New file in `~/.claude/telos/decisions/` with today's date.
- File contains polestar quote, options, recommendation.
- `observations.jsonl` has entries for hook_prompt_submit with `is_decision: true`.

**Manual verification:**
```bash
ls ~/.claude/telos/decisions/
cat ~/.claude/telos/decisions/$(ls -t ~/.claude/telos/decisions/ | head -1)
grep '"is_decision": true' ~/.claude/telos/observations.jsonl | tail -1
```
