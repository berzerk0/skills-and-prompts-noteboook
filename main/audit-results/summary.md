# Audit Summary - crispy-couscous

**Repository:** berzerk0/crispy-couscous  
**Audit Date:** 2026-08-22  
**Auditor:** Vibe Code  
**Plan:** main/plans/repo-bug-audit-plan.md  
**Status:** COMPLETED (Partial - Core phases done)

---

## Executive Summary

This audit of the crispy-couscous repository identified **1 CRITICAL**, **4 HIGH/MEDIUM**, and **3 LOW** severity findings across configuration, compatibility, and structure issues. The repository is a multi-agent skill development workspace for Claude Code, Pi Agent, and Mistral Vibe Code.

**Key Discovery:** The previous audit (docs/audit-report-2026-08-22.md) reported 7 agents missing the `skill` tool, but the actual count is **3 agents** - a significant discrepancy that has been corrected.

---

## Critical Findings

### [31mCRITICAL 1.1: 3 Agents Missing `skill` Tool Configuration[0m

**Affected:** `.vibe/agents/repo-auditor.toml`, `.vibe/agents/skill-validator.toml`, `.vibe/agents/vibe-reference.toml`

**Impact:** These 3 subagents CANNOT load or invoke any skills at all. This is a silent failure - the skill tool is simply unavailable with no error message.

**Root Cause:** These agents use syntax `[python]`, `[bash]`, `[read_file]`, etc. but lack a `[skill]` or `[tools.skill]` section.

**Fix:** Add `[skill]` section with `enabled = true` to each of the 3 affected agent TOML files.

---

## Medium Severity Findings

### MEDIUM 1.2: Stale Path References - PREVIOUSLY REPORTED BUT NOT FOUND

**Previous Report:** docs/audit-report-2026-08-22.md claimed:
- `skills/skill-extractor/references/skill-lifecycle.md`: contains `.claude/` and `~/.claude/`
- `skills/writing-for-agents/SKILL.md`: contains `CLAUDE.md`

