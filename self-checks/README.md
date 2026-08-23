# Self-Checks

> **Purpose:** Dated audit logs for repository self-assessment. Both Mistral Vibe Code and Claude Code can read these to understand what needs improvement.

---

## 📁 Structure

```
self-checks/
├── README.md                    # This file
├── 2026-08-23/                 # Date-based audit logs (YYYY-MM-DD)
│   ├── audit.md                # General audit findings
│   ├── action-items.md         # Prioritized next steps
│   ├── structure.md            # Repository structure assessment
│   └── compatibility.md         # Cross-agent compatibility check
└── [future dates]/
    ├── audit.md
    ├── action-items.md
    └── [additional audits]
```

---

## 🎯 Audit Types

### General Audit (`audit.md`)
Comprehensive assessment of the entire repository:
- Repository structure correctness
- File organization and naming
- Documentation completeness
- Skill format compliance
- Cross-agent compatibility
- Mailroom contents review

### Structure Audit (`structure.md`)
Focused on directory layout and organization:
- Directory structure validation
- File location appropriateness
- README.md completeness
- Symlink integrity
- Discovery path configuration

### Compatibility Audit (`compatibility.md`)
Focused on cross-agent compatibility:
- Tool name consistency
- Skill frontmatter validation
- Agent configuration correctness
- Cross-tool workflow verification
- Compatibility field completeness

---

## 📊 Audit Format

Each audit log follows this structure:

### Header
```markdown
# Audit: [Type] - [Date]

**Auditor:** [Agent Name]
**Date:** [YYYY-MM-DD]
**Scope:** [What was audited]
```

### Summary Section
```markdown
## Summary

**Overall Status:** [Pass/Needs Work/Critical]
**Issues Found:** [count]
**Critical Issues:** [count]
**High Priority:** [count]
**Medium Priority:** [count]
**Low Priority:** [count]

**Overall Assessment:** [Brief summary]
```

### Findings Sections
```markdown
## Findings

### ✅ Pass (Working Correctly)
- [x] [Finding]

### ⚠️ Needs Work (Should Fix)
- [ ] [Finding] - [Impact] - [Priority]

### ❌ Critical (Must Fix)
- [ ] [Finding] - [Impact] - [Priority]
```

### Action Items Table
```markdown
## Action Items

| Priority | Task | Owner | Status | Notes |
|----------|------|-------|--------|-------|
| High | [Task] | [Agent] | [Open/In Progress/Done] | [Notes] |
```

### Next Steps
```markdown
## Next Steps (Prioritized)

### Immediate (Do Now)
1. [Task]

### Short Term (Next 1-3 days)
1. [Task]

### Medium Term (Next 1-2 weeks)
1. [Task]

### Long Term (Ongoing)
1. [Task]
```

---

## 📅 Audit Schedule

| Audit Type | Frequency | Next Due | Owner |
|------------|-----------|----------|-------|
| General Audit | Weekly | 2026-08-30 | Both agents |
| Structure Audit | Bi-weekly | 2026-09-06 | Both agents |
| Compatibility Audit | Weekly | 2026-08-30 | Both agents |
| Full Review | Monthly | 2026-09-23 | Both agents |

---

## 📈 Current Status

**Last Audit:** 2026-08-23
**Auditor:** Mistral Vibe Code

### Summary
- **General Audit:** ⚠️ Needs Work (12 issues, 0 critical)
- **Structure Audit:** ✅ Good (4 issues, 0 critical)
- **Compatibility Audit:** ⚠️ Needs Work (8 issues, 0 critical)

### Progress
- **Action Items Created:** 14
- **Action Items Completed:** 3 (21%)
- **Action Items Open:** 11 (79%)

### Top Priorities
1. ✅ Add mailroom reference to CLAUDE.md - **DONE**
2. ✅ Add self-checks reference to AGENTS.md - **DONE**
3. ✅ Add self-checks reference to README.md - **DONE**
4. ⏳ Process multi-agent-drop-823 content - **NEXT**
5. ⏳ Fix skill frontmatter consistency
6. ⏳ Deduplicate skills

---

## 🔍 How to Use

### For Both Agents

1. **Before starting work:** Check `self-checks/[latest-date]/audit.md` for current issues
2. **When adding content:** Review `compatibility.md` for format requirements
3. **When organizing:** Review `structure.md` for directory guidelines
4. **After completing work:** Update `action-items.md` with progress
5. **Regularly:** Run new audits and save to dated directories

### For Repository Maintainers

1. **Review audit logs weekly** - Check for new issues
2. **Monitor action items** - Track progress on identified issues
3. **Prioritize based on audit findings** - Focus on high-impact items
4. **Run audits before major changes** - Ensure compatibility

---

## 📝 Audit Index

| Date | Type | Status | Issues | Action Items | Auditor |
|------|------|--------|--------|--------------|---------|
| 2026-08-23 | General | ⚠️ Needs Work | 12 | 14 | Mistral Vibe Code |
| 2026-08-23 | Structure | ✅ Good | 4 | 3 | Mistral Vibe Code |
| 2026-08-23 | Compatibility | ⚠️ Needs Work | 8 | 8 | Mistral Vibe Code |

---

## 🎨 Conventions

### File Naming
- Use `YYYY-MM-DD` format for date directories
- Use lowercase with hyphens for file names
- Use `.md` extension for all audit files

### Status Indicators
- ✅ **Pass** - Working correctly, no action needed
- ⚠️ **Needs Work** - Should fix, but not blocking
- ❌ **Critical** - Must fix, blocking functionality

### Priority Levels
- **Critical** - Blocks functionality, must fix immediately
- **High** - Important, should fix within 1-3 days
- **Medium** - Nice to have, should fix within 1-2 weeks
- **Low** - Cosmetic, fix when convenient

---

## 🔗 Related Files

- [AGENTS.md](../AGENTS.md) - Shared instructions (references self-checks)
- [CLAUDE.md](../CLAUDE.md) - Claude-specific instructions (references mailroom)
- [README.md](../README.md) - Repository overview (references audit logs)
- [mailroom/README.md](../mailroom/README.md) - Mailroom processing guidelines

---

*Last updated: 2026-08-23*
