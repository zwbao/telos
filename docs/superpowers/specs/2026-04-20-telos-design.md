# Telos: Life Auto-Navigation Claude Code Plugin

**Status:** Draft v2 for user review
**Date:** 2026-04-20
**Author:** zwbao + Claude
**Reference:** obra/superpowers (structure + product philosophy)

## 1. Goal

Build `telos` — a Claude Code plugin that functions as a **life-navigation methodology**, not a life-management tool. It gives the user a persistent 北极星 (telos), enforces the discipline of consulting that telos before decisions, logs what actually happened, and surfaces drift when it appears.

Ship V0 that the founder can self-run for ≥ 2 weeks with enough instrumentation + reflection surface to decide "is this useful to me."

## 2. Why "telos"

Greek τέλος = the end-goal a thing inherently aims at (Aristotle). It names what the autopilot needs to function: a destination. The product takes a stand — meaning is not "discovered" through aimless drift; it is **declared** (or LLM-extracted from your own words), then executed against.

## 3. Product Philosophy (copied with adaptation from obra/superpowers)

Four design principles, load-bearing for everything below:

1. **Methodology > Features.** telos does not ship "a morning brief feature." It ships a **practice** — declare telos → consult telos at decision points → log what happened → measure meaning weekly → recalibrate when drift is severe. Skills exist to enforce that practice.

2. **Auto-trigger over command-memorization.** Users don't remember `/telos-decide`. Decisions just come up. Skills fire when their triggers match (decision-shaped prompt, morning session start, end-of-day, Sunday). Commands are for explicit override only.

3. **Hard-gates between stages.** Like superpowers' "no implementation before spec approved," telos has analogous gates:
   - **DO NOT give decision advice without first consulting the user's telos.** (enforced in `deciding-with-telos`)
   - **DO NOT begin the day's work without the morning brief noting whether yesterday aligned.** (enforced in `briefing-daily`)
   - **DO NOT claim insight from observations without the raw numbers.** (enforced in `analyzing-observations`)

4. **Skills hand off to each other.** `setting-polestar` → first `briefing-daily`. `deciding-with-telos` → logs to `reflecting-on-day`. `observing-drift` detects pattern → invokes `recalibrating-telos`. Like brainstorming→writing-plans→subagent-driven-development, the chain is mechanical.

## 4. Non-Goals (V0)

- ❌ Distribution / CC plugin marketplace publish
- ❌ Multi-user data aggregation / cloud sync
- ❌ Web / mobile companion
- ❌ Real interruption — hooks inject context, never block
- ❌ Encryption beyond filesystem perms
- ❌ 八字 / 紫微 algorithm — LLM textual interpretation of user-provided命盘 only
- ❌ Sentiment analysis / NLP on journals — raw text only
- ❌ Calendar / email / task integrations
- ❌ Gamification (streaks, badges, levels) — antithetical to the philosophy

## 5. Architecture

### 5.1 Repository Layout

Standalone git repo at `/Users/baozhiwei/telos/`, modeled on obra/superpowers:

