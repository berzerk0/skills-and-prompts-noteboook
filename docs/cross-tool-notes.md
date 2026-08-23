# Cross-tool notes: Claude Code ↔ Mistral Vibe Code

Distilled from [`berzerk0/cl-repo`](https://github.com/berzerk0/cl-repo)'s
`docs/vibe-code-reference.md`, which verified these against Vibe's source
(`mistralai/mistral-vibe` @ `a84be03`, v2.24.3, 2026-08-20) with `file:line`
citations. **Go there for the full reference and evidence**; this file only
keeps what's load-bearing for how `skills/` in this repo is organized. If
you're on a materially newer Vibe version, treat anything here as suspect
and re-check against that repo.

## Skill format is shared, discovery paths are not

Both tools read a directory containing `SKILL.md` with YAML frontmatter.
Fields Vibe actually parses: `name`, `description`, `license`,
`compatibility`, `metadata`, `allowed-tools`, `user-invocable`.

| | Claude Code | Vibe |
|---|---|---|
| Project-level | `./.claude/skills/` | `./.vibe/skills/` |
| User-level | `~/.claude/skills/` | `~/.vibe/skills/` |

Vibe's own docs claim `./.agents/skills/` also works. It does not — checked
against source, not just the docs.

## Tool name translation

Rewrite `allowed-tools` before installing a skill written for one tool into
the other:

| Claude Code | Vibe | Note |
|---|---|---|
| `Read` | `read_file` | |
| `Write` | `write_file` | |
| `Edit` | `edit` | Not `search_replace` — that tool doesn't exist in Vibe |
| `Grep` | `grep` | |
| `Glob` | *(none)* | No glob/list tool in Vibe. Use `grep`, or `bash` running `find`/`ls` |
| `Bash` | `bash` | |
| `Task` | `task` | |
| `AskUserQuestion` | `ask_user_question` | Unavailable to Vibe subagents |

**Vibe silently drops unrecognized tool names** — no error, the skill just
loses the capability quietly. Audit every port for this; a broken port looks
identical to a working one until you check.

## `disable-model-invocation` does not exist in Vibe

A Claude Code skill using this frontmatter field to stay user-invocable-only
becomes model-invocable the moment it's ported into Vibe — costing
description tokens every turn and firing unpredictably. The only lever Vibe
has is `enabled_skills`/`disabled_skills` in `config.toml` (global,
all-or-nothing per skill, supports exact names/globs/`re:`-prefixed regex).
If a skill's behavior depends on staying model-invocation-free, narrow its
`description` deliberately instead of relying on the flag.

## Context residency differs

Vibe loads skills in two stages: only `name` + `description` + `path` are
resident in the system prompt every turn. The full `SKILL.md` body loads via
the `skill` tool on invocation, then stays resident for the rest of the
session. `user-invocable: true` does not change this — enabling many skills
is cheap; invoking a large one is a one-time-per-session cost, not
per-turn. Claude Code's own residency model may differ — don't assume parity
without checking.

## AGENTS.md loading

Vibe is **not** limited to two `AGENTS.md` files (contrary to its own docs):
it loads the user-level file plus one per project root, walking up to the
trust root, and additional files are auto-discovered for lazy injection when
reading files below open project roots. All are resident every turn once
loaded — an always-on cost.

## Hooks

Vibe has hooks: `PRE_TOOL`, `POST_TOOL`, `POST_AGENT`, configured in
`hooks.toml` (`.vibe/hooks.toml` project-level, `~/.vibe/hooks.toml`
user-level) — not `hooks.json`. Rough Claude Code mapping: `PRE_TOOL` ≈
`PreToolUse`, `POST_AGENT` ≈ `Stop`. **`UserPromptSubmit` has no Vibe
equivalent at all.**

## When in doubt

Trust the tool's own source over its docs, and trust the artifact the tool
actually parses over one written for a human to read — both tools' docs
have been caught describing an older or simpler model than the code
implements. See `cl-repo`'s `METHOD.md` for the general version of this
rule and how it was arrived at.
