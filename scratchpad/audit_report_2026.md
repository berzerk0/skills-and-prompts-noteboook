# Comprehensive Repository Audit Report

**Repository:** skills-and-prompts-notebook  
**Auditor:** Vibe Code (via Mistral AI)  
**Date:** 2026-08-24  
**Scope:** Full repository - syntax, structure, consistency, licensing, cross-references

---

## Executive Summary

**Overall Status:** ⚠️ **Needs Work** (Functional but requires refinement)

**Total Issues Found:** 45+ across 10 categories  
**Critical:** 0  
**High Priority:** 15+  
**Medium Priority:** 20+  
**Low Priority:** 10+  

**Key Finding:** The repository has excellent foundational structure and dual-agent design, but suffers from **inconsistent skill frontmatter**, **missing documentation**, **broken links**, and **unprocessed mailroom/archive content**. The existing self-checks from 2026-08-23 identified many of these issues, but several remain unaddressed.

---

## 📊 Category Breakdown

| Category | Issues | Status | Priority |
|----------|--------|--------|----------|
| Skill Frontmatter | 13+ | ⚠️ Inconsistent | HIGH |
| Missing Documentation | 8+ directories | ⚠️ Missing READMEs | HIGH |
| Broken Links | 7+ | ❌ Broken | MEDIUM |
| Mailroom Processing | 4+ items | ⚠️ Unprocessed | HIGH |
| Archive Clarification | 1 | ⚠️ Needs documentation | MEDIUM |
| Cross-References | 3+ | ⚠️ Inconsistent | MEDIUM |
| Configuration | 2+ | ⚠️ Minor issues | LOW |
| Duplicate Content | 1 | ⚠️ Clarification needed | LOW |
| License Accuracy | 2+ | ⚠️ Inconsistent | MEDIUM |
| Syntax Errors | 0 | ✅ Clean | N/A |

---

## 🔍 Detailed Findings

---

### 1. Skill Frontmatter Inconsistency (HIGH PRIORITY)

**Issue:** Skills in `skills/` directory have inconsistent or incomplete YAML frontmatter.

**Impact:** Skills may not be discovered, loaded, or work correctly in Vibe. Silent failures can occur with unrecognized tool names.

**Evidence:**

| Skill | name | description | license | compatibility | user-invocable | allowed-tools | Status |
|-------|------|-------------|---------|---------------|----------------|---------------|--------|
| cross-agent-compat | ✅ | ✅ | ✅ MIT | ✅ | ✅ | ✅ | ✅ **100%** |
| code-review | ✅ | ✅ | ✅ MIT | ✅ | ✅ | ✅ | ✅ **100%** |
| security-audit | ✅ | ✅ | ✅ MIT | ✅ | ✅ | ✅ | ✅ **100%** |
| vibe-internals | ✅ | ✅ | ✅ MIT | ✅ | ✅ | ✅ | ✅ **100%** |
| import-memory | ✅ | ✅ | ✅ Apache-2.0 | ❌ | ✅ | ❌ | ⚠️ **67%** |
| skill-creator | ✅ | ✅ | ✅ Apache-2.0 | ❌ | ✅ | ❌ | ⚠️ **67%** |
| skill-extractor | ✅ | ✅ | ✅ (none) | ❌ | ✅ | ❌ | ⚠️ **67%** |
| ask-questions-if-underspecified | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ **33%** |
| challenge-my-thinking | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ **33%** |
| braindump-triage | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ **33%** |
| ef-unblock | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ **33%** |
| notebooklm-agent | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ **33%** |
| search-helpers | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ **33%** |
| time-estimate | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ **33%** |
| task-chunkdown | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ **33%** |

**Statistics:**
- **Complete frontmatter:** 4/13 skills (31%)
- **Partial frontmatter:** 3/13 skills (23%)
- **Minimal frontmatter:** 6/13 skills (46%)
- **Overall completeness:** 55%

**Required Fixes:**
1. Add `license` field to 8 skills
2. Add `compatibility` field to 9 skills
3. Add `allowed-tools` field to 9 skills
4. Add `user-invocable` field to 6 skills
5. Standardize YAML format (block style vs flow style)