```
telos/
├── README.md                               # Pitch + install + example transcript
├── CLAUDE.md                               # Plugin system instructions (auto-loaded)
├── LICENSE                                 # MIT
├── .claude-plugin/
│   ├── plugin.json                         # CC plugin manifest
│   └── marketplace.json                    # (V1) for future marketplace
├── skills/
│   ├── using-telos/SKILL.md                # Orientation — loaded at session start
│   ├── setting-polestar/SKILL.md           # Bootstrap (onboarding)
│   ├── recalibrating-telos/SKILL.md        # Major re-bootstrap
│   ├── briefing-daily/SKILL.md             # Morning rhythm
│   ├── deciding-with-telos/SKILL.md        # Decision discipline (hard-gate)
│   ├── reflecting-on-day/SKILL.md          # End-of-day reflection
│   ├── checking-in-weekly/SKILL.md         # Sunday meaning report
│   ├── observing-drift/SKILL.md            # Pattern-detected nudge
│   ├── analyzing-observations/SKILL.md     # Retrospective on jsonl log
│   └── reviewing-decisions/SKILL.md        # Retrospective on decision history
├── commands/
│   ├── telos.md                            # Smart router — main entry
│   ├── telos-setup.md                      # Explicit setting-polestar
│   └── telos-review.md                     # Deep review (chains analyzing + reviewing + reflecting)
├── agents/
│   └── telos-analyst.md                    # Subagent for deep analysis, protects main context
├── hooks/
│   ├── session_start.py                    # Inject polestar + activate using-telos
│   ├── user_prompt_submit.py               # Silent alignment hint on decision prompts
│   ├── stop.py                             # Append session summary to today's journal
│   └── hooks.json                          # Manifest
├── lib/
│   ├── __init__.py
│   ├── storage.py                          # ~/.claude/telos/ I/O primitives
│   ├── profile.py                          # Polestar spec read/write + parse
│   ├── journal.py                          # Daily journal append + block queries
│   ├── decisions.py                        # Decision snapshot read/write
│   ├── observations.py                     # JSONL experiment logger
│   └── drift.py                            # Drift detection heuristics
├── docs/
│   ├── methodology.md                      # The telos life-navigation method (whitepaper)
│   ├── experiment.md                       # Social experiment framing + data dictionary
│   └── superpowers/
│       ├── specs/2026-04-20-telos-design.md   # this file
│       └── plans/2026-04-20-telos-mvp.md      # written next
├── tests/
│   ├── test_storage.py
│   ├── test_profile.py
│   ├── test_journal.py
│   ├── test_decisions.py
│   ├── test_observations.py
│   ├── test_drift.py
│   ├── test_hooks.py                       # Subprocess-level stdout golden tests
│   └── scenarios/                          # Skill scenario transcripts (markdown fixtures)
│       ├── onboarding_first_run.md
│       ├── decision_with_polestar.md
│       └── weekly_checkin.md
└── scripts/
    └── bump_version.sh
```

**Code lives in repo. User life-data lives in `~/.claude/telos/`.** Always separable.

### 5.2 Skills (10 cognitive units)

Each SKILL.md has: frontmatter (`name`, `description` with trigger phrasing), the discipline it enforces, a hand-off clause to the next skill, and a red-flags table for rationalizing around it.

#### 5.2.1 `using-telos` — orientation
- **Trigger:** session start (via hook) OR any message mentioning life direction / drift / meaning / purpose.
- **Discipline:** "Before any life-relevant response, check `~/.claude/telos/profile.md`. If absent, invoke `setting-polestar`. If present, frame responses through the polestar."
- **Hand-off:** invokes `setting-polestar` when profile missing; invokes `deciding-with-telos` when decision language detected; invokes `reflecting-on-day` at end of session.
- **Red flags:** "this doesn't sound like a 'life' question" → most questions are downstream of direction. Default to consulting telos.

#### 5.2.2 `setting-polestar` — bootstrap
- **Trigger:** profile.md missing; user runs `/telos-setup`; user explicitly says "I need to figure out what I'm doing with my life."
- **Discipline:** structured interview (生辰 optional, MBTI/人类图 optional, 5 core values, one-sentence 10-year vision, one existential sore-spot). Synthesize ≤ 300-char polestar paragraph. Write profile.md with timestamp.
- **Hand-off:** on completion, invoke `briefing-daily` for immediate first brief.
- **Red flags:** "user seems unsure, let's shorten intake" → the intake IS the point; don't skip.

#### 5.2.3 `recalibrating-telos` — deep re-bootstrap
- **Trigger:** user says "my life changed" / "I don't recognize myself anymore"; OR `observing-drift` reports ≥ 4 consecutive weekly checkins below 4/10.
- **Discipline:** start from current profile, ask "what changed? what no longer fits?" for each profile section. Do NOT just overwrite — append to `调整历史` with reasoning, THEN rewrite polestar.
- **Hand-off:** invokes `briefing-daily` with a "fresh polestar" framing.
- **Red flags:** "user just had a bad day, let's recalibrate" → no. Transient bad days are for `reflecting-on-day`, not for tearing down the polestar.

#### 5.2.4 `briefing-daily` — morning rhythm
- **Trigger:** first `/telos` of the day OR no `[brief]` block in today's journal yet OR session starts after 6am with no brief.
- **Discipline:** read profile + last 3 days journal + today's date. Output must contain: (a) one-line restatement of polestar, (b) yesterday alignment score (self-perceived 1-5), (c) 3 to-do framed by polestar, (d) 2 to avoid, (e) 1 "surprise" (unusual suggestion aligned with polestar). Write `[brief]` block to today's journal.
- **Hand-off:** returns control to user; next decision prompt will trigger `deciding-with-telos`.
- **Red flags:** "user wants generic productivity tips" → every brief MUST cite the polestar. If it could be the same brief for anyone, it's a failure.

