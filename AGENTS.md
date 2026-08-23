# AGENTS.md

Shared instructions for any agent working in this repo — written primarily for
**Mistral Vibe Code** and **Claude Code** working here together. This is a
content repo: prompts, musings, docs, notebooks, and skills. There is no code
to build and no tests to run. Treat every change as documentation.

## What this repo is

A shared notebook, not a live agent configuration. Nothing under `skills/`
is auto-discovered by either tool from this location — Vibe looks in
`.vibe/skills/`, Claude Code looks in `.claude/skills/`. This repo is the
**source library** both tools' real skill directories get populated from.
See [`skills/README.md`](skills/README.md) before adding, editing, or
installing anything from here.

## Before trusting anything about Vibe internals

Don't re-derive facts about Mistral Vibe Code from memory or from
`docs.mistral.ai` alone. A companion repo,
[`berzerk0/cl-repo`](https://github.com/berzerk0/cl-repo), verified Vibe's
behavior against its own source (tool names, skill loading, subagent
isolation, hooks, token accounting) with `file:line` citations, and recorded
several places where the official docs disagree with the code. Prefer that
repo's `docs/vibe-code-reference.md` over docs.mistral.ai, and prefer Vibe's
source over both. [`docs/cross-tool-notes.md`](docs/cross-tool-notes.md) in
this repo distills only the facts load-bearing for how `skills/` is
organized here — go to `cl-repo` for the full verified reference.

## Facts most likely to be got wrong

- **Skill format is shared**, but discovery paths are not: Claude Code reads
  `./.claude/skills/` (project) or `~/.claude/skills/` (user); Vibe reads
  `./.vibe/skills/` (project) or `~/.vibe/skills/` (user) — never
  `./.agents/skills/`, despite what Vibe's docs claim.
- **`disable-model-invocation` does not exist in Vibe.** A skill written for
  Claude Code that relies on it to stay user-invocable-only becomes
  model-invocable the moment it's installed into Vibe. Narrow the
  `description` deliberately if that matters.
- **Tool names differ.** `Edit`→`edit`, `Read`→`read_file`, `Write`→
  `write_file`, `Grep`→`grep`, `Glob`→**no equivalent** in Vibe, `Bash`→
  `bash`, `Task`→`task`. Any `allowed-tools` list in a skill's frontmatter
  needs translating before the skill will work as written in the other tool.
  Vibe **silently drops** unrecognized tool names — no error, just a quietly
  crippled skill. Audit for this after every port; don't assume success
  because nothing complained.
- **Vibe skills load in two stages.** Only `name` + `description` + `path`
  are resident every turn; the full `SKILL.md` body loads on invocation via
  the `skill` tool. `user-invocable` does not change that residency.

## Editing rules

- **Never add the four proprietary Anthropic file-format skills** (`docx`,
  `pdf`, `pptx`, `xlsx`) or any other skill marked proprietary to this repo.
  Their license forbids extracting or redistributing them outside Anthropic's
  Services. See [`NOTICE.md`](NOTICE.md). Both tools ship their own
  equivalents natively — link to a tool's own docs instead of copying its
  bundle here.
- When adding a skill, record its actual source and license in
  `skills/README.md` — don't assume something is original just because it
  arrived without a bundled `LICENSE` file. Check for embedded authorship
  notices before treating content as this repo's own.
- Prompts in `prompts/` should stay reusable across sessions, not
  one-off transcripts — see [`prompts/README.md`](prompts/README.md) for the
  format convention.
- `docs/` is reference material and verified claims; `notebooks/` is
  informal, exploratory, allowed to be wrong or unfinished. Don't mix the
  two — move a notebook entry into `docs/` once it's been checked, don't
  edit it in place to look more authoritative than it is.

## Compatibility pointer for Claude Code specifically

Claude Code's own instructions file is `CLAUDE.md` at repo root — it just
points back here so both tools read one shared source of truth.
