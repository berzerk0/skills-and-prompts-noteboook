# Fix Plan for Vibe Skill Installation

**Repository:** crispy-couscous  
**Date:** 2026-08-22  
**Audit Reference:** docs/audit-report-2026-08-22.md  
**Status:** Draft

---

## Executive Summary

The audit revealed that **7 out of 14 agent TOML files are missing the `skill` tool** in their `enabled_tools` configuration. This means those subagents **cannot load or invoke any skills at all**, including the skills they are meant to wrap. This is a silent failure — the agents would appear to work but fail when attempting to use skills.

Additionally, there are stale path references and a prompt resolution issue.

---

## Issues by Priority

### P0 - Critical (Silent Failures)

**Issue:** 7 agents cannot load skills due to missing `skill` tool in TOML

**Affected agents:**
- `.vibe/agents/challenge-my-thinking.toml`
- `.vibe/agents/clarify.toml`
- `.vibe/agents/codeberg.toml`
- `.vibe/agents/escalate.toml`
- `.vibe/agents/modern-python.toml`
- `.vibe/agents/napkin.toml`
- `.vibe/agents/planning-with-files.toml`
- `.vibe/agents/timestamp.toml`

**Fix:** Add `[tools.skill]` with `enabled = true` to each affected agent TOML file.

**Why this is critical:** Without the `skill` tool, a subagent cannot load *any* skills via the `skill` tool. This defeats the entire purpose of having a subagent wrapper. The agent would start but be unable to perform its function.

---

### P1 - Medium (Configuration Issues)

**Issue 1:** `implementer.toml` references `system_prompt_id = "implementer"` but prompt file is at `prompts/implementer.md` (repo root), not `.vibe/prompts/implementer.md`

**Fix options:**
- A. Move `prompts/implementer.md` to `.vibe/prompts/implementer.md`
- B. Remove `system_prompt_id` from implementer.toml (use default)
- C. Create symlink: `.vibe/prompts/implementer.md` -> `../../prompts/implementer.md`

**Recommended:** Option C (symlink) - maintains single source of truth while satisfying Vibe's search path.

**Issue 2:** Stale path references in skill bodies
- `skills/skill-extractor/references/skill-lifecycle.md`: contains `.claude/` and `~/.claude/`
- `skills/writing-for-agents/SKILL.md`: contains `CLAUDE.md`

**Fix:** Update references to use Vibe paths (`.vibe/` or remove Claude-specific references).

**Note:** These are in reference files, not the main SKILL.md, so impact is lower. However, they could confuse users reading the documentation.

---

### P2 - Low (Non-Critical)

**Issue:** No `config.toml` or `hooks.toml` in `.vibe/`

**Status:** Acceptable for repository. These are optional and the defaults work fine.

---

## Repository Conventions Review

Before implementing, validate against:

1. **docs/cross-agent-primitives.md** - Tool name mappings, bash as universal primitive
2. **docs/SKILL_DESIGN.md** - Script-First Architecture, portable frontmatter
3. **AGENTS.md** - Repository structure, per-agent wrappers

Key conventions:
- SKILL.md files: **tool-agnostic**, no `allowed-tools`, use only 6 standard frontmatter fields
- TOML files: **Vibe-specific**, include `enabled_tools` with Vibe tool names
- Structure: `skills/<name>/SKILL.md` + `.vibe/agents/<name>.toml` + symlink

---

## Implementation Plan

### Phase 1: Fix Critical (P0)

For each of the 8 affected agent TOML files:

1. Open the file
2. Add the following block:
   ```toml
   [tools.skill]
   enabled = true
   ```
3. Verify the file is valid TOML

**Files to fix:**
- [ ] challenge-my-thinking.toml
- [ ] clarify.toml
- [ ] codeberg.toml
- [ ] escalate.toml
- [ ] modern-python.toml
- [ ] napkin.toml
- [ ] planning-with-files.toml
- [ ] timestamp.toml

**Verification:** After fix, each agent should have `[tools.skill]` section.

---

### Phase 2: Fix Medium (P1)

**2.1: Fix implementer prompt resolution**
- [ ] Create `.vibe/prompts/` directory if it doesn't exist
- [ ] Create symlink: `.vibe/prompts/implementer.md` -> `../../prompts/implementer.md`
- [ ] Verify symlink resolves correctly

**2.2: Fix stale path references**
- [ ] In `skills/skill-extractor/references/skill-lifecycle.md`:
  - Replace `.claude/` with `.vibe/`
  - Replace `~/.claude/` with `~/.vibe/`
- [ ] In `skills/writing-for-agents/SKILL.md`:
  - Replace `CLAUDE.md` with `VIBE.md` or remove reference

---

### Phase 3: Verification

After all fixes:
1. Re-run the audit script
2. Verify all agents have `[tools.skill]` enabled
3. Verify no stale path references remain
4. Verify prompt resolution works
5. Commit all changes

---

## Success Criteria

- [ ] All 14 agent TOML files have `[tools.skill]` with `enabled = true`
- [ ] No stale `.claude/` or `CLAUDE.md` references in skill files
- [ ] `implementer.toml` system_prompt_id resolves to a valid file
- [ ] Audit re-run shows zero critical issues

---

## Files to Modify

### Agent TOML files (8 files)
- `.vibe/agents/challenge-my-thinking.toml`
- `.vibe/agents/clarify.toml`
- `.vibe/agents/codeberg.toml`
- `.vibe/agents/escalate.toml`
- `.vibe/agents/modern-python.toml`
- `.vibe/agents/napkin.toml`
- `.vibe/agents/planning-with-files.toml`
- `.vibe/agents/timestamp.toml`

### Reference files (2 files)
- `skills/skill-extractor/references/skill-lifecycle.md`
- `skills/writing-for-agents/SKILL.md`

### New files/directories
- `.vibe/prompts/` directory
- `.vibe/prompts/implementer.md` symlink

---

## Notes

The repository's design intentionally separates:
- **SKILL.md**: Portable, tool-agnostic, no allowed-tools
- **TOML files**: Vibe-specific, with enabled_tools

This is correct. The bug is in the TOML files, not the SKILL.md files.

The `skill` tool is required for any subagent that needs to load and invoke skills. Since all these agents are skill wrappers, they all need it.
