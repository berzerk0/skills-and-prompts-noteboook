# Shared Documentation

This directory contains documentation that applies to both **Mistral Vibe Code** and **Claude Code** when working in this repository.

---

## 📚 Documentation Index

| File | Purpose |
|------|---------|
| [workflows.md](workflows.md) | Cross-agent workflow patterns |
| [patterns.md](patterns.md) | Reusable code patterns for both agents |
| [best-practices.md](best-practices.md) | General best practices |

---

## 🎯 Key Principles

### 1. Dual-First Design
Every artifact should work with both agents:
- **Mistral Vibe Code** (primary focus)
- **Claude Code** (secondary focus)
- **Self-documenting** for human readers

### 2. Directory Structure

```
skills-and-prompts-notebook/
├── AGENTS.md                    # Shared compatibility layer
├── CLAUDE.md                    # Pointer to AGENTS.md for Claude
├── README.md                    # Repository overview
│
├── .vibe/                       # Mistral Vibe configuration
│   ├── skills/                 # Vibe skills (SKILL.md format)
│   │   ├── cross-agent-compat/ # Cross-agent compatibility helper
│   │   ├── code-review/        # Code review assistant
│   │   ├── security-audit/     # Security audit skill
│   │   └── vibe-internals/    # Vibe internals reference
│   ├── agents/                 # Vibe agent configs
│   │   └── default.toml
│   ├── prompts/                 # Custom system prompts
│   └── config.toml             # Vibe configuration
│
├── .claude/                     # Claude Code configuration
│   ├── commands/               # Custom Claude commands
│   │   ├── cross-agent.md      # Cross-agent compatibility
│   │   ├── code-review.md      # Code review commands
│   │   └── security-audit.md   # Security audit commands
│   └── skills/                 # Claude skills (future)
│
├── docs/                        # Documentation
│   ├── shared/                 # Cross-agent docs (THIS DIRECTORY)
│   │   ├── README.md           # This file
│   │   ├── workflows.md
│   │   └── patterns.md
│   ├── vibe/                   # Vibe-specific docs
│   │   └── internals.md        # Vibe internals deep dive
│   └── claude/                 # Claude-specific docs
│
├── skills/                      # Portable skill library
│   ├── ask-questions-if-underspecified/
│   ├── challenge-my-thinking/
│   ├── code-review/            # Code review skill (library version)
│   ├── cross-agent-compat/      # Cross-agent compatibility
│   ├── import-memory/
│   ├── prompt-committee/
│   ├── prompt-pipeline/
│   ├── security-audit/         # Security audit skill (library version)
│   ├── skill-creator/
│   ├── skill-extractor/
│   └── task-chunkdown/
│
├── prompts/                     # Reusable prompts
│
└── notebooks/                   # Working documents
```

### 3. How It Works

- **`skills/`**: Library of portable `SKILL.md` files. Copy to `.vibe/skills/` or `.claude/skills/` to use.
- **`.vibe/skills/`**: Live Vibe skills for this project
- **`.claude/commands/`**: Claude command documentation
- **`docs/`**: Reference material and verified claims
- **`notebooks/`**: Informal, exploratory notes

---

## 🔗 Quick Links

- [AGENTS.md](../../AGENTS.md) - Shared instructions for both agents
- [docs/cross-tool-notes.md](../../docs/cross-tool-notes.md) - Tool translation table
- [skills/README.md](../../skills/README.md) - Skill library index
- [.vibe/skills/cross-agent-compat/SKILL.md](../../.vibe/skills/cross-agent-compat/SKILL.md) - Cross-agent skill

---

## 📝 Adding New Documentation

When adding new shared documentation:

1. Create file in `docs/shared/`
2. Add entry to the index table above
3. Reference from relevant skills/commands
4. Keep content cross-agent compatible

---

*Last updated: 2026-08-23*