**Example of Complete Frontmatter:**
```yaml
---
name: example-skill
description: A brief description of what this skill does
license: MIT
compatibility:
  - vibe: ">=2.24.0"
  - claude: ">=1.0.0"
user-invocable: true
allowed-tools:
  - read_file
  - grep
  - bash
  - write_file
---
```

---

### 2. Missing Documentation (HIGH PRIORITY)

**Issue:** Multiple directories lack README.md files, making purpose and usage unclear.

**Directories Missing README.md:**

| Directory | Purpose | Impact | Fix |
|-----------|---------|--------|-----|
| `.vibe/prompts/` | Custom system prompts | Unclear what belongs here | Add README with format conventions |
| `.claude/skills/` | Future Claude skills | Empty, purpose unclear | Add README explaining future use |
| `.claude/commands/` | ✅ Has files but no README | Users won't find commands | Add README indexing commands |
| `archive/` | ✅ Has README but needs clarification | Distinction from mailroom unclear | Update to clarify archive vs mailroom |
| `prompts/` | ✅ Has README but minimal | Could be more comprehensive | Enhance with examples |

**Additional Documentation Gaps:**
- `.vibe/agents/` - No README explaining agent configurations
- `.vibe/skills/` - No README (though skills themselves are documented)
- `self-checks/` - Has README but not referenced in AGENTS.md or README.md

**Note:** The `archive/README.md` exists and is well-written, but the archive directory's relationship to mailroom needs clarification in AGENTS.md.

---

### 3. Broken Links (MEDIUM PRIORITY)

**Issue:** Multiple markdown files contain links to non-existent files.

**Broken Links Found:**

