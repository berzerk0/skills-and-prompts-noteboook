# Fix Tasks Checklist

**Purpose:** Track and check off fixes for issues identified in audit-report-2026-08-22.md  
**Date:** 2026-08-22  
**Status:** In progress

---

## Task List

- [ ] Review audit report to identify all issues
- [ ] Create fix plan document
- [ ] Validate plan against repository docs (cross-agent-primitives.md, SKILL_DESIGN.md, AGENTS.md)
- [ ] Adjust plan based on research
- [ ] Implement fixes
- [ ] Commit changes

---

## Issues Identified from Audit

### Critical (Silent Failures)
1. **7 agents missing `skill` tool** - Cannot load any skills
   - challenge-my-thinking.toml
   - clarify.toml
   - codeberg.toml
   - escalate.toml
   - modern-python.toml
   - napkin.toml
   - planning-with-files.toml
   - timestamp.toml

2. **implementer.toml** - system_prompt_id='implementer' may not resolve
   - Prompts directory at repo root, not .vibe/prompts/

### Medium (Translation Errors)
3. **Stale path references**
   - skills/skill-extractor/references/skill-lifecycle.md: contains .claude/
   - skills/skill-extractor/references/skill-lifecycle.md: contains ~/.claude/
   - skills/writing-for-agents/SKILL.md: contains CLAUDE.md

### Low
4. **No config.toml** - Using defaults (acceptable for repo)
5. **No hooks.toml** - No hooks configured (acceptable)

---

## Notes

The repository follows a **Script-First Architecture** where:
- Portable skills are in `skills/<name>/SKILL.md`
- Per-agent wrappers are in `.vibe/agents/<name>.toml`
- Symlinks connect `.vibe/skills/` to `skills/`
- Tool names in SKILL.md should be tool-agnostic (no allowed-tools)
- Tool names in TOML files should be Vibe-specific

The critical issue is that **agent TOML files** (not SKILL.md files) control which tools are enabled for subagents. The SKILL.md files correctly omit `allowed-tools` per repository conventions, but the TOML wrappers need the `skill` tool enabled.