**Current Status:** [32mVERIFIED AS RESOLVED[0m - These specific references do NOT exist in the current codebase. The issues appear to have been fixed already.

**New Minor Issue:** `skills/writing-for-agents/SKILL.md` has `VIBE.md` duplicated in description:
```yaml
description: Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md, VIBE.md, or VIBE.md.
```

### MEDIUM 1.3: Prompt Path Resolution Issue

**Affected:** `.vibe/agents/implementer.toml` references `system_prompt_id = "implementer"`

**Status:** [32mRESOLVED BY SYMLINK[0m - The prompt file exists at `prompts/implementer.md` (repo root), and there's a symlink at `.vibe/prompts/implementer.md -> ../../prompts/implementer.md`. Vibe Code should find it.

**Note:** This is a clever workaround, but the canonical location for Vibe Code prompts is `.vibe/prompts/`. Consider moving the file there for clarity.

### MEDIUM 2.1: Inconsistent Tool Configuration Syntax

**Affected:** 3 agents use different syntax than the other 14:
- `repo-auditor.toml`, `skill-validator.toml`, `vibe-reference.toml` use: `[python]`, `[bash]`, `[read_file]`, etc.
- Other 14 agents use: `[tools.read_file]`, `[tools.write_file]`, `[tools.skill]`, etc.

**Impact:** Inconsistent style makes maintenance harder. The 3 Syntax B agents are also the ones missing `[skill]` tool.

**Fix:** Standardize on `[tools.xxx]` syntax (used by majority).

### MEDIUM 3.1: Documentation Out of Date

**Affected:** README.md lists only 5 skills but there are **13 skills** in the repository.

**Missing from README table:**
- clarify, escalate, modern-python, napkin, planning-with-files, skill-extractor, vibe-reference, writing-for-agents

**Impact:** Users may not know about all available skills.

**Fix:** Update README.md skills table to include all 13 skills.

---

## Low Severity / Informational Findings

### LOW 4.1: Symlink Structure Inconsistency

**.vibe/skills/** has a **mixed structure**:
- 6 symlinks: challenge-my-thinking, codeberg, repo-auditor, skill-validator, timestamp, vibe-reference
- 7 real directories: clarify, escalate, modern-python, napkin, planning-with-files, skill-extractor, writing-for-agents

**.claude/skills/** and **.pi/skills/** have only symlinks (6 each).

**Impact:** Inconsistent - some skills are duplicated as real directories in `.vibe/skills/` while being symlinked in `.claude/skills/` and `.pi/skills/`.

**Fix:** Consider making all skills symlinks in `.vibe/skills/` for consistency, or make all real directories.

### LOW 6.1: Bash Tool Enabled on All Agents

**Status:** All 17 agents have bash tool enabled. This is **intentional** for a development workspace.

**Impact:** All subagents can execute shell commands. Appropriate for skill development.

**Recommendation:** No fix needed - this is by design.

### LOW 7.1: Context Cost Within Acceptable Range

**Calculated:**
- Always-on cost (skill descriptions): **2,244 characters**
- AGENTS.md: **7,194 characters**
- Total always-on: **9,438 characters**
- Total skill body lines: **657 lines**

**Comparison:** Previous audit reported 8,171 characters. Current is 9,438 - slightly higher but still reasonable.

**Impact:** Acceptable for most use cases. Monitor if adding many more skills.

---

## Configuration Details

### Agent Counts
- **Total agents in .vibe/agents/:** 17 TOML files
- **Agent types:** All are `"subagent"` (no user-facing agents)
- **Agents with `skill` tool:** 14
- **Agents WITHOUT `skill` tool:** 3 (CRITICAL)
- **Agents with `python` tool:** 5 (codeberg, challenge-my-thinking, repo-auditor, skill-validator, timestamp, vibe-reference)

### Skill Counts
- **Total skills in skills/:** 13
- **All have SKILL.md:** Yes
- **All have valid frontmatter:** Yes (based on spot checks)

### Symlink Status
- **All symlinks valid:** Yes
- **All point to correct targets:** Yes (../../skills/<name>)

---

## Cross-Agent Compatibility

| Platform | Agent Files | Skills Directory | Symlinks Valid |
|----------|--------------|------------------|----------------|
| Vibe Code | 17 TOML | Mixed (6 symlinks, 7 real) | Yes |
| Claude Code | 6 MD | 6 symlinks | Yes |
| Pi Agent | 6 MD | 6 symlinks | Yes |

**Note:** Claude Code uses `.md` files for agents, Vibe Code uses `.toml` files. The generation scripts in `meta/` handle this conversion.

---

## Files Created During Audit

1. **main/plans/repo-bug-audit-plan.md** - The audit plan
2. **main/audit-results/audit-log.md** - Execution log
3. **main/audit-results/findings.md** - Detailed findings (in progress)
4. **main/audit-results/summary.md** - This file

---

## Recommendations

### Immediate (Critical)
1. **Fix CRITICAL 1.1:** Add `[skill]` tool to 3 agent TOML files
   - repo-auditor.toml
   - skill-validator.toml  
   - vibe-reference.toml

### Short-term (Medium)
2. **Fix MEDIUM 2.1:** Standardize tool configuration syntax in the 3 affected agents
3. **Fix MEDIUM 3.1:** Update README.md to list all 13 skills
4. **Fix minor typo:** Remove `VIBE.md` duplication in writing-for-agents SKILL.md

### Long-term (Low)
5. **Consider:** Standardize symlink structure across all agent directories
6. **Consider:** Move prompts/implementer.md to .vibe/prompts/ for canonical location

---

## Validation Status

- [x] Phase 0: Preparation
- [x] Phase 1: Known Issues Validation (with corrections)
- [x] Phase 2: Configuration Audit
- [x] Phase 3: Skill Validation (partial)
- [x] Phase 4: Cross-Agent Compatibility (partial)
- [ ] Phase 5: Path & Reference Audit (not fully executed)
- [ ] Phase 6: Security & Permissions (not fully executed)
- [x] Phase 7: Performance & Cost Analysis
- [ ] Phase 8: Tool Name Consistency (not fully executed)
- [x] Phase 9: Symlink Integrity
- [ ] Phase 10: Synthesis & Prioritization (this document)

---

## Next Steps

1. **Apply critical fix** (1.1) - Add skill tool to 3 agents
2. **Apply medium fixes** (2.1, 3.1) - Standardize syntax, update docs
3. **Complete remaining phases** (5, 6, 8, 10) for full coverage
4. **Re-run audit** after fixes to verify resolution

---

## Conclusion

The repository is generally well-structured with good cross-agent compatibility. The **CRITICAL finding** (3 agents missing skill tool) must be addressed as it causes silent failures. Most other findings are documentation or consistency issues that should be cleaned up for maintainability.

The previous audit's finding of "7 agents missing skill tool" was **incorrect** - the actual count is 3, which is still critical but less severe than initially reported.

---

*Audit completed: 2026-08-22*  
*Repository: berzerk0/crispy-couscous*
