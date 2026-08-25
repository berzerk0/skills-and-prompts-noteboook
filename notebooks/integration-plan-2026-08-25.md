# Integration plan — 2026-08-25

Merge `berzerk0/skills-and-prompts-noteboook` and `berzerk0/crispy-couscous` into
one repository, then assess the result against
[`IDEAL.md`](IDEAL.md).

**Repositories:**
- `berzerk0/skills-and-prompts-noteboook` — a library of skills and prompts
- `berzerk0/crispy-couscous` — a multi-agent skill repo with a working
  build step that compiles one canonical source into per-agent files
  (Claude Code, Pi, Mistral Vibe)

**Owner:** the human. Sessions contribute retrieval, not decisions.

> **This file is meant to be acted on.** Other files in this directory are an
> exploratory record and carry a "do not act on this" banner. If you were
> pointed here, work from this file and the ones it links.

---

## The fact this plan is built on

**Almost nothing in either repository has ever been run.**

The work was built across web sessions and never deployed anywhere it executes.
Most skills have never been invoked. One repo's agent-routing prompt has never
been used. The third target agent, Pi, has never been touched at all.

Two consequences, and they decide everything below:

1. **The merge cannot break working software, because there isn't any.** The
   real risk is **contradiction accumulation** — pulling two bodies of claims
   into one repo, then later having to decide which was right with no evidence
   either way.
2. **Assessment means running things, not reading them.** Reading cannot tell a
   working skill from one that only names an intent. In a sample of four skills
   read closely, two were shells: a description, a list of trigger phrases, and
   no logic — while a README table listed both as complete and working on all
   three agents.

---

## Phase 1 — Document the ideal ✅ done

**Output:** [`IDEAL.md`](IDEAL.md) — ten principles, each with an observable and
a falsifier, written so phase 3 can score against them by running the system
rather than by listing its files.

Not a spec and not a commitment. The thing to measure against.

---

## Phase 2 — Merge

### 2a. Collect loose ends *(precondition)*

Two sources, and they answer different questions. **Don't ask a session for
what git already knows.**

**From git** — branches, unmerged commits, stale refs, uncommitted work.
Gathered for one repo already; see the appendix.

**From each session that did work on either repo** — what git cannot know:

- What was decided but never written down
- What was started and abandoned, and why
- What was learned that isn't in any file
- Anything it did that a later reader would misread

Ask each session to **close its own loop, not to review this plan.** A session
holds its own state; it does not hold the full picture, since no session can
currently see both repositories at once.

Also collect each session's branch name and current commit, so its work can be
matched against the git inventory.

### 2b. Merge

**The rule for this phase:**

> **Record contradictions. Do not resolve them.**

When the two repos disagree, do not pick a winner. There is no basis to pick
one — nothing runs, so there is no evidence either version is correct.
Preserve both and mark the disagreement.

**Preserve provenance.** Record which repo each artifact came from. It is
cheapest to capture during the merge and becomes evidence later.

### 2c. Build the pile

A single place in the merged repo holding everything unresolved. This is an
output of phase 2, not an afterthought.

**On the pile:**

- Contradictions found during the merge
- Known defects in the crispy-couscous repo, carried forward unfixed
  (see [`verified-defects-2026-08-25.md`](verified-defects-2026-08-25.md))
- Which copy wins where a skill exists in both repos with different content —
  currently `challenge-my-thinking` and `skill-extractor`
- Whether the three skills kept outside both repos, in the user-level
  `~/.claude/skills/synced/` directory, come back in
- Whether `clarify` and `ask-questions-if-underspecified` are one skill or two
- Every "we'll figure this out later" a session reports

**Not on the pile:**

| Kind | Example | Fate |
|---|---|---|
| **Evidence** — a record of what was true | the defect log, `IDEAL.md` | Stays as reference. It's what you adjudicate *with*. Needs a "valid as of `<commit>`" stamp, not a queue position. |
| **Task** — a thing to do | pick a skill version, fix a wrong claim | Goes on the pile. |

Sorting the pile into **drop** is a valid outcome for any item.

