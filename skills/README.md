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
| `challenge-my-thinking` | original | none asserted | Socratic stress-test for plans/decisions. |
| `prompt-committee` | original | none asserted | Send a prompt/decision to another model for review, triage the feedback. |
| `prompt-pipeline` | original | none asserted | Five-phase idea → production prompt workflow. |
| `skill-extractor` | original | none asserted | Extract a reusable skill from a work session. |
| `task-chunkdown` | original | none asserted | Break a large task into granular first steps. Successor to "Todo Goblin" (see `../archive/`) — built independently, before the archive was rediscovered. No new skill needed for Todo Goblin; this one already does the job, with a better delivery model (drip-fed steps vs. an upfront checklist). |
| `ef-unblock` | original, adapted from archive | none asserted | Clarify a goal and name the executive-function trap blocking the start. Adapted from "EF Goblin" (`../archive/original-goblins.txt`) — kept the trap taxonomy and questioning framework, dropped the chat-mode activation/exit scaffolding. |
| `time-estimate` | original, adapted from archive | none asserted | Realistic time range with rationale, never a single number. Adapted from "Time Goblin" (`../archive/`) — estimation logic and range-sizing heuristics kept as-is; scaffolding dropped. |
| `braindump-triage` | original, adapted from archive | none asserted | Convert a brain dump into an actionable list, triaged do-now/do-later/delegate/drop. Adapted from "Braindump Goblin" (`../archive/original-goblins.txt`) — sharpened against real mind-sweep/ADHD brain-dump practice (GTD's mind sweep, action-bucket triage) rather than ported as-is: added explicit permission to drop trivial items and a destination step, replacing the original's topic-only tagging. |
| `import-memory` | Anthropic example skill | Apache-2.0 ([shared copy](_third-party-licenses/apache-2.0-anthropic-examples.txt)) | Imports another assistant's memory export. |
| `skill-creator` | Anthropic example skill | Apache-2.0 (bundled `LICENSE.txt`) | Create and iterate on skills; enables testing and refining skills in this repo. |

**Not included, on purpose:** `docx`, `pdf`, `pptx`, `xlsx`. These are
Anthropic's proprietary built-in skills — their license forbids extracting or
redistributing them outside Anthropic's Services. See [`../NOTICE.md`](../NOTICE.md).
Both tools ship their own file-format handling natively; there is nothing to
port.

**Intentionally removed:** `copilot-preset`, `karpathy-guidelines`, `pilot-preset`,
`solus-skill`, `prompt-master`, `morning`, `session-start-hook`. These were
ported initially but removed as out-of-scope for this notebook's focus on
reusable skills and prompts.

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
