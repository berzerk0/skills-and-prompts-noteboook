# Findings: Audit Corrections & Multi-Agent Drop Processing

**Created:** 2026-08-23
**Skill Used:** planning-with-files (from mailroom)
**Agent:** Mistral Vibe Code

---

## Corrections from User Clarifications

### Finding 1: Mailroom is REFERENCE ONLY
**Source:** User clarification
**Impact:** CRITICAL - Changes how we count and treat mailroom contents
**Status:** VERIFIED

**Details:**
- mailroom/ is a read-only staging area for reference material
- mailroom/SKILL.md is NOT a duplicate of skills/challenge-my-thinking/SKILL.md
- It's just reference material, not viable/invocable skills
- Agents MUST NEVER write to mailroom/
- Already documented in AGENTS.md and CLAUDE.md

**Action Required:**
- Update audit.md to remove duplicate claim
- Update skill count to only count skills/ directory
- Update Mailroom Processing section

---

### Finding 2: Skill Count Correction
**Source:** User clarification
**Impact:** HIGH - Affects metrics accuracy
**Status:** VERIFIED

**Details:**
- Current audit counts mailroom items in skill count
- Should only count skills/ directory
- skills/ has 13 skills (confirmed by directory listing)
- mailroom/ contents should NOT be counted

**Action Required:**
- Update "Skills in library" metric from "13 (format issues)" to "13 (skills/ only)"
- Update any references to mailroom duplicates

---

### Finding 3: multi-agent-drop-823 Corrections (from Claude)
**Source:** User's Claude feedback
**Impact:** HIGH - Contains errors that need fixing before integration
**Status:** VERIFIED

**Issues Identified:**
1. **CONTRADICTION**: cross-agent-primitives.md claims Vibe's edit tool is `search_replace` - WRONG. It's `edit`
2. **External content**: Written for `berzerk0/crispy-couscous` repo - internal links point to non-existent paths
3. **New intel**: Pi Agent is real with specific conventions

**Action Required:**
- Fix search_replace error when integrating
- Add Pi Agent section to docs/cross-tool-notes.md
- Add script-first principle as documented convention
- Correct GAPS.md's claim about Vibe allowed-tools syntax

---

## New Intel: Pi Agent Conventions

**Source:** Claude's feedback on multi-agent-drop-823
**Status:** NEW - Needs integration

**Conventions:**
- Skills at `.pi/skills/` (cwd + ancestors) or `~/.pi/agent/skills/` (user)
- Tool names: `read`, `write`, `edit`, `bash`, `grep`, `find`, `ls`
- Natively supports `AGENTS.md`
- Allows skill name to mismatch directory name (unlike Claude/Vibe)
- No native subagents (extension-based only)

**Action Required:**
- Add Pi Agent section to docs/cross-tool-notes.md

---

## Script-First Principle

**Source:** Claude's feedback (flagged as unverified specifics)
**Status:** NEW - Needs integration

**Principle:** "Script-first, wrap-second" - write core logic as CLI scripts, invoke via `bash`, generate thin per-agent wrappers

**Action Required:**
- Add to docs/cross-tool-notes.md as documented convention
- Flag as unverified specifics

---

## Audit.md Specific Corrections Needed

### Section: Findings - Needs Work - High Priority

**Current (line ~47-51):**
```
2. **Duplicate content** - Some skills appear in both `skills/` and `mailroom/`
   - **Impact:** Confusion about which is canonical, potential for divergence
   - **Priority:** High
   - **Location:** mailroom/SKILL.md appears to duplicate skills/challenge-my-thinking/SKILL.md
   - **Issue:** Need to deduplicate and decide on single source of truth
```

**Corrected To:**
```
2. **Mailroom reference material** - mailroom/ contains reference-only content, not duplicates
   - **Impact:** None - mailroom is read-only staging, not viable skills
   - **Priority:** Low (documentation clarification)
   - **Location:** mailroom/ directory
   - **Note:** mailroom is REFERENCE ONLY per AGENTS.md and CLAUDE.md. Agents MUST NEVER write to mailroom/
```

---

### Section: Mailroom Processing

**Current (line ~240-245):**
```
1. `SKILL.md` - challenge-my-thinking (appears to be duplicate)
```

**Corrected To:**
```
1. `SKILL.md` - challenge-my-thinking (reference material, NOT a duplicate)
```

---

### Section: Metrics

**Current:**
```
| Skills in library | 13 | \u26a0\ufe0f (format issues) |
```

**Corrected To:**
```
| Skills in library | 13 | \u26a0\ufe0f (format issues, skills/ only) |
```

---

## Files Requiring Updates

### Priority 1: self-checks/2026-08-23/audit.md
- Remove duplicate claim
- Update mailroom description
- Update skill count clarification

### Priority 2: docs/cross-tool-notes.md
- Add Pi Agent section
- Add script-first principle
- Fix search_replace error reference

---

## Validation Checklist

- [ ] All mailroom references updated to "reference-only"
- [ ] Duplicate claim removed from audit.md
- [ ] Skill count clarified as "skills/ only"
- [ ] Pi Agent section added to cross-tool-notes.md
- [ ] Script-first principle documented
- [ ] search_replace error corrected in integrated content

---

*Last updated: 2026-08-23*
