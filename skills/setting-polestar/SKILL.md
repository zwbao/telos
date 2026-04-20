---
name: setting-polestar
description: Use when ~/.claude/telos/profile.md is missing, or when user runs /telos-setup, or when user expresses "I don't know what I'm doing with my life." Conducts structured intake and synthesizes the polestar paragraph.
---

# Setting Polestar

Bootstrap the user's telos through a guided interview, then synthesize a ≤ 300-char polestar paragraph and write `~/.claude/telos/profile.md`.

## The Intake (in order — do not skip)

Ask ONE question at a time. Wait for answer. Then next.

1. **Birth info (optional)**: "如果你愿意，告诉我你的生辰八字 / 出生日期时间。不愿意跳过。"
2. **Personality frame (optional)**: "MBTI / 人类图 / 星座，知道哪个说哪个。都没有跳过。"
3. **Five core values**: "不加解释，写下对你最重要的 5 个词。例：诚实、好奇、自由、责任、美。"
4. **10-year vision**: "如果十年后人生顺遂，一段话描述那个场景——你在哪里、做什么、和谁在一起、感觉如何。"
5. **Existential sore-spot**: "当前最卡住你的一个问题，不管是关于工作、关系、身份、还是意义。一句话。"

## Synthesis (after intake complete)

Compose a polestar paragraph ≤ 300 chars that:
- Names the load-bearing direction (from vision + values)
- Is written in second person ("你...")
- Acknowledges the sore-spot as the journey, not the destination
- Does NOT promise outcomes (no "you will achieve X")

Example:
> "你在用自己的手做一件会比你更长久的事。价值以诚实和好奇为轴——不是因为它们正确，而是因为它们是你。当下的卡点（X）不是要解决的 bug，是这条路本身的弯。"

## Write to File

Invoke `lib/profile.py::write_profile` with dict:
```
{
  "北极星": "<synthesized paragraph>",
  "命盘": "<raw intake from Q1 + Q2>",
  "五个核心价值": "1. X\n2. Y\n...",
  "十年图景": "<raw from Q4>",
  "调整历史": "",
}
```

## Hand-off

After `profile.md` is written, immediately invoke `briefing-daily` for the first brief.

## Red Flags

| Thought | Reality |
|---|---|
| "User seems unsure, let me shorten the intake" | The intake IS the point. Don't skip. |
| "I'll synthesize the polestar without showing my reasoning" | Show the user the synthesized paragraph and ask 'does this ring true?' before writing. |
| "Let me add a 'goals' section too" | YAGNI. Values + vision cover it. Goals are for `briefing-daily`. |
