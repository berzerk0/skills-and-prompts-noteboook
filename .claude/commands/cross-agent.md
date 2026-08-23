# Claude Code: Cross-Agent Compatibility Commands

> **Purpose:** Enable Claude Code to work seamlessly with the dual-agent repository structure. This file provides Claude-specific commands and integrations that mirror the Vibe skills.

---

## 🎯 Overview

This repository is designed to work with **both Mistral Vibe Code and Claude Code**. While Vibe uses a skill system based on `SKILL.md` files, Claude uses commands, MCP servers, and marketplace skills.

This file documents Claude-specific configurations that provide equivalent functionality to the Vibe skills in this repo.

---

## 📁 Repository Structure for Claude

```
skills-and-prompts-notebook/
├── AGENTS.md                    # Shared compatibility layer (read by both)
├── CLAUDE.md                    # Pointer to AGENTS.md for Claude
├── README.md                    # Repository overview
│
├── .vibe/                       # Mistral Vibe configuration
│   └── skills/                 # Vibe skills (SKILL.md format)
│       ├── cross-agent-compat/
│       ├── code-review/
│       └── security-audit/
│
├── .claude/                     # Claude Code configuration (THIS DIRECTORY)
│   ├── commands/               # Custom Claude commands (THIS FILE)
│   │   ├── cross-agent.md      # Cross-agent compatibility
│   │   ├── code-review.md      # Code review commands
│   │   └── security-audit.md    # Security audit commands
│   └── skills/                 # Claude skills (future)
│
├── docs/                        # Documentation
│   └── shared/                 # Cross-agent docs
│
├── skills/                      # Portable skill library
│   ├── ask-questions-if-underspecified/
│   ├── challenge-my-thinking/
│   └── ...
│
└── notebooks/                   # Working documents
```

---

## 🔧 Claude Configuration

### Required Settings

Add to your `~/.claude/settings.json`:

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  },
  "features": {
    "enableMCP": true,
    "enableMarketplaceSkills": true
  },
  "workspaceTrust": {
    "enabled": true,
    "trustedDirectories": [
      "/path/to/skills-and-prompts-notebook"
    ]
  }
}
```

### Recommended Marketplace Skills

```bash
# Install these skills for enhanced functionality
claude plugin marketplace add anthropics/skills
claude plugin marketplace add trailofbits/skills
claude plugin marketplace add trailofbits/skills-curated
```

---

## 📋 Tool Translation: Vibe → Claude

| Vibe Tool | Claude Tool | Notes |
|-----------|--------------|-------|
| `read_file: path` | `Read: path` | Direct equivalent |
| `write_file: path, content` | `Write: path, content` | Direct equivalent |
| `edit: old, new` | `Edit: path, old, new` | **NOT** search_replace |
| `grep: pattern, path` | `Grep: pattern, path` | Direct equivalent |
| `bash: "command"` | `Bash: "command"` | Direct equivalent |
| `task: "description"` | `Task: "description"` | Both spawn subagents |
| `todo: [...]` | Use `Task` or manual tracking | Claude doesn't have structured todo |
| `skill: name` | Use commands or marketplace skills | No direct equivalent |
| `web_fetch: url` | `Fetch: url` | Direct equivalent |
| `web_search: query` | `WebSearch: query` | Direct equivalent |

---

## 🎯 Cross-Compatible Patterns

### Pattern 1: Universal File Reader
```
Read: path/to/file.txt
# Process content
Write: path/to/result.txt, "processed content"
```

### Pattern 2: Safe Directory Listing
```
Bash: "ls -la /path/to/directory"
Bash: "find /path/to/directory -type f -name '*.py'"
```

### Pattern 3: Multi-File Search
```
Grep: "search_pattern", "/path/to/directory"
Bash: "rg 'pattern' /path/to/directory"
```

### Pattern 4: Task Delegation
```
Task: "Analyze the codebase for security issues. Write findings to /tmp/security-audit.md"
Read: /tmp/security-audit.md
```

---

## 🔗 Related Files

### In This Repository
- [AGENTS.md](../../AGENTS.md) - Shared compatibility layer
- [.vibe/skills/cross-agent-compat/SKILL.md](../.vibe/skills/cross-agent-compat/SKILL.md) - Vibe cross-agent skill
- [.vibe/skills/code-review/SKILL.md](../.vibe/skills/code-review/SKILL.md) - Vibe code review skill
- [.vibe/skills/security-audit/SKILL.md](../.vibe/skills/security-audit/SKILL.md) - Vibe security audit skill
- [docs/cross-tool-notes.md](../../docs/cross-tool-notes.md) - Tool translation reference

### External Resources
- [Claude Code Documentation](https://docs.claude.com/en/docs)
- [Mistral Vibe Docs](https://docs.mistral.ai/vibe/)
- [cl-repo](https://github.com/berzerk0/cl-repo) - Verified Vibe internals reference

---

*File version: 1.0.0*
*Last updated: 2026-08-23*
*Compatibility: Claude Code >= 1.0*
