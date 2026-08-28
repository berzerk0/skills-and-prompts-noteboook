# AGENTS.md template

Fill each section by hand from the interview. Delete any section with nothing
project-specific to say -- an empty section is better than a padded one, and a
deleted one is better than an empty one.

The one test that decides whether a line belongs here: **could the agent infer
this from the code, a package manifest, or a lint config?** If yes, delete it.
Restating an enforced rule costs tokens every turn and buys nothing.

Length: aim for 30-100 lines, treat ~150 as the point of diminishing returns,
and remember pi concatenates this file with the global one and every ancestor
`AGENTS.md` -- the budget covers the sum. Generic, bulk-generated content is
reported to reduce agent task success while raising cost; treat that as a
working heuristic rather than a measured law.

---

## Template body

```markdown
# AGENTS.md

## Project overview

<!-- 2-3 sentences. What this does, who or what consumes it, and WHY it
     exists -- what breaks if it goes away. Note monorepo/monolith shape. -->

## Setup commands

<!-- Exact and copy-pasteable: install, build, run locally, with flags.
     State the runtime constraints an agent cannot infer: language version,
     whether commands run inside a container or on the host, virtualenv or
     toolchain activation, globally installed dependencies. -->

## Test commands

<!-- Full suite, a single file, a single test. Where the CI config lives.
     If the local command differs from what CI runs, say both. -->

## Code style

<!-- ONLY what the formatter and linter do not already enforce. One real
     snippet from this codebase beats three paragraphs. If a linter covers
     it, delete it. -->

## Architecture notes

<!-- Non-obvious structure only: module boundaries, and WHY they are drawn
     where they are. What a new teammate needs explained, never what the
     file tree already shows. -->

## Protected paths

<!-- Files an agent must not edit directly: lockfiles, generated code,
     migrations, vendored dependencies, golden-output fixtures. Say how each
     is regenerated instead. -->

## Commit and PR guidelines

<!-- Branch naming, commit message format, PR title format. -->

## Security considerations

<!-- Secrets handling, auth patterns, dependency constraints -- the things a
     linter cannot catch. Keep it specific to this project; generic security
     advice belongs nowhere. -->

## Global conventions

- ASCII only in identifiers, commit messages, comments, and any prose you
  write. No smart quotes, em dashes, curly apostrophes, or unicode arrows.
  String literals, data files, and user-facing content follow project need.
- Do not invent file paths, APIs, or CLI flags. Verify against the repo
  before using one.
- Keep diffs minimal and surgical. Do not reformat or refactor code outside
  the requested change, even where it looks wrong.
- Never commit secrets, keys, tokens, or credentials, including in examples
  and test fixtures.
- State assumptions explicitly when the spec is ambiguous, rather than
  guessing silently.
- Match the style of the file being edited when it conflicts with generic
  best practice.
- Leave pre-existing test and lint failures alone unless fixing them is the
  assigned task. Report them instead.
- Ask before committing, pushing, deploying, running destructive commands, or
  editing generated files.
```

---

## Notes on two of the global conventions

**ASCII.** The rule is scoped to what the agent writes, not to the project's
data. An earlier unqualified version drew the objection that it bans CJK, i18n
strings, and math notation. Scoping fixes that without a project-type exception
clause -- exceptions invite an agent to declare itself exempt.

**Ask before committing or pushing.** Most agent harnesses already gate these,
so this line arguably restates an enforced rule. Kept because the enforcement
varies by harness and the cost of restating it is one line. Delete it if the
harness in use already blocks these reliably.

## Placement

- A root `AGENTS.md` applies to the whole repo.
- pi walks up from cwd and concatenates every `AGENTS.md` it finds, plus the
  global `~/.pi/agent/AGENTS.md`. Nested files add to the root file; they do not
  replace it.
- `AGENTS.override.md` in a directory replaces `AGENTS.md` and `CLAUDE.md` for
  that directory only. It does not suppress the global file. Reach for it only
  when a subdirectory must contradict the root, not to scope ordinary additions.
- pi also reads `CLAUDE.md`. Precedence between `AGENTS.md` and `CLAUDE.md` in
  the same directory is not documented in sources checked -- avoid keeping both
  in one directory until you have verified which wins.
