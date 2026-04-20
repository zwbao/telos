---
description: Smart router for telos — routes to onboarding, morning brief, decision, or reflection based on state.
---

# /telos

User input: $ARGUMENTS

Route based on state:

1. If `~/.claude/telos/profile.md` does NOT exist → invoke `setting-polestar` skill.
2. Else if input matches decision regex (要不要 / 该不该 / 应不应该 / 选哪 / should I / vs / 哪个更) OR input ends with `?` / `？` → invoke `deciding-with-telos` skill.
3. Else if today's journal has no `[brief]` block → invoke `briefing-daily` skill.
4. Else if today's journal has `[brief]` but no `[reflect]` → invoke `reflecting-on-day` skill.
5. Else if today is Sunday and this week has no `[weekly]` block → invoke `checking-in-weekly` skill.
6. Else → conversational mode guided by `using-telos`.

State check via:
- `bash: test -f ~/.claude/telos/profile.md`
- `bash: grep -l "\[brief\]" ~/.claude/telos/journal/$(date +%Y-%m-%d).md 2>/dev/null`
- `bash: grep -l "\[reflect\]" ~/.claude/telos/journal/$(date +%Y-%m-%d).md 2>/dev/null`
- `bash: grep -l "\[weekly\]" ~/.claude/telos/journal/$(date +%Y-%m-%d).md 2>/dev/null`
- `bash: date +%u` (7 = Sunday)

Do the state checks first, then invoke the single most-specific matching skill.
