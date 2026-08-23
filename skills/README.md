# Skills

This directory is a **library**, not a live skill path for either tool.
Neither Claude Code nor Mistral Vibe Code auto-discovers skills from here —
copy or symlink a skill directory into the tool's real discovery path to
actually use it:

| Tool | Project-level | User-level |
|---|---|---|
| Claude Code | `./.claude/skills/<name>/` | `~/.claude/skills/<name>/` |
| Mistral Vibe Code | `./.vibe/skills/<name>/` | `~/.vibe/skills/<name>/` |

Format is shared: a directory containing `SKILL.md` with YAML frontmatter
(`name`, `description`, optionally `license`, `allowed-tools`/`enabled_tools`,
`user-invocable`). See [`../docs/cross-tool-notes.md`](../docs/cross-tool-notes.md)
for the differences that bite when moving a skill between the two — tool
name translation, the missing `disable-model-invocation` in Vibe, and Vibe's
silent-drop behavior on unrecognized tool names. **Never install a skill into
either tool without checking that doc first** — a skill that looks installed
can be silently missing a capability.

## Index

| Skill | Source | License | Notes |
|---|---|---|---|
| `ask-questions-if-underspecified` | original | none asserted | Clarify before acting on ambiguous requests. |
| `challenge-my-thinking` | original | none asserted | Socratic stress-test for plans/decisions. Already ported from Mistral Vibe once — see its own frontmatter. |
| `copilot-preset` | original | none asserted | Always-on compressed-output + clarification preset. |
| `karpathy-guidelines` | original, cites [@karpathy](https://x.com/karpathy/status/2015883857489522876) | none asserted | Coding-discipline guidelines; **flagged retired in `cl-repo`'s Vibe install plan** — check that repo's `docs/skill-action-plan-v3.md` amendments before installing into Vibe. |
| `pilot-preset` | original | none asserted | Bundles `solus-skill` + `karpathy-guidelines` + `ask-questions-if-underspecified`. |
| `prompt-committee` | original | none asserted | Send a prompt/decision to another model for review, triage the feedback. |
| `prompt-pipeline` | original | none asserted | Five-phase idea → production prompt workflow; depends on `prompt-master` + `prompt-committee`. |
| `skill-extractor` | original | none asserted | Extract a reusable skill from a work session. |
| `solus-skill` | original | none asserted | Compressed, answer-first communication mode. |
| `task-chunkdown` | original | none asserted | Break a large task into granular first steps. |
| `prompt-master` | third-party — [Nidhin Joseph Nelson](https://github.com) | MIT (bundled `LICENSE`) | Generates tool-specific prompts. `prompt-pipeline` depends on this — keep both in sync if either is edited. |
| `import-memory` | Anthropic example skill | Apache-2.0 ([shared copy](_third-party-licenses/apache-2.0-anthropic-examples.txt)) | Imports another assistant's memory export. |
| `morning` | Anthropic example skill | Apache-2.0 ([shared copy](_third-party-licenses/apache-2.0-anthropic-examples.txt)) | Morning-brief artifact / recurring task. |
| `skill-creator` | Anthropic example skill | Apache-2.0 (bundled `LICENSE.txt`) | Create and iterate on skills; the tool used to build most of the skills in this repo. |
| `session-start-hook` | Anthropic example skill | Apache-2.0 ([shared copy](_third-party-licenses/apache-2.0-anthropic-examples.txt)) | `SessionStart` hooks for Claude Code on the web. Claude-Code-specific — the hook mechanism doesn't map onto Vibe's `PRE_TOOL`/`POST_AGENT` model; see `cl-repo`'s reference before attempting a Vibe port. |

**Not included, on purpose:** `docx`, `pdf`, `pptx`, `xlsx`. These are
Anthropic's proprietary built-in skills — their license forbids extracting or
redistributing them outside Anthropic's Services. See [`../NOTICE.md`](../NOTICE.md).
Both tools ship their own file-format handling natively; there is nothing to
port.

## Adding a skill here

1. Confirm what you're actually adding: original content, a third-party
   skill under its own license, or an example from a tool vendor. Check for
   an embedded `LICENSE`/`README` before assuming authorship — several
   entries above were mislabeled "custom" upstream and turned out to be
   third-party.
2. Add a row to the table above with source and license.
3. If the skill has a tool-scoping list (`allowed-tools` / `enabled-tools`),
   note in this table (or the skill's own frontmatter comment) whether it's
   been translated for both tools, or only tested on one.
4. Never add anything under a proprietary or redistribution-restricted
   license.
