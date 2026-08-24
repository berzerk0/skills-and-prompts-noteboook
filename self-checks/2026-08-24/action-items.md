# Action Items - 2026-08-24

**Status:** Tracker for follow-up work identified during the 2026-08-24
version-reconciliation review and merger scoping. Follows the format
established in `self-checks/2026-08-23/action-items.md`.

---

## Open

| # | Priority | Task | Repo(s) | Owner | Status | Notes |
|---|----------|------|---------|-------|--------|-------|
| 1 | Medium | Source skills that are adapted/borrowed from other developers' work, in comments | `skills-and-prompts-noteboook`, `crispy-couscous` | Either agent | Open | Almost all skills in both repos' `skills/` directories appear to be adapted from other authors' published work rather than written from scratch. Add attribution (author/source, and license if known) in a comment near the top of each affected `SKILL.md` — or a `source:`/`attribution:` frontmatter field if that fits the existing schema better. Needs a pass across both repos' skill libraries to identify which skills need it and find real sources, not just a blanket note. Raised by the user 2026-08-24; not yet scoped or started. |

---

## Resolved this session (for context, not new work)

- `claude/validate-mistral-patches-ipuxh1` (notebook): superseded — its action
  items (correct `FILE_EDITING_WORKAROUNDS.md`, preserve `audit_report_2026.md`,
  add pre-edit tool-name verification to `AGENTS.md`, discard
  `RECOVERY_PROCEDURE.md`) were all independently completed via the
  `vibe/errors-2026-08-24` merge and this session's own work. See conversation
  record; PR #2 recommended for closure without merging.
- `vibe/implementation-roadmap-4105aff` (couscous): stale — its real content
  already landed on `main` via the PR #9 merge commit; the unmerged branch tip
  is a stray commit that would fight with later fixes. Recommended for deletion.