**One pile, not two.** The `notebook/foundation-harness-exercise` branch already
holds the earlier design work in exactly this form. Post-merge, the pile is that
branch plus whatever the merge surfaces — one location.

---

## Phase 3 — Assess the merged repo against the ideal

**The method is exercise, not inventory.** A file listing is fast and
misleading; it cannot separate a working component from a named one.

**Minimum viable pass:** invoke every skill once, on a real request, and record
what came back. Anything that cannot be invoked, or that returns only its own
description, is a shell regardless of what any table claims.

Score the result against [`IDEAL.md`](IDEAL.md). Then sort the pile, which is
now possible because there is finally evidence to sort it with.

**Worth knowing before designing the pass:** invoking a skill by hand and
reading the result is straightforward. Confirming that a skill *fires on its own
when it should* is harder, since agents select skills by matching their
descriptions and that selection is not always visible. Design the pass around
what can be observed in whatever tooling is available at the time.

---

## After phase 3, and only then

**Stability before expansion.** No new skills — including any third-party set
waiting to be imported — until phase 3 has produced a baseline.

Imported skills are indistinguishable from local ones by inspection, and every
skill's description consumes context on every turn whether or not it is ever
used. Without a baseline there is no way to tell what any of them contribute.

---

## Decided — do not relitigate

| Question | Decision | Reason |
|---|---|---|
| Fix the known defects before or after the merge? | **After** | They are not separate defects but samples of one condition: written, never run. Fixing only the ones found by reading patches the visible instances of an unmeasured class. |
| Look for contradictions between the repos before or after the merge? | **After** | Cross-repo comparison is what the merge exists to make possible. |
| Merge two sources or three? | **Open** | The user-level `~/.claude/skills/synced/` directory holds three skills excluded from both repos. On the pile. |
| Target one agent first, or stay cross-agent? | **Stay cross-agent** | crispy-couscous already targets three agents and its build step works. Narrowing would give up capability, not avoid work. |

---

## Appendix — git inventory, gathered 2026-08-25

### `skills-and-prompts-noteboook`

Working tree clean. Four branches unmerged:

| Branch | Size | Contents |
|---|---|---|
| `notebook/foundation-harness-exercise` | 20 commits | The design exercise and this plan |
| `claude/repo-vision-debate-r1-ya1c00` | 16 commits | An earlier version of the branch above, in a layout since abandoned |
| `claude/validate-mistral-patches-ipuxh1` | 3 commits, 1 file | `scratchpad/VIBE_FOLLOWUP_ACTION_ITEMS.md` |
| `vibe/errors-2026-08-24` | 3 commits, 3 files | A tool-version inconsistency audit and two version-reconciliation self-checks |

Four branches already merged and safe to delete:
`claude/agent-external-comms-guardrails-gjrjl4`, `claude/log-attribution-todo`,
`claude/repo-vision-clarify-u3pays`,
`claude/version-reconciliation-review-jvzxfw`.

**Suggested, not decided:** delete `claude/repo-vision-debate-r1-ya1c00`. It is
superseded by `notebook/foundation-harness-exercise` and still contains a
`docs/` directory with working instructions for installing a git hook — a
contradiction source if anyone finds it after the merge.

### `crispy-couscous` — not assessed

Three branches exist besides `main`: `fix/generator-symlink-bug`,
`fix/readme-remove-codeberg-and-stale-refs`,
`vibe/implementation-roadmap-4105aff`.

**Their merge status was not determined.** The clone available at the time was
shallow, and commit counts from a shallow clone are artifacts rather than facts.
Assessing these needs a full clone and belongs to phase 2.

---

## Reference

- [`IDEAL.md`](IDEAL.md) — the ten principles this is measured against. Start here.
- [`verified-defects-2026-08-25.md`](verified-defects-2026-08-25.md) — defects
  reproduced with the commands that produced them, valid as of
  `crispy-couscous@4d2c23d`. Paths will move during the merge; re-verify after.
- [`wants-and-priorities-2026-08-25.md`](wants-and-priorities-2026-08-25.md) —
  what the project was originally trying to build, and which parts already exist.

Everything else in this directory is lower-confidence record, not guidance.
