# Mistral Vibe Code Agent Configurations

Agent configuration files for Mistral Vibe Code.

## Available Agents

- [`default.toml`](default.toml) - 

## Configuration Format

Vibe Code agents are configured via TOML files. Each `.toml` file defines:
- `agent_type`: Type of agent (e.g., `code`, `chat`)
- `display_name`: Human-readable name
- `description`: What the agent does
- `safety`: Safety settings
- `enabled_tools`: Tools available to the agent
- `disabled_tools`: Tools explicitly disabled
- `system_prompt_id`: System prompt reference

## Discovery Paths

Vibe Code discovers agent configurations in:
- Project-level: `./.vibe/agents/` (this directory)
- User-level: `~/.vibe/agents/`

## See Also

- [Mistral Vibe Code Agents Documentation](https://docs.mistral.ai/vibe/code/cli/agents)
- [.claude/commands/](.claude/commands/) - Claude Code command configurations
