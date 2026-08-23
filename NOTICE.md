# Notice

This repository contains original prompts, skills, and musings, alongside a
small number of third-party and vendor-example skills kept for reference and
active use.

## Original content

Skills without a bundled `LICENSE` file in [`skills/`](skills/) are original
work: `ask-questions-if-underspecified`, `challenge-my-thinking`,
`copilot-preset`, `karpathy-guidelines`, `pilot-preset`, `prompt-committee`,
`prompt-pipeline`, `skill-extractor`, `solus-skill`, `task-chunkdown`. No
license is asserted over these beyond ordinary copyright; treat them as
all-rights-reserved until a `LICENSE` file says otherwise.

## Third-party content, included with attribution

| Skill | Author / source | License |
|---|---|---|
| `prompt-master` | Nidhin Joseph Nelson | MIT — see `skills/prompt-master/LICENSE` |
| `import-memory`, `morning`, `skill-creator`, `session-start-hook` | Anthropic, example skills | Apache-2.0 — see `skills/skill-creator/LICENSE.txt` and `skills/_third-party-licenses/apache-2.0-anthropic-examples.txt` |

## Deliberately excluded — do not add these

`docx`, `pdf`, `pptx`, `xlsx` (Anthropic's built-in file-format skills) are
**not** in this repo and must not be added. Their bundled license is
explicit:

> Notwithstanding anything in the Agreement to the contrary, users may not:
> extract these materials from the Services or retain copies of these
> materials outside the Services; reproduce or copy these materials...;
> distribute, sublicense, or transfer these materials to any third party...

Both Claude Code and (per the underlying file-format handling) Vibe already
provide this functionality natively — there's nothing gained by copying the
bundle here, and doing so would violate Anthropic's terms.

## Companion repo

[`berzerk0/cl-repo`](https://github.com/berzerk0/cl-repo) reviewed several
other third-party skill sources (`trailofbits/skills`, `mattpocock/skills`,
`obra/superpowers`, `anthropics/claude-plugins-official`, `blader/*`) for a
Vibe/Claude Code multi-agent setup. Check that repo's own `NOTICE.md` before
pulling anything from those sources into this one — some carry share-alike
obligations (e.g. Trail of Bits material is CC-BY-SA-4.0).
