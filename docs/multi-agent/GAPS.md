# Undocumented Gaps in Multi-Agent Standards

**Last Updated:** August 21, 2026  
**Repository:** [berzerk0/crispy-couscous](https://github.com/berzerk0/crispy-couscous)  
**Purpose:** Track officially undocumented aspects of Claude Code, Pi Agent, and Mistral Vibe Code that impact portability and interoperability.

---

## 📌 Overview

While the **Agent Skills**, **AGENTS.md**, and **MCP** specifications are well-documented, the **tool-specific implementations** of these standards (and their built-in primitives) have **gaps in official documentation**. This document lists these gaps to guide future contributions and avoid assumptions.

> **⚠️ Impact:** These gaps can lead to **non-portable skills**, **unexpected behavior**, or **integration issues** across agents. Contributions to this repo should **test across all three agents** where possible.

---

## 🔍 Officially Undocumented Gaps

### 1. Exact JSON Schemas for Built-in Primitives

| **Gap** | **Affected Tools** | **Details** | **Workaround** |
|---------|--------------------|-------------|---------------|
| No official JSON schemas for tool inputs/outputs | Claude Code, Pi Agent, Vibe Code | The **input/output schemas** (parameters, types, required fields) for built-in tools (e.g., `Bash`, `Read`, `Edit`) are **not documented** in any official spec or tool docs. | Refer to [Claude Code System Prompts](https://github.com/Piebald-AI/claude-code-system-prompts) for **tool descriptions** (unofficial but comprehensive). For Pi/Vibe, inspect the [source code](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/tools) or [README examples](https://github.com/mistralai/mistral-vibe). |

#### Example: Missing Schema for `Bash` Tool
- **Claude Code**: No schema for `timeout` parameter or exit code handling.
- **Pi Agent**: No schema for `bash` tool parameters (e.g., `command`, `timeout`).
- **Vibe Code**: No schema for `shell` tool (invoked as `!`).

---

### 2. Vibe Code’s `SKILL.md` Argument-Passing Syntax

| **Gap** | **Affected Tools** | **Details** | **Workaround** |
|---------|--------------------|-------------|---------------|
| `allowed-tools` field syntax and behavior | Mistral Vibe Code | The `allowed-tools` frontmatter field (e.g., `- read_file`, `- grep`) is **undocumented**. It is unclear: <ul><li>Whether the syntax is YAML array or space-separated.</li><li>How tools are restricted (deny-list vs. allow-list).</li><li>Whether wildcards or glob patterns are supported.</li></ul> | See [Mistral Docs Examples](https://docs.mistral.ai/vibe/code/cli/skills) and existing skills in the wild (e.g., [vibe-skills](https://github.com/search?q=vibe+skills)). Test empirically. |

#### Example: `allowed-tools` in `SKILL.md`
```yaml
---
name: example
allowed-tools:
  - read_file
  - grep
---
```
- **Is this correct?** Unclear from official docs.
- **Does it block or allow these tools?** Unclear.

---

### 3. MCP Scaling Limits

| **Gap** | **Affected Tools** | **Details** | **Workaround** |
|---------|--------------------|-------------|---------------|
| No hard numeric caps for MCP servers/tools | All (MCP clients/servers) | The [MCP Specification](https://modelcontextprotocol.io/specification/2026-07-28) **intentionally omits** hard limits for: <ul><li>Maximum number of tools per server.</li><li>Maximum number of concurrent MCP servers.</li><li>Context window scaling for MCP resources.</li><li>Rate limits for MCP requests.</li></ul> | <ul><li>Monitor [MCP Spec Updates](https://modelcontextprotocol.io/specification/2026-07-28).</li><li>Test empirically with your MCP server/client.</li><li>Assume **no limits** and design for scalability.</li></ul> |

#### Example: MCP Server Limits
- **Question**: Can an MCP server expose 1,000 tools?
- **Answer**: **Yes**, but no official limit is documented. Test with your client (Claude Code, Vibe, etc.).

---

### 4. Claude Code Tool Hook Output Limits

| **Gap** | **Affected Tools** | **Details** | **Workaround** |
|---------|--------------------|-------------|---------------|
| 50K token threshold behavior | Claude Code | While the **50,000-token backup trigger** is documented (see [Hooks Guide](https://claudefa.st/blog/tools/hooks/hooks-guide)), the **exact behavior** of tool hook outputs >50K tokens is unclear: <ul><li>Are they **truncated** or **diverted to disk**?</li><li>Are they **compressed** or **split**?</li><li>Is the **50K limit per-tool or per-hook**?</li></ul> | <ul><li>Test with large tool outputs (e.g., `Bash` commands generating >50K tokens).</li><li>Monitor [Claude Code Costs Docs](https://code.claude.com/docs/en/costs) for updates.</li></ul> |

---

### 5. Pi Agent Skill Name vs. Directory Name

| **Gap** | **Affected Tools** | **Details** | **Workaround** |
|---------|--------------------|-------------|---------------|
| Skill name vs. directory name rules | Pi Agent | The [Agent Skills standard](https://agentskills.io/specification) requires that the **skill name matches the parent directory**. However, **Pi deliberately allows mismatches** for shared skill directories. It is unclear: <ul><li>How Pi resolves **name collisions** (same name from different locations).</li><li>Whether this behavior is **stable** or may change in future versions.</li></ul> | <ul><li>See [Pi Skills Docs](https://pi.dev/docs/latest/skills): "Pi allows skill names to differ from their parent directory even though the standard disallows it."</li><li>Avoid relying on this behavior for **portability** (Claude Code enforces the standard).</li></ul> |

---

### 6. Subagent Permission Inheritance

| **Gap** | **Affected Tools** | **Details** | **Workaround** |
|---------|--------------------|-------------|---------------|
| Permission inheritance for subagents | Claude Code, Mistral Vibe Code | Unclear how subagents inherit **permissions** (e.g., file access, tool restrictions) from the parent agent: <ul><li>Do subagents **inherit** the parent’s permissions?</li><li>Can subagents **override** permissions?</li><li>Are there **default restrictions** (e.g., read-only)?</li></ul> | <ul><li>For **Claude Code**: See [Subagents Docs](https://hidekazu-konishi.com/entry/claude_code_features_settings_reference_2026.html): "The recommended pattern is to restrict subagents to read-only tool sets."</li><li>For **Vibe Code**: See [Mistral Docs](https://docs.mistral.ai/mistral-vibe/agents-skills): "By default, the built-in subagents do not write files."</li><li>Test empirically with your use case.</li></ul> |

---

## 📊 Gap Severity Assessment

| **Gap** | **Severity** | **Impact** | **Mitigation** |
|---------|--------------|------------|---------------|
| JSON Schemas for Primitives | **High** | Breaks portability; tools may behave differently across agents. | Use unofficial docs (e.g., system prompts) and test. |
| Vibe `SKILL.md` Syntax | **Medium** | May cause skill loading failures in Vibe Code. | Follow examples from Mistral docs. |
| MCP Scaling Limits | **Low** | No immediate impact; design for scalability. | Assume no limits; test with your setup. |
| Hook Output Limits | **Low** | Affects only edge cases (very large outputs). | Test with large outputs. |
| Skill Name vs. Directory | **Low** | Affects only Pi Agent; not portable to Claude Code. | Avoid relying on this behavior. |
| Subagent Permissions | **Medium** | May cause unexpected permission errors. | Restrict subagents to read-only by default. |

---

## 🛠️ Workarounds and Best Practices

### For Skill Authors
1. **Test Across All Agents**: Always test skills in **Claude Code**, **Pi Agent**, and **Vibe Code** to catch undocumented behaviors.
2. **Use Minimal Frontmatter**: Stick to **required fields** (`name`, `description`) and avoid agent-specific fields (e.g., `allowed-tools` in Vibe).
3. **Document Assumptions**: If your skill relies on undocumented behavior (e.g., `allowed-tools`), document it in the skill’s `README.md`.
4. **Avoid Large Outputs**: For tools that may generate >50K tokens, **stream or chunk** the output to avoid hitting limits.

### For Subagent Authors
1. **Restrict Permissions**: Default to **read-only** tool sets for subagents (Claude Code/Vibe recommendation).
2. **Explicit Model Selection**: Set `active_model` explicitly in subagent configs to avoid cost surprises (e.g., inheriting Opus).
3. **Test Isolation**: Verify that subagents **do not share context** with the parent agent.

### For MCP Developers
1. **Assume No Limits**: Design MCP servers to handle **unbounded** tools/resources.
2. **Test with Multiple Clients**: Verify your server works with **Claude Code**, **Vibe Code**, and other MCP clients.
3. **Monitor Spec Updates**: Watch for [MCP Spec Changes](https://modelcontextprotocol.io/specification/2026-07-28).

---

## 📚 Related Resources

### Unofficial Documentation
- [Claude Code System Prompts](https://github.com/Piebald-AI/claude-code-system-prompts) (Tool descriptions)
- [Vibe Code DeepWiki](https://deepwiki.com/mistralai/mistral-vibe/) (Implementation details)
- [Pi Agent DeepWiki](https://deepwiki.com/agentic-dev-io/pi-agent/) (Tool internals)

### Community Discussions
- [Claude Code GitHub Issues](https://github.com/anthropics/claude-code/issues) (Search for `BASH_DEFAULT_TIMEOUT_MS`, `allowed-tools`)
- [MCP GitHub Discussions](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions) (Scaling, limits)

---

## 📝 Changelog

| **Date** | **Change** | **Author** |
|----------|------------|------------|
| 2026-08-21 | Initial documentation | Vibe Code |
