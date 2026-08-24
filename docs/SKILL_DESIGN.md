# Skill Design Guidelines

---

## :rotating_light: Symlink Safety Invariant

**NEVER write through symlinks in `.claude/skills/`, `.pi/skills/`, or `.vibe/skills/`.**

These directories are **symlink farms** pointing to the canonical `skills/` directory. Writing through a symlink silently overwrites the canonical SKILL.md file. This caused the 2026-08-24 incident where all 14 SKILL.md files were flattened to 13-line stubs.

**Safe pattern for skill development:**
- **READ through symlinks**: Agents discover skills via `.claude/skills/`, `.pi/skills/`, `.vibe/skills/`
- **WRITE only to agent wrapper files**: `.claude/agents/`, `.pi/agents/`, `.vibe/agents/`
- **Canonical source**: `skills/<name>/SKILL.md` - single source of truth
- **Generation scripts**: `meta/generate_*.py` create wrapper files, never modify skills/

The generators enforce this invariant with guardrails that refuse to write through symlinks.



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
├── generate_claude.py     # SKILL.md → .claude/agents/*.md (agent configs)
├── generate_pi.py         # SKILL.md → .pi/agents/*.md (agent configs)
└── generate_vibe.py       # SKILL.md → .vibe/agents/*.toml (agent configs)

**Note:** Skills use SKILL.md directly (portable). Agent configs are framework-specific.
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
