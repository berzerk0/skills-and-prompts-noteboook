# Cross-Agent Primitive Standardization — Research Verdict

**Status**: Confirmed via independent verification  
**Date**: 2026-08-21  
**Source**: Gemini 3 deep research + cross-check against official documentation

---

## Executive Verdict

**Hybrid architecture, not pure MCP.**

Do **NOT** build a monolithic MCP server as a universal tool layer. Instead:

1. Write core logic as **plain CLI scripts**
2. Invoke via each agent's native `bash`/`Bash` primitive (the **only** tool name spelled consistently across Claude Code, Pi Agent, and Vibe Code)
3. Generate **per-agent wrapper configs** (`.claude/agents/*.md`, `.pi/agents/*.md`, `.vibe/agents/*.toml`) from a single canonical source

This approach **matches our independent conclusions** before the research — the research corroborates rather than overturns it.

---

## Supporting Evidence

### MCP Tool-Count/Token Limits (Confirmed)

Cursor hard-caps at **~40 active MCP tools** across all servers combined. Exceeding this limit **silently drops tools** rather than erroring.

**Sources:**
- [forum.cursor.com/t/mcp-server-40-tool-limit-in-cursor](https://forum.cursor.com/t/mcp-server-40-tool-limit-in-cursor)
- [truefoundry.com/blog/mcp-servers-in-cursor-setup-configuration-and-security-guide](https://truefoundry.com/blog/mcp-servers-in-cursor-setup-configuration-and-security-guide)
- GitLab MCP server issue citing the same constraint

> **Implication**: MCP's per-session schema-loading overhead costs more than it returns for lightweight utilities. Reserve MCP for capabilities that genuinely need structured params, persistent state, or external API access.

### MCP + Skills Complementarity (Confirmed, with Correction)

MCP provides **execution capability**, while Skills provide the **procedural "when/how" context**. MCP-only setups measurably underperform because agents don't know when to reach for a tool without instructional steering.

**Source:** [aaif.io/blog/closing-the-context-gap-why-mcp-skills-works](https://aaif.io/blog/closing-the-context-gap-why-mcp-skills-works)

> **Correction**: This is **not** an Agentic AI Foundation institutional position. It's a conference talk by **Pedro Rodrigues, AI Tooling Engineer at Supabase**, published via AAIF's blog. The core claim still checks out.

### Tool Name Inconsistency (Confirmed)

| Operation | Claude Code | Pi Agent | Vibe Code |
|-----------|--------------|----------|-----------|
| Read file | `Read` | `read` | `read_file` |
| Search | `Grep` | `grep` | `grep` |
| Find files | `Glob` | `find` | varies |
| Edit | `Edit` | `edit` | `edit` |
| Write | `Write` | `write` | `write_file` |
| Shell | `Bash` | `bash` | `bash` |

> **Conclusion**: `bash`/`Bash` is the **only reliable cross-tool primitive**. All other tool names are agent-specific.

---

## Practical Implications for This Repo

### ✅ DO

1. **Write core logic as CLI scripts** (Python, Bash, etc.)
2. **Invoke via `bash`** primitive in all agent wrappers
3. **Generate per-agent configs** from canonical YAML/TOML source
4. **Use MCP selectively** for:
   - Structured parameter requirements
   - Persistent state needs
   - External API access
5. **Keep lightweight utilities** (timestamp, simple transforms) as direct CLI invocations

### ❌ DON'T

1. **Build monolithic MCP servers** for simple utilities
2. **Assume tool name portability** across agents
3. **Use `allowed-tools` in portable SKILL.md** (tool names differ)
4. **Rely on MCP for lightweight operations** (overhead > benefit)

---

## Corrections from Research

1. **"MCP Tools by f"** — Unverified product name. **Drop this reference.** The pattern (wrapping CLI commands as MCP tools via proxy) is real (e.g., `mcp-command-proxy`), but cite the pattern, not the unverified product.

2. **AAIF attribution** — The "Closing the Context Gap" piece is **Pedro Rodrigues (Supabase)**, not an Agentic AI Foundation institutional position. Cite the practitioner.

3. **Failed abstraction postmortems** — No documented cases found. Treat as "no evidence found," not "proof this never fails."

---

## Architecture Decision

**Core Principle**: *Script-first, wrap-second.*

```
Canonical Logic (Python/CLI)
    ↓
Per-Agent Wrappers
    ├── .claude/agents/*.md  (YAML frontmatter)
    ├── .pi/agents/*.md      (YAML frontmatter)
    └── .vibe/agents/*.toml  (TOML format)
    ↓
Agent Invocation (via native bash/Bash)
```

This ensures:
- Single source of truth for logic
- Native tool compatibility per agent
- No MCP overhead for simple operations
- Clear separation between execution and orchestration
