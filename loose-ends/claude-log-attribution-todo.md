# Loose ends — skills-and-prompts-noteboook

**Repository:** berzerk0/skills-and-prompts-noteboook
**Branch:** claude/log-attribution-todo
**Commit:** 348b1a9
**Uncommitted changes:** none

This covers all work I did in this repo this session, including
claude/version-reconciliation-review-jvzxfw, which is already merged into
`main` via PR #3 (commit f3ae634), per the user's instruction to file on my
current branch only rather than reopening merged branches.

## What I decided that never got written down

The judgment call that "the SDK/Core three-tier architecture" investigation
in `docs/vibe/TOOL_VERSION_INCONSISTENCY_AUDIT.md` was fabricated, not
merely unverified, rests on a pattern I never wrote out explicitly anywhere:
`docs/vibe/internals.md` earns trust because it cites a pinned commit hash
and `file:line` for every claim; the newer investigation earns distrust
because it makes more specific claims (exact file paths, an
`/opt/app/vibe_agents/` base path, a `sandbox_dispatch.py` tuple) with zero
citations, plus the runtime version shifted three times across documents
(v2.7.0 -> v2.9.4 -> v2.24.3) with increasing confidence each time. The
conclusion is in `CLAUDE_RESPONSE_VERSION_RECONCILIATION.md`; the "why
increasing specificity without citations is itself the red flag" reasoning
only exists in our conversation.

## What I started and abandoned

Nothing abandoned. The one open thread — verifying `docs/multi-agent/
COMPATIBILITY.md`'s technical claims before merging it — was never started
by design; it's explicitly deferred to its own future PR in
`self-checks/2026-08-24/MERGER_PLAN.md`, not silently dropped.

## What I learned that is not in any file

- `git push --delete` on a branch can fail two different ways that look
  similar but aren't: a genuine GitHub 403 (the Claude GitHub App not
  installed/authorized for push on that repo -- happened once on couscous,
  resolved itself on retry with no config change I could observe) versus
  the harness's own auto-mode permission classifier blocking the delete
  outright and demanding fresh per-turn confirmation (happened on this
  repo's `vibe/errors-2026-08-24`). Retrying blindly only fixes the first
  kind. Neither branch has actually been deleted yet -- both deletions are
  still pending, one on GitHub's side, one on the user's explicit
  confirmation.
- Pushing a new branch in this environment can trigger the Claude Code web
  UI to auto-create a PR for it, independent of anything I do. This
  happened twice (PR #3, PR #4) -- I didn't call any PR-creation tool
  either time; the notification just arrived after the push.

## What I did that a later reader would misread

- `self-checks/2026-08-24/MERGER_PLAN.md` reads as an active plan with a
  suggested execution order, but none of its four PRs (GAPS.md,
  STANDARDS.md, MAINTENANCE.md, COMPATIBILITY.md) have been started. The
  source files are untouched in `mailroom/multi-agent-drop-823/`. The
  confident, ordered tone of the plan could read as "in progress" when
  it's "not started."
- `docs/vibe/TOOL_VERSION_INCONSISTENCY_AUDIT.md` is thoroughly rejected in
  `CLAUDE_RESPONSE_VERSION_RECONCILIATION.md`, but the rejected file itself
  is still sitting on the (still-live, undeleted) `vibe/errors-2026-08-24`
  branch. Anyone who checks out that branch directly, without also reading
  `self-checks/2026-08-24/`, will find the fabricated investigation with no
  visible pointer to its rebuttal.
- The skill-attribution TODO in `self-checks/2026-08-24/action-items.md` is
  logged as "Open" with a description of the problem, but zero actual
  scoping happened -- I didn't check even one skill's real origin. It
  reads as a defined task; it's really just a flagged concern.
