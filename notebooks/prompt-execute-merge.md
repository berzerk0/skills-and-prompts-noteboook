You are merging two GitHub repositories into one: `berzerk0/skills-and-prompts-noteboook`
and `berzerk0/crispy-couscous`. Nobody has decided the target layout yet — that
is part of your job, not something to infer from what follows.

You have no memory of any prior session on either repository — "session" here
just means an earlier instance of an AI assistant, in a separate conversation,
that did work here. That absence of memory is intended. Everything you need is
in the files below; read them yourself rather than trusting a summary,
including this one.

**This is a consequential, partly irreversible action on real repositories.
Plan first, get sign-off, then execute. Do not skip the sign-off step because
the plan seems obvious to you.**

**Where the line actually is:** reading files, cloning repositories to local
disk, and writing a local plan file are all safe and expected before sign-off
— do them, that's Steps 1 through 3. **The line is anything that changes the
real repositories on GitHub:** creating a branch there, pushing a commit,
opening a PR, merging anything. None of that happens until Step 4, and Step 4
does not start until the owner has confirmed your Step 3 plan. Cloning is not
execution. Pushing is.

**Be clear about what kind of stop this is.** This document is text; it has no
way to technically prevent you from continuing past Step 3. The stop only
works if you choose to honor it. If the owner running this can control your
credentials separately, the actual safeguard is not granting push access to
either repository until the Step 3 plan is approved — that stops it whether or
not the text is followed. If that's not controllable here, honoring the stop
is the only mechanism there is, so treat it as a hard rule, not a suggestion.

## Step 1 — Read the primary sources, not a summary of them

Reading these means having a checkout. If you don't have one yet, clone
`skills-and-prompts-noteboook` now — that's a safe, local, read-only action;
see Step 2 for why it's fine to do before planning, and for the fuller
clone-both-repositories-and-check-branches pass that comes next.

In `skills-and-prompts-noteboook`, on branch `notebook/foundation-harness-exercise`:

- `notebooks/integration-plan-2026-08-25.md` — the plan this task is phase 2
  of. (Phase 1 was writing `IDEAL.md`, described below — you don't need its
  content for this task, just that it happened first.) Read the plan in full,
  including the appendix.
- `notebooks/verified-defects-2026-08-25.md` — defects to carry forward
  **unfixed**, not to fix now.
- Every file under `loose-ends/` in both repositories, on every branch that has
  one. Do not skip any — each is a report a session or a local-archaeology pass
  wrote specifically for this step. As of this writing that includes at least:
  - `loose-ends/fix-readme-remove-codeberg-and-stale-refs.md` on
    crispy-couscous's `fix/readme-remove-codeberg-and-stale-refs` branch
  - `loose-ends/local-archaeology-2026-08-25.md` on crispy-couscous's
    `local-archaeology-2026-08-25` branch
  - Whatever landed on `skills-and-prompts-noteboook`'s own branches — check
    `claude/validate-mistral-patches-ipuxh1` and `vibe/errors-2026-08-24`
    specifically, and any `report/…` branches
  - **This list may be incomplete by the time you run. Search for `loose-ends/`
    across every branch of both repositories yourself; do not rely on this
    enumeration.** For each repository: `git branch -a` to list every branch,
    then for each one `git ls-tree -r <branch> --name-only | grep loose-ends`
    to check whether it has a report. Do this after Step 2's clone.
  - A "local-archaeology pass" (mentioned above) is the same kind of report,
    produced by a session with no memory of prior work in the repo, checking
    for anything left on local disk that a remote clone can't see. Read it the
    same way as any other `loose-ends/` file — the label just tells you how it
    was produced, not that it should be treated differently.

Do **not** open `notebooks/IDEAL.md` for this task — phase 3, after this one,
checks the merged result against it; this merge doesn't need it.

## Step 2 — Get the real repository state yourself (local, read-only, safe before sign-off)

A `git clone` only writes to your own local disk. It does not touch either
repository on GitHub and there is nothing to undo. Do this now, before
planning — you cannot write a sound plan in Step 3 without seeing the real
branches first.

**A general fact about git, with a concrete local instance of it:** a shallow
clone (`--depth N`) truncates history, so `git merge-base`, ahead/behind
counts, and anything else that depends on full history are unreliable against
it — not just incomplete, but capable of reporting plausible-looking wrong
numbers, because the truncation point can look like a fork point that never
existed. This actually happened during the planning for this merge: a
`--depth 1` clone of crispy-couscous reported all three of its non-main
branches as 40-50 commits ahead and unmerged. A full clone of the same
repository, same moment, showed two were already merged and the third had
exactly one unmerged commit.

Clone both repositories fresh, with no `--depth` flag:

```bash
git clone https://github.com/berzerk0/skills-and-prompts-noteboook
git clone https://github.com/berzerk0/crispy-couscous
```

For each:

```bash
git remote -v
git branch -a
git log --oneline main -5   # or the default branch if not main
```

For crispy-couscous specifically, confirm the branch table in the integration
plan's appendix still matches reality — it may have changed since that was
written. Do not add `--depth 1` to save time; that flag is what caused the
false report in the first place.

