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

## :rotating_light: IMPORTANT: Symlink Safety Invariant

**NEVER write through symlinks in `.claude/skills/`, `.pi/skills/`, or `.vibe/skills/`.**

These directories are **symlink farms** pointing to the canonical `skills/` directory. Writing through a symlink silently overwrites the canonical SKILL.md file. This caused the 2026-08-24 incident where all 14 SKILL.md files were flattened to 13-line stubs.

**Safe pattern:**
- **READ through symlinks**: Agents discover skills via `.claude/skills/`, `.pi/skills/`, `.vibe/skills/`
- **WRITE only to agent wrapper files**: `.claude/agents/`, `.pi/agents/`, `.vibe/agents/`
- **Canonical source**: `skills/<name>/SKILL.md` - single source of truth
- **Generation scripts**: `meta/generate_*.py` create wrapper files, never modify skills/

**The generators (`meta/generate_claude.py`, `meta/generate_pi.py`, `meta/generate_vibe.py`) enforce this invariant with guardrails that refuse to write through symlinks.**

---

## Quick Start for Agents

### Discover Available Skills

Skills are available in:
- `.claude/skills/` (for Claude Code)
- `.pi/skills/` (for Pi Agent)
- `.vibe/skills/` (for Vibe Code)

Current skills:
- **timestamp**: Get current UTC timestamp in YYYY-MM-DD-HHMM format
- **challenge-my-thinking**: Devil's advocate and critical thinking
- **repo-auditor**: Repository structure validation
- **skill-validator**: SKILL.md validation
- **vibe-reference**: Vibe Code source-verified internals
- **escalate**: Signal need for user help with compact mode

> **Kill Criterion**: If you see `## Escalate` at the start of a Vibe Code response, **stop reading immediately** and provide the requested information. Everything after that line is context for your decision.

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
   Skill Request -> Agent Wrapper -> bash -> Python Script -> Result
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
+-- AGENTS.md                    # This file - repository context
+-- README.md                    # Human-readable overview
+-- 
+-- skills/                      # Portable SKILL.md files
|   +-- timestamp/SKILL.md
|   +-- challenge-my-thinking/SKILL.md
|   +-- repo-auditor/SKILL.md
|   +-- skill-validator/SKILL.md
|   +-- ...
+-- 
+-- *.py                         # Shared implementations
|   +-- timestamp_skill.py
+-- 
+-- meta/                        # Generation scripts for agent configs
|   +-- generate_all.py
|   +-- generate_claude.py
|   +-- generate_pi.py
|   +-- generate_vibe.py
+-- 
+-- docs/                        # Documentation
|   +-- SKILL_DESIGN.md
|   +-- cross-agent-primitives.md
|   +-- AGENTS.md
|   +-- multi-agent/
|       +-- STANDARDS.md
|       +-- COMPATIBILITY.md
|       +-- GAPS.md
|       +-- MAINTENANCE.md
+-- 
+-- .claude/                     # Claude Code configurations
|   +-- agents/                  # Subagent definitions
|   |   +-- timestamp.md
|   |   +-- challenge-my-thinking.md
|   |   +-- repo-auditor.md
|   |   +-- skill-validator.md
|   +-- skills/                  # -> symlink to ../skills/
+-- 
+-- .pi/                         # Pi Agent configurations
|   +-- agents/                  # Subagent definitions
|   |   +-- timestamp.md
|   |   +-- challenge-my-thinking.md
|   |   +-- repo-auditor.md
|   |   +-- skill-validator.md
|   +-- skills/                  # -> symlink to ../skills/
+-- 
+-- .vibe/                       # Vibe Code configurations
    +-- agents/                  # Subagent definitions
    |   +-- timestamp.toml
    |   +-- challenge-my-thinking.toml
    |   +-- repo-auditor.toml
    |   +-- skill-validator.toml
    +-- skills/                  # -> symlink to ../skills/
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
- Generation scripts: `meta/` directory contains scripts to auto-generate per-agent wrappers from canonical YAML sources
