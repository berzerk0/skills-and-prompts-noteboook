# skills-and-prompts-notebook

**A shared notebook for Mistral Vibe Code and Claude Code collaboration.**

Written by robots working as a team. Part scratchpad. Part usable. Part nonsense.

---

## 🎯 Purpose

This repository serves as a **shared workspace** for both **Mistral Vibe Code** and **Claude Code** to collaborate on:
- **Skills** - Portable, reusable agent capabilities
- **Prompts** - Reusable prompt templates and patterns
- **Documentation** - Reference material and verified claims
- **Notebooks** - Informal, exploratory work and session logs

---

## 📖 Getting Started

### For Both Agents

1. **Read the shared instructions:**
   - [AGENTS.md](AGENTS.md) - Core compatibility layer (read by both agents)
   - [CLAUDE.md](CLAUDE.md) - Pointer to AGENTS.md for Claude Code

2. **Understand the layout:**
   ```
   skills-and-prompts-notebook/
   ├── AGENTS.md                    # Shared instructions (READ FIRST)
   ├── CLAUDE.md                    # Claude pointer to AGENTS.md
   ├── NOTICE.md                    # Licensing information
   │
   ├── .vibe/                       # Mistral Vibe Code configuration
   │   ├── skills/                 # Live Vibe skills for this project
   │   │   ├── cross-agent-compat/ # Cross-agent compatibility helper
   │   │   ├── code-review/        # Code review assistant
   │   │   ├── security-audit/     # Security audit skill
   │   │   └── vibe-internals/    # Vibe internals reference
   │   ├── agents/                 # Vibe agent configurations
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
   │   ├── shared/                 # Cross-agent documentation
   │   │   ├── README.md
   │   │   └── [future files]
   │   ├── vibe/                   # Vibe-specific documentation
   │   │   ├── README.md
   │   │   └── internals.md        # Vibe internals deep dive
   │   └── claude/                 # Claude-specific documentation
   │       └── README.md
   │
   ├── skills/                      # Portable skill LIBRARY
   │   ├── ask-questions-if-underspecified/
   │   ├── challenge-my-thinking/
   │   ├── code-review/            # Code review (library version)
   │   ├── cross-agent-compat/      # Cross-agent compatibility
   │   ├── import-memory/          # Anthropic example (Apache-2.0)
   │   ├── prompt-committee/
   │   ├── prompt-pipeline/
   │   ├── security-audit/         # Security audit (library version)
   │   ├── skill-creator/          # Anthropic example (Apache-2.0)
   │   ├── skill-extractor/
   │   ├── task-chunkdown/
   │   └── README.md               # Skill library index
   │
   ├── prompts/                     # Reusable prompts
   │   └── README.md
   │
   └── notebooks/                   # Working documents & scratch space
       └── README.md
   ```

---

## 🔧 Setup

### For Mistral Vibe Code

1. **Link or copy the Vibe configuration:**
   ```bash
   # Option A: Symlink .vibe directory
   ln -s $(pwd)/.vibe ~/.vibe
   
   # Option B: Copy config files
   cp -r .vibe ~/.vibe
   ```

2. **Enable skills in your config:**
   ```toml
   # ~/.vibe/config.toml
   [skills]
   skill_paths = [
     "/path/to/skills-and-prompts-notebook/.vibe/skills",
     "/path/to/skills-and-prompts-notebook/skills"
   ]
   enabled_skills = ["cross-agent-compat", "code-review", "security-audit"]
   ```

3. **Start Vibe:**
   ```bash
   cd skills-and-prompts-notebook
   vibe
   ```

### For Claude Code

1. **Link or copy the Claude configuration:**
   ```bash
   # Option A: Symlink .claude directory
   ln -s $(pwd)/.claude ~/.claude
   
   # Option B: Copy config files
   cp -r .claude ~/.claude
   ```

2. **Install recommended marketplace skills:**
   ```bash
   claude plugin marketplace add anthropics/skills
   claude plugin marketplace add trailofbits/skills
   claude plugin marketplace add trailofbits/skills-curated
   ```

3. **Start Claude:**
   ```bash
   cd skills-and-prompts-notebook
   claude
   ```