## Step 3 — Decide the shape of the merge, and write it down before touching anything

Items 1 and 3–6 are undecided — you are deciding them, not discovering a
pre-made answer. Item 2 is different: it has a rule already, from
`notebooks/integration-plan-2026-08-25.md`, and you're applying that rule, not
choosing whether to follow it.

1. **Which repository is the base, or is this a new repository?** State which,
   and why.
2. **What happens to skills that exist in both repos with different content?**
   Diffing the two repos directly turned up `challenge-my-thinking` and
   `skill-extractor` as the known cases — check for others yourself with the
   same method, do not assume this list is complete. The plan's rule: do not
   resolve which version wins. Keep both, record the conflict. This item has
   no decision to make; note that you followed it.
3. **What happens to crispy-couscous's build tooling** (`meta/generate_*.py`,
   the `agents/` YAML directory, and its compiled output in `.claude/`,
   `.vibe/`, and `.pi/` — `.pi/` is for Pi Agent, the third coding tool this
   project targets, alongside Claude Code and Mistral Vibe)? Per the integration
   plan's verification pass, this is the only piece of infrastructure in
   either repo confirmed to work by actually running it: `python3
   meta/generate_all.py --all` followed by `git status` reported zero changed
   files at that time, meaning nothing generated had been hand-edited since.
   That's why it matters. Separately: **run that same check yourself, now,
   after cloning** — the verification above is a past result, not a current
   guarantee, and time has passed since it was recorded. Confirm it still
   holds before you rely on it. Whatever layout you choose, that property
   should still hold afterward, or you should say clearly that it doesn't and
   why — this is a soft constraint, not an absolute: preserve it if you can,
   but never break it silently.
4. **What happens to `vibe/implementation-roadmap-4105aff`?** (A real branch
   name on crispy-couscous — `vibe/` prefix, then a descriptive slug, not a
   hash.) Per the loose-ends findings in Step 1, it contains real, finished
   work on crispy-couscous's internals — a router agent, five agents made
   directly callable, tool-profile standardization. You don't need to
   understand what those terms mean just to know this is finished work, not an
   abandoned branch, and that losing it silently would be a real loss, not
   cleanup. You do need to look at the branch's actual commits and diffs
   (not just this summary) if you're checking whether its changes conflict
   with anything from the other repo — that's a Step 4 task, and this summary
   isn't detailed enough to make that call. It cannot simply be left behind or
   silently overwritten by whatever the merge does to `.vibe/agents/`.
5. **Git history: preserved, or a fresh start with provenance recorded in
   files instead?** Either is defensible. State which and why — this is
   effectively permanent once done.
6. **Where does the pile live?** One markdown file, per the plan — pick its
   path. (Step 4 below specifies what each entry in it needs to contain.)

Write this as a short plan file (anywhere sensible — your call), covering all
six points with your reasoning, not just your conclusion.

**Stop here. Report the plan and wait for the owner to confirm before
executing anything in Step 4.** If the owner asks you to change something,
update the plan and confirm again before proceeding — do not treat a partial
answer as approval for the rest.

**What counts as confirmation:** an explicit, unambiguous instruction to
proceed, said after seeing this specific plan. Silence does not count. A
message that doesn't address the plan does not count. Your own judgment that
the plan looks solid does not count — that judgment is not the owner's. If
you're unsure whether something said to you was approval, it wasn't — ask
directly instead of proceeding on an inference.

## Step 4 — Execute, once approved

Two rules from the integration plan, carried over verbatim because they are
easy to drift from mid-execution:

> **Record contradictions. Do not resolve them.** When the two repos disagree,
> there is no evidence either version is correct — nothing in either repo has
> been run or invoked at scale. Preserve both, mark the disagreement, move on.

> **Preserve provenance.** Which repo (and which branch, for anything pulled
> from a non-default branch) each artifact came from. Once merged, this is not
> recoverable from the file tree — capture it now or it's gone.

As you go:

- Pull in `vibe/implementation-roadmap-4105aff`'s changes rather than losing
  them. If they conflict with something from the other repo, that is exactly
  the kind of contradiction to record, not silently resolve in either
  direction.
- Copy the defects from `verified-defects-2026-08-25.md` onto the pile
  **unfixed**. Do not fix them as you encounter the files they describe, even
  if the fix looks small.
- Copy every genuinely unresolved item out of every `loose-ends/` file onto the
  pile too — the stale `docs/SKILL_DESIGN.md` claim, the possible three-way
  `AGENTS.md` duplication, and anything else you found in Step 1 that isn't
  already handled by one of your Step 3 decisions.
- Each pile entry needs three things: what's unresolved, where it came from
  (repo, branch, or session), and why it wasn't settled now. That third field
  is what makes it sortable later — don't skip it.

## Step 5 — Report, don't just announce done

When finished, report:

- The plan you executed (link or paste it)
- Where the merged repository actually lives
- The pile's path and how many entries it holds
- Anything from Step 1's reading that you could not account for anywhere —
  say so explicitly rather than letting it quietly drop
- Anything you were not confident about and proceeded on anyway, with your
  reasoning

"It's done" is not a report. A reader who wasn't here should be able to tell
what happened from what you write.
