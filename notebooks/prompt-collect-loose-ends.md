# Prompt — collect loose ends from a working session

Paste-ready. Everything below the line goes to a session that did work on either
repository.

**How to use it.** Send it to one session at a time. Expect questions back before
you get a file — that is the intended behaviour, not a failure. Answer them, then
let the session write its report.

**Why questions come first.** These sessions have real context but no idea a merge
is coming. A session that writes a report without asking will guess at what you
want, and guessing is the failure mode this whole exercise exists to prevent.

**If a session cannot push** (no write access, or a sandbox that cannot reach the
remote), have it paste the report in chat instead and hand it to your driving
session. Same content, slower path.

**Track who has responded.** After the merge, `ls loose-ends/` shows who reported.
Anyone missing did not answer, and you will not otherwise notice.

---

Two repositories — `berzerk0/skills-and-prompts-noteboook` and
`berzerk0/crispy-couscous` — are about to be merged into one. I am asking every
session that may have worked on either of them for anything it knows that is not
already written down in a file.

You may not be one of those sessions. Step 1 establishes whether you are, and "I
did not work on either of these" is a complete and useful answer.

**This is a retrieval task. Do not fix, refactor, merge, delete, or reorganise
anything.** Do not act on anything you find. Report only.

## Step 1 — Check where you actually are

**Run these before answering anything. Do not answer from memory** — memory of
which repo you were in, which branch you were on, or what you committed is
exactly the thing most likely to be wrong.

```bash
git remote -v              # which repository is this
git branch --show-current  # which branch (empty output means detached HEAD)
git rev-parse HEAD         # current commit
git status --short         # anything uncommitted
git log --oneline -10      # recent commits -- do you recognise this work as yours?
```

Then tell me:

- **Which of the two repositories this is**, or that it is neither
- **Whether you actually did work here.** Being checked out in a repo is not the
  same as having worked in it. If you did no work in either repository, say
  exactly that and **stop — you are done, and that is a useful answer.**
- **Whether what you find matches what you remember.** If you thought you were on
  a different branch, or expected commits that are not there, say so. That
  mismatch is itself worth reporting.

**If you have no repository checked out and cannot run git**, say so, and answer
the rest from memory — but label it clearly as from memory rather than checked.

## Step 2 — Ask me anything you need

Do this before writing anything. You almost certainly have questions, and I would
rather answer them than receive a report built on a guess. Ask about anything:
what the merge is for, whether some piece of work still matters, whether something
you did was ever finished, what counts as worth reporting.

**If you have no questions, say so explicitly and move to step 3.**

## Step 3 — Report these

You already established the mechanical facts in step 1 — repository, branch,
commit, uncommitted work. Repeat them at the top of the report so it stands on
its own.

Then the part I cannot get from git:

1. **What did you decide that never got written down?** Choices you made about
   structure, naming, approach — anything where the reasoning lives only in our
   conversation.
2. **What did you start and abandon?** And why you stopped. Half-finished work
   that looks finished is the specific thing I am worried about.
3. **What did you learn that is not in any file?** Things that did not work,
   constraints you discovered, dead ends worth not repeating.
4. **What did you do that a later reader would misread?** Anything that looks
   more finished, more tested, or more intentional than it is.

**"Nothing" is a complete answer to any of these.** A short true report beats a
padded one. Do not invent items to fill the list.

## Step 4 — Write it to a file

Create `loose-ends/<your-branch-name>.md` in the repository you worked in,
replacing any `/` in the branch name with `-`. For example, a session on
`vibe/errors-2026-08-24` writes `loose-ends/vibe-errors-2026-08-24.md`.

Plain prose under the headings above. No template, no formatting requirements.

Commit it to **your own branch** — do not switch branches, do not merge, do not
push anywhere else — and push. Then tell me the file path and the commit hash.

If you cannot push, paste the whole report to me in chat and say that pushing
failed.

## Done means

Either:

- You checked, found you did no work in either repository, and said so. **Done.**

Or:

- You checked where you are and reported it; you asked your questions and had
  them answered, or explicitly said you had none; and there is a file on your
  branch — or a report in chat — covering the mechanical facts and the four
  questions, with "nothing" where that is the honest answer.
