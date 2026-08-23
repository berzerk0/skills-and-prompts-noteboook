# CLAUDE.md

Shared instructions for this repo live in [AGENTS.md](AGENTS.md) -- read
that file first, it applies to Claude Code and Mistral Vibe Code equally.

One Claude Code-specific note: skills copied out of [skills/](skills/) for
actual use belong in `./.claude/skills/<name>/` (project) or
`~/.claude/skills/<name>/` (user) to be discovered -- this repo's own
`skills/` directory is a library, not a live skill path.

---

## Mailroom and Archive (Read-Only)

The `mailroom/` and `archive/` directories are both **read-only**. Agents
MUST NEVER write to either. Full guidelines live in AGENTS.md; see
[mailroom/README.md](mailroom/README.md) and
[archive/README.md](archive/README.md) for the details of each.
