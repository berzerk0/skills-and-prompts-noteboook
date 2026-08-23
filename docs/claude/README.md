# Claude-Specific Documentation

This directory contains documentation specific to **Claude Code** when working in this repository.

---

## 📚 Documentation Index

| File | Purpose |
|------|---------|

*(Currently empty - add Claude-specific docs as needed)*

---

## 🎯 Claude Configuration

### Project-Level Configuration

The `.claude/` directory contains Claude-specific configuration:

```
.claude/
├── commands/               # Custom Claude commands
│   ├── cross-agent.md      # Cross-agent compatibility
│   ├── code-review.md      # Code review commands
│   └── security-audit.md   # Security audit commands
└── skills/                 # Claude skills (future)
```

### Settings

Claude Code uses `~/.claude/settings.json` for configuration:

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
  "features": {
    "enableMCP": true,
    "enableMarketplaceSkills": true
  }
}
```

### Discovery Paths

Claude looks for skills in:
- Project-level `./.claude/skills/`
- User-level `~/.claude/skills/`

---

## 🔧 Command System

Claude uses a command-based system. This repository provides:

### Custom Commands

| Command | File | Purpose |
|---------|------|---------|
| `/code-review` | [code-review.md](../.claude/commands/code-review.md) | Code review workflow |
| `/security-audit` | [security-audit.md](../.claude/commands/security-audit.md) | Security audit workflow |
| `/cross-agent-info` | [cross-agent.md](../.claude/commands/cross-agent.md) | Cross-agent compatibility info |

### Marketplace Skills

Recommended marketplace skills:

```bash
# Install Trail of Bits skills
claude plugin marketplace add trailofbits/skills

# Install Anthropics skills
claude plugin marketplace add anthropics/skills
```

---

## 🛠️ Tools Reference

### Builtin Tools

| Category | Tools |
|----------|-------|
| **File I/O** | `Read`, `Write`, `Edit` |
| **Search** | `Grep` |
| **Shell** | `Bash` |
| **Web** | `Fetch`, `WebSearch` |
| **Code** | `Task` |

### Tool Name Translation (Claude ↔ Vibe)

| Claude | Vibe | Notes |
|--------|------|-------|
| `Read` | `read_file` | |
| `Write` | `write_file` | |
| `Edit` | `edit` | Vibe has **NO** `search_replace` |
| `Grep` | `grep` | |
| `Bash` | `bash` | |
| `Task` | `task` | |
| `Fetch` | `web_fetch` | |
| `WebSearch` | `web_search` | |

---

## 🔗 Quick Links

- [AGENTS.md](../../AGENTS.md) - Shared instructions
- [CLAUDE.md](../../CLAUDE.md) - Claude pointer file
- [.claude/commands/cross-agent.md](../../.claude/commands/cross-agent.md) - Cross-agent commands
- [.claude/commands/code-review.md](../../.claude/commands/code-review.md) - Code review commands
- [.claude/commands/security-audit.md](../../.claude/commands/security-audit.md) - Security audit commands

---

## 📝 Adding New Claude Documentation

When adding new Claude-specific documentation:

1. Create file in `docs/claude/`
2. Add entry to the index table above
3. Reference from relevant commands
4. Keep content Claude-specific

---

*Last updated: 2026-08-23*
