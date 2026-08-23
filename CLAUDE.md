# CLAUDE.md

Shared instructions for this repo live in [AGENTS.md](AGENTS.md) — read
that file first, it applies to Claude Code and Mistral Vibe Code equally.

One Claude Code-specific note: skills copied out of [skills/](skills/) for
actual use belong in `./.claude/skills/<name>/` (project) or
`~/.claude/skills/<name>/` (user) to be discovered — this repo's own
`skills/` directory is a library, not a live skill path.

---

## Mailroom (Read-Only)

The `mailroom/` directory is a **read-only** staging area. See
[mailroom/README.md](mailroom/README.md) for processing guidelines.
**Agents MUST NEVER write to mailroom/.**
