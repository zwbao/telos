---
name: deciding-with-telos
description: Use when user prompt contains decision language (要不要 / 该不该 / 应不应该 / 选哪 / should I / vs / 哪个更) OR when user invokes /telos with a question. HARD-GATE skill — do not output a recommendation without completing the four required steps.
---

# Deciding With Telos

<HARD-GATE>
DO NOT output a decision recommendation until you have:
1. Read and quoted the polestar paragraph verbatim (from `profile.md`) in a blockquote
2. Restated the decision as a single sentence
3. Enumerated ≥ 2 options, each with:
   - Pro aligned with polestar (one sentence)
   - Con misaligned with polestar (one sentence)
4. Given a recommendation with reasoning traceable to specific polestar values
</HARD-GATE>

After all four, write the decision snapshot to `~/.claude/telos/decisions/YYYY-MM-DD-<slug>.md` via `lib/decisions.py::write_decision`.

## Output Format

```
🤔 deciding-with-telos

**Polestar**:
> <verbatim paragraph>

**Decision restated**: <one sentence>

**Options**:
- **A**: <name>
  - Aligned: <sentence>
  - Misaligned: <sentence>
- **B**: <name>
  - Aligned: <sentence>
  - Misaligned: <sentence>

**Recommendation**: <option>
**Reasoning**: <traceable to polestar values>
```

## Write the snapshot

Call `lib/decisions.py::write_decision(d=today, question=..., polestar_quote=..., options=[{name, pro, con}], recommendation=..., reasoning=...)`.

## Hand-off

Remind user: "When the outcome is known, run `/telos` and I'll append it to this decision file."

## Red Flags

| Thought | Reality |
|---|---|
| "This is low-stakes, skip the polestar step" | The discipline is practiced on small decisions so it's available on big ones. |
| "Polestar is long, paraphrase it" | NO. Quote verbatim. Paraphrase smuggles in your own interpretation. |
| "User is impatient, give the recommendation first" | No. The structure IS the value. If user wants fast answers, they can ask a different AI. |
| "One option is obviously better, no need to list both" | List both anyway. The enumeration surfaces the polestar-tradeoffs explicitly. |
