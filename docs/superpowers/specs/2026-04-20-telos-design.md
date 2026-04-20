# Telos: Life Auto-Navigation Claude Code Plugin

**Status:** Draft for user review
**Date:** 2026-04-20
**Author:** zwbao + Claude

## 1. Goal

Build `telos` — a Claude Code plugin that turns CC into a "life autopilot." Give the user a 北极星 (telos), morning brief, on-demand decision support, and passive observation of CC session activity that keeps the system honest about what the user is actually doing.

Ship a working V0 the founder can self-run for ≥ 2 weeks before any distribution thought.

## 2. Why "telos"

Greek τέλος = the end-goal a thing inherently aims at (Aristotle). It names what the autopilot needs to function: a destination. The product takes a stand — meaning is not "discovered" through aimless drift; it is **declared** (or LLM-extracted from your own words), then executed against.

## 3. Non-Goals (V0)

- ❌ Distribution / publishing to CC plugin marketplace
- ❌ Multi-user data aggregation / anonymized upload
- ❌ Web / mobile companion
- ❌ Real interruption — hooks **inject context only, never block**
- ❌ Encryption beyond filesystem perms
- ❌ 八字 / 紫微 algorithm implementation — LLM textual interpretation of user-provided命盘 only
- ❌ Sentiment analysis pipeline — raw observation logs only; analyze later
- ❌ Calendar / email / task integrations — local files only

## 4. Architecture

### 4.1 Repository Layout

