You have no memory of any prior session in this repository. That is expected —
this is not the same kind of task as asking a session to recall its own work.

Prior sessions did real work in `crispy-couscous` and closed without a full
handoff. Most of what they knew lived only in their own conversation and is
gone. **What is not gone is anything that landed on disk in this checkout but
never got committed or pushed** — that survives independently of any session's
memory, and you can find it by looking.

**This is a retrieval task. Do not fix, refactor, merge, delete, commit over,
or push-force anything. Do not run anything destructive** (`git clean -f`,
`rm`, `git reset --hard`, force-push). Report only, except for the one new file
in step 5.

## Step 1 — Confirm this checkout actually has history worth finding

```bash
git remote -v
git branch --show-current
git rev-parse HEAD
git log --oneline -5
git reflog show --date=iso | head -20
```

If the reflog is short (a handful of entries, all from today, all matching what
`git log` already shows) and there is nothing before your own checkout, **this
is a fresh clone with nothing local to recover.** Say so plainly, skip to step
4 (the loose top-level files are still worth doing regardless of environment),
then post the status line in step 6.

If the reflog goes back further than your own session, or references commits
and branches `git log` does not show, there is local-only history here. Continue.

## Step 2 — Local git state a remote clone would never show

None of the following is visible to anyone working from a plain `git clone` of
this repository. If prior sessions left anything uncommitted, unpushed, or
stashed, this is the only place it still exists.

```bash
git stash list
git branch -vv                          # local branches and their upstream status
for b in $(git for-each-ref --format='%(refname:short)' refs/heads/); do
  echo "-- $b --"
  git log --oneline "origin/$b..$b" 2>/dev/null || echo "  (no matching remote branch)"
done
git status --ignored --short
git clean -ndx                          # DRY RUN ONLY -- lists what would be deleted, deletes nothing
```

Report: any stashes (what's in them, not just that they exist), any local
commits not on a matching remote branch, any untracked or ignored files that
look like real work rather than build output.

## Step 3 — Look for local session data, but don't assume where it is

Mistral Vibe writes a transcript per session and hands the path to a
`POST_AGENT` hook (`session_id`, `transcript_path`, `cwd`). Where those
transcripts live on disk, and what format they're in, is not documented
anywhere available to you — so search rather than guess, and report exactly
what you find, including "found nothing."

```bash
cat .vibe/hooks.toml 2>/dev/null; cat ~/.vibe/hooks.toml 2>/dev/null
echo "VIBE_HOME=$VIBE_HOME"
find "${VIBE_HOME:-$HOME/.vibe}" -maxdepth 4 -iname "*session*" -o -iname "*transcript*" 2>/dev/null
find "${VIBE_HOME:-$HOME/.vibe}" -maxdepth 4 -newer .git/HEAD 2>/dev/null | head -20
```

If you find something that looks like a session log or transcript, report its
path and describe its structure and rough contents. **Do not paste large
amounts of raw content into your report** — summarize what's in it and quote
only what's specifically relevant to loose ends.

## Step 4 — Explain the loose files already sitting in the repo root

These are already committed, so they are not secret, but nothing documents
what they are or whether they're still current:

```bash
ls -la
wc -l audit-output.md fix-plan.md fix-plan-validated.md fix-tasks.md 2>/dev/null
head -30 audit-output.md 2>/dev/null
head -30 fix-plan.md 2>/dev/null
head -30 fix-plan-validated.md 2>/dev/null
head -30 fix-tasks.md 2>/dev/null
```

For each of `audit-output.md`, `fix-plan.md`, `fix-plan-validated.md`,
`fix-tasks.md`, and `timestamp_skill.py`: say what it appears to be, whether it
looks finished or abandoned mid-way, and whether its content overlaps with
anything already in `docs/`. If you genuinely cannot tell what one is for, say
that rather than guessing.

## Step 5 — Write it up

Create `loose-ends/local-archaeology-<today's-date>.md` (e.g.
`loose-ends/local-archaeology-2026-08-26.md`), plain prose, covering steps 1–4.
"Nothing found" is a complete and correct answer for any section — do not
invent findings to fill it out.

Commit it to whatever branch you're currently on and push. If push fails,
paste the full report here in chat instead and say that pushing failed.

## Step 6 — Post a status line

Last message, on its own line:

```
LOOSE-ENDS DONE — crispy-couscous — <branch> — <what happened>
```

`<what happened>` is one of: `fresh clone, nothing local to find`,
`loose-ends/local-archaeology-<date>.md pushed`, `push failed, reported in chat
above`.
