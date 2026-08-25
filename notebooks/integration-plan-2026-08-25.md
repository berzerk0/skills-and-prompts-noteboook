# Integration plan — 2026-08-25

> **This file is different from its neighbours. It IS a work plan.**
> Everything else on this branch is an inert thought exercise carrying a "do not
> act on this" banner. This one is meant to be acted on. If you are a session
> that was pointed here, read this file and the two it links; do not go
> exploring the rest of the branch for instructions.

**Scope:** merging `berzerk0/skills-and-prompts-noteboook` and
`berzerk0/crispy-couscous` into one repo, and finding out where the result
actually stands.

**Owner:** the human. Sessions contribute retrieval, not decisions.

---

## The one fact this plan is built on

**Almost nothing has ever been run.**

Not the router. Not most skills. The work has been half-implemented across Vibe
and Claude Code web sessions and never deployed into a repo where it executes.
Pi has never been touched. There is also no visibility from the UI into when a
skill is invoked.

Two consequences, and they drive every choice below:

1. **The merge cannot break working software, because there isn't any.** The
   risk is not breakage. It is **contradiction accumulation** — pulling two
   bodies of claims into one repo and later having to decide which was right,
   with no way to tell.
2. **Assessment has to mean running things.** Reading cannot distinguish a
   working skill from a stub that names an intent. That was established the hard
   way — see [`verified-defects-2026-08-25.md`](verified-defects-2026-08-25.md),
   where four of eight defects are exactly that mistake, three of them made
   while writing these very documents.

---

## Phase 1 — Document the ideal ✅ done

**Output:** [`IDEAL.md`](IDEAL.md) — ten principles, each with an observable and
a falsifier so phase 3 can score by running rather than by listing.

Not a spec, not a commitment. The thing to measure against.

---

## Phase 2 — Merge

### 2a. Collect dangling bits *(precondition)*

Two sources, different answerers. **Do not ask a session for what git already
knows.**

**Git-answerable — mostly already gathered, see appendix.**
Branches, unmerged commits, stale refs, uncommitted work.

**Session-only — needs the paste prompt.**
What was decided but never written down. What was started and abandoned, and
why. What was learned that isn't in any file. Anything the session did that a
later reader would misread.

Sessions are asked to **close their own loop, not to judge this plan.** They
hold state; they do not hold the full picture — no session can currently see
both repos at once, which is itself part of why the merge comes first.

### 2b. Merge

**Discipline, and it is the whole point of this phase:**

> **Record contradictions. Do not resolve them.**

When the two repos disagree, the merge does not pick a winner. There is no
basis to pick one — nothing runs, so there is no evidence either version is
correct. Preserve both, mark the disagreement, move on. Resolving on a hunch
is how a contradiction becomes a false claim that outlives the person who
guessed.

**Preserve provenance.** Which repo did each artifact come from? That is
cheapest to record now and is evidence later when the pile gets sorted.

### 2c. Build the pile

The pile is the second output of this phase, not an afterthought. Everything
unresolved goes in **one place**, in the merged repo.

**What goes on the pile:** contradictions found during the merge; the open
defects (D1–D4); which version of a differing skill wins; whether
`karpathy-guidelines` / `solus-skill` / `pilot-preset` come back in; whether
`clarify` and `ask-questions-if-underspecified` are one skill or two; every
"we'll figure this out later" from a session.

**What does NOT go on the pile — this distinction matters:**

| Kind | Example | Fate |
|---|---|---|
| **Evidence** | the defect log, `IDEAL.md` | Stays as reference. It's what you adjudicate *with*. Needs a "valid as of `<sha>`" stamp, not a queue position. |
| **Task** | fix D1's prose, pick a skill version | Goes on the pile. |

The pile is allowed to sort into **drop**. Most of it probably should.

**Do not build a second container.** The
`notebook/foundation-harness-exercise` branch is already an inert pile with the
committee material in it. Post-merge the pile is that branch plus whatever the
merge surfaces — one place, not two.

---

## Phase 3 — Assess the merged repo against the ideal

**The method is exercise, not inventory.** Inventory is fast and lies. A
directory listing and a README compatibility table both presented
`skill-validator` as complete; it is 25 lines of trigger phrases that validate
nothing.

