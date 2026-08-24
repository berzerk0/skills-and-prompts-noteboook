# Vibe Session Follow-up: Action Items

**Written by:** Claude Code (validate-mistral-patches branch)  
**Date:** 2026-08-24  
**Context:** Post-mortem of the vibe/errors-2026-08-24 session (commits 96ef7e3 and 79c8e4a)  
**Status:** Awaiting implementation -- do not merge those commits as-is

---

## What Actually Happened in That Session

The session tried to use a tool called `search_replace` to edit files. That tool
does not exist in Vibe. The correct tool is `edit`. When `search_replace` was
called, Vibe returned an error that looked like "file not found" -- a misleading
error message for an unknown tool name.

The agent interpreted "file not found" as evidence that the file editing system
was broken, concluded `edit`/`search_replace` was entirely non-functional, and
spent the rest of the session building workarounds for a problem that did not
exist.

Critically: AGENTS.md (always-resident in Vibe, every turn) explicitly states:

> "Tool names differ. `Edit`->`edit`... Any `allowed-tools` list in a skill's
> frontmatter needs translating... Vibe silently drops unrecognized tool names."

The agent had this in its system prompt and still called `search_replace`.

---

## Action Items

### 1. Report to Mistral (priority: high)

Two real bugs worth reporting, framed as a compound failure:

**Bug A -- Misleading error for unknown tool names**  
Calling a non-existent tool returns "file not found" rather than "unknown tool"
or similar. This is the proximate cause of the misdiagnosis: the agent could not
tell the difference between "file does not exist" and "tool does not exist."

**Bug B -- write_file context-overflow silently drops content (issue #667)**  
When context fills mid-edit, write_file produces a partial file rewrite, drops
the rest, but reports success. The workaround doc from that session recommends
write_file + cp as the safe fallback -- which walks directly into this bug.
The compound effect: misleading error -> wrong diagnosis -> workaround that has
its own data-loss bug.

Include the Vibe version the session ran on (check the session logs). The
skills-not-loading bug in v2.7.0 (issue #545) may be part of the story too --
if skills were silently failing to load, that would explain why `vibe-internals`
wasn't consulted even if the agent tried.

---

### 2. Fix FILE_EDITING_WORKAROUNDS.md (priority: high)

`scratchpad/FILE_EDITING_WORKAROUNDS.md` labels `search_replace` as BROKEN and
recommends a create-then-replace pattern using `write_file`. Both claims are
wrong or misleading:

- `search_replace` doesn't exist -- it was never the right tool
- `write_file` + copy is not a safe fallback; issue #667 shows it silently drops
  content on context overflow

The correct fix for file editing in Vibe is simply to use `edit`. If `edit` has
real limitations (unicode edge cases, large file handling), those should be
documented separately with accurate root causes -- not conflated with the wrong-
tool-name error.

---

### 3. Add a pre-edit verification step to AGENTS.md (priority: medium)

One directive to add: before attempting file edits in any session, verify the
tool name against the builtin list in `docs/vibe/internals.md`. The current
AGENTS.md has the translation table but no explicit "check this before you start"
instruction. A Vibe agent that reads AGENTS.md and then ignores the tool name
table suggests the instruction needs to be more imperative, not just informational.

Draft:
> "Before using any file-editing tool, confirm the tool name exists in the
> builtin list in `docs/vibe/internals.md`. Do not guess tool names or carry
> over names from Claude Code. Vibe silently drops unrecognized tool names
> with no error."

---

### 4. Capture the Vibe version (priority: medium, prerequisite for item 1)

The session logs for vibe/errors-2026-08-24 should contain the Vibe version.
Find it before writing the Mistral bug report -- version matters for both bugs.
If the session ran on v2.7.0, the skills bug (issue #545) may be relevant.
If it ran on an earlier version, the story is simpler: just the wrong tool name.

---

## Research Backing

All findings above were validated against:
- Repo docs: `docs/vibe/internals.md`, `docs/cross-tool-notes.md`,
  `skills/vibe-internals/SKILL.md`
- Official sources: docs.mistral.ai, mistral-vibe GitHub issue tracker
- Specific issue: github.com/mistralai/mistral-vibe/issues/667 (write_file
  context-overflow, confirmed real, affects v1.2.3 and v2.7.2)

Full research notes: `scratchpad/VALIDATION_RESEARCH.md` (scratchpad dir,
session-local, may not be committed)