#### 5.2.5 `deciding-with-telos` — decision discipline **(HARD-GATE)**
- **Trigger:** prompt matches decision regex (要不要 / 该不该 / 选哪 / 应不应 / should I / which... / vs); OR user explicitly `/telos "<question>"`.
- **HARD-GATE:** DO NOT output a decision recommendation until you have:
  1. Read and quoted the polestar paragraph verbatim
  2. Restated the decision in one sentence
  3. Enumerated ≥ 2 options with 北极星-aligned pros and 北极星-misaligned cons for each
  4. Given a recommendation with reasoning traceable to polestar values
- **Output:** decision snapshot written to `decisions/YYYY-MM-DD-<slug>.md`.
- **Hand-off:** reminds user to come back and log the actual outcome via `reflecting-on-day`.
- **Red flags:** "this seems low-stakes, I'll skip the polestar check" → the discipline is practiced on small decisions so it's available for big ones.

#### 5.2.6 `reflecting-on-day` — end-of-day reflection
- **Trigger:** Stop hook at session end (when last session of day, heuristic: after 9pm or no further session within 2h); OR user runs `/telos` after today's brief exists.
- **Discipline:** Socratic three questions — "what aligned today?" / "what didn't?" / "one thing to carry forward." Append `[reflect]` block to today's journal. If prior decisions were logged today, ask if outcomes are known.
- **Hand-off:** if today is Sunday, chain into `checking-in-weekly`.
- **Red flags:** "user seems tired, keep it short" → the three questions are the whole discipline. Don't cut.

#### 5.2.7 `checking-in-weekly` — Sunday meaning report
- **Trigger:** Sunday evening; OR `reflecting-on-day` detects 7+ days since last weekly checkin.
- **Discipline:** ask "1-10 how meaningful did this week feel? one sentence why." Append `[weekly]` block to Sunday's journal, also mirror to `~/.claude/telos/weekly.md` (flat time-series).
- **Hand-off:** if score ≤ 3 for ≥ 3 weeks running, invoke `observing-drift`.
- **Red flags:** "let me analyze what happened this week" → that's `analyzing-observations`. Here, just capture the score + sentence. Fast.

#### 5.2.8 `observing-drift` — pattern-detected nudge
- **Trigger:** `analyzing-observations` reports: (a) ≥ 3 consecutive low weekly scores, OR (b) ≥ 5 decisions where `deciding-with-telos` flagged "option misaligned with polestar" as chosen.
- **Discipline:** surface the pattern as one paragraph + one question ("does the polestar still fit, or has the behavior drifted?"). Do NOT auto-recalibrate. Only nudge.
- **Hand-off:** user chooses to invoke `recalibrating-telos` or dismiss.
- **Red flags:** "we should just update the polestar" → changing the destination because you drove off-course is bad autopilot. Ask first.

#### 5.2.9 `analyzing-observations` — retrospective on log
- **Trigger:** `/telos-review`; OR automatic weekly (Sunday, before `checking-in-weekly`).
- **Discipline:** read `observations.jsonl` + weekly.md + decisions/. Compute: (a) brief-frequency, (b) decision-count + alignment rate, (c) drift signals (polestar-misaligned chosen options frequency), (d) weekly meaning trend. Output markdown report.
- **Output:** report goes to journal as `[analysis]` block + can be printed.
- **Red flags:** "let me pattern-match on journal text" → no. Only the structured fields (jsonl + weekly.md). Journal text is for the user, not the analyzer.

#### 5.2.10 `reviewing-decisions` — decision-history retrospective
- **Trigger:** `/telos-review`; OR quarterly auto-trigger.
- **Discipline:** walk through all decisions/YYYY-MM-DD-*.md. For each: ask user "known outcome?" Capture outcome into decision file. Summarize hit-rate.
- **Output:** appends hit-rate summary to each decision file's `[outcome]` block + aggregate report.

### 5.3 Slash Commands (3 — explicit override only)

| Command | Behavior |
|---|---|
| `/telos [optional text]` | **Smart router.** No-args: routes to onboarding / brief / reflection based on state. With decision-language text: invokes `deciding-with-telos`. With anything else: conversational using-telos context. |
| `/telos-setup` | Force `setting-polestar` even if profile.md exists (invokes `recalibrating-telos` if profile exists). |
| `/telos-review` | Deep review: invokes `analyzing-observations` → `reviewing-decisions` → `reflecting-on-day` in sequence, delegating heavy analysis to `telos-analyst` subagent. |

