# Merger Gate: Version/Implementation Questions Resolved

**Date:** 2026-08-24
**Gates:** merger of `berzerk0/skills-and-prompts-noteboook` with
`berzerk0/crispy-couscous` (the source of `mailroom/multi-agent-drop-823/`)
**Status:** These three questions are resolved. See "What's still open" at the
bottom for what this document does *not* clear.

This document exists because the user identified these three questions as
blocking the notebook/couscous merger, following the review recorded in
`self-checks/2026-08-24/CLAUDE_RESPONSE_VERSION_RECONCILIATION.md`. That
review found that the elaborate "three-tier Vibe architecture" investigation
in `docs/vibe/TOOL_VERSION_INCONSISTENCY_AUDIT.md` was unverified and
contradicted the one source-verified reference in this repo
(`docs/vibe/internals.md`) — the real incident was a single wrong tool name
(`search_replace` instead of `edit`), already fixed. These three questions
are the residue worth answering on their own merits, independent of that
now-discredited investigation.

---

## Q1. Can we definitely state that automatic update to the newest Vibe
version is possible for every sandbox?

**Answer: No.**

This is a sandbox-provisioning/infrastructure question, not something
answerable from static analysis of this repo. Nothing in this repo's
documentation (including `docs/vibe/internals.md`, the source-verified
reference) describes how Vibe is installed, versioned, or upgraded inside a
sandbox. The `TOOL_VERSION_INCONSISTENCY_AUDIT.md` claim that a sandbox
session ran `pip install --upgrade mistral-vibe` mid-session is itself
unverified and uncorroborated elsewhere in the repo — it cannot be used as
evidence that this is a supported or routine mechanism.

**For the merger:** if version-pinning or auto-update behavior matters to how
crispy-couscous content gets used across both agents, that has to be answered
by whoever controls sandbox provisioning for each repo, not inferred from
either repo's docs. Treat it as an open infrastructure question, not a
documentation gap.

**Also flagged:** even if auto-update turns out to be possible, an agent
triggering it unilaterally mid-session is a mutating, blast-radius action
that should require explicit user confirmation under this repo's existing
risk posture — not something folded into a docs or audit task.

---

## Q2. Can we detect the differences between this repo's documentation and
the actual implementation, and what can we do about it?

**Answer: Yes — and it's already been done correctly once.**

The method already exists in this repo: `docs/vibe/internals.md`'s approach
is to pin a specific commit hash of the actual `mistralai/mistral-vibe`
source, read it directly, cite `file:line` for every claim, and explicitly
flag every place the code disagrees with `docs.mistral.ai`. It already
surfaced three real discrepancies (skill discovery path, `AGENTS.md` file
count, programmatic-mode default agent) using exactly this technique.

**What to do about drift going forward:** re-run the same discipline —
pinned commit, direct source read, `file:line` citation — rather than
re-deriving facts from memory, from a prior session's summary, or from a
document that itself wasn't source-verified (which is what went wrong in the
`TOOL_VERSION_INCONSISTENCY_AUDIT.md` case). No new tooling is required; the
method is already proven and repeatable.

**For the merger:** if crispy-couscous content (`mailroom/multi-agent-drop-823/`)
makes claims about Vibe or Claude Code internals, hold it to the same bar —
source-verified with citations — before treating it as authoritative
alongside `docs/vibe/internals.md`.

---

## Q3. How can we future-proof the skills and setup here?

**Answer: Minimally — most of it is already in place, and I added the one
missing piece.**

Already present before this review:
- `AGENTS.md`'s "Facts most likely to be got wrong" section, including the
  Claude Code → Vibe tool-name translation table and the note that Vibe
  silently drops unrecognized tool names with no error.
- The instruction to confirm any file-editing tool name against
  `docs/vibe/internals.md`'s builtin list before use.

Added as part of this review (`AGENTS.md`, "Facts most likely to be got
wrong" section):
> If a tool call fails, check whether the tool name exists in
> `docs/vibe/internals.md` before writing a new theory about why it failed.

This targets the actual failure mode that occurred: a wrong tool name
escalating into an invented multi-tier architecture explaining the failure,
instead of a two-second check against the already-verified tool list.

**Explicitly rejected as future-proofing:** a version-compatibility matrix, a
version-detection step at session start, or per-skill "version contracts."
No case in this repo has shown a skill or tool actually breaking *because of*
a version difference — the one incident that looked like that was a wrong
tool name, full stop. Building infrastructure for a failure mode that hasn't
occurred repeats the same mistake as the fabricated architecture document,
just aimed at prevention instead of explanation.

**For the merger:** the same minimal posture should apply to anything pulled
in from crispy-couscous — don't adopt compatibility-matrix or version-contract
machinery from that repo without first checking whether it's solving a
problem that's actually happened here, versus one that sounds thorough.

---

## What's still open

This document resolves the three specific questions above. It does **not**:

- Resolve whether `docs/vibe/TOOL_VERSION_INCONSISTENCY_AUDIT.md`'s broader
  architecture claims are true or false — that would need a fresh,
  reproducible, pinned-commit source check, which hasn't been done (see
  `CLAUDE_RESPONSE_VERSION_RECONCILIATION.md`, recommendation 2).
- Process the crispy-couscous content itself
  (`mailroom/multi-agent-drop-823/multi-agent/{COMPATIBILITY,STANDARDS,GAPS,
  MAINTENANCE}.md`), which multiple prior audits (`self-checks/2026-08-23/`,
  `self-checks/2026-08-24/audit_report.md`) have flagged as high-value and
  still unprocessed.
- Answer any merger-scoping questions beyond these three (repo structure,
  ownership, what gets merged vs. archived, timeline). Those are tracked as a
  follow-up conversation, not in this document.