A standalone git repo at `/Users/baozhiwei/telos/`, structured as a Claude Code plugin (modeled on https://github.com/obra/superpowers — exact `plugin.json` / hook manifest may be tweaked during implementation to match upstream conventions).

```
telos/
├── README.md
├── LICENSE                            # MIT
├── plugin.json                        # CC plugin manifest (skills + commands + hooks)
├── skills/
│   └── telos/
│       └── SKILL.md                   # Dialog kernel: router + 4 mode prompts
├── commands/
│   └── telos.md                       # /telos slash command → invokes the skill
├── hooks/
│   ├── session_start.py               # Inject 北极星 paragraph into CC session
│   ├── user_prompt_submit.py          # Silent alignment hint on decision-shaped prompts
│   └── stop.py                        # Append session summary to today's journal
├── lib/
│   ├── __init__.py
│   ├── storage.py                     # ~/.claude/telos/ I/O primitives
│   ├── profile.py                     # 北极星 spec read/write
│   ├── journal.py                     # Daily journal append
│   └── observations.py                # JSONL experiment logger
├── tests/
│   ├── test_storage.py
│   ├── test_profile.py
│   ├── test_journal.py
│   ├── test_observations.py
│   └── test_hooks.py                  # Hooks tested via subprocess + golden stdout
└── docs/
    └── superpowers/
        ├── specs/2026-04-20-telos-design.md   # this file
        └── plans/2026-04-20-telos-mvp.md      # written next
```

**Code lives in repo. User data lives in `~/.claude/telos/`.** This separation makes the plugin portable and the data the user's life-property.

### 4.2 Component Responsibilities

#### `skills/telos/SKILL.md` — dialog kernel

Single entrypoint via `/telos [optional free text]`. Internal router decides which mode to enter based on state:

| Trigger | Mode | Behavior |
|---|---|---|
| `~/.claude/telos/profile.md` missing | **Onboarding (D)** | Conversational intake: 生辰八字 (optional), MBTI / 人类图 (optional), 5 core values, one sentence "if my life works out, what does it look like in 10 years". LLM synthesizes a ≤ 300-char "北极星 paragraph" + structured profile body; writes `profile.md`. |
| `/telos` no args + today's journal lacks `[brief]` section | **Morning brief (A)** | Reads profile + last 3 journal entries + today's date. Outputs: 3 things to do today, 2 to skip, 1 unexpected suggestion — all framed by the 北极星. Writes `[brief]` block into today's journal. |
| `/telos "<question>"` matches decision keywords (要不要 / 该不该 / 选 / should / vs) | **Decision support (B)** | Frames options through 北极星 lens, gives ranked recommendation + reasoning. Writes `decisions/YYYY-MM-DD-<topic>.md`. |
| `/telos` no args + today's brief already exists | **Reflection** | "What aligned today? What didn't? One thing to carry forward." Appends `[reflect]` block to today's journal. |

The router itself is a ~50-line prompt section at the top of SKILL.md.

#### `hooks/session_start.py`

- Read `~/.claude/telos/profile.md` (skip silently if missing — first-time users)
- Extract the 北极星 paragraph (the section between `## 北极星` and the next `##`)
- Output to stdout:
  ```json
  {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "用户的北极星: <paragraph>"}}
  ```
- Log to observations: `{mode: "hook_session_start", profile_present: bool}`

#### `hooks/user_prompt_submit.py`

- For prompts where `len(prompt) > 80` OR matching decision regex (`要不要|该不该|选哪|应不应该|should I|vs `)
- Append context (NOT block):
  ```json
  {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "提示：用户的北极星是 <paragraph>。这个 prompt 与北极星的关系，可以提一下。"}}
  ```
- Never blocks. Main LLM decides whether to mention alignment.
- Log: `{mode: "hook_prompt_submit", matched: bool, prompt_len: N}`

#### `hooks/stop.py`

- On session stop: take last 3 user/assistant exchanges (truncate to ~2k chars total)
- For V0: heuristic summary (first user prompt + last assistant final paragraph, truncated to 300 chars). LLM-call summarization deferred to V1.
- Append to `~/.claude/telos/journal/YYYY-MM-DD.md` under a `[session]` block with timestamp
- Log: `{mode: "hook_stop", chars_logged: N}`

#### `lib/storage.py`

Pure file I/O. No business logic.

```python
def data_root() -> Path                   # ~/.claude/telos/, mkdir if missing
def read_text(rel_path) -> str | None     # safe read, None if missing
def write_text(rel_path, content)         # mkdir parent, write atomically
def append_text(rel_path, content)        # append, mkdir parent
```

#### `lib/profile.py`

```python
def profile_path() -> Path                # data_root() / "profile.md"
def read_profile() -> dict | None         # parse markdown sections to dict
def write_profile(profile_dict)           # serialize to markdown
def polestar(profile_dict) -> str         # extract 北极星 paragraph
```

#### `lib/journal.py`

```python
def journal_path(date) -> Path            # data_root() / "journal" / f"{date}.md"
def append_block(date, block_type, body)  # block_type: "brief" | "session" | "reflect" | "manual"
def has_block(date, block_type) -> bool   # used by router to decide mode
def recent_journals(n=3) -> list[str]     # last n days, newest first
```

#### `lib/observations.py`

```python
def log(event_dict)                       # append JSONL to data_root()/observations.jsonl
                                          # auto-add ts; never raises (best-effort)
```

### 4.3 Data Storage Layout (`~/.claude/telos/`)

```
~/.claude/telos/
├── profile.md                 # 北极星 + 命盘 + 5 values + 10-year vision
├── journal/
│   └── YYYY-MM-DD.md          # Append-only blocks: [brief], [session]*, [reflect], [manual]*
├── decisions/
│   └── YYYY-MM-DD-<slug>.md   # Decision snapshots from B-mode
└── observations.jsonl         # Experiment event stream
```

`profile.md` template:
```markdown
# Profile

## 北极星
<≤ 300 char paragraph synthesized at onboarding; the load-bearing thing>

## 命盘 (optional)
<生辰八字 / MBTI / 人类图 raw text, if user provided>

## 五个核心价值
1. ...
2. ...
...

## 十年图景
<one-paragraph vision the user wrote at onboarding>

## 调整历史
<append-only log of profile updates>
```

### 4.4 Hook Configuration

`plugin.json` registers all three hooks against `*` matcher:
```json
{
  "name": "telos",
  "version": "0.1.0",
  "hooks": {
    "SessionStart": [{"matcher": "*", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/session_start.py"}],
    "UserPromptSubmit": [{"matcher": "*", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/user_prompt_submit.py"}],
    "Stop": [{"matcher": "*", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/stop.py"}]
  }
}
```

(Exact field names follow CC plugin docs — may differ slightly; resolved during implementation.)

## 5. Social Experiment Instrumentation

- **Every interaction → `observations.jsonl`** with `{ts, mode, ...meta}`. No PII, no prompt content. Counts and lengths only.
- **Weekly self-report**: each Sunday brief appends a soft question — "1-10, did this week feel meaningful? One sentence why." User's reply goes into `journal`.
- **No outcome variable predetermined.** Accumulate raw data; analyze whenever there's enough to look at. Per user direction: don't constrain the experiment with hypotheses upfront.
- **All data local.** Filesystem perms only; opt-in upload deferred indefinitely.

## 6. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| SessionStart prompt bloat | Inject ≤ 500 chars (just 北极星 paragraph), never the full profile |
| Stop hook latency annoys user | V0 uses heuristic summary, no LLM call; latency < 50ms |
| Alignment nudge feels paternalistic | Silent context injection, never blocks; user can disable hook in `plugin.json` |
| 北极星 calcifies | `profile.md` is plain text + onboarding can re-run anytime + every change logged in `调整历史` |
| Hooks crash break CC | All hooks wrap main logic in try/except, fail open (empty stdout), log error to `observations.jsonl` with `error` field |
| User confused which mode is active | Each mode's first line of output names itself: "🌅 早间 brief", "🤔 决策代理", etc. |

## 7. V0 Acceptance Criteria

A V0 release passes if all of these are true:

1. User runs `/telos` first time → onboarding completes → `profile.md` exists with a non-empty `## 北极星` section
2. Next morning, `/telos` returns a brief that demonstrably references the 北极星 (manual eyeball check)
3. User runs `/telos "应该接 X offer 吗"` → gets structured analysis tied to 北极星 + decision file written to `decisions/`
4. After a CC session unrelated to telos, `journal/YYYY-MM-DD.md` has an auto-appended `[session]` block (proves Stop hook works)
5. `observations.jsonl` accumulates ≥ 4 distinct event types after a day of normal use
6. Founder runs telos for 2 weeks; journal has daily entries; founder can self-assess "is this useful to me"
7. All `lib/*` modules have ≥ 80% line coverage from `tests/`
8. Hooks tested via subprocess invocation with golden stdout

## 8. Locked Defaults (override anytime)

These were not explicitly confirmed but proceeded with as defaults:

- ⚙️ Hook behavior: silent context injection, no real blocking
- ⚙️ 命理: LLM textual interpretation only, no algorithm
- ⚙️ Instrumentation granularity: ts/mode/lengths + weekly meaning question; no per-decision adoption tracking (yet)
- ⚙️ Single-user (founder) for V0; no marketplace publish
- ⚙️ Heuristic Stop summary for V0; LLM-summary deferred
- ⚙️ MIT license

## 9. Out of Scope (named so they don't sneak in)

Distribution mechanics, social sharing, gamification, streak tracking, voice input, mobile app, integration with calendar/email/Slack, multi-language UI (Chinese-first, English second-class), payment, accounts, cloud sync, plugin marketplace listing.

---

**Next step:** user reviews this spec. If approved, proceed to write `docs/superpowers/plans/2026-04-20-telos-mvp.md` (TDD-style task-by-task plan with file paths, code, commits).
