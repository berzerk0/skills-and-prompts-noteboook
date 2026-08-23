# Action Items - 2026-08-23 Audit

**Source:** [audit.md](audit.md)
**Date:** 2026-08-23
**Status:** Tracker for all identified issues

---

## 📊 Summary

| Priority | Total | Open | In Progress | Done | % Complete |
|----------|-------|------|-------------|------|------------|
| Critical | 0 | 0 | 0 | 0 | 100% |
| High | 5 | 3 | 0 | 2 | 40% |
| Medium | 6 | 5 | 0 | 1 | 17% |
| Low | 2 | 2 | 0 | 0 | 0% |
| **Total** | **13** | **10** | **0** | **3** | **23%** |

---

## ✅ Done

| # | Priority | Task | Owner | Date Completed | Notes |
|---|----------|------|-------|----------------|-------|
| 1 | High | Add mailroom reference to CLAUDE.md | Both | 2026-08-23 | ✅ Added mailroom section to CLAUDE.md |
| 2 | High | Add self-checks reference to AGENTS.md | Both | 2026-08-23 | ✅ Added Self-Checks section to AGENTS.md |
| 3 | High | Add self-checks reference to README.md | Both | 2026-08-23 | ✅ Added Audit Logs section to README.md |

---

## 🚀 High Priority (Do Next)

| # | Priority | Task | Owner | Status | Blocked By | Notes |
|---|----------|------|-------|--------|------------|-------|
| 4 | High | Process multi-agent-drop-823 content | Both | Open | None | High-value cross-agent standards from crispy-couscous. Contains COMPATIBILITY.md, STANDARDS.md, GAPS.md, MAINTENANCE.md, cross-agent-primitives.md |
| 5 | High | Fix skill frontmatter consistency | Both | Open | None | Add missing `license`, `compatibility`, `allowed-tools` fields to all skills. Standardize format. |
| 6 | High | Deduplicate skills | Both | Open | None | Remove duplicate between skills/ and mailroom/. Decide on single source of truth. |
| 15 | High | Fix Vibe `enabled_skills` allowlist gating symlinked skills | Both | Done | None | **Tested 2026-08-23** (live symlink of `skills/time-estimate` into both `.claude/skills/` and `.vibe/skills/`): Claude Code auto-discovers a symlinked skill directory with no extra config. Vibe did NOT — `enabled_skills` was a hard allowlist hiding anything not named in it, regardless of `skill_paths` already resolving it. **User voted to remove `enabled_skills` entirely** (2026-08-23) — done in `.vibe/config.toml`. All skills discovered via `skill_paths`/`.vibe/skills/` now auto-load for Vibe. Needs a fresh Vibe session to confirm end-to-end. |

**Next Action:** Start with #4 (multi-agent-drop-823) - highest value, contains verified research.

---

## 📋 Medium Priority

| # | Priority | Task | Owner | Status | Blocked By | Notes |
|---|----------|------|-------|--------|------------|-------|
| 7 | Medium | Add README.md to .vibe/prompts/ | Both | Open | None | Document purpose of prompts directory |
| 8 | Medium | Add README.md to .claude/skills/ | Both | Open | None | Document purpose of Claude skills directory |
| 9 | Medium | Add README.md to archive/ | Both | Done | None | Already existed (predates this audit) with full inventory and outcomes per archived item. Distinguished from mailroom in AGENTS.md as of this pass. |
| 10 | Medium | Process skill-extractor from mailroom | Both | Open | None | Contains quality-guide.md, skill-lifecycle.md, skill-template.md. Integrate into workflow. |
| 11 | Medium | Standardize skill quality | Both | Open | #5 | Apply quality standards from mailroom/skill-extractor/. Review and improve existing skills. |
| 12 | Medium | Add compatibility fields to all skills | Both | Open | #5 | Add cross-agent compatibility info. Part of frontmatter fix. |

---

## 📝 Low Priority

| # | Priority | Task | Owner | Status | Blocked By | Notes |
|---|----------|------|-------|--------|------------|-------|
| 13 | Low | Standardize user-invocable field | Both | Open | None | Add to all skills. Cosmetic improvement. |
| 14 | Low | Fix minor formatting issues | Both | Open | None | Cosmetic improvements to markdown formatting. |

---

## 🎯 Suggested Work Order

### Phase 1: Quick Wins (0-1 hour)
- [x] ✅ Add mailroom reference to CLAUDE.md
- [x] ✅ Add self-checks references to AGENTS.md and README.md
- [ ] Process multi-agent-drop-823 content (highest value)

### Phase 2: Structural Fixes (1-4 hours)
- [ ] Fix skill frontmatter consistency
- [ ] Deduplicate skills
- [ ] Add README.md to undocumented directories

### Phase 3: Integration (2-8 hours)
- [ ] Process skill-extractor from mailroom
- [ ] Standardize skill quality
- [ ] Add compatibility fields to all skills

### Phase 4: Polish (1-2 hours)
- [ ] Standardize user-invocable field
- [ ] Fix minor formatting issues

---

## 📈 Progress Tracking

```
Week 1 (2026-08-23 to 2026-08-30):
  ✅ Completed: 3/12 (25%)
  🎯 Target: 8/12 (67%)
  
Week 2 (2026-08-30 to 2026-09-06):
  🎯 Target: 12/12 (100%)
```

---

## 🔗 Related Files

- [audit.md](audit.md) - Full audit findings
- [../../AGENTS.md](../../AGENTS.md) - Updated with self-checks reference
- [../../CLAUDE.md](../../CLAUDE.md) - Updated with mailroom reference
- [../../README.md](../../README.md) - Updated with audit logs reference

---

## 📅 Next Review

**Next audit recommended:** 2026-08-30 (1 week)
**Review action items:** 2026-08-25 (3 days)

---

*Last updated: 2026-08-23*