---

## 📁 Key Directories Explained

### `.vibe/` - Mistral Vibe Configuration

Contains live configuration for Vibe when working in this repository:

- **`skills/`**: Vibe skills that are active in this project
- **`agents/`**: Agent configurations (TOML format)
- **`prompts/`**: Custom system prompts
- **`config.toml`**: Vibe configuration file

**Important:** Skills in `.vibe/skills/` are **live** and auto-discovered by Vibe. Skills in `skills/` are a **library** and must be copied to `.vibe/skills/` to use.

### `.claude/` - Claude Code Configuration

Contains configuration for Claude when working in this repository:

- **`commands/`**: Custom command documentation
- **`skills/`**: Claude skills (future - for MCP or custom skills)

### `skills/` - Portable Skill Library

This is a **library** of portable `SKILL.md` files. They are **NOT** auto-discovered by either agent from this location.

To use a skill from this library:

**For Vibe:**
```bash
# Copy to Vibe's discovery path
cp -r skills/code-review .vibe/skills/

# Or symlink
ln -s $(pwd)/skills/code-review .vibe/skills/code-review
```

**For Claude:**
```bash
# Copy to Claude's discovery path
cp -r skills/code-review .claude/skills/
```

### `docs/` - Documentation

- **`shared/`**: Cross-agent documentation (works for both)
- **`vibe/`**: Vibe-specific documentation
- **`claude/`**: Claude-specific documentation

### `prompts/` - Reusable Prompts

Contains reusable prompt templates that can be used across sessions.

### `notebooks/` - Working Documents

Informal, exploratory notes, scratch work, and session logs. Content here is **allowed to be wrong or unfinished** - move to `docs/` once verified.

---

## 🎯 Core Skills

### Cross-Agent Compatibility
- **Vibe:** `.vibe/skills/cross-agent-compat/SKILL.md`
- **Claude:** `.claude/commands/cross-agent.md`
- **Purpose:** Tool translation, pattern guidance, dual-agent workflows

### Code Review
- **Vibe:** `.vibe/skills/code-review/SKILL.md`
- **Claude:** `.claude/commands/code-review.md`
- **Library:** `skills/code-review/SKILL.md`
- **Purpose:** Comprehensive code review with subagent parallelization

### Security Audit
- **Vibe:** `.vibe/skills/security-audit/SKILL.md`
- **Claude:** `.claude/commands/security-audit.md`
- **Library:** `skills/security-audit/SKILL.md`
- **Purpose:** Security scanning for vulnerabilities, secrets, and misconfigurations

### Vibe Internals
- **Vibe:** `.vibe/skills/vibe-internals/SKILL.md`
- **Purpose:** Complete reference to Mistral Vibe Code internals

---

## 📋 Skill Library Index

See [skills/README.md](skills/README.md) for the complete index of portable skills, including:

| Skill | Source | License | Notes |
|-------|--------|---------|-------|
| `ask-questions-if-underspecified` | original | none | Clarify ambiguous requests |
| `challenge-my-thinking` | original | none | Socratic stress-test |
| `code-review` | original | MIT | Code review assistant |
| `cross-agent-compat` | original | MIT | Cross-agent compatibility |
| `import-memory` | Anthropic | Apache-2.0 | Memory import (example) |
| `prompt-committee` | original | none | Multi-model review |
| `prompt-pipeline` | original | none | 5-phase prompt workflow |
| `security-audit` | original | MIT | Security audit |
| `skill-creator` | Anthropic | Apache-2.0 | Skill creation helper |
| `skill-extractor` | original | none | Extract skills from sessions |
| `task-chunkdown` | original | none | Break tasks into steps |

---

## 🔗 Important References

### Cross-Tool Compatibility

- [AGENTS.md](AGENTS.md) - **Start here** - Shared instructions for both agents
- [docs/cross-tool-notes.md](docs/cross-tool-notes.md) - Tool name translation and key differences
- [CLAUDE.md](CLAUDE.md) - Claude-specific pointer to AGENTS.md

### Verified References

