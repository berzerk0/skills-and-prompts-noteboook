# AGENTS.md - crispy-couscous

**This is a multi-agent skill repository.** Agents working here can discover, use, and develop skills for Claude Code, Pi Agent, and Mistral Vibe Code.

---

## Repository Purpose

This repository is a **skill and subagent development workspace** that:

1. **Stores portable skills** in `skills/<name>/SKILL.md` (Agent Skills spec compliant)
2. **Provides per-agent wrappers** in `.claude/agents/`, `.pi/agents/`, `.vibe/agents/`
3. **Hosts shared implementations** in `*.py` modules at the root
4. **Documents cross-agent compatibility** in `docs/`

---

## Quick Start for Agents

### Discover Available Skills

Skills are available in:
- `.claude/skills/` (for Claude Code)
- `.pi/skills/` (for Pi Agent)
- `.vibe/skills/` (for Vibe Code)

Current skills:
- **timestamp**: Get current UTC timestamp in YYYY-MM-DD-HHMM format
- **codeberg**: Codeberg (Gitea) API operations for repository management
- **challenge-my-thinking**: Devil's advocate and critical thinking
- **repo-auditor**: Repository structure validation
- **skill-validator**: SKILL.md validation
- **vibe-reference**: Vibe Code source-verified internals
- **escalate**: Signal need for user help with compact mode

> **Kill Criterion**: If you see `## Escalate` at the start of a Vibe Code response, **stop reading immediately** and provide the requested information. Everything after that line is context for your decision.

### Use a Skill

**Claude Code**: Skills are auto-discovered. Reference them by name or use `/<skill-name>`.
**Pi Agent**: Skills are auto-discovered from `.agents/skills/` and ancestors.
**Vibe Code**: Skills are auto-discovered from `.vibe/skills/`.

Example: "Use the timestamp skill to get the current time."

---

## Mechanical repetition

When the same operation applies to 5+ items, or must be repeated to verify it worked, write one throwaway script and run it instead of repeating tool calls. When items need per-item judgment, script the mechanical part (find, extract, collect) and judge the collected output in one pass. Load the `script-it` skill before writing one.