### 5.4 Subagent

**`telos-analyst`** — for deep retrospective analysis. Reads full `observations.jsonl` + `journal/**` + `decisions/**` + `weekly.md`, runs statistical summaries, returns a structured markdown report to the main session. Isolates heavy context from main chat. Modeled on obra/superpowers' `code-reviewer`.

### 5.5 Hooks (3)

| Hook | Behavior |
|---|---|
| `SessionStart` | Inject: (a) polestar paragraph (if profile exists), (b) "using-telos is active" reminder. Log `{mode: "hook_session_start", profile_present: bool}`. |
| `UserPromptSubmit` | If prompt length > 80 OR matches decision regex, inject context: "用户的北极星是 <...>. 若此 prompt 是决策，请遵守 `deciding-with-telos` 的 HARD-GATE." Never blocks. Log `{mode: "hook_prompt_submit", matched: bool, prompt_len: N}`. |
| `Stop` | Heuristic-summarize last 3 exchanges (300 char truncation). Append to today's journal as `[session]` block. Log `{mode: "hook_stop", chars_logged: N}`. |

All hooks wrap logic in try/except, fail open. Errors logged to observations with `error` field; never break CC.

### 5.6 Libraries (`lib/*`)

Pure functions, no business logic in business layer.

```
storage.py      — data_root(), read_text/write_text/append_text; atomic writes
profile.py      — profile_path(), read_profile() → dict, write_profile(dict), polestar(dict) → str, append_调整历史(reason, old, new)
journal.py      — journal_path(date), append_block(date, kind, body), has_block(date, kind), recent_journals(n)
decisions.py    — decision_path(date, slug), write_decision(snapshot), list_decisions(since?), append_outcome(file, text)
observations.py — log(event_dict) → append JSONL; read_since(ts) → list[dict]; fail-open
drift.py        — compute_alignment_stats(decisions, window), detect_weekly_drift(weekly_md), nudge_trigger(stats) → bool
```

### 5.7 Data Storage (`~/.claude/telos/`)

```
~/.claude/telos/
├── profile.md                 # Polestar + 命盘 + 5 values + 10-year vision + 调整历史
├── weekly.md                  # Flat time-series: one line per week, score + note
├── journal/
│   └── YYYY-MM-DD.md          # Append-only blocks: [brief], [session]*, [reflect], [weekly], [analysis], [manual]*
├── decisions/
│   └── YYYY-MM-DD-<slug>.md   # Polestar quote + options + recommendation + [outcome] (filled later)
└── observations.jsonl         # Experiment event stream
```

### 5.8 Plugin Manifest (`plugin.json`)

```json
{
  "name": "telos",
  "version": "0.1.0",
  "description": "Life auto-navigation methodology for Claude Code",
  "author": {"name": "zwbao", "email": "zwbao1996@gmail.com"},
  "homepage": "https://github.com/zwbao/telos",
  "license": "MIT",
  "keywords": ["life", "navigation", "methodology", "telos", "mindfulness", "decision-support"],
  "hooks": {
    "SessionStart": [{"matcher": "*", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/session_start.py"}],
    "UserPromptSubmit": [{"matcher": "*", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/user_prompt_submit.py"}],
    "Stop": [{"matcher": "*", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/stop.py"}]
  }
}
```

(Exact fields resolved during implementation against CC plugin docs.)

### 5.9 Top-Level `CLAUDE.md` (plugin instructions)

Loaded when plugin is active. Contains:
- One-paragraph pitch of the methodology
- The four design principles (from §3)
- A red-flags table: rationalizations that should trigger a skill invocation
- Skill trigger map: "when user says X → invoke Y"
- Data locations (profile / journal / decisions / observations)

Modeled on obra/superpowers' `CLAUDE.md` (which calls in `using-superpowers`).

## 6. Docs (`docs/*`)