**Minimum viable:** invoke every skill once, on a real ask, and record what came
back. Anything that cannot be invoked, or that returns only its own
description, is a stub regardless of what any table says.

**Known limit — half of principle 0 is not testable right now:**

- *Does it work when called?* Testable. Invoke it, read the response.
- *Does it get called when it should?* **Not observable.** Skills fire on
  description match and the UI shows no invocation events. This is also why
  principle 8 (retirement) has no data to work from.

A hook could log invocations. That is the highest-value thing that does not
exist. **Do not build it during this plan** — note it and move on.

Phase 3 is also where the pile gets sorted, because that is when there is
finally evidence to sort it with.

---

## After phase 3, and only then

**Stability before expansion.** No new skills — including the third-party set
on deck — until phase 3 has produced a baseline.

Three reasons, in order of how much they cost: imported skills are
indistinguishable from your own by inventory; they add description residency
from the moment they land; and without invocation visibility there is no way to
tell whether any of them work.

---

## Decided, and not to be relitigated

| Question | Decision | Why |
|---|---|---|
| Fix crispy-couscous defects before or after the merge? | **After.** | D1–D4 are not four defects; they are four samples of one condition — written, never run. Fixing the two found by reading patches the visible instances of a pervasive, unmeasured class. |
| Hunt contradictions before or after the merge? | **After.** | Cross-repo comparison is what the merge exists to make tractable. No session can see both repos today. |
| Merge two repos or three sources? | **Open.** | `~/.claude/skills/synced/` holds `pilot-preset`, `karpathy-guidelines`, `solus-skill`. On the pile. |
| Single-agent first or cross-agent? | **Cross-agent is the goal.** | crispy-couscous is already tri-agent with a working compiler. Going single-agent would give up capability, not avoid work. |

---

## Appendix — git-answerable dangling bits, gathered 2026-08-25

### `skills-and-prompts-noteboook`

**Unmerged branches:**

| Branch | Size | Contents | Disposition |
|---|---|---|---|
| `notebook/foundation-harness-exercise` | 20 commits | The committee exercise + this plan | Keep unmerged, deliberately |
| `claude/repo-vision-debate-r1-ya1c00` | 16 commits | **Superseded predecessor of the above.** Still contains `docs/behaviors/`, `scripts/`, root `.tools-registry.yaml` — the layout deliberately abandoned | **Delete.** Live contradiction source: it holds working git-hook install instructions in `docs/` |
| `claude/validate-mistral-patches-ipuxh1` | 3 commits, 1 file | `scratchpad/VIBE_FOLLOWUP_ACTION_ITEMS.md` | Needs a decision |
| `vibe/errors-2026-08-24` | 3 commits, 3 files | Tool-version inconsistency audit + two version-reconciliation self-checks | Needs a decision |

**Merged, safe to delete (4):** `claude/agent-external-comms-guardrails-gjrjl4`,
`claude/log-attribution-todo`, `claude/repo-vision-clarify-u3pays`,
`claude/version-reconciliation-review-jvzxfw`

Working tree clean.

### `crispy-couscous` — **not assessed**

Three non-main branches exist: `fix/generator-symlink-bug`,
`fix/readme-remove-codeberg-and-stale-refs`,
`vibe/implementation-roadmap-4105aff`.

Their merge status **was not determined.** The available clone is `--depth 1`,
and the ahead-counts a shallow clone produces are artifacts, not facts. Assessing
these needs a full clone and belongs to phase 2.

`vibe/implementation-roadmap-4105aff` is worth looking at first — a roadmap
branch is where undocumented intent hides.

---

## Reference

- [`IDEAL.md`](IDEAL.md) — what we are aiming at. Start here.
- [`verified-defects-2026-08-25.md`](verified-defects-2026-08-25.md) — eight
  defects reproduced with commands, valid as of `crispy-couscous@4d2c23d`.
  Paths will move in the merge; re-verify after.
- [`wants-and-priorities-2026-08-25.md`](wants-and-priorities-2026-08-25.md) —
  what the original brain dump was really asking for, and which parts already
  exist.

Everything else in `notebooks/` is lower-confidence record, not guidance.
