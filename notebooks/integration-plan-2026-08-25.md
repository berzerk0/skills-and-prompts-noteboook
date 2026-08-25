# Integration plan — 2026-08-25

Merge `berzerk0/skills-and-prompts-noteboook` and `berzerk0/crispy-couscous` into
one repository, then assess the result against
[`IDEAL.md`](IDEAL.md).

**Repositories:**
- `berzerk0/skills-and-prompts-noteboook` — a library of skills and prompts
- `berzerk0/crispy-couscous` — a multi-agent skill repo whose build step
  (`meta/generate_all.py`) compiles one canonical source, a directory of
  per-skill YAML files in `agents/`, into per-agent output for Claude Code, Pi,
  and Mistral Vibe

**Owner:** the project owner. **Policy for this effort:** sessions contribute
retrieval — what they did, what they know, what they found — and the owner makes
the decisions. This is a choice about how the work is run, not a claim about
what sessions are capable of.

> **This file is meant to be acted on.** Other files in this directory are an
> exploratory record and carry a "do not act on this" banner. If you were
> pointed here, work from this file and the ones it links.

---

## The fact this plan is built on

**Almost nothing in either repository has been deployed or invoked.**

The source for this is the project owner, who reports that the work was built
across web chat sessions and never installed anywhere it runs: most skills have
never been invoked, `crispy-couscous/prompts/router.md` (the prompt that routes
requests to sub-agents) has never been used, and Pi — a third coding agent,
alongside Claude Code and Mistral Vibe — has never been targeted at all.

**Two exceptions, both verified by running them on 2026-08-25.** The
crispy-couscous build step works: `python3 meta/generate_all.py --all` followed
by `git status` reports zero changed files, so it is idempotent and nothing it
generates has been hand-edited. A draft skill-name validator also runs. Nothing
else in either repo has a comparable check.

Two consequences, and they decide everything below:

1. **The merge cannot break working software, because almost none is running.**
   The real risk is **contradiction accumulation** — pulling two bodies of
   claims into one repo, then later having to decide which was right with no
   evidence either way.
2. **Assessment means running things, not reading them.** Reading cannot tell a
   working skill from one that only names an intent. In a sample of four
   crispy-couscous skills read closely, two were shells — a description, a list
   of trigger phrases, no logic — while the repo's README listed both as
   complete and working on all three agents.

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
Gathered for `skills-and-prompts-noteboook` already; see the appendix. The
crispy-couscous side is still outstanding and needs a full (non-shallow) clone;
whoever performs the merge does this first.

**From each session that did work on either repo** — what git cannot know.
A "session" here means a chat session in Claude Code or Mistral Vibe that did
work on one of these repos. **The project owner contacts these by hand through
each app; there is no programmatic way to enumerate or address them.** This
step is the owner's to perform, not a session's.

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

**Preserve provenance.** Record which repo each artifact came from. Once
merged, that information is no longer recoverable from the file tree, so it has
to be captured while the two sides are still distinguishable.

### 2c. Build the pile

One markdown file in the merged repo holding everything unresolved — path
chosen at merge time, but one file, not a directory and not scattered notes.
This is an output of phase 2, not an afterthought.

Each entry records three things: what is unresolved, where it came from (which
repo, branch, or session), and why it could not be settled during the merge.
That third field is what makes an entry sortable later.

**On the pile:**

- Contradictions found during the merge
- Known defects in the crispy-couscous repo, carried forward **unfixed** — see
  [`verified-defects-2026-08-25.md`](verified-defects-2026-08-25.md), which is a
  record of what was true at a specific commit, not a task list. Do not start
  fixing from it
- Which copy wins where a skill exists in both repos with different content:
  `challenge-my-thinking` (52 lines in one repo, 26 in the other) and
  `skill-extractor` (210 lines vs 54). The longer copies are in
  `skills-and-prompts-noteboook`; the shorter ones are wired into
  crispy-couscous's build step
- Whether three skills kept outside both repos, in the user-level
  `~/.claude/skills/synced/` directory, come back in: `pilot-preset`,
  `karpathy-guidelines`, `solus-skill`
- Whether `clarify` (crispy-couscous) and `ask-questions-if-underspecified`
  (skills-and-prompts-noteboook) are one skill under two names or genuinely two
  — both describe asking the user to clarify an underspecified request, so
  after the merge their descriptions compete for the same trigger
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

> **Do not start this early.** What follows is the most concrete, immediately
> runnable part of this document, which makes it tempting to begin before the
> merge is done. It depends on the merge: assessing the two repos separately
> produces two partial pictures and no single session can currently see both.

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

Both agents load skills in two stages: every skill's description sits in the
prompt on every turn, and only the body loads when the skill is invoked. So an
unused skill is not free — it costs description tokens continuously and
competes to be selected. Until phase 3 establishes which existing skills earn
that cost, adding more makes the measurement harder rather than easier.

---

## Decided — do not relitigate

| Question | Decision | Reason |
|---|---|---|
| Fix the known defects before or after the merge? | **After** | Two reasons. The merge moves paths and changes counts, so several of the recorded defects are about to be invalidated or restated — fixing them now means fixing them twice. And they are not independent bugs but samples of one condition (written, never run), so patching the few found by reading would leave the class unmeasured either way. |
| Look for contradictions between the repos before or after the merge? | **After** | Cross-repo comparison is what the merge exists to make possible. |
| Merge two sources or three? | **Open** | The user-level `~/.claude/skills/synced/` directory holds three skills excluded from both repos. On the pile. |
| Target one agent first, or stay cross-agent? | **Stay cross-agent** | crispy-couscous already targets three agents, and its build step is one of the two things verified to run (see the top of this document). Narrowing would give up working capability, not avoid work. |

---

## Appendix — git inventory, gathered 2026-08-25

### `skills-and-prompts-noteboook`

Working tree clean. Four branches unmerged:

| Branch | Size | Contents |
|---|---|---|
| `notebook/foundation-harness-exercise` | 20 commits | The design exercise and this plan |
| `claude/repo-vision-debate-r1-ya1c00` | 16 commits | An earlier version of the branch above, in a layout since abandoned. Its `docs/behaviors/QUICKSTART.md` gives working copy-paste instructions for installing a git pre-commit hook that was never tested |
| `claude/validate-mistral-patches-ipuxh1` | 3 commits, 1 file | `scratchpad/VIBE_FOLLOWUP_ACTION_ITEMS.md` |
| `vibe/errors-2026-08-24` | 3 commits, 3 files | A tool-version inconsistency audit and two version-reconciliation self-checks |

Four branches fully merged into `main`, so nothing would be lost by deleting
them. **Listed as inventory, not as an instruction — do not delete anything
without asking the owner:**
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
shallow (`--depth 1`), which truncates history — so `git` cannot compute a real
merge base, and the ahead/behind counts it reports are artifacts of the
truncation rather than facts about the branches. Assessing these needs a full
clone and belongs to phase 2.

---

## Reference

- [`IDEAL.md`](IDEAL.md) — the ten principles this is measured against. Start here.
- [`verified-defects-2026-08-25.md`](verified-defects-2026-08-25.md) — defects
  reproduced with the commands that produced them, valid as of
  `crispy-couscous@4d2c23d`. Paths will move during the merge; re-verify after.
- [`wants-and-priorities-2026-08-25.md`](wants-and-priorities-2026-08-25.md) —
  what the project was originally trying to build, and which parts already exist.

Everything else in this directory is lower-confidence record, not guidance.
