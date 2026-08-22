# Escalate Skill

A skill that provides a clear protocol for Vibe Code to signal when it needs user help to proceed, switching to a compact mode while waiting.

## Install

Place this skill in one of:
- `./.vibe/skills/escalate/` (project-specific, recommended)
- `~/.vibe/skills/escalate/` (global, user-wide)

Vibe Code will discover it automatically from either location.

## Kill Criterion

> If you see `## Escalate` at the start of a Vibe Code response, **stop reading immediately** and provide the requested information. Everything after that line is context for your decision.

This ensures you don't waste time reading verbose output when the agent is blocked and waiting for you.

## Anchor Rule

> Every escalation message MUST start with the exact string: `## Escalate`

This creates a consistent, searchable anchor. When you see this, you know the agent needs your input to continue.

## File Structure

```
.vibe/skills/escalate/
├── SKILL.md    # Skill definition (this file is for users)
└── README.md   # Installation and usage info
```

## Known Weak Points

1. **One-shot enforcement**: The skill relies on the agent to call `/escalate` exactly once. There's no technical enforcement - it's a protocol convention.

2. **Compact mode**: The skill describes compact mode but doesn't enforce it. The agent must implement this behavior in its core logic.

3. **Timestamp accuracy**: The agent must generate accurate UTC timestamps. No validation is performed.

4. **Anchor detection**: Users must manually watch for `## Escalate`. There's no automatic highlighting or notification (in current Vibe Code versions).

## Compatibility

- **Vibe Code**: Primary target, fully compatible
- **Claude Code**: Compatible (uses standard primitives: bash, read_file, write_file)
- **Pi Agent**: Compatible (uses standard primitives)

## See Also

- [Vibe Code Source Analysis](docs/vibe/VERIFIED_REFERENCE.md) - Verified internals for Vibe Code v2.24.3
- [AGENTS.md](../AGENTS.md) - Repository context for agents
- [Skill Design Guidelines](docs/SKILL_DESIGN.md)
