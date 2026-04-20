---
description: Force setting-polestar even if a profile already exists. Used for re-bootstrapping after major life changes.
---

# /telos-setup

User input: $ARGUMENTS

Check: does `~/.claude/telos/profile.md` exist?

- **No** → invoke `setting-polestar` skill (first-time bootstrap).
- **Yes** → tell user "你已有 profile。是想完整重启（recalibrate，V1 feature）还是只改北极星段落？"
  - Full recalibrate: in V0, run `setting-polestar` again but preserve existing `调整历史` and append a note explaining the reset.
  - Just edit polestar: open `~/.claude/telos/profile.md` in conversation (show the file), let user edit inline, use `lib/profile.py::append_调整历史` to log the change.
