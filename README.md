# skills-and-prompts-noteboook

Skills and prompts notebook. Written by robots working as a team with me.
Part scratchpad. Part usable. Part nonsense.

Maintained jointly by **Mistral Vibe Code** and **Claude Code**. Start with
[`AGENTS.md`](AGENTS.md) — it's the shared instructions file both tools read;
[`CLAUDE.md`](CLAUDE.md) is a thin pointer to it for Claude Code specifically.

## Layout

| Directory | What's in it |
|---|---|
| [`skills/`](skills/) | Portable `SKILL.md` skills — a library, not a live discovery path for either tool. See its own README for install instructions and the source/license of each entry. |
| [`prompts/`](prompts/) | Reusable, re-runnable prompts. |
| [`docs/`](docs/) | Reference material and checked claims, including [`cross-tool-notes.md`](docs/cross-tool-notes.md) on where Vibe and Claude Code diverge. |
| [`notebooks/`](notebooks/) | Informal, exploratory notes — allowed to be wrong or unfinished. |

See [`NOTICE.md`](NOTICE.md) for licensing — this repo mixes original
content with a couple of attributed third-party and vendor-example skills,
and deliberately excludes anything under a redistribution-restricted
license.

## Companion repo

[`berzerk0/cl-repo`](https://github.com/berzerk0/cl-repo) is the verified
reference for Mistral Vibe Code's internals (source-cited, not docs-derived)
and the transferable method behind evaluating and adopting agent tooling in
general. This repo leans on it rather than re-deriving the same facts.
