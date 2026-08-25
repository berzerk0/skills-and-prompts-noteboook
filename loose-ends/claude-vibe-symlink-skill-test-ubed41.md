# Loose ends — claude/vibe-symlink-skill-test-ubed41

## Mechanical facts (from git, checked not recalled)

- Repository: berzerk0/skills-and-prompts-noteboook
- Branch: claude/vibe-symlink-skill-test-ubed41
- HEAD: fedae91071c0426fb1dbae10c997cc433e2963a7
- Uncommitted changes: none
- Recent commits recognized as mine: "Test: mirror time-estimate symlink into
  .vibe/skills/" and "Test: symlink skills/time-estimate into .claude/skills/".
  Everything below those in the log (mailroom docs, audit logs, AGENTS.md
  changes) predates this session and is not mine.
- No mismatch between what git shows and what I expected.

## What I decided that never got written down

I pointed the new `.vibe/skills/time-estimate` symlink at
`../../skills/time-estimate` directly (same target as the pre-existing
`.claude/skills/time-estimate` symlink), rather than chaining it through
`.claude/skills/time-estimate`. The idea was to keep both symlink trees
independently resolving to the canonical source in `skills/`, in case one
tree gets evaluated in isolation later. This wasn't discussed or deliberated
anywhere — it's just the choice I made — so it's only recorded here now.

## What I started and abandoned

Nothing was abandoned. Both symlink tests (Claude Code's `.claude/skills/`
and the `.vibe/skills/` mirror for a hypothetical Vibe session) were run to
completion and their results reported in chat. The one gap: the test
conclusions lived only in the chat transcript until this loose-ends report —
no file previously captured them.

## What I learned that isn't in any file

- Claude Code's Skill tool follows a symlinked skill directory identically
  to a real one — loaded the full real SKILL.md content, no special-casing,
  no failure, no unexpected behavior.
- There is no `vibe` binary available in this Claude Code session/container,
  so Vibe's own skill-discovery behavior for `.vibe/skills/` could NOT be
  verified from here. That test needs to run from an actual Vibe session —
  the `.vibe/skills/time-estimate` symlink is in place and ready for it, but
  unverified from the Vibe side.

## What could be misread by a later reader

The two "Test:" commits leave real symlinks in the tree
(`.claude/skills/time-estimate` and `.vibe/skills/time-estimate`), and
nothing in the tree marks them as test artifacts. A later reader might
assume they're intentional permanent structure rather than a one-off
discovery check. They're harmless as-is (both resolve to real content), but
worth knowing they were added to answer a specific question, not as part of
a larger skills-packaging decision.
