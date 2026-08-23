# Archive

Old prompts, kept for the record — not live, not skills, not auto-discovered
by either tool. These predate this repo's understanding of how Claude Code
and Vibe actually invoke skills; several were written as chat-mode "personas"
for stateless chatbots (explicit trigger phrases, activation/exit
confirmations, a mode menu) rather than as harness-native skills. That
scaffolding existed for a real reason at the time — older Claude models
sometimes read elaborate "mode" framing as a prompt-injection attempt and
resisted it — but it isn't needed once something becomes an actual
`SKILL.md`, so it didn't carry over into the ports below.

## What's here, and what happened to each one

| File | What it was | Outcome |
|---|---|---|
| `original-goblins.txt` | "Super Goblin" — Todo/Time/EF/Braindump modes bundled together. Note: Mode 2 is missing from the original file (jumps Mode 1 → Mode 3) — a pre-existing gap, not a transcription error. | See below, per mode. |
| `time-goblin.txt` | Standalone duplicate of the Time Goblin mode from `original-goblins.txt`, renamed "Style" instead of "Mode." | Superseded by `../skills/time-estimate/`. |
| `solus-mode.txt`, `solus-mode-mini.txt` | Precursor to a compressed, answer-first communication style. | Already graduated into a working skill (`solus-skill`) prior to this archive pass; not currently in this repo's `skills/` (removed as out of scope — see `../skills/README.md`). |

### Todo Goblin
Not re-adapted. `../skills/task-chunkdown/` already covers this — built
independently, before this archive was rediscovered — and does it better:
drip-fed steps instead of an upfront checklist dump, which is a sounder
delivery model for avoiding overwhelm.

### Time Goblin
Adapted into `../skills/time-estimate/`. The estimation logic (range sizing,
widen/narrow factors, common estimation traps) held up; only the chat-mode
scaffolding was dropped.

### EF Goblin
Adapted into `../skills/ef-unblock/`. The executive-function trap taxonomy
was the most genuinely distinctive content in the whole archive — kept
close to verbatim.

### Braindump Goblin
Adapted into `../skills/braindump-triage/`, and sharpened rather than
ported as-is: the original only tagged items by topic ([work], [home]).
Real brain-dump/mind-sweep practice (GTD's mind sweep, ADHD brain-dump
guidance) argues for triaging by *action* instead — do-now / do-later /
delegate / drop — plus explicit permission to drop trivial items and a
"where does this go" destination step, since an ungrounded list just gets
re-dumped next time. See the skill's own `SKILL.md` for the reasoning.
