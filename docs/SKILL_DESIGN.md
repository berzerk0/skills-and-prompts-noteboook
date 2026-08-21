# Skill Design Guidelines

This document outlines **how to design skills** for this multi-agent repository.

---

## Core Principles

### 1. Script-First Architecture

**All skills must have a CLI-executable core.**

```
Skill Request → Agent Wrapper → bash → Python Script → Result
```

This ensures:
- Single source of truth (the script)
- Cross-tool compatibility (via universal `bash` primitive)
- Testability outside agent contexts
- No MCP overhead for simple operations

### 2. Tool-Agnostic Instructions

**Never reference specific tool names** in SKILL.md files or agent instructions.

| ❌ Bad | ✅ Good |
|-------|---------|
| "Use `Read` to open the file" | "Read the file contents" |
| "Call `Grep` with pattern" | "Search for the pattern in files" |
| "Use `Edit` to modify" | "Modify the file to..." |

**Why**: Tool names differ across agents (see table in `cross-agent-primitives.md`).

### 3. Portable Frontmatter Only

SKILL.md files **MUST** use only the **6 Agent Skills spec fields**:

```yaml
---
name: skill-name          # Required
description: ...          # Required
license: MIT             # Optional
compatibility: [...]     # Optional
metadata: {...}          # Optional
---
```

**Explicitly omit**:
- `allowed-tools` (tool names not portable)
- `user-invocable` (Claude-specific)
- `model` (Claude-specific)
- Any other Claude Code extensions

---

## Skill Types

### Type A: Pure Function Skills

**Characteristics**:
- Stateless computation
- No file I/O
- No external API calls
- Example: `timestamp`

**Implementation**:
```python
# timestamp_skill.py
def get_utc_timestamp() -> str:
    ...
```

**SKILL.md**:
```markdown
---
name: timestamp
description: Get current UTC timestamp...
---
Return the current UTC time in YYYY-MM-DD-HHMM format.
```

### Type B: API Client Skills

**Characteristics**:
- Wraps external API
- May require authentication
- Stateful operations
- Example: `codeberg`

**Implementation**:
```python
# codeberg_connector.py
class CodebergClient:
    async def list_repos(self):
        ...
```

**SKILL.md**:
```markdown
---
name: codeberg
description: Codeberg API operations...
---
Use the codeberg_connector module. Auth via CODEBERG_TOKEN env var.
```

### Type C: File Operation Skills

**Characteristics**:
- Read/write files
- Search/replace content
- File system operations

**Implementation**:
- Use `bash` to invoke scripts
- Scripts use standard Python file I/O
- Never reference agent-specific tool names

**SKILL.md**:
```markdown
---
name: file-helper
description: File manipulation utilities...
---
Use the file_operations.py module via bash commands.
```

---

## Subagent Design

### Vibe Code (TOML)

```toml
# .vibe/agents/timestamp.toml
agent_type = "subagent"
display_name = "timestamp"
description = "Get current UTC timestamp..."

[tools.python]
enabled = true

[tools.bash]
enabled = true
```

**Key differences**:
- Delegation-only (`task use timestamp`)
- TOML format
- `enabled_tools` uses Vibe's tool names (`read_file`, `write_file`, etc.)

### Claude Code (MD+YAML)

```markdown
---
name: timestamp
description: Get current UTC timestamp...
user-invocable: true
model: sonnet
---

# Timestamp Agent

Return UTC time in YYYY-MM-DD-HHMM format.
```

**Key differences**:
- Slash-invocable (`/timestamp`)
- YAML frontmatter
- Can use Claude-specific fields

### Pi Agent (MD+YAML)

Similar to Claude Code but with Pi's tool names and model defaults.

---

## File Naming Conventions

| Component | Path | Format |
|-----------|------|--------|
| Portable Skill | `skills/<name>/SKILL.md` | MD+YAML (6 fields) |
| Vibe Subagent | `.vibe/agents/<name>.toml` | TOML |
| Claude Subagent | `.claude/agents/<name>.md` | MD+YAML |
| Pi Subagent | `.pi/agents/<name>.md` | MD+YAML |
| Implementation | `<name>_skill.py` or `<name>_connector.py` | Python |

---

## Testing Guidelines

### Unit Tests
- Test Python modules directly (no agent required)
- Use `pytest` for implementation logic

### Integration Tests
- Test each agent wrapper in its native environment
- Verify tool name mappings work correctly
- Confirm file paths resolve properly

### Cross-Tool Verification
1. Clone repo in each agent's environment
2. Verify SKILL.md files load without errors
3. Test subagent invocation
4. Confirm shared modules are accessible

---

## Future: Generation Scripts

**Planned** (not yet implemented):

```
agents/
├── timestamp.yaml          # Canonical source
└── codeberg.yaml

meta/
├── generate_claude.py     # YAML → .claude/agents/*.md
├── generate_pi.py         # YAML → .pi/agents/*.md
└── generate_vibe.py       # YAML → .vibe/agents/*.toml
```

This will:
- Eliminate manual duplication
- Ensure consistency across formats
- Allow single-source updates
- Support validation of canonical schemas

---

## References

- [Cross-Agent Primitive Standardization](cross-agent-primitives.md)
- [Agent Manifest](AGENTS.md)
- [Agent Skills Specification](https://github.com/Agentic-AI/agent-skills)
