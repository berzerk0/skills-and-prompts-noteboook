# Fix Plan for Vibe Skill Installation (Validated)

**Repository:** crispy-couscous  
**Date:** 2026-08-22  
**Audit Reference:** docs/audit-report-2026-08-22.md  
**Validation Against:** docs/cross-agent-primitives.md, docs/SKILL_DESIGN.md, AGENTS.md  
**Status:** Validated and Approved

---

## Validation Findings

### Repository Design Confirmed

From **docs/SKILL_DESIGN.md** and **docs/cross-agent-primitives.md**:

1. **Script-First Architecture**: All skills must have CLI-executable cores (Python/Bash)
   - ✅ Our installation follows this (skills have implementations)

2. **Tool-Agnostic SKILL.md**: 
   - SKILL.md files should use **only 6 standard frontmatter fields**
   - Should **NOT** include `allowed-tools` (tool names are NOT portable)
   - ✅ Our SKILL.md files correctly omit `allowed-tools`

3. **Per-Agent Wrappers**:
   - `.vibe/agents/<name>.toml` should use **Vibe's tool names**
   - Tool names: `read_file`, `write_file`, `edit`, `grep`, `bash`, `skill`, etc.
   - ✅ Our TOML files use Vibe tool names

4. **Structure**:
   - Portable: `skills/<name>/SKILL.md`
   - Vibe-specific: `.vibe/agents/<name>.toml`
   - Symlinks: `.vibe/skills/<name>` -> `../../skills/<name>`
   - ✅ Our installation follows this structure

### Key Insight from Validation

The repository design **intentionally separates** concerns:
- **SKILL.md**: Portable, tool-agnostic, no tool references
- **TOML files**: Vibe-specific, with `enabled_tools` using Vibe names

The bug is **NOT** in the SKILL.md files (they correctly omit `allowed-tools`).
The bug **IS** in the TOML files that are missing the `skill` tool.

### What the `skill` Tool Does

From Vibe's documentation and the repository's design:
- The `skill` tool allows a subagent to **load and invoke other skills**
- Without it, a subagent **cannot use any skills at all**
- This is critical for skill wrapper agents

---

## Revised Implementation Plan

### Phase 1: Fix Critical (P0) - Missing `skill` Tool

**Issue:** 8 agents cannot load skills due to missing `[tools.skill]` in TOML

**Fix:** Add the following to each affected agent TOML file:
```toml
[tools.skill]
enabled = true
```

**Files to fix (8 files):**
- [ ] `.vibe/agents/challenge-my-thinking.toml` - Currently has `[python]` and `[bash]` only
- [ ] `.vibe/agents/clarify.toml` - Currently has `read_file`, `grep`, `ask_user_question`, `bash` but NOT `skill`
- [ ] `.vibe/agents/codeberg.toml` - Currently has `[python]` and `[read_file]`, `[write_file]`, `[edit]`, `[grep]`, `[bash]` but NOT `skill`
- [ ] `.vibe/agents/escalate.toml` - Currently has `read_file`, `write_file`, `grep`, `bash` but NOT `skill`
- [ ] `.vibe/agents/modern-python.toml` - Currently has `read_file`, `write_file`, `edit`, `grep`, `bash` but NOT `skill`
- [ ] `.vibe/agents/napkin.toml` - Currently has `read_file`, `write_file`, `edit`, `bash` but NOT `skill`
- [ ] `.vibe/agents/planning-with-files.toml` - Currently has `read_file`, `write_file`, `edit`, `grep`, `bash` but NOT `skill`
- [ ] `.vibe/agents/timestamp.toml` - Currently has `[python]` and `[bash]` only

**Note:** The existing agents that already have `[tools.skill]`:
- architect.toml ✅
- escalation-fixer.toml ✅
- implementer.toml ✅
- reviewer.toml ✅
- skill-extractor.toml ✅
- transcription.toml ✅
- writing-for-agents.toml ✅

### Phase 2: Fix Medium (P1)

**2.1: Fix implementer prompt resolution**

**Issue:** `implementer.toml` has `system_prompt_id = "implementer"` but:
- Prompt file exists at `prompts/implementer.md` (repo root)
- Vibe likely looks in `.vibe/prompts/` by default

**Repository Convention:** From AGENTS.md, prompts should be accessible to agents.

**Fix:** Create symlink to maintain single source of truth:
```bash
mkdir -p .vibe/prompts
ln -s ../../prompts/implementer.md .vibe/prompts/implementer.md
```

**Alternative:** Move `prompts/implementer.md` to `.vibe/prompts/implementer.md`
- **Rejected:** This breaks the repository's multi-agent design (Claude and Pi agents also need access)
- **Decision:** Use symlink approach

**2.2: Fix stale path references**

**Issue:** Reference files contain Claude-specific paths

**Fixes:**
- `skills/skill-extractor/references/skill-lifecycle.md`:
  - Replace `.claude/` → `.vibe/`
  - Replace `~/.claude/` → `~/.vibe/`
- `skills/writing-for-agents/SKILL.md`:
  - Replace `CLAUDE.md` → `VIBE.md` (or remove the reference)

**Repository Convention Check:** 
- From SKILL_DESIGN.md: "Never reference specific tool names in SKILL.md files"
- Paths like `.claude/` are **tool-specific paths**, not tool names
- However, they still represent stale references that should be updated
- ✅ Fix is valid

---

## What Will NOT Be Fixed

1. **No config.toml** - This is acceptable. The repository uses defaults.
2. **No hooks.toml** - This is acceptable. No hooks are needed for basic skill functionality.
3. **AGENTS.md at repo root** - This is intentional per repository design.

---

## Success Criteria

After implementation:

### P0 (Critical)
- [ ] All 14 agent TOML files have `[tools.skill]` with `enabled = true`

### P1 (Medium)
- [ ] `.vibe/prompts/implementer.md` symlink exists and resolves
- [ ] No `.claude/` or `~/.claude/` references in skill files
- [ ] No `CLAUDE.md` references in skill files

### Verification
- [ ] Re-run audit shows zero critical issues
- [ ] All agents can theoretically load skills

---

## Implementation Order

1. **Fix all 8 TOML files** (P0 - highest priority)
2. **Create prompt symlink** (P1)
3. **Fix stale path references** (P1)
4. **Re-run audit and verify**
5. **Commit all changes**

---

## Notes

The repository's design is **correct**. The issue is purely in the agent TOML files that were created without the `skill` tool enabled. This was an oversight during the initial installation, not a design flaw.

The `skill` tool is **essential** for any agent that needs to invoke skills, which includes all skill wrapper agents.