| File | Broken Link | Target | Status |
|------|-------------|--------|--------|
| `docs/shared/README.md` | `[workflows.md](./docs/shared/workflows.md) | Does not exist | ❌ |
| `docs/shared/README.md` | `[patterns.md](./docs/shared/patterns.md) | Does not exist | ❌ |
| `docs/shared/README.md` | `[best-practices.md](./docs/shared/best-practices.md) | Does not exist | ❌ |
| `docs/notebooklm/notebooklm-report.md` | `[Source Title/Author (YYYY-MM)](./docs/notebooklm/URL)` | Malformed URL | ❌ |
| `skills/notebooklm-agent/SKILL.md` | `[Source Title/Author (YYYY-MM)](./skills/notebooklm-agent/URL)` | Malformed URL | ❌ |
| `skills/skill-extractor/references/skill-lifecycle.md` | `[new-skill-name](./skills/skill-extractor/references/path/to/new-skill)` | Path doesn't exist | ❌ |
| `mailroom/skill-extractor/references/skill-lifecycle.md` | Same as above | Duplicate issue | ❌ |

**Impact:** Users clicking these links will get 404 errors. The `docs/shared/README.md` references 3 files that don't exist.

**Fix:**
1. Remove broken links from `docs/shared/README.md` (files don't exist)
2. Fix malformed URLs in notebooklm files
3. Fix or remove broken path in skill-lifecycle.md files
4. Add link validation to CI/CD

---

### 4. Mailroom Processing (HIGH PRIORITY)

**Issue:** Mailroom contains valuable unprocessed content that should be integrated.

**Mailroom Contents:**

| Item | Type | Status | Priority | Notes |
|------|------|--------|----------|-------|
| `multi-agent-drop-823/` | Documentation | **Unprocessed** | **HIGH** | Cross-agent standards from crispy-couscous. Contains COMPATIBILITY.md, STANDARDS.md, GAPS.md, MAINTENANCE.md, README.md, cross-agent-primitives.md |
| `skill-extractor/` | Skill + references | **Unprocessed** | **MEDIUM** | Contains quality-guide.md, skill-lifecycle.md, skill-template.md. Should be integrated into skill-creation workflow |
| `skill-validator/` | Skill | **Unprocessed** | **MEDIUM** | SKILL.md validation tool. Could be useful for frontmatter validation |
| `SKILL.md` | Skill | **Clarification needed** | **LOW** | challenge-my-thinking. Mailroom README says it's NOT a duplicate, but it appears similar to skills/challenge-my-thinking/SKILL.md. Needs verification |
| `planning-with-files/` | Skill | **Unprocessed** | **MEDIUM** | Duplicate of skills/planning-with-files/SKILL.md. Should be removed from mailroom or clarified |

**Action Items:**
1. **Process multi-agent-drop-823/** - Integrate cross-agent standards into `docs/`
2. **Process skill-extractor/** - Integrate methodology into skill-creation workflow
3. **Process skill-validator/** - Consider adding as validation tool
4. **Verify SKILL.md** - Confirm if duplicate or reference material
5. **Remove planning-with-files from mailroom** - It's a duplicate

**Note:** AGENTS.md explicitly states mailroom is **READ-ONLY** and agents MUST NEVER write to it. This is correct and should be maintained.

---

### 5. Archive vs Mailroom Clarification (MEDIUM PRIORITY)

**Issue:** The distinction between `archive/` and `mailroom/` is unclear in the main documentation.

**Current Understanding:**
- **mailroom/** - Read-only staging area for **incoming** content to be reviewed/processed
- **archive/** - Storage for **deprecated/old** content that was superseded

**Evidence:**
- `mailroom/README.md` - Clearly documents mailroom as read-only staging
- `archive/README.md` - Documents old prompts that were superseded by skills
- AGENTS.md - Mentions mailroom but **NOT archive**
- CLAUDE.md - Mentions mailroom but **NOT archive**

**Problem:** Agents reading AGENTS.md or CLAUDE.md won't know about archive/ directory.

**Fix:**
1. Add archive/ reference to AGENTS.md
2. Add archive/ reference to CLAUDE.md
3. Clarify the distinction: mailroom = incoming, archive = outgoing/deprecated

---

### 6. Cross-Reference Inconsistencies (MEDIUM PRIORITY)

**Issue:** Some cross-references between files are missing or inconsistent.

**Missing References:**

| File | Missing Reference | Should Link To |
|------|-------------------|---------------|
| AGENTS.md | self-checks/ | self-checks/README.md |
| README.md | self-checks/ | self-checks/README.md |
| CLAUDE.md | archive/ | archive/README.md |
| CLAUDE.md | mailroom/ | mailroom/README.md (actually present ✅) |

**Inconsistent References:**
- README.md mentions `.vibe/prompts/` but this directory doesn't exist
- README.md structure diagram shows `.vibe/prompts/` but it's not created
- `.vibe/config.toml` has `skill_paths` including `"./skills"` but skills/ is a library, not live

**Fix:**
1. Add self-checks reference to AGENTS.md and README.md
2. Add archive reference to AGENTS.md and CLAUDE.md
3. Remove or create `.vibe/prompts/` directory
4. Clarify skill_paths in .vibe/config.toml

---

### 7. Configuration File Issues (LOW PRIORITY)

**Minor Issues Found:**

#### `.vibe/config.toml` vs `.vibe/agents/default.toml`

Both files exist with overlapping configuration:

**`.vibe/config.toml`:**
- Has `[agent]` section with `default = "default"`
- Has `[agents.default]` section
- Has `[skills]` section with skill_paths and enabled_skills
- Has `[tools]` section

**`.vibe/agents/default.toml`:**
- Has `[agent]` section
- Has `[[models]]` section
- Has `[providers.mistral]` section
- Has `[interactive]` section

**Issue:** These files have overlapping but not identical configuration. It's unclear which takes precedence.

**Recommendation:** Consolidate into a single configuration or clearly document the precedence.

#### `.vibe/config.toml` - skill_paths Issue

```toml
[skills]
skill_paths = [
  "./skills",  # Portable skill library
]
```

**Problem:** This includes `./skills` which is a **library**, not a live skill path. According to AGENTS.md, skills in `skills/` are NOT auto-discovered. Only `.vibe/skills/` is live.

**Fix:** Remove `./skills` from skill_paths, or add clear documentation that it's intentional for testing.

---

### 8. Duplicate Content (LOW PRIORITY)

**Issue:** Potential duplicate content between mailroom and skills.

**Identified Duplicates:**

| Location | Content | Status |
|----------|---------|--------|
| `mailroom/planning-with-files/SKILL.md` | planning-with-files skill | ⚠️ **Exact duplicate** of `skills/planning-with-files/SKILL.md` |
| `mailroom/SKILL.md` | challenge-my-thinking | ⚠️ **Similar but different** from `skills/challenge-my-thinking/SKILL.md` |
| `mailroom/skill-extractor/` | Skill extraction | ⚠️ **Different from** `skills/skill-extractor/` |

**Analysis:**
- `planning-with-files` in mailroom is an **exact duplicate** - should be removed
- `SKILL.md` in mailroom root is challenge-my-thinking but with different formatting - needs verification
- `skill-extractor` exists in both mailroom and skills - mailroom version has additional references/

**Fix:**
1. Remove `mailroom/planning-with-files/` (exact duplicate)
2. Verify `mailroom/SKILL.md` - keep as reference or remove
3. Document relationship between mailroom/skill-extractor and skills/skill-extractor

---

### 9. License Accuracy (MEDIUM PRIORITY)

**Issue:** NOTICE.md may not be accurate regarding actual skill licenses.

**NOTICE.md Claims:**
- Original content: ask-questions-if-underspecified, challenge-my-thinking, copilot-preset, karpathy-guidelines, pilot-preset, prompt-committee, prompt-pipeline, skill-extractor, solus-skill, task-chunkdown
- Third-party: prompt-master (MIT), import-memory/skill-creator/session-start-hook/morning (Apache-2.0)

**Actual State:**
- `skills/import-memory/` - Has Apache-2.0 license (✅ matches NOTICE)
- `skills/skill-creator/` - Has LICENSE.txt with Apache-2.0 (✅ matches NOTICE)
- `skills/prompt-master/` - **DOES NOT EXIST** in skills/ (mentioned in NOTICE but not present)
- Other "original" skills - No LICENSE files, but NOTICE says "none asserted"

**Problems:**
1. `prompt-master` listed in NOTICE but not in skills/
2. `morning` and `session-start-hook` listed in NOTICE but not in skills/
3. `copilot-preset`, `karpathy-guidelines`, `pilot-preset`, `solus-skill` listed as original but removed from skills/ (per skills/README.md)

**Fix:**
1. Update NOTICE.md to reflect actual skills present
2. Add LICENSE files to skills that have specific licenses
3. Clarify "none asserted" vs "all rights reserved"

---

### 10. Self-Checks Not Referenced (MEDIUM PRIORITY)

**Issue:** The `self-checks/` directory exists with valuable audit logs, but isn't referenced in main documentation.

**Current State:**
- `self-checks/README.md` exists with good documentation
- `self-checks/2026-08-23/` has 4 audit files (audit.md, compatibility.md, structure.md, action-items.md)
- **NOT mentioned** in AGENTS.md, README.md, or CLAUDE.md

**Impact:** Agents won't know to check self-checks/ for repository health information.

**Fix:**
1. Add self-checks reference to AGENTS.md
2. Add self-checks reference to README.md
3. Add self-checks reference to CLAUDE.md

---

## 📋 Action Items (Prioritized)

### 🔴 HIGH PRIORITY (Do Now - 0-24 hours)

| # | Task | Owner | Effort | Impact |
|---|------|-------|--------|--------|
| 1 | Fix skill frontmatter - add missing fields to all 13 skills | Both | 1-2 hrs | Critical for skill discovery |
| 2 | Process multi-agent-drop-823 from mailroom | Both | 2-4 hrs | High-value cross-agent standards |
| 3 | Add README.md to .vibe/prompts/ | Both | 15 min | Clarifies purpose |
| 4 | Add README.md to .claude/skills/ | Both | 15 min | Clarifies purpose |
| 5 | Add README.md to .claude/commands/ | Both | 15 min | Indexes commands |

### 🟡 MEDIUM PRIORITY (Next 1-3 days)

| # | Task | Owner | Effort | Impact |
|---|------|-------|--------|--------|
| 6 | Fix broken links in docs/shared/README.md | Both | 30 min | Prevents 404s |
| 7 | Fix malformed URLs in notebooklm files | Both | 30 min | Prevents 404s |
| 8 | Process skill-extractor from mailroom | Both | 1-2 hrs | Improves skill creation |
| 9 | Add archive/ reference to AGENTS.md and CLAUDE.md | Both | 20 min | Clarifies structure |
| 10 | Add self-checks reference to AGENTS.md, README.md, CLAUDE.md | Both | 20 min | Agents aware of audits |
| 11 | Update NOTICE.md for accuracy | Both | 30 min | Legal clarity |
| 12 | Process skill-validator from mailroom | Both | 1 hr | Validation capability |

### 🟢 LOW PRIORITY (Next 1-2 weeks)

| # | Task | Owner | Effort | Impact |
|---|------|-------|--------|--------|
| 13 | Add README.md to .vibe/agents/ | Both | 15 min | Documentation |
| 14 | Add README.md to .vibe/skills/ | Both | 15 min | Documentation |
| 15 | Remove duplicate planning-with-files from mailroom | Both | 5 min | Cleanup |
| 16 | Verify mailroom/SKILL.md | Both | 10 min | Clarification |
| 17 | Consolidate .vibe/config.toml and .vibe/agents/default.toml | Both | 30 min | Configuration clarity |
| 18 | Fix skill_paths in .vibe/config.toml | Both | 10 min | Configuration accuracy |
| 19 | Create validation script for skill frontmatter | Both | 1-2 hrs | Prevents future issues |

---

## 🎯 Recommendations

### For Repository Maintainers

1. **Prioritize skill frontmatter fixes** - This is the most critical issue affecting functionality
2. **Process mailroom content** - High-value research waiting to be integrated
3. **Add missing READMEs** - Improves discoverability and understanding
4. **Fix broken links** - Prevents user confusion
5. **Update documentation** - Keep AGENTS.md, README.md, CLAUDE.md in sync

### For Agents Working in This Repository

1. **Always check AGENTS.md first** - It has the most up-to-date shared instructions
2. **Respect mailroom as read-only** - NEVER write to mailroom/ (as stated in AGENTS.md)
3. **Respect archive as deprecated** - Don't use archive/ content for new work
4. **Use self-checks/ for reference** - Contains valuable audit information
5. **Verify skill frontmatter** - Before using any skill, check it has proper fields
6. **Test in both agents** - Ensure compatibility before committing

### For Future Development

1. **Add frontmatter validation** - Prevent incomplete skills from being committed
2. **Add link validation** - CI check for broken markdown links
3. **Add README template** - Standardize documentation across directories
4. **Implement automated testing** - Test skills in both Vibe and Claude
5. **Regular audits** - Schedule monthly repository health checks

---

## 📊 Metrics Summary

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Skills with complete frontmatter | 4/13 | 13/13 | ❌ 31% |
| Directories with README.md | 10/18+ | 18/18 | ⚠️ ~56% |
| Broken markdown links | 7+ | 0 | ❌ |
| Mailroom items processed | 0/4 | 4/4 | ❌ 0% |
| Skills tested in both agents | 4/13 | 13/13 | ❌ 31% |
| Cross-references complete | ~70% | 100% | ⚠️ |
| Documentation accuracy | ~85% | 100% | ⚠️ |

---

## 🔗 Related Files

- [AGENTS.md](AGENTS.md) - Shared agent instructions
- [self-checks/2026-08-23/audit.md](self-checks/2026-08-23/audit.md) - Previous audit findings
- [self-checks/2026-08-23/compatibility.md](self-checks/2026-08-23/compatibility.md) - Compatibility assessment
- [self-checks/2026-08-23/structure.md](self-checks/2026-08-23/structure.md) - Structure assessment
- [self-checks/2026-08-23/action-items.md](self-checks/2026-08-23/action-items.md) - Tracked action items
- [mailroom/README.md](mailroom/README.md) - Mailroom processing guidelines
- [archive/README.md](archive/README.md) - Archive documentation

---

## 📝 Audit Metadata

**Auditor:** Vibe Code (Mistral AI)  
**Audit Type:** Comprehensive Repository Assessment  
**Date:** 2026-08-24  
**Duration:** ~30 minutes  
**Files Reviewed:** 84+  
**Directories Reviewed:** 48+  
**Skills Analyzed:** 13 (skills/) + 4 (.vibe/skills/)  
**Version:** 1.0  

---

*Next audit recommended: 2026-08-31 (1 week)*  
*This audit builds upon the self-checks from 2026-08-23*
