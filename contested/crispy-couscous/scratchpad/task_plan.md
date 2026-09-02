# Task Plan: Execute Immediate Action Items

**Created:** 2026-08-24  
**Scope:** Fix critical documentation and configuration issues in crispy-couscous  
**Skill Used:** planning-with-files  

---

## Executive Summary

Execute the 5 immediate action items identified in the audit to bring the repository to a fully functional state across all platforms (Claude, Pi, Vibe).

---

## Phases

### Phase 1: Setup & Planning (COMPLETED)
- [x] Create scratchpad directory
- [x] Create task_plan.md (this file)
- [x] Create findings.md
- [x] Create progress.md
- [x] Review all immediate action items

**Status:** ✅ COMPLETED

---

### Phase 2: Documentation Fixes (P0 - HIGH PRIORITY)

#### Task 2.1: Update README.md with all 13 skills
- **File:** README.md
- **Issue:** Only 5 skills listed, 13 exist
- **Missing skills:** clarify, escalate, modern-python, napkin, planning-with-files, script-it, skill-extractor, writing-for-agents
- **Estimate:** 10 minutes
- **Status:** ⏳ PENDING

#### Task 2.2: Fix CLAUDE.md reference in writing-for-agents/SKILL.md
- **File:** skills/writing-for-agents/SKILL.md
- **Issue:** Line 3 references CLAUDE.md which doesn't exist
- **Fix:** Remove "CLAUDE.md" from description
- **Estimate:** 2 minutes
- **Status:** ⏳ PENDING

---

### Phase 3: Cross-Agent Compatibility (P0 - HIGH PRIORITY)

#### Task 3.1: Run generate_all.py to create missing agent files
- **File:** meta/generate_all.py
- **Issue:** .claude/agents/ and .pi/agents/ only have 4 files each, should have 13+
- **Command:** `python meta/generate_all.py --all`
- **Estimate:** 5 minutes
- **Status:** ⏳ PENDING

---

### Phase 4: Structure Standardization (P1 - MEDIUM PRIORITY)

#### Task 4.1: Standardize .vibe/skills/ to all symlinks
- **Directory:** .vibe/skills/
- **Issue:** Mixed structure - 10 symlinks, 3+ real directories
- **Action:** Remove real directories, create symlinks to ../../skills/<name>
- **Estimate:** 10 minutes
- **Status:** ⏳ PENDING

#### Task 4.2: Standardize agent_type values
- **Files:** .vibe/agents/*.toml
- **Issue:** Inconsistent - some "agent", some "subagent"
- **Action:** Review and standardize (document rationale or make consistent)
- **Estimate:** 5 minutes
- **Status:** ⏳ PENDING

---

## Success Criteria

- [ ] README.md lists all 13 skills in the table
- [ ] No CLAUDE.md references in skill files
- [ ] .claude/agents/ has all 13+ skill agent files
- [ ] .pi/agents/ has all 13+ skill agent files
- [ ] .vibe/skills/ contains only symlinks (no real directories)
- [ ] All agent_type values are consistent or documented

---

## File Checklist

| File | Action | Status |
|------|--------|--------|
| README.md | Add 8 missing skills to table | ⏳ PENDING |
| skills/writing-for-agents/SKILL.md | Remove CLAUDE.md reference | ⏳ PENDING |
| meta/generate_all.py | Run to generate agent files | ⏳ PENDING |
| .vibe/skills/* | Convert real dirs to symlinks | ⏳ PENDING |
| .vibe/agents/*.toml | Standardize agent_type | ⏳ PENDING |

---

## Phase Execution Order

1. **Phase 2** (Documentation) - Quick wins, low risk
2. **Phase 3** (Cross-Agent) - Critical for multi-platform support
3. **Phase 4** (Standardization) - Cleanup and consistency

---

## Risk Assessment

| Task | Risk Level | Mitigation |
|------|------------|------------|
| README.md update | LOW | Git backup, review changes before commit |
| SKILL.md fix | LOW | Small change, easy to verify |
| generate_all.py | MEDIUM | Check output files, don't overwrite existing |
| Symlink conversion | MEDIUM | Backup first, verify symlinks resolve |
| agent_type standardization | LOW | Document rationale for differences |

---

## Notes

- All changes should be committed with descriptive messages
- Verify each change after execution
- Log all actions in progress.md
- Update findings.md with any discoveries
