# Vibe Install Audit Report

**Audited:** `/workspace/github__berzerk0__crispy-couscous/.vibe/`  
**Date:** 2026-08-22  
**Type:** Repository installation audit (not user `~/.vibe/`)  
**Scope:** Skills installed in the crispy-couscous repository structure

---

## SECTION 1 — SKILL INVENTORY

skill name | directory | line count | user-invocable | allowed-tools (verbatim)
--|--|--|--|--
challenge-my-thinking | skills/challenge-my-thinking | 182 lines | false | none
clarify | skills/clarify | 45 lines | false | none
codeberg | skills/codeberg | 22 lines | false | none
escalate | skills/escalate | 62 lines | false | none
modern-python | skills/modern-python | 43 lines | false | none
napkin | skills/napkin | 98 lines | false | none
planning-with-files | skills/planning-with-files | 63 lines | false | none
skill-extractor | skills/skill-extractor | 47 lines | false | none
timestamp | skills/timestamp | 24 lines | false | none
writing-for-agents | skills/writing-for-agents | 83 lines | false | none

### Extra files in each skill directory:

- **modern-python**: templates/dependabot.yml, templates/pre-commit-config.yaml, assets/trail-of-bits-mark.svg, references/dependabot.md, references/migration-checklist.md, references/pep723-scripts.md, references/prek.md, references/pyproject.md, references/ruff-config.md, references/security-setup.md, references/testing.md, references/uv-commands.md
- **planning-with-files**: references/examples.md, references/principles.md, references/templates.md
- **skill-extractor**: references/quality-guide.md, references/skill-lifecycle.md, references/skill-template.md
- **writing-for-agents**: SKILL-MECHANICS.md

---

## SECTION 2 — TRANSLATION ERRORS

### 2a. Untranslated tool names

None found

### 2b. Nonexistent tool names

None found

### 2c. Stale paths

- `skills/skill-extractor/references/skill-lifecycle.md`: contains `\.claude/`
- `skills/skill-extractor/references/skill-lifecycle.md`: contains `~/\.claude/`
- `skills/writing-for-agents/SKILL.md`: contains `CLAUDE\.md`

### 2d. disable-model-invocation

None found

---

## SECTION 3 — CONFIGURATION

**config.toml:** NOT FOUND

- `skill_paths`: Not set (default)
- `enabled_skills`: Not set (default: all skills enabled)
- `disabled_skills`: Not set
- `default_agent`: Not set

---

## SECTION 4 — AGENTS AND PROMPTS

### Agent files:

All 14 agent TOML files present in `.vibe/agents/`.

### Prompt files:

- `prompts/implementer.md`: 45 lines (exists at **repo root**, not `.vibe/prompts/`)

### Specific checks:

**Agents missing `skill` tool in enabled_tools:**
- challenge-my-thinking.toml
- clarify.toml
- codeberg.toml
- escalate.toml
- modern-python.toml
- napkin.toml
- planning-with-files.toml
- timestamp.toml

**system_prompt_id resolution:**
- implementer.toml: system_prompt_id='implementer' -> **MISSING** (resolves to `prompts/implementer.md`, but Vibe may look in `.vibe/prompts/`)
- All other agents: no system_prompt_id

---

## SECTION 5 — HOOKS AND AGENTS.md

**hooks.toml:** NOT FOUND (no user or project hooks.toml)

**AGENTS.md:** Found at repo root (231 lines, 6458 characters)

**Claude Code event names in hooks:** None (no hooks files exist)

---

## SECTION 6 — CONTEXT COST ESTIMATE

skill name | description char count | SKILL.md line count
--|--|--
challenge-my-thinking | 191 | 177
clarify | 130 | 40
codeberg | 113 | 14
escalate | 133 | 57
modern-python | 159 | 38
napkin | 288 | 93
planning-with-files | 277 | 58
skill-extractor | 195 | 42
timestamp | 114 | 16
writing-for-agents | 113 | 78

**Always-on cost:** 1713 characters (sum of all skill descriptions)

**Worst-case invocation cost:** 613 lines (sum of all skill bodies)

**Skills exceeding 200 lines:** None

**AGENTS.md:** 6458 characters

**Total always-on cost (descriptions + AGENTS.md):** 8171 characters

---

## SECTION 7 — SUMMARY

1. **Installed skills (10):** challenge-my-thinking, clarify, codeberg, escalate, modern-python, napkin, planning-with-files, skill-extractor, timestamp, writing-for-agents

2. **Translation errors:**
   - 2a. Untranslated tool names: **None found**
   - 2b. Nonexistent tool names: **None found**
   - 2c. Stale paths: **3 findings**
     - `skills/skill-extractor/references/skill-lifecycle.md`: contains `.claude/`
     - `skills/skill-extractor/references/skill-lifecycle.md`: contains `~/.claude/`
     - `skills/writing-for-agents/SKILL.md`: contains `CLAUDE.md`
   - 2d. disable-model-invocation: **None found**

3. **Installed but unreachable:**
   - No config.toml found, so default behavior applies (all skills enabled)
   - However, prompts directory is at repo root, not `.vibe/prompts/`
   - implementer.toml references system_prompt_id='implementer' which resolves to `prompts/implementer.md`

4. **Always-on context cost:** **8171 characters** (sum of all skill descriptions + AGENTS.md)

5. **What is broken right now that would fail silently:**
   - **7 agents missing `skill` tool in enabled_tools:**
     challenge-my-thinking, clarify, codeberg, escalate, modern-python, napkin, planning-with-files
     **These agents CANNOT load or invoke any skills at all.**
   - **Stale path references in skill bodies:**
     skill-extractor references `.claude/` paths (won't work in Vibe)
     writing-for-agents references `CLAUDE.md` (won't work in Vibe)
   - **implementer.toml system_prompt_id='implementer':**
     Resolves to `prompts/implementer.md` (exists at repo root, not `.vibe/prompts/`)
     May not be found by Vibe depending on its prompt search path

---

*Report generated from repository audit. For user `~/.vibe/` audit, run this same process against the actual user directory.*
