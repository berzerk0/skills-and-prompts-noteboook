---
name: escalate
description: Create escalation brief when stuck. Use when 3-strike protocol fails, cheap model routing hits dead end, or manual escalation needed.
license: MIT
compatibility: [claude, pi, vibe]
---

## Escalation Protocol

**Four steps — every one retrieval and formatting, zero self-assessment:**

1. **Halt.** Stop troubleshooting. No apology, no final attempt, no "let me just try one thing."
2. **Read** the session transcript from `transcript_path` (from POST_AGENT hook payload).
3. **Write** brief to `.escalation/brief-<timestamp>.md`, or into `scratchpad_dir` when a subagent failed.
4. **Output one line:** `Brief at <path>. <route>.`

## Brief Format

```markdown
# Escalation Brief — <timestamp>

## Goal
<original ask, one paragraph, from the first user turn>

## Current state
<what works, what's broken, exact repro command>

## Errors (verbatim)
<exact stderr/stack, unedited, deduplicated>

## Attempted and failed
- <approach> → <why it failed>

## Files touched
<paths + one-line what changed>

## Uncertain / unverified
<anything assumed but never confirmed>
```

**Deliberately does NOT:** count attempts, decide if escalation is warranted, attempt solution summary, clean up to look competent.

## Route Fork (Vibe-specific)

- **Self-contained problem**: Dispatch subagent with stronger `active_model` and brief path. Subagents start with fresh, empty context.
- **Might need dialogue**: Open fresh session. Subagents cannot use `ask_user_question`.
- **Never Shift+Tab**: Agent switching keeps polluted context.

## Return Leg

After strong model solves it, append lesson to napkin.md in required format:

```markdown
1. **[2026-08-22] Devstral loops on multi-file async refactors**
   Do instead: route async refactors to Mistral Large from the start.
```

## When to Use

- 3-strike protocol exhausted (from planning-with-files)
- Cheap model routing hits dead end
- Manual escalation needed for complex problems
