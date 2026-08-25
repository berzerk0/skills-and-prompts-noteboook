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
> exploratory record and carry a "do not act on this" banner. Three of them are
> linked below and each says whether you need to open it — the links are
> references, not an instruction to go work through them.

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
generates has been hand-edited. A draft validator that checks skill files for tool names invalid on a target
agent also runs; it lives at
`notebooks/behaviors/validate-tool-names.py` on the
`notebook/foundation-harness-exercise` branch and is unpromoted draft tooling,
not part of any workflow. Nothing
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
Gathered for `skills-and-prompts-noteboook` already; see the appendix.

The crispy-couscous side is outstanding. The clone used for the appendix was
shallow and cannot answer it. Clone that repo again at full depth, to a fresh
directory rather than reusing or repairing the shallow one (`git clone
https://github.com/berzerk0/crispy-couscous`, no `--depth`), then for each
branch record whether it is merged into `main` and what it changes. Discard the
shallow clone once the full one is confirmed to have complete history — `git
log --oneline main | wc -l` returning more than a handful of commits is enough
to confirm it.

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

**On the pile.** Every item below is *recorded*, not worked — the pile is built
during phase 2 and sorted during phase 3. Nothing here is a task yet.

- Contradictions found during the merge
- Known defects in the crispy-couscous repo, copied across **unfixed** from
  [`verified-defects-2026-08-25.md`](verified-defects-2026-08-25.md)
- Which copy wins where a skill exists in both repos with different content.
  `challenge-my-thinking` (stress-tests a plan by asking pointed questions
  rather than giving a verdict) is 52 lines in `skills-and-prompts-noteboook`
  and 26 in crispy-couscous. `skill-extractor` (turns a finished piece of work
  into a reusable skill file) is 210 lines and 54. **Line count is not a quality
  measure** — the shorter copies may be deliberate condensations, and they are
  the ones wired into crispy-couscous's build step. Neither version has been
  invoked, so there is currently no basis for choosing
- Whether three skills should be brought into the merged repo: `pilot-preset`,
  `karpathy-guidelines`, `solus-skill`. They currently live only in the owner's
  personal Claude Code directory (`~/.claude/skills/synced/`) on whichever
  machines that directory is synced to, so they are in neither repo and travel
  with the user rather than the project
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

**The method is exercise, not inventory.** Close reading does catch some
shells — that is how the four-skill sample above was found — but it is slow, it
does not scale to a whole repo, and it cannot establish the two things that
matter most: that a skill does what it claims when invoked, and that it fires
when it should. A file listing catches none of it.

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
| Fix the known defects before or after the merge? | **After** | Two reasons, both inference rather than measurement. The merge is expected to move paths and change counts, which would invalidate or restate several recorded defects — fixing them now would likely mean fixing them twice. And they are not independent bugs but samples of one condition (written, never run), so patching the few found by reading would leave the class unmeasured either way. |
| Look for contradictions between the repos before or after the merge? | **After** | One of the reasons for merging at all is to make cross-repo comparison tractable — currently no session can see both repos at once. Doing the comparison first would mean doing it under exactly the conditions the merge is meant to remove. |
| Merge two sources or three? | **Open** | The user-level `~/.claude/skills/synced/` directory holds three skills excluded from both repos. On the pile. |
| Target one agent first, or stay cross-agent? | **Stay cross-agent** | crispy-couscous already targets three agents, and its build step is one of the two things verified to run (see the top of this document). Narrowing would discard that build step, which works. It would not avoid work — and note the skills the build step produces are themselves unverified, so this is a decision about keeping working machinery, not working skills. |

---

## Appendix — git inventory, gathered 2026-08-25

### `skills-and-prompts-noteboook`

Working tree clean. Four branches unmerged:

| Branch | Size | Contents |
|---|---|---|
| `notebook/foundation-harness-exercise` | 20 commits | The design exercise and this plan |
| `claude/repo-vision-debate-r1-ya1c00` | 16 commits | An earlier version of the branch above, in a layout since abandoned. Its `docs/behaviors/QUICKSTART.md` gives copy-paste `cp` and `chmod` commands that would successfully install a git pre-commit hook. The hook itself was never installed or run, so what it does when it fires is unknown |
| `claude/validate-mistral-patches-ipuxh1` | 3 commits, 1 file | `scratchpad/VIBE_FOLLOWUP_ACTION_ITEMS.md` |
| `vibe/errors-2026-08-24` | 3 commits, 3 files | A tool-version inconsistency audit and two version-reconciliation self-checks |

Four branches fully merged into `main`, so nothing would be lost by deleting
them. **Listed as inventory, not as an instruction — do not delete anything
without asking the owner:**
`claude/agent-external-comms-guardrails-gjrjl4`, `claude/log-attribution-todo`,
`claude/repo-vision-clarify-u3pays`,
`claude/version-reconciliation-review-jvzxfw`.

**Suggested, not decided — the owner's call, and there is a case either way.**
`claude/repo-vision-debate-r1-ya1c00` holds the same material as
`notebook/foundation-harness-exercise` in an earlier layout: the later branch
was created by moving that content and correcting it, so the two overlap almost
entirely. *For deleting:* its `docs/` directory presents unverified material as
checked reference and includes hook-install commands. *For keeping:* it is
history, and deleting it is not reversible from a clone. Do not act on this
without asking.

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

- [`IDEAL.md`](IDEAL.md) — ten principles describing what the merged system
  should be like, each written so it can be tested by running something rather
  than by reading. **Open it before phase 3**; it is the scoring sheet. You do
  not need it for phase 2.
- [`verified-defects-2026-08-25.md`](verified-defects-2026-08-25.md) — a list of
  wrong or misleading claims found in crispy-couscous, each with the command
  that reproduced it, valid as of commit `4d2c23d`. **A record, not a task
  list.** Open it when building the pile, to copy items across. Do not fix from
  it — paths will move during the merge and several entries will need
  re-verifying afterwards.
- [`wants-and-priorities-2026-08-25.md`](wants-and-priorities-2026-08-25.md) —
  background on what the project was originally trying to build and which parts
  already exist. **Optional**; nothing in this plan depends on it.

Everything else in this directory is lower-confidence record, not guidance.