### 6.1 `methodology.md` — the life-navigation whitepaper
- What is telos, why Aristotle
- The practice (declare → consult → log → measure → recalibrate)
- Analogy: life is autopilot-driving, not no-destination wandering
- Why AI makes this tractable now (persistent memory, daily availability)
- How this differs from journaling apps, life coaches, and meditation apps
- Honest limits (fatalism isn't required; LLM hallucination; the demographic this works for)

### 6.2 `experiment.md` — the social experiment framing
- Hypothesis (stated loosely, not prescriptive): "does externalizing a polestar + logging life against it change subjective meaning?"
- Data dictionary for `observations.jsonl` (every field, every enum value)
- Anonymization protocol (if ever aggregated later): drop journal text, keep counts + timestamps only
- Participant consent framework (for when distributed beyond founder)
- What we are NOT measuring: personality changes, productivity, income, relationships

## 7. Social Experiment Instrumentation

- `observations.jsonl` — `{ts, mode, ...meta}`. Every hook, every skill invocation, every decision.
- `weekly.md` — flat score time-series.
- `decisions/**` — structured decision snapshots with post-hoc outcomes.
- Journal — free text, private to user, never anonymized.
- **No predetermined outcome variable.** User's own weekly score is the closest thing; all else accumulated for later analysis.

## 8. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| SessionStart prompt bloat | ≤ 500 chars injected, polestar paragraph only |
| Stop hook latency | V0 heuristic summary (no LLM call); < 50ms |
| Alignment nudge feels paternalistic | Silent context injection only; `plugin.json` toggle |
| Polestar calcifies | `recalibrating-telos` available; `调整历史` preserves audit |
| Hook crash breaks CC | Try/except wrap + fail open + log error |
| Mode confusion | Every skill's first line names itself: "🌅 briefing-daily" etc. |
| User treats telos as oracle | `methodology.md` is explicit: telos is a lens, not a truth-teller |
| Skill over-invocation (too noisy) | `observing-drift` + `analyzing-observations` rate-limited to weekly |

## 9. V0 vs V1 Scope Split

### V0 (founder 2-week self-trial)
- Skills: `using-telos`, `setting-polestar`, `briefing-daily`, `deciding-with-telos`, `reflecting-on-day`, `checking-in-weekly`
- Commands: `/telos`, `/telos-setup`
- Hooks: all 3
- Libraries: `storage`, `profile`, `journal`, `decisions`, `observations`
- Docs: `CLAUDE.md`, `methodology.md`, `experiment.md`, `README.md`
- Tests: lib + hooks + 3 scenario transcripts

### V1 (after self-trial — needs accumulated data)
- Skills: `recalibrating-telos`, `observing-drift`, `analyzing-observations`, `reviewing-decisions`
- Command: `/telos-review`
- Subagent: `telos-analyst`
- Library: `drift`
- Tests: drift + analyzer scenario transcripts

## 10. V0 Acceptance Criteria

1. User runs `/telos` for the first time → `setting-polestar` fires → conversational intake completes → `profile.md` exists with non-empty `## 北极星`
2. Next morning's first `/telos` → `briefing-daily` returns 3-2-1 brief quoting the polestar verbatim; `[brief]` block appended to today's journal
3. User runs `/telos "应该接 X offer 吗"` → `deciding-with-telos` HARD-GATE enforced (polestar quoted, options enumerated, recommendation traceable) → decision file created
4. At session end, `hooks/stop.py` appends `[session]` block to today's journal (auto)
5. Any message mentioning "meaning / purpose / drift" in an unrelated CC session → `using-telos` surfaces polestar context (via SessionStart injection)
6. Sunday evening run → `checking-in-weekly` prompts 1-10 + sentence → score stored in `weekly.md`
7. `observations.jsonl` accumulates ≥ 6 distinct event types after 1 week of use
8. 2 weeks: founder reviews journal/weekly.md, self-reports "is this useful"
9. All V0 `lib/*` modules ≥ 80% line coverage
10. All V0 hooks tested via subprocess (stdin fixture → golden stdout)
11. 3 scenario transcripts pass as skill-level integration tests

## 11. Locked Defaults (override anytime)

- Plugin name: `telos`
- Hook policy: silent context injection, never blocking
- 命理: LLM textual interpretation only
- Instrumentation: ts/mode/lengths + weekly score; no PII, no prompt content
- Single-user (founder) for V0
- Heuristic Stop summary for V0; LLM summary deferred
- MIT license
- Chinese-first UI text, English secondary

## 12. Explicitly Out of Scope

Distribution mechanics, marketplace listing, social sharing, gamification, voice, mobile, calendar/email/Slack integration, payment, accounts, cloud sync, team/multi-user, LLM fine-tuning, web companion, public experiment aggregation.

---

**Next step:** user reviews this spec. If approved, proceed to `docs/superpowers/plans/2026-04-20-telos-mvp.md` with TDD task breakdown for V0 (V1 deferred to a second plan after self-trial).
