# Mistral Vibe Code Skills

This directory contains **symlinks** to the portable skill library in `../skills/`.

## Symlink Pattern

All skills in this directory are symbolic links pointing to `../../skills/<skill-name>/`.
This ensures:

- **Single source of truth**: Skill content lives in `skills/` directory
- **Portability**: Same skills work for both Mistral Vibe Code and Claude Code
- **Easy updates**: Changes to skills in `skills/` automatically apply to both tools

## Discovery Paths

Mistral Vibe Code discovers skills in:
- Project-level: `./.vibe/skills/` (this directory)
- User-level: `~/.vibe/skills/`

## Current Symlinks

- `_third-party-licenses` -> ../../skills/_third-party-licenses
- `ask-questions-if-underspecified` -> ../../skills/ask-questions-if-underspecified
- `braindump-triage` -> ../../skills/braindump-triage
- `challenge-my-thinking` -> ../../skills/challenge-my-thinking
- `code-review` -> ../../skills/code-review
- `cross-agent-compat` -> ../../skills/cross-agent-compat
- `ef-unblock` -> ../../skills/ef-unblock
- `import-memory` -> ../../skills/import-memory
- `notebooklm-agent` -> ../../skills/notebooklm-agent
- `planning-with-files` -> ../../skills/planning-with-files
- `prompt-committee` -> ../../skills/prompt-committee
- `prompt-pipeline` -> ../../skills/prompt-pipeline
- `search-helpers` -> ../../skills/search-helpers
- `security-audit` -> ../../skills/security-audit
- `skill-creator` -> ../../skills/skill-creator
- `skill-extractor` -> ../../skills/skill-extractor
- `task-chunkdown` -> ../../skills/task-chunkdown
- `time-estimate` -> ../../skills/time-estimate
- `vibe-internals` -> ../../skills/vibe-internals

## Adding a New Skill

1. Add the skill to `skills/` directory
2. Create a symlink: `ln -s ../../skills/<name> .vibe/skills/<name>`
3. Verify: `ls -la .vibe/skills/<name>` should show the symlink

## Configuration

The enabled skills are configured in `.vibe/config.toml`. The `enabled_skills` allowlist
was removed to allow all symlinked skills to be discovered automatically.

## See Also

- [skills/README.md](../skills/README.md) - Full skill library index
- [docs/cross-tool-notes.md](../docs/cross-tool-notes.md) - Cross-agent compatibility details
