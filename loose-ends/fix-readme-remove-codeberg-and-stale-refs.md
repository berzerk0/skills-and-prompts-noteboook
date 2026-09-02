# Loose ends — crispy-couscous

**Repository:** berzerk0/crispy-couscous
**Branch:** fix/readme-remove-codeberg-and-stale-refs
**Commit:** 57ca601
**Uncommitted changes:** none

This covers all work I did in this repo this session, including
fix/generator-symlink-bug, which is already merged into `main` via PR #10
(commit a451178), per the user's instruction to file on my current branch
only rather than reopening merged branches.

## What I decided that never got written down

- On `fix/generator-symlink-bug`, I verified the `write_file()`
  symlink-guardrail (the code that's supposed to refuse a write through
  `.claude/skills/`, `.pi/skills/`, `.vibe/skills/`) by tracing the Python
  logic by hand, not by actually attempting a malicious write and watching
  it raise `RuntimeError`. The PR body says "Verified clean," which is true
  for the happy path (generators don't touch `skills/` on a normal run) --
  it does not mean I executed a test that proves the guardrail itself
  fires. That distinction isn't written anywhere.
- While removing `codeberg.yaml` from `docs/SKILL_DESIGN.md`'s "Future:
  Generation Scripts (Planned, not yet implemented)" section, I noticed
  that whole section is itself stale -- `meta/generate_*.py` already
  exists and is implemented, contradicting "Planned." I judged fixing that
  out of scope for a codeberg-removal pass and moved on without flagging it
  anywhere else.

## What I started and abandoned

Nothing abandoned. Both PRs (#10, #11) are complete for what they set out
to do.

## What I learned that is not in any file

- `git push --delete` on this repo failed once with a GitHub 403 (Claude
  GitHub App apparently not authorized for push on this specific
  operation, even though ordinary commits/PRs worked fine), then succeeded
  on retry with no config change I could see. I never got a real root
  cause -- just a symptom and a workaround (retry, or the user's manual
  `gh api -X DELETE` fallback). Don't assume delete is now reliably
  enabled just because it worked once.
- There are three different "agent instructions" files in this repo, not
  two: root `AGENTS.md`, `docs/AGENTS.md`, and `.vibe/AGENTS.md`. I flagged
  the first two as an unreconciled duplicate pair in the README (PR #11),
  but I only ever touched `.vibe/AGENTS.md` to strip one codeberg bullet
  line out of it -- I never compared its full content against the other
  two. There may be a three-way duplication problem, not the two-way one
  I documented.

## What I did that a later reader would misread

- PR #11's test-plan checkboxes (grep returns nothing, generator runs
  clean, CI passes) are unchecked. I ran the grep and the generator myself
  in the sandbox and confirmed both -- I did not watch the actual GitHub
  Actions run on this PR go green. "Verified clean" in the PR body means
  local verification, not an observed CI pass.
- I treated `fix/generator-symlink-bug`'s premise -- that a real incident
  on 2026-08-24 flattened all 14 `SKILL.md` files to stubs by writing
  through symlinks -- as fact, and reviewed the fix on its own technical
  merits (which are sound: I traced the guardrail logic and it's correct).
  I did not independently verify the incident itself happened as
  described. That's a different standard than I applied to this same
  narrative's sibling on the notebook repo, where I treated an unverified
  incident story as reason for skepticism rather than as a given. The
  difference is defensible -- this fix is independently checkable by
  reading the code regardless of whether the origin story is exactly
  accurate -- but a later reader shouldn't assume I fact-checked the
  incident itself.
