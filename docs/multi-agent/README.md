# Multi-Agent Standards Documentation

**Purpose:** Central hub for cross-platform agent compatibility, standards, and maintenance guidelines for [berzerk0/crispy-couscous](https://github.com/berzerk0/crispy-couscous).

---

## 📚 Documentation Overview

This directory contains **validated, source-backed** documentation for developing **portable skills and subagents** across **Claude Code**, **Pi Agent**, and **Mistral Vibe Code**. Each file focuses on a specific aspect of multi-agent compatibility:

| **File** | **Purpose** | **Audience** |
|----------|-------------|--------------|
| **[STANDARDS.md](./STANDARDS.md)** | Cross-tool standards: Agent Skills, AGENTS.md, MCP | Developers, maintainers |
| **[COMPATIBILITY.md](./COMPATIBILITY.md)** | Tool-specific behaviors: built-ins, skills, subagents, AGENTS.md support | Developers, testers |
| **[GAPS.md](./GAPS.md)** | Officially undocumented gaps in standards/tool implementations | Contributors, maintainers |
| **[MAINTENANCE.md](./MAINTENANCE.md)** | How to keep the docs up-to-date with official sources | Maintainers |

---

## 🎯 Quick Start

### For Skill Authors
1. **Read [STANDARDS.md](./STANDARDS.md)** to understand the **Agent Skills** and **AGENTS.md** specifications.
2. **Check [COMPATIBILITY.md](./COMPATIBILITY.md)** for **tool-specific behaviors** (e.g., skill paths, subagent configs).
3. **Follow the examples** in this repo:
   - Skills: [`../../skills/timestamp/SKILL.md`](../../skills/timestamp/SKILL.md)
   - Subagents: [`../../.vibe/agents/timestamp.toml`](../../.vibe/agents/timestamp.toml)

### For Maintainers
1. **Monitor official sources** (see [MAINTENANCE.md](./MAINTENANCE.md)).
2. **Validate claims** against primary documentation quarterly.
3. **Update docs** when discrepancies are found.

---

## 🔗 Cross-Tool Standards at a Glance

| **Standard** | **Purpose** | **Official Source** | **Adoption** |
|-------------|-------------|---------------------|--------------|
| **Agent Skills** | Portable skill format (`SKILL.md` + frontmatter) | [agentskills.io](https://agentskills.io/specification) | 27+ agents |
| **AGENTS.md** | "README for agents" (project instructions) | [agents.md](https://agents.md/) | 60,000+ repos |
| **MCP** | Model Context Protocol (JSON-RPC 2.0 for tools/resources) | [modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2026-07-28) | 500M+ SDK downloads |

---

## 🛠️ Tool-Specific Behaviors

| **Tool** | **Skills Path** | **Subagents Path** | **AGENTS.md Support** | **Built-in Tools** |
|---------|----------------|--------------------|-----------------------|-------------------|
| **Claude Code** | `.claude/skills/`, `~/.claude/skills/` | `.claude/agents/`, `~/.claude/agents/` | ❌ (Uses `CLAUDE.md`) | `Agent`, `Artifact`, `AskUserQuestion`, `Bash`, `Read`, `Grep`, `Glob`, `LS`, `Write`, `Edit` |
| **Pi Agent** | `.pi/skills/`, `~/.pi/agent/skills/` | Extensions (e.g., `subagent.ts`) | ✅ | `read`, `bash`, `edit`, `write`, `grep`, `find`, `ls` |
| **Vibe Code** | `.vibe/skills/`, `~/.vibe/skills/` | `.vibe/agents/`, `~/.vibe/agents/` | ✅ | `read`, `write_file`, `edit`, `shell`/`!`, `grep`, `todo`, `ask_user_question`, `task` |

---

## ⚠️ Known Gaps

The following are **not documented in official sources** (see [GAPS.md](./GAPS.md)):
- **JSON schemas** for built-in tool inputs/outputs.
- **Vibe Code’s `SKILL.md` `allowed-tools` syntax**.
- **MCP scaling limits** (no hard caps for tools/servers).
- **Claude Code tool hook output limits** (>50K tokens).

---

## 📅 Maintenance

To keep these docs **accurate and up-to-date**:
1. **Monitor official sources** (see [MAINTENANCE.md](./MAINTENANCE.md)).
2. **Validate claims quarterly** against primary documentation.
3. **Update after major releases** (e.g., Pi v0.81.0, Vibe v2.25.0).

> **💡 Tip:** A **CI check** can automate validation (see [MAINTENANCE.md](./MAINTENANCE.md) for details).

---

## 🏗️ This Repository’s Implementation

This repo demonstrates **cross-agent compatibility** with:

### Skills
- **Location:** [`../../skills/`](../../skills/)
- **Format:** Agent Skills standard (`SKILL.md` + frontmatter).
- **Compatibility:** Designed for **Claude Code**, **Pi Agent**, and **Vibe Code**.
- **Examples:**
  - [`timestamp/SKILL.md`](../../skills/timestamp/SKILL.md): UTC timestamp generation.

### Subagents (Vibe Code)
- **Location:** [`../../.vibe/agents/`](../../.vibe/agents/)
- **Format:** `.toml` files (Vibe Code specific).
- **Examples:**
  - [`timestamp.toml`](../../.vibe/agents/timestamp.toml): Timestamp subagent.

---

## 🤝 Contributing

1. **Report issues**: Open a GitHub issue for discrepancies or outdated claims.
2. **Submit updates**: PRs are welcome! Include **official source links** for new claims.
3. **Test changes**: Ensure compatibility across all three agents.

---

## 📄 License

This documentation is provided under the [MIT License](https://opensource.org/licenses/MIT).
