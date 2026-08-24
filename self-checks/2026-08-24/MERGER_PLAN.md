# Merger Plan: crispy-couscous → skills-and-prompts-noteboook

**Date:** 2026-08-24
**Scope:** Structural plan only — per user decision, technical claims in the
content itself are NOT verified here (see "Verification" at the bottom).
**Source:** `mailroom/multi-agent-drop-823/multi-agent/` (5 files, 837 lines):
`README.md`, `STANDARDS.md`, `COMPATIBILITY.md`, `GAPS.md`, `MAINTENANCE.md`

Decisions already made (see conversation record):
- End state: absorb couscous content into this repo; couscous itself
  archived later, not automatically as part of this work.
- `mailroom/` stays alive as a concept for now — its own long-term fitness is
  a separate open question (see below), not a blocker for this merge.
- Merge shape: **incremental, per-topic PRs** — one PR per file/topic, not
  one large PR.

---

## Per-file destination

| File | Topic | Proposed destination | Notes |
|---|---|---|---|
| `STANDARDS.md` | Cross-tool standards: Agent Skills spec, AGENTS.md spec, MCP spec | `docs/shared/` (new file, e.g. `docs/shared/standards.md`) | Genuinely cross-agent, not tool-specific. Matches mailroom's own integration table ("Cross-agent docs → docs/shared/"). |
| `COMPATIBILITY.md` | Tool-specific behavior comparison: built-ins, skill formats, subagents, AGENTS.md support, permissions — across **three** tools (Claude Code, Vibe Code, **Pi Agent**) | Split: Vibe-specific rows → cross-check against `docs/vibe/internals.md`; Claude-specific rows → `docs/claude/`; comparison framing → `docs/shared/` | **Blocking decision below** — this repo currently only documents Claude Code and Vibe. Pi Agent is a third tool with no existing footprint here. |
| `GAPS.md` | Undocumented gaps in official specs (JSON schemas, Vibe `allowed-tools` syntax, MCP limits, Claude hook output limits, etc.) | `docs/shared/` (new file, e.g. `docs/shared/gaps.md`) | Reference material, cross-agent, no tool-specific home needed. |
| `MAINTENANCE.md` | Process for keeping the above docs current (quarterly review, CI-check concept) | `docs/shared/` or a new `CONTRIBUTING.md`-style doc | This is process/meta, not reference content — different in kind from the other three. Could also just become a section of `docs/shared/README.md` rather than its own file. |
| `README.md` | Index/overview of the above four | Superseded — becomes redundant once the four are integrated into `docs/shared/`'s own README/index | **Do not copy as-is.** Its relative links (`../../skills/codeberg/SKILL.md`, `../../.vibe/agents/codeberg.toml`) point to examples that exist in crispy-couscous, not in this repo — already flagged as broken in `scratchpad/findings.md`. Use it only as a guide for what index entries to add, not as content to merge. |

This gives **4 candidate PRs** (STANDARDS, COMPATIBILITY, GAPS, MAINTENANCE),
with `README.md` handled as index cleanup alongside whichever PR lands last,
not as its own PR.

---

## Two decisions needed before scoping PRs further

### 1. Does this repo adopt Pi Agent as a third supported tool?

`COMPATIBILITY.md` and its `README.md` are written for **three** tools:
Claude Code, Vibe Code, and **Pi Agent** (`earendil-works/pi`). This repo's
`AGENTS.md` currently frames everything as dual-agent (Vibe + Claude Code)
only — Pi Agent doesn't appear anywhere else in this repo. Bringing
`COMPATIBILITY.md` in as-is would silently introduce a third tool this repo
otherwise has zero support, skills, or docs for.

Options: (a) adopt Pi Agent as a third documented tool going forward, (b)
strip Pi Agent content out during the `COMPATIBILITY.md` PR and keep this
repo dual-agent, (c) keep Pi Agent rows but mark them explicitly
out-of-scope/unsupported here.

### 2. Does `mailroom/` deserve to keep existing, structurally?

You raised this directly: *"i'm not convinced the mailroom in general isn't
my bootleg way of doing something that's already been solved by 'real'
developers."* Worth answering plainly rather than deferring again:

**It mostly is a bootleg version of something with a name.** What
`mailroom/` does — a read-only staging area where content lands, gets
triaged (accept/adapt/extract/reject), and moves to its real home — is a real
and common pattern, usually called a **vendor/incoming or "third-party"
staging directory**, or handled by process rather than a folder at all (an
open PR *is* the staging state in most repos; review happens on the diff,
not in a parked directory). The parts of `mailroom/README.md` that are doing
real work — the accept/adapt/extract/reject taxonomy, the "never write to
it" read-only rule, the integration-location table — are worth keeping
regardless of the folder's name. The parts that look like reinvention: a
whole separate directory tree plus a template plus a workflow doc, for
something a `git mv` out of a feature branch (or, in this repo's case, out of
`vibe/errors-2026-08-24`-style branches) would do with less ceremony and
better history.

This doesn't need resolving before the four PRs above — none of them depend
on it. But it's worth deciding before *more* content lands in `mailroom/`,
since every new drop adds to what eventually needs migrating off the pattern
if you decide to retire it.

---

## Verification

Per your explicit choice, this plan does **not** verify `COMPATIBILITY.md`'s
technical claims (tool paths, built-in lists, version numbers like "Vibe
v2.25.0") against source. That happens during each file's own processing PR,
using the same pinned-commit method as `docs/vibe/internals.md` — not before.
One thing already known without deep verification: `COMPATIBILITY.md`'s Vibe
skill/subagent paths (`.vibe/skills/`, `.vibe/agents/`) match what
`docs/vibe/internals.md` and `AGENTS.md` already state, so at least that
slice is consistent with this repo's verified reference on first glance.

---

## Suggested order

1. **GAPS.md** — lowest risk, no tool-specific claims to verify, smallest
   surface area (138 lines).
2. **STANDARDS.md** — general reference, moderate size (125 lines), still
   low-risk.
3. **MAINTENANCE.md** — process doc; decide during this PR whether it
   becomes its own file or folds into `docs/shared/README.md`.
4. **COMPATIBILITY.md** — largest (261 lines) and the one that needs the
   Pi Agent decision resolved first, plus source verification of its
   tool-specific claims. Do this last.

Each PR: pull the relevant file's content, verify factual claims against
source where practical (or explicitly flag what's carried over unverified),
rewrite links so nothing points at crispy-couscous-only paths, land in the
destination above, and remove the corresponding piece from
`mailroom/multi-agent-drop-823/` once integrated (per mailroom's own
"Cleanup" step).
