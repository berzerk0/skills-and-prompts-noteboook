# Agent Manifest

This repository contains **skills** and **subagents** for cross-tool AI agent workflows.

## Structure

```
.
├── docs/                          # Documentation
│   └── cross-agent-primitives.md  # Architecture decisions
├── skills/                       # Portable SKILL.md files (Agent Skills spec)
│   ├── timestamp/SKILL.md
│   └── codeberg/SKILL.md
├── .vibe/agents/                  # Vibe Code subagents (TOML format)
│   ├── timestamp.toml
│   └── codeberg.toml
├── .claude/agents/                # Claude Code subagents (MD+YAML)
│   ├── timestamp.md
│   └── codeberg.md
├── .pi/agents/                   # Pi Agent subagents (MD+YAML)
│   ├── timestamp.md
│   └── codeberg.md
└── *.py                          # Shared Python implementations
    ├── timestamp_skill.py
    └── codeberg_connector.py
```

## Skills (Portable)

Skills in `skills/<name>/SKILL.md` follow the **Agent Skills specification** and use only the **6 portable frontmatter fields**:

- `name` (required)
- `description` (required)
- `license` (optional)
- `compatibility` (optional)
- `metadata` (optional)
- `allowed-tools` (optional, but **tool names are NOT portable** — omit for cross-tool compatibility)

**Important**: Tool names differ across agents (e.g., `Read` vs `read` vs `read_file`). Instructions should be **tool-agnostic** ("read the file" not "use `Read`").

## Subagents (Tool-Specific)

Subagents are **NOT portable** across tools due to:

1. **Format differences**: Vibe uses TOML, Claude/Pi use Markdown+YAML
2. **Invocation model**: Vibe subagents are delegation-only (`task use <name>`), Claude/Pi support slash commands (`/<name>`)
3. **Tool name mismatches**: See `docs/cross-agent-primitives.md` for details

### Generation Strategy

Subagent files should be **generated** from a canonical source (future: YAML files in `agents/`) rather than manually maintained. This ensures consistency while respecting each tool's native format.

## Implementation Modules

Shared Python modules in the root directory provide the actual functionality:

- `timestamp_skill.py` — UTC timestamp in `YYYY-MM-DD-HHMM` format
- `codeberg_connector.py` — Full Codeberg (Gitea) API client

**All agent wrappers (SKILL.md and subagents) should invoke these modules via `bash`/`Bash`** — the only tool name consistent across all three agents.

## Adding New Skills

1. Create implementation: `new_skill.py`
2. Create portable skill: `skills/new_skill/SKILL.md` (6 fields only, tool-agnostic)
3. Create subagents:
   - `.vibe/agents/new_skill.toml`
   - `.claude/agents/new_skill.md`
   - `.pi/agents/new_skill.md`
4. Document in this file

## References

- [Agent Skills Specification](https://github.com/Agentic-AI/agent-skills) (emerging standard)
- [Claude Code Skills Docs](https://code.claude.com/docs/en/skills)
- [Vibe Code Skills Docs](https://docs.mistral.ai/vibe/code/cli/skills)
- [Cross-Agent Primitive Standardization](docs/cross-agent-primitives.md) (this repo)
