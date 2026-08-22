# AGENTS.md - crispy-couscous

**This is a multi-agent skill repository.** Agents working here can discover, use, and develop skills for Claude Code, Pi Agent, and Mistral Vibe Code.

---

## Repository Purpose

This repository is a **skill and subagent development workspace** that:

1. **Stores portable skills** in `skills/<name>/SKILL.md` (Agent Skills spec compliant)
2. **Provides per-agent wrappers** in `.claude/agents/`, `.pi/agents/`, `.vibe/agents/`
3. **Hosts shared implementations** in `*.py` modules at the root
4. **Documents cross-agent compatibility** in `docs/`

---

## Quick Start for Agents

### Discover Available Skills

Skills are available in:
- `.claude/skills/` (for Claude Code)
- `.pi/skills/` (for Pi Agent)
- `.vibe/skills/` (for Vibe Code)

Current skills:
- **timestamp**: Get current UTC timestamp in YYYY-MM-DD-HHMM format
- **codeberg**: Codeberg (Gitea) API operations for repository management

### Use a Skill

**Claude Code**: Skills are auto-discovered. Reference them by name or use `/<skill-name>`.
**Pi Agent**: Skills are auto-discovered from `.agents/skills/` and ancestors.
**Vibe Code**: Skills are auto-discovered from `.vibe/skills/`.

Example: "Use the timestamp skill to get the current time."

---

## Adding New Skills

### 1. Create the Implementation

Create a Python module at the repository root:
```python
# new_skill.py
"""Your skill implementation."""

def main_function():
    """Core logic."""
    pass
```

### 2. Create the Portable Skill Definition

Create `skills/<name>/SKILL.md`:
```markdown
---
name: new_skill
description: What this skill does and when to use it.
license: MIT
compatibility: [claude, pi, vibe]
---

## Instructions

Tool-agnostic instructions here. Never reference specific tool names like `Read`, `read_file`, etc.

Use the implementation: `from new_skill import main_function`

## Usage

- When to trigger this skill
- What inputs it expects
- What outputs it produces
```

**Important**: 
- Use only the **6 standard frontmatter fields**: `name`, `description`, `license`, `compatibility`, `metadata`
- Omit `allowed-tools` (tool names are NOT portable)
- Use **tool-agnostic language**: "read the file" not "use `Read`"

### 3. Create Per-Agent Wrappers

#### Vibe Code (TOML)
Create `.vibe/agents/<name>.toml`:
```toml
agent_type = "subagent"
display_name = "new_skill"
description = "What this skill does"
active_model = "mistral-small"

[tools.python]
enabled = true

[tools.bash]
enabled = true
```

#### Claude Code (MD+YAML)
Create `.claude/agents/<name>.md`:
```markdown
---
name: new_skill
description: What this skill does and when to use it.
tools: ["Read", "Write", "Edit", "Bash", "Grep"]
user-invocable: true
model: sonnet
---

# Skill Name Agent

You are a skill assistant. Use the new_skill module.

Implementation: `from new_skill import main_function`
```

#### Pi Agent (MD+YAML)
Create `.pi/agents/<name>.md`:
```markdown
---
name: new_skill
description: What this skill does and when to use it.
tools: ["read", "write", "edit", "bash", "grep"]
model: gpt-4o-mini
---

# Skill Name Agent

You are a skill assistant. Use the new_skill module.

Implementation: `from new_skill import main_function`
```

### 4. Update Documentation

- Add to `docs/AGENTS.md` under the Skills section
- Update compatibility notes if needed

---

## Cross-Agent Development

### Core Principles

1. **Script-First Architecture**: All skills must have a CLI-executable core
   ```
   Skill Request → Agent Wrapper → bash → Python Script → Result
   ```

2. **bash/Bash is the Universal Primitive**: The only tool name consistent across all three agents

3. **Tool-Agnostic Instructions**: Never reference specific tool names in SKILL.md files

### Tool Name Mappings

| Operation | Claude Code | Pi Agent | Vibe Code |
|-----------|--------------|----------|-----------|
| Read file | `Read` | `read` | `read` |
| Write file | `Write` | `write` | `write_file` |
| Edit file | `Edit` | `edit` | `edit` |
| Shell | `Bash` | `bash` | `bash` |
| Search | `Grep` | `grep` | `grep` |

**Use `bash`/`Bash` for all script invocations** to ensure cross-tool compatibility.

---

## Repository Structure

```
.
├── AGENTS.md                    # This file - repository context
├── README.md                    # Human-readable overview
├── skills/                      # Portable SKILL.md files
│   ├── timestamp/SKILL.md
│   └── codeberg/SKILL.md
├── *.py                         # Shared implementations
│   ├── timestamp_skill.py
│   └── codeberg_connector.py
├── .claude/                     # Claude Code configurations
│   ├── agents/                  # Subagents
│   │   ├── timestamp.md
│   │   └── codeberg.md
│   └── skills/                  # → symlink to ../skills/
│       ├── timestamp/          # → ../skills/timestamp
│       └── codeberg/           # → ../skills/codeberg
├── .pi/                         # Pi Agent configurations
│   ├── agents/                  # Subagents
│   │   ├── timestamp.md
│   │   └── codeberg.md
│   └── skills/                  # → symlink to ../skills/
│       ├── timestamp/          # → ../skills/timestamp
│       └── codeberg/           # → ../skills/codeberg
└── .vibe/                       # Vibe Code configurations
    ├── agents/                  # Subagents
    │   ├── timestamp.toml
    │   └── codeberg.toml
    └── skills/                  # → symlink to ../skills/
        ├── timestamp/          # → ../skills/timestamp
        └── codeberg/           # → ../skills/codeberg
```

---

## Skill Development Workflow

1. **Implement**: Write the core logic in a Python module
2. **Document**: Create the portable SKILL.md with tool-agnostic instructions
3. **Wrap**: Create per-agent wrapper configurations
4. **Test**: Verify in each agent's environment
5. **Iterate**: Refine based on usage

---

## References

- [Agent Skills Specification](https://agentskills.io/specification)
- [Cross-Agent Primitive Standardization](docs/cross-agent-primitives.md)
- [Multi-Agent Standards Reference](docs/multi-agent/STANDARDS.md)
- [Compatibility Guide](docs/multi-agent/COMPATIBILITY.md)
- [Skill Design Guidelines](docs/SKILL_DESIGN.md)

---

## Maintenance Notes

- Skills directories use symlinks to avoid duplication
- All skill definitions reference shared Python implementations
- Generation scripts (future): `meta/` directory will contain scripts to auto-generate per-agent wrappers from canonical YAML sources
