# Vibe-Specific Documentation

This directory contains documentation specific to **Mistral Vibe Code** when working in this repository.

---

## 📚 Documentation Index

| File | Purpose |
|------|---------|
| [internals.md](internals.md) | Vibe internals deep dive (from vibe-container) |

---

## 🎯 Vibe Configuration

### Project-Level Configuration

The `.vibe/` directory contains Vibe-specific configuration:

```
.vibe/
├── skills/                 # Vibe skills (SKILL.md format)
│   ├── cross-agent-compat/ # Cross-agent compatibility helper
│   ├── code-review/        # Code review assistant
│   ├── security-audit/     # Security audit skill
│   └── vibe-internals/    # Vibe internals reference skill
├── agents/                 # Vibe agent configs
│   └── default.toml        # Default agent configuration
├── prompts/                 # Custom system prompts
└── config.toml             # Vibe configuration
```

### Agent Configuration

See `.vibe/agents/default.toml` for the default agent configuration.

Key settings:
- `active_model`: Primary model for the agent
- `bypass_tool_permissions`: Skip permission prompts
- `enabled_tools`: Tools available to the agent
- `providers`: Provider configurations (Mistral, etc.)

---

## 🔧 Skill System

### Skill Format

Vibe skills are directories containing a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: skill-name
description: What this skill does
license: MIT
compatibility:
  - vibe: ">=2.24.0"
user-invocable: true
allowed-tools:
  - read_file
  - grep
  - bash
---

# Skill Content

This skill helps with...
```

### Discovery Paths

Vibe looks for skills in:
1. `skill_paths` in `config.toml`
2. Project-level `./.vibe/skills/`
3. User-level `~/.vibe/skills/`

### Progressive Loading

- **Enabled but uninvoked**: Only name, description, path in system prompt (cheap)
- **On invocation**: Full `SKILL.md` body loaded, enters conversation history once
- **Subsequent turns**: Full content remains in context (resident)

---

## 🛠️ Tools Reference

### Builtin Tools

| Category | Tools |
|----------|-------|
| **File I/O** | `read_file`, `write_file`, `edit` |
| **Search** | `grep` |
| **Shell** | `bash`, `bash_stdin`, `bash_log_file`, `bash_output`, `bash_sessions` |
| **Git** | `git_bash`, `git_bash_stdin`, `git_bash_log_file`, `git_bash_output`, `git_bash_sessions` |
| **Web** | `web_fetch`, `web_search` |
| **Code** | `todo`, `task`, `skill` |
| **PowerShell** | `powershell`, `powershell_stdin`, `powershell_log_file`, `powershell_output`, `powershell_sessions` |

### Tool Name Translation (Vibe ↔ Claude)

| Vibe | Claude | Notes |
|------|--------|-------|
| `read_file` | `Read` | |
| `write_file` | `Write` | |
| `edit` | `Edit` | **NOT** `search_replace` |
| `grep` | `Grep` | |
| `bash` | `Bash` | |
| `task` | `Task` | |
| `todo` | N/A | Use `Task` or manual tracking |
| `skill` | N/A | Use commands or marketplace |
| `web_fetch` | `Fetch` | |
| `web_search` | `WebSearch` | |

---

## 🔗 Quick Links

- [AGENTS.md](../../AGENTS.md) - Shared instructions
- [.vibe/config.toml](../../.vibe/config.toml) - Vibe configuration
- [.vibe/agents/default.toml](../../.vibe/agents/default.toml) - Default agent
- [.vibe/skills/cross-agent-compat/SKILL.md](../../.vibe/skills/cross-agent-compat/SKILL.md) - Cross-agent skill
- [.vibe/skills/vibe-internals/SKILL.md](../../.vibe/skills/vibe-internals/SKILL.md) - Vibe internals skill

---

## 📝 Adding New Vibe Documentation

When adding new Vibe-specific documentation:

1. Create file in `docs/vibe/`
2. Add entry to the index table above
3. Reference from relevant skills
4. Keep content Vibe-specific

---

*Last updated: 2026-08-23*
