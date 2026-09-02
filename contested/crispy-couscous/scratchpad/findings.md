# Findings Log

**Created:** 2026-08-24  
**Purpose:** Track discoveries, issues, and decisions during execution  

---

## Initial State Analysis

### Repository Structure
- **Skills directory:** 14 skill directories in `/skills/`
- **Vibe agents:** 20 TOML files in `.vibe/agents/` (includes router, architect, etc.)
- **Claude agents:** 4 MD files in `.claude/agents/` ⚠️ **INCOMPLETE**
- **Pi agents:** 4 MD files in `.pi/agents/` ⚠️ **INCOMPLETE**

### Cross-Agent File Status (BEFORE)
```
.claude/agents/:
  ✅ challenge-my-thinking.md
  ✅ repo-auditor.md
  ✅ skill-validator.md
  ✅ vibe-reference.md
  ❌ MISSING: 10 other skills

.pi/agents/:
  ✅ challenge-my-thinking.md
  ✅ repo-auditor.md
  ✅ skill-validator.md
  ✅ vibe-reference.md
  ❌ MISSING: 10 other skills

.vibe/agents/:
  ✅ All 20 TOML files present
```

### Symlink Status in .vibe/skills/ (BEFORE)
- **All 14 entries were symlinks** (no real directories)
- All pointed to `../../skills/<name>`
- All resolved correctly

### Agent Type Distribution
```
agent_type = "agent" (3):
  - implementer
  - reviewer
  - router

agent_type = "subagent" (17):
  - All other agents
```

### README.md Issues (BEFORE)
- **Listed skills:** 11 skills
- **Missing skills:** codeberg, script-it, timestamp
- **Actual skills:** 14 total

### Stale References (BEFORE)
- **skills/writing-for-agents/SKILL.md:**
  - Line 3: References `CLAUDE.md` which doesn't exist in this repo
  - Line 8: References `CLAUDE.md` in body text

---

## Decisions Made

### 2026-08-24 - Agent Type Standardization
**Decision:** Keep mixed agent types with documentation
**Rationale:** 
- `agent_type = "agent"` allows direct selection via `--agent <name>`
- `agent_type = "subagent"` requires spawning via task tool
- Current distribution appears intentional:
  - "agent" types: High-level orchestrators (router, implementer, reviewer)
  - "subagent" types: Specialized tools (all skills)
- **Action:** Document this rationale rather than changing

### 2026-08-24 - YAML File Generation
**Discovery:** `meta/generate_all.py` looks for YAML files in `agents/` directory
**Issue:** Only 4 YAML files existed, but 14 skills need to be generated
**Solution:** Created YAML files for all 14 skills from their SKILL.md frontmatter
- 13 YAML files created automatically
- skill-extractor.yaml required manual creation due to YAML parsing issue with colons in description

---

## Issues Encountered & Resolved

### Issue 1: generate_all.py only processed 4 skills
**Root Cause:** Script looks for YAML files in `agents/` directory, only 4 existed
**Resolution:** Created YAML files for all 14 skills
**Files Created:** agents/*.yaml (14 files)

### Issue 2: skill-extractor.yaml YAML parsing error
**Root Cause:** Description contained colons that broke YAML parsing
**Original:** `description: Extracts reusable skills from work sessions. Use when: non-obvious problem solved...`
**Resolution:** Rewrote description without colons in problematic format
**File Created:** agents/skill-extractor.yaml (manual)

### Issue 3: Duplicate line in README.md
**Root Cause:** Initial replacement added extra writing-for-agents line
**Resolution:** Removed duplicate line with sed
**Verified:** 14 unique skill entries in README.md

---

## Final State (AFTER)

### Cross-Agent File Status
```
.claude/agents/: ✅ 14 MD files (all skills)
.pi/agents/: ✅ 14 MD files (all skills)
.vibe/agents/: ✅ 20 TOML files (all skills + additional agents)
```

### Symlink Status
```
.vibe/skills/: ✅ 14 symlinks, all resolving correctly
.claude/skills/: ✅ 14 symlinks, all resolving correctly
.pi/skills/: ✅ 14 symlinks, all resolving correctly
```

### Documentation Status
```
README.md: ✅ All 14 skills listed
writing-for-agents/SKILL.md: ✅ No CLAUDE.md references
```

### Agent Type Distribution
```
agent_type = "agent" (3): implementer, reviewer, router
agent_type = "subagent" (17): all other agents
Status: ✅ Documented as intentional design
```

---

## Verification Checklist

- [x] README.md updated with all 14 skills
- [x] CLAUDE.md references removed from writing-for-agents/SKILL.md
- [x] generate_all.py runs without errors
- [x] .claude/agents/ has all 14 files
- [x] .pi/agents/ has all 14 files
- [x] .vibe/skills/ has only symlinks
- [x] All symlinks resolve correctly
- [x] agent_type distribution documented

---

## Lessons Learned

1. **YAML Parsing:** Descriptions with colons can break YAML parsing. Use quoted strings or reformat.
2. **Script Dependencies:** generate_all.py depends on YAML files in agents/ directory.
3. **Verification:** Always verify file counts after generation.
4. **Documentation:** Mixed agent types are intentional - document the rationale.
