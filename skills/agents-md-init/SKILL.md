---
name: agents-md-init
description: "Builds a workspace AGENTS.md for pi by interviewing the user, section by section, and writing a non-loading AGENTS.candidate.md draft for review. Use when someone wants to set up agent instructions for a repo, asks for an AGENTS.md, says the agent keeps getting the project's conventions wrong, or is onboarding a fresh workspace or devcontainer that has no context file yet."
---

# AGENTS.md Init

Produces a workspace `AGENTS.md` for pi. Inspects the repo lightly, then asks
the user for what it cannot read. Writes a candidate file the user promotes by
hand.

Two rules override everything else in this skill:

- **Never write `AGENTS.md`, `CLAUDE.md`, or `AGENTS.override.md`.** Write only
  `AGENTS.candidate.md`. Those three filenames load into pi's context; the
  candidate name does not, so a rejected draft pollutes no future session.
- **Never overwrite an existing file.** If the target exists, show a diff and
  ask.

## Step 0: declare the target and measure the budget

Print the absolute path you will write to before doing anything else.

pi concatenates every context file it finds -- the global one plus every
`AGENTS.md` walking up from cwd -- so the length budget applies to the sum, not
to one file. Measure what is already loaded:

```sh
found=0
echo "global:"
g="$HOME/.pi/agent/AGENTS.md"
if [ -s "$g" ]; then echo "  $(wc -l < "$g") lines  $g"; found=1; else echo "  none ($g)"; fi
echo "ancestors of $PWD:"
d="$PWD"
while :; do
  for n in AGENTS.md CLAUDE.md AGENTS.override.md; do
    if [ -f "$d/$n" ]; then echo "  $(wc -l < "$d/$n") lines  $d/$n"; found=1; fi
  done
  echo "  scanned: $d"
  [ "$d" = / ] && break
  d=$(dirname "$d")
done
[ "$found" = 0 ] && echo "RESULT: no context files anywhere"
```

Report the total. Aim for 30-100 lines across all layers, and treat ~150 as the
point where added lines stop helping. If existing layers already spend most of
that, say so and target the remainder.

If an `AGENTS.md` already exists in the repo root, read it. The job becomes
"propose a revision as a candidate," not "start from scratch."

## Step 1: read before asking

Never ask for anything the repo already states. Read what exists:

- Package manifests and lockfiles: build, test, and run commands, language
  version, dependency set
- Linter and formatter configs: everything they enforce is off-limits for the
  Code style section
- CI config: the commands that actually gate a merge
- `README`, `CONTRIBUTING`, `.editorconfig`, `Makefile`, `justfile`
- The directory tree, one or two levels deep

Keep this to a few minutes of reading. Report what you learned in three or four
lines so the user can correct a wrong reading before it reaches the file.

## Step 2: interview in batches

Ask in 2-3 rounds, not one question per section. Every question is numbered,
options are lettered, defaults are marked, and `defaults` accepts all of them.

Round 1 covers what no repo file reveals:

```text
1) Why does this project exist -- what breaks if it goes away? (one sentence)
2) Which commands do you actually run, and where?
   a) exactly what CI runs (default)
   b) different locally -- specify
3) Are these commands run inside a container or on the host?
   a) inside the devcontainer (default)
   b) host
   c) both, and they differ -- specify
4) Any path an agent must not edit?
   a) lockfiles and generated code only (default)
   b) also migrations, vendored code, or fixtures -- specify
   c) none

Reply with: defaults (or 1... 2a 3a 4a)
```

Round 2 covers judgment the code does not encode:

```text
5) Which convention gets broken most often by someone new?
6) What would a new teammate need explained that the file tree does not show?
7) Branch and commit format?
   a) whatever git log already shows (default)
   b) specify
8) Anything security-sensitive a linter cannot catch?
```

Rules for this step:

- A section with nothing worth saying stays a comment. An empty section beats a
  padded one.
- If an answer restates what a linter or manifest already enforces, say so and
  drop it rather than writing it down.
- Push back once on an answer that is generic advice rather than a fact about
  this project. Generic content measurably hurts: it costs tokens every turn and
  tells the agent nothing it could not infer. (heuristic, not a measured law
  -- see the note in references/template.md)

## Step 3: write the candidate

Fill `references/template.md` from the answers. Delete every section the user
had nothing for -- do not leave an instruction to the agent that says nothing.

Write to `<repo-root>/AGENTS.candidate.md`. If that file exists, diff against it
and ask before replacing.

## Step 4: hand off

Print the final line count against the budget from Step 0, then tell the user
exactly how to promote it:

```sh
mv AGENTS.candidate.md AGENTS.md
```

Then `/reload` in pi, or restart it. Say both -- a context file edited mid-session
does not take effect on its own.

## What this skill does not do

- It does not write or edit `$HOME/.pi/agent/AGENTS.md`. That file is global to
  the container; changing it changes every project. Read it for the budget, and
  leave it alone.
- It does not use `AGENTS.override.md`. That file replaces `AGENTS.md` and
  `CLAUDE.md` for one directory, and it is the wrong tool for a first draft. It
  suppresses nothing from the global layer.