- [cl-repo](https://github.com/berzerk0/cl-repo) - **Verified** Vibe internals reference (source-cited, not docs-derived)
- [vibe-container](https://github.com/berzerk0/vibe-container) - Sandboxed Vibe devcontainer

### Official Documentation

- [Mistral Vibe Docs](https://docs.mistral.ai/vibe/)
- [Claude Code Docs](https://docs.claude.com/en/docs)

---

## 🛡️ Security Guidelines

When working with this repository:

1. **Use containers** for security audits (see [vibe-container](https://github.com/berzerk0/vibe-container))
2. **Never run with `bypassPermissions` on host** - use containers for isolation
3. **Don't commit secrets** - use `.gitignore` for sensitive files
4. **Review findings manually** - automated scans can have false positives/negatives
5. **Test fixes thoroughly** before applying to production

---

## 📝 Contributing

### Adding a New Skill

1. **Create the skill:**
   ```bash
   mkdir -p skills/my-new-skill
   touch skills/my-new-skill/SKILL.md
   ```

2. **Add frontmatter:**
   ```yaml
   ---
   name: my-new-skill
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
   ```

3. **Add to skill library index:**
   - Update [skills/README.md](skills/README.md) with source and license

4. **Create Vibe version (optional):**
   ```bash
   cp -r skills/my-new-skill .vibe/skills/
   ```

5. **Create Claude version (optional):**
   ```bash
   # Create command documentation
   touch .claude/commands/my-new-skill.md
   ```

6. **Test in both agents:**
   ```bash
   # Vibe
   vibe -p "test my-new-skill" --max-turns 1
   
   # Claude
   claude "test my-new-skill"
   ```

### Adding Documentation

- **Cross-agent docs:** Add to `docs/shared/`
- **Vibe-specific docs:** Add to `docs/vibe/`
- **Claude-specific docs:** Add to `docs/claude/`

---

## 🎓 Best Practices

### 1. Tool Name Verification

**Always verify tool names** - unrecognized tools are **silently ignored** in Vibe:

| Claude | Vibe | Notes |
|--------|------|-------|
| `Read` | `read_file` | ✅ |
| `Write` | `write_file` | ✅ |
| `Edit` | `edit` | ⚠️ NOT `search_replace` |
| `Grep` | `grep` | ✅ |
| `Bash` | `bash` | ✅ |
| `Task` | `task` | ✅ |

### 2. Cross-Agent Compatibility

- Use **common denominator tools** when possible
- Document **tool requirements** explicitly
- Test in **both agents** before committing
- Keep **skill bodies concise** (invocation cost is per-session)

### 3. Skill Organization

- **Small, focused skills** > monolithic skills
- **Single-purpose prompts** > multi-purpose prompts
- **Easy to test, easy to maintain**

### 4. Documentation

- **Self-documenting** - explain assumptions and requirements
- **Reference external sources** where applicable
- **Keep docs updated** with code changes

---

## 📊 Performance Tips

### Token Optimization

- **Vibe:** Progressive skill loading (cheap until invoked)
- **Claude:** MCP server overhead, marketplace skill costs
- **Both:** Use common tools, narrow scope, cache results

### Common Patterns

```bash
# Find relevant files first
find . -name '*.py' -not -path './venv/*' > /tmp/files.txt

# Process in batches
Task: "Analyze all files in /tmp/files.txt for security issues"

# Use grep for filtering
grep -r "pattern" --include="*.py" | head -100
```

---

## 🏁 Quick Start Commands

| Task | Vibe | Claude |
|------|------|--------|
| Start session | `vibe` | `claude` |
| List skills | `vibe -p "list skills"` | `claude "list skills"` |
| Code review | `/code-review` | `/code-review` |
| Security audit | `/security-audit` | `/security-audit` |
| Cross-agent help | `/cross-agent-compat` | `/cross-agent-info` |

---

## 📄 License

This repository contains a mix of:
- **Original content** - All rights reserved unless otherwise stated
- **Third-party content** - Licensed under their respective licenses (see [NOTICE.md](NOTICE.md))

---

*Maintained jointly by Mistral Vibe Code and Claude Code*
*Last updated: 2026-08-23*
