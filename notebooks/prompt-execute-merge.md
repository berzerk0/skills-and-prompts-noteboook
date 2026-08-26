You are merging two GitHub repositories into one: `berzerk0/skills-and-prompts-noteboook`
and `berzerk0/crispy-couscous`. Nobody has decided the target layout yet — that
is part of your job, not something to infer from what follows.

You have no memory of any prior session on either repository. That is
intended. Everything you need is in the files below; read them yourself rather
than trusting a summary, including this one.

**This is a consequential, partly irreversible action on real repositories.
Plan first, get sign-off, then execute. Do not skip the sign-off step because
the plan seems obvious to you.**

## Step 1 — Read the primary sources, not a summary of them

In `skills-and-prompts-noteboook`, on branch `notebook/foundation-harness-exercise`:

- `notebooks/integration-plan-2026-08-25.md` — the plan this task is phase 2
  of. Read it in full, including the appendix.
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
    enumeration.**

Do **not** open `notebooks/IDEAL.md` for this task — it is the scoring sheet
for the phase after this one, not an input to the merge itself.

## Step 2 — Get the real repository state yourself

**Shallow clones lie about history. This is not hypothetical — it happened
during the planning for this exact merge:** a `--depth 1` clone of
crispy-couscous reported all three of its non-main branches as 40-50 commits
ahead and unmerged. A full clone showed two were already merged and the third
had exactly one unmerged commit. `git merge-base`, ahead/behind counts, and
anything else that depends on history are **meaningless against a shallow
clone** — it doesn't just under-report, it fabricates plausible-looking wrong
numbers.

Clone both repositories fresh, with no `--depth` flag. For each:

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

Nothing has settled these. You are deciding them, not discovering a pre-made
answer:

1. **Which repository is the base, or is this a new repository?** State which,
   and why.
2. **What happens to skills that exist in both repos with different content?**
   `challenge-my-thinking` and `skill-extractor` are the known cases — check
   for others yourself, do not assume the list is complete. Per the plan: do
   not resolve which version wins. Keep both, record the conflict.
3. **What happens to crispy-couscous's build tooling** (`meta/generate_*.py`,
   the `agents/` YAML directory, `.claude/`, `.vibe/`, `.pi/`)? This is the
   only working, verified piece of infrastructure either repo has — regenerating
   from `agents/*.yaml` currently produces zero diff against checked-in output.
   Whatever layout you choose, that property should still hold afterward, or
   you should say clearly that it doesn't and why.
4. **What happens to `vibe/implementation-roadmap-4105aff`?** It is real,
   finished work, not a stale branch. It cannot simply be left behind or
   silently overwritten by whatever the merge does to `.vibe/agents/`.
5. **Git history: preserved, or a fresh start with provenance recorded in
   files instead?** Either is defensible. State which and why — this is
   effectively permanent once done.
6. **Where does the pile live?** One markdown file, per the plan — pick its
   path.

Write this as a short plan file (anywhere sensible — your call), covering all
six points with your reasoning, not just your conclusion.

**Stop here. Report the plan and wait for the owner to confirm before
executing anything in Step 4.** If the owner asks you to change something,
update the plan and confirm again before proceeding — do not treat a partial
answer as approval for the rest.

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
