# telos

> *τέλος* — the end-goal a thing inherently aims at (Aristotle)

A Claude Code plugin that turns CC into a life autopilot: declare your telos, consult it at decision points, log life against it, measure meaning weekly.

**Not a todo app.** Not a journaling tool. A **methodology** that enforces the practice of navigating life against a declared direction.

## Install

Clone this repo into your Claude Code plugins directory or install via marketplace (V1):

```bash
git clone https://github.com/zwbao/telos ~/.claude/plugins/telos
```

Then in Claude Code:

```
/plugin install telos
```

(Exact install command may evolve with CC plugin system — check CC docs.)

## First run

```
/telos
```

First time: guided polestar intake (≈ 10 minutes).
Thereafter: smart router that gives you a morning brief, decision support, or evening reflection based on state.

## The practice

1. **Declare** — `setting-polestar` synthesizes a ≤ 300-char polestar from your intake
2. **Consult** — `deciding-with-telos` forces you to quote the polestar before any decision
3. **Log** — `Stop` hook auto-appends every CC session's summary to today's journal
4. **Measure** — Sunday `checking-in-weekly` captures a 1-10 meaning score
5. **Recalibrate** — (V1) `recalibrating-telos` handles major life shifts

## What it does not do

- Give motivational advice
- Track streaks or gamify anything
- Sync to cloud
- Mine your journal for AI training
- Replace therapy or a life coach

## What's in the plugin

- **10 skills** (V0 ships 6; V1 adds 4 analysis skills)
- **3 hooks** — inject polestar on session start, alignment hint on decision prompts, session summary on stop
- **3 slash commands** — `/telos` router, `/telos-setup`, `/telos-review` (V1)
- **1 subagent** — `telos-analyst` (V1)
- Your data lives in `~/.claude/telos/`, never leaves your machine

## Read before you install

- [docs/methodology.md](docs/methodology.md) — the life-navigation method
- [docs/experiment.md](docs/experiment.md) — the social experiment frame

## License

MIT. See LICENSE.

## Credits

Product philosophy adapted from [obra/superpowers](https://github.com/obra/superpowers).
