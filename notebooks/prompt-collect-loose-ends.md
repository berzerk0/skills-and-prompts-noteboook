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

The two repositories you have worked in — `berzerk0/skills-and-prompts-noteboook`
and `berzerk0/crispy-couscous` — are about to be merged into one. Before that
happens I need to capture anything you know that is not already written down in a
file somewhere.

**This is a retrieval task. Do not fix, refactor, merge, delete, or reorganise
anything.** Do not act on anything you find. Report only.

## Step 1 — Ask me anything you need first

Do this before writing anything. You almost certainly have questions, and I would
rather answer them than receive a report built on a guess. Ask about anything:
what the merge is for, whether some piece of work still matters, whether something
you did was ever finished, what counts as worth reporting.

**If you have no questions, say so explicitly and move to step 2.**

## Step 2 — Report these

Start with the mechanical facts:

- **Which repository** you worked in
- **Your branch name** and **current commit** (`git rev-parse HEAD`)
- **Anything uncommitted** in your working tree right now (`git status`)

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

## Step 3 — Write it to a file

Create `loose-ends/<your-branch-name>.md` in the repository you worked in,
replacing any `/` in the branch name with `-`. For example, a session on
`vibe/errors-2026-08-24` writes `loose-ends/vibe-errors-2026-08-24.md`.

Plain prose under the headings above. No template, no formatting requirements.

Commit it to **your own branch** — do not switch branches, do not merge, do not
push anywhere else — and push. Then tell me the file path and the commit hash.

If you cannot push, paste the whole report to me in chat and say that pushing
failed.

## Done means

You have either asked your questions and had them answered, or explicitly said you
had none — and there is a file on your branch (or a report in chat) covering the
three mechanical facts and the four questions, with "nothing" where that is the
honest answer.
