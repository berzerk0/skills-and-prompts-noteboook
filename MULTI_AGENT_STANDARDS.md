# Multi-Agent Standards Reference

**Last Updated:** August 21, 2026  
**Repository:** [berzerk0/crispy-couscous](https://github.com/berzerk0/crispy-couscous)  
**Purpose:** Canonical reference for cross-platform agent compatibility, built-in primitives, skill formats, subagents, and instruction files across Claude Code, Pi Agent, and Mistral Vibe Code.

---

## 📋 Overview

This document validates and consolidates the **official standards and tool-specific behaviors** for three major coding agents:
- **Claude Code** (Anthropic)
- **Pi Agent** (earendil-works/pi)
- **Mistral Vibe Code** (mistralai/mistral-vibe)

Each section includes **verified claims** with **direct links to official sources** for traceability. This repo (`crispy-couscous`) uses these standards to enable **portable skills** (see [`skills/`](./skills/)) and **subagent configurations** (see [`.vibe/agents/`](./.vibe/agents/)).

---

## 🔗 Cross-Tool Standards

### Agent Skills Specification
**Standard:** [agentskills.io/specification](https://agentskills.io/specification) | [GitHub](https://github.com/agentskills/agentskills)

| **Claim** | **Status** | **Official Source** |
|----------|------------|---------------------|
| A skill is a directory containing a `SKILL.md` file with YAML frontmatter + Markdown instructions | ✅ Verified | [Agent Skills Spec](https://agentskills.io/specification) |
| Frontmatter fields: `name`, `description` (required); `license`, `compatibility`, `user-invocable`, `allowed-tools` (optional) | ✅ Verified | [Agent Skills Spec](https://agentskills.io/specification), [SKILL.md Format Reference](https://www.agensi.io/learn/agent-skills-open-standard) |
| Progressive disclosure: Only `name` + `description` load at startup (~30-50 tokens/skill); full `SKILL.md` loads on activation | ✅ Verified | [Agent Skills Spec](https://agentskills.io/specification), [Agentman Guide](https://agentman.ai/blog/build-your-first-agent-skill-skillmd-anatomy) |
| Recommended: Keep `SKILL.md` body under **5,000 tokens** and skill directories under **500 lines** | ✅ Verified | [Agent Skills Spec](https://agentskills.io/specification), [Firecrawl Blog](https://www.firecrawl.dev/blog/agent-skills) |
| Adopted by **27+ agents** (Claude Code, Cursor, Codex CLI, Pi, Vibe, etc.) | ✅ Verified | [agentskills.io](https://agentskills.io), [mdskills.ai](https://www.mdskills.ai/specs/skill-md) |

> **💡 This Repo:** The [`skills/`](./skills/) directory follows this standard. Each skill (e.g., [`codeberg/SKILL.md`](./skills/codeberg/SKILL.md), [`timestamp/SKILL.md`](./skills/timestamp/SKILL.md)) includes `compatibility: [claude, pi, vibe]` to indicate cross-agent support.

---

### AGENTS.md Specification
**Standard:** [agents.md](https://agents.md/) | [GitHub](https://github.com/agentsmd/agents.md)

| **Claim** | **Status** | **Official Source** |
|----------|------------|---------------------|
| AGENTS.md is a **"README for agents"**—a predictable location for project-specific instructions | ✅ Verified | [AGENTS.md Site](https://agents.md/), [Spec DeepWiki](https://deepwiki.com/agentsmd/agents.md/7-agents.md-specification) |
| **No required fields or rigid schema**—standard Markdown parsed by agents | ✅ Verified | [AGENTS.md Spec](https://deepwiki.com/agentsmd/agents.md/7-agents.md-specification), [MorphLLM Guide](https://www.morphllm.com/agents-md-guide) |
| **Explicitly advises against** enforcing deterministic tooling/formatting constraints | ✅ Verified | [AGENTS.md Spec](https://agents.md/), [ASDLC Guide](https://asdlc.io/practices/agents-md-spec/) |
| Used by **60,000+ open-source projects** | ✅ Verified | [AGENTS.md Site](https://agents.md/) |
| Nested files: Subdirectory `AGENTS.md` overrides parent rules for that subtree | ✅ Verified | [AGENTS.md DeepWiki](https://deepwiki.com/openai/agents.md/5-agents.md-format-documentation) |

> **⚠️ Tool-Specific Behavior:**
> - **Claude Code:** Does **not** natively read `AGENTS.md`; uses `CLAUDE.md` and `.claude/rules/` instead. Workaround: `@AGENTS.md` import in `CLAUDE.md`.
>   *Source: [MorphLLM Guide](https://www.morphllm.com/agents-md-guide)*
> - **Pi Agent:** Natively reads `AGENTS.md` from `~/.pi/agent/`, parent directories, and cwd.
>   *Source: [Pi Skills Docs](https://pi.dev/docs/latest/skills)*
> - **Vibe Code:** Natively reads `AGENTS.md` at user (`~/.vibe/AGENTS.md`) and project levels (`.vibe/AGENTS.md`).
>   *Source: [Mistral Docs](https://docs.mistral.ai/mistral-vibe/agents-skills)*

---

### Model Context Protocol (MCP) Specification
**Standard:** [modelcontextprotocol.io/specification/2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28) | [GitHub](https://github.com/modelcontextprotocol/modelcontextprotocol)

| **Claim** | **Status** | **Official Source** |
|----------|------------|---------------------|
| MCP uses **JSON-RPC 2.0** for all messages (requests, responses, notifications) | ✅ Verified | [MCP Spec](https://modelcontextprotocol.io/specification/2026-07-28), [MCP Blog](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/) |
| Standardizes **Prompts, Resources, and Tools** for LLM-to-external-system integration | ✅ Verified | [MCP Spec](https://modelcontextprotocol.io/specification/2026-07-28) |
| **No hard numeric caps** for tool counts, server limits, or context scaling | ✅ Verified | [MCP Spec](https://modelcontextprotocol.io/specification/2026-07-28), [Latenode Blog](https://latenode.com/blog/model-context-protocol-json-rpc) |
| Supports **stdio** (local) and **Streamable HTTP** (remote) transports | ✅ Verified | [MCP Cheat Sheet](https://www.webfuse.com/mcp-cheat-sheet) |

---

## 🛠️ Tool-Specific Standards

### Claude Code (Anthropic)
**Official Docs:** [code.claude.com/docs](https://code.claude.com/docs) | [platform.claude.com/docs](https://platform.claude.com/docs) | [GitHub](https://github.com/anthropics/claude-code)

#### Built-in Primitives
| **Tool** | **Purpose** | **Official Source** |
|---------|-------------|---------------------|
| `Agent` | Spawn subagents for parallel/delegated tasks | [Tools Reference](https://code.claude.com/docs/en/tools-reference), [System Prompts](https://github.com/Piebald-AI/claude-code-system-prompts) |
| `Artifact` | Publish HTML/Markdown as shareable pages on claude.ai | [Tools Reference](https://code.claude.com/docs/en/tools-reference), [Support Article](https://support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them) |
| `AskUserQuestion` | Ask multiple-choice questions to gather requirements/clarifications | [Tools Reference](https://code.claude.com/docs/en/tools-reference), [Agent SDK Guide](https://ai-workshop.dometrain.com/docs/getting-work-done/planning/ask-user-question) |
| `Bash` | Execute shell commands; default timeout **2 minutes**, max **10 minutes** | [Tools Reference](https://code.claude.com/docs/en/tools-reference), [Env Vars Docs](https://code.claude.com/docs/en/env-vars) |
| `Read` | Read file contents | [Tools Reference](https://code.claude.com/docs/en/tools-reference) |
| `Grep` | Search file contents for regex patterns (ripgrep-backed) | [Tools Reference](https://code.claude.com/docs/en/tools-reference) |
| `Glob` | Find files by name patterns | [Tools Reference](https://code.claude.com/docs/en/tools-reference) |
| `ListDirectory` | List files/directories (also referenced as `LS`) | [Tools Reference](https://code.claude.com/docs/en/tools-reference), [Gist](https://gist.github.com/wong2/e0f34aac66caf890a332f7b6f9e2ba8f) |
| `Write` | Create/overwrite files | [Tools Reference](https://code.claude.com/docs/en/tools-reference) |
| `Edit` | Modify existing files | [Tools Reference](https://code.claude.com/docs/en/tools-reference) |

#### Skill Format
| **Claim** | **Status** | **Official Source** |
|----------|------------|---------------------|
| Follows **Agent Skills standard** with **proprietary Anthropic extensions** | ✅ Verified | [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) |
| Skills discovered in `.claude/skills/` (project) and `~/.claude/skills/` (user) | ✅ Verified | [Skills Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), [Reference](https://hidekazu-konishi.com/entry/claude_code_features_settings_reference_2026.html) |
| Subagents defined as Markdown + YAML frontmatter in `.claude/agents/` and `~/.claude/agents/` | ✅ Verified | [Subagents Docs](https://hidekazu-konishi.com/entry/claude_code_features_settings_reference_2026.html), [Totalum Blog](https://www.totalum.app/blog/claude-code-subagents-totalum) |
| Subagents **hot-loaded** by CLI upon detection | ✅ Verified | [Totalum Blog](https://www.totalum.app/blog/claude-code-subagents-totalum) |

#### AGENTS.md Support
| **Claim** | **Status** | **Official Source** |
|----------|------------|---------------------|
| **Does not natively read `AGENTS.md`** | ✅ Verified | [MorphLLM Guide](https://www.morphllm.com/agents-md-guide) |
| Exclusively reads `CLAUDE.md` and `.claude/rules/` | ✅ Verified | [Claude Code Docs](https://code.claude.com/docs), [MorphLLM Guide](https://www.morphllm.com/agents-md-guide) |

#### Limits
| **Claim** | **Status** | **Official Source** |
|----------|------------|---------------------|
| Bash default timeout: **`BASH_DEFAULT_TIMEOUT_MS` = 120,000ms (2 minutes)** | ✅ Verified | [Env Vars Docs](https://code.claude.com/docs/en/env-vars), [Issue #25881](https://github.com/anthropics/claude-code/issues/25881) |
| Bash hard ceiling: **`BASH_MAX_TIMEOUT_MS` = 600,000ms (10 minutes)** | ✅ Verified | [Issue #25881](https://github.com/anthropics/claude-code/issues/25881), [Reddit](https://www.reddit.com/r/ClaudeCode/comments/1o1ywz9) |
| Tool hook outputs > **50,000 tokens** diverted to disk | ✅ Verified | [Hooks Guide](https://claudefa.st/blog/tools/hooks/hooks-guide), [Costs Docs](https://code.claude.com/docs/en/costs) |

---

### Pi Agent (earendil-works/pi)
**Official Docs:** [pi.dev/docs](https://pi.dev/docs) | [GitHub](https://github.com/earendil-works/pi)

#### Version
| **Claim** | **Status** | **Official Source** |
|----------|------------|---------------------|
| **v0.80.6** (Published ~August 19–20, 2026) | ✅ Verified | [GitHub Release v0.80.6](https://github.com/earendil-works/pi/releases/tag/v0.80.6), [Pi News](https://pi.dev/news/releases) |

#### Built-in Primitives
| **Tool** | **Purpose** | **Official Source** |
|---------|-------------|---------------------|
| `read` | Read file contents (truncates to 2,000 lines by default) | [Pi Tool System](https://pt-act-pi-mono.mintlify.app/concepts/tools), [Usage Guide](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/usage.md) |
| `bash` | Execute shell commands | [Pi Tool System](https://pt-act-pi-mono.mintlify.app/concepts/tools) |
| `edit` | Patch files | [Pi Tool System](https://pt-act-pi-mono.mintlify.app/concepts/tools) |
| `write` | Create/overwrite files | [Pi Tool System](https://pt-act-pi-mono.mintlify.app/concepts/tools) |
| `grep` | Search files for regex patterns | [Pi Tool System](https://pt-act-pi-mono.mintlify.app/concepts/tools) |
| `find` | Find files/directories | [Pi Tool System](https://pt-act-pi-mono.mintlify.app/concepts/tools) |
| `ls` | List directory contents | [Pi Tool System](https://pt-act-pi-mono.mintlify.app/concepts/tools) |

#### Skill Format
| **Claim** | **Status** | **Official Source** |
|----------|------------|---------------------|
| Follows **Agent Skills standard** (`SKILL.md` + frontmatter) | ✅ Verified | [Pi Skills Docs](https://pi.dev/docs/latest/skills) |
| Skills discovered in **`.agents/skills/`** (cwd and ancestors) and **`~/.pi/agent/skills/`** | ✅ Verified | [Pi Skills Docs](https://pi.dev/docs/latest/skills), [Pi Mono Docs](https://hochej.github.io/pi-mono/coding-agent/skills/) |
| Project-scope skills **override** user-global skills | ✅ Verified | [Pi Skills Docs](https://pi.dev/docs/latest/skills) |

#### Subagents
| **Claim** | **Status** | **Official Source** |
|----------|------------|---------------------|
| **Not built natively** into TUI/CLI core loop | ✅ Verified | [Pi README](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md) |
| Supported via **extensions** (e.g., `examples/extensions/subagent.ts`) using `harness-v2` lanes API | ✅ Verified | [Pi README](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md) |

#### AGENTS.md Support
| **Claim** | **Status** | **Official Source** |
|----------|------------|---------------------|
| Natively reads `AGENTS.md` and `CLAUDE.md` from global (`~/.pi/agent/`) and project directories | ✅ Verified | [Pi Skills Docs](https://pi.dev/docs/latest/skills), [MorphLLM Guide](https://www.morphllm.com/agents-md-guide) |

---

### Mistral Vibe Code (mistralai/mistral-vibe)
**Official Docs:** [docs.mistral.ai](https://docs.mistral.ai) | [GitHub](https://github.com/mistralai/mistral-vibe) | [PyPI](https://pypi.org/project/mistral-vibe/)

#### Version
| **Claim** | **Status** | **Official Source** |
|----------|------------|---------------------|
| **v2.24.2** (Released **August 20, 2026**) | ✅ Verified | [PyPI](https://pypi.org/project/mistral-vibe/), [GitHub](https://github.com/mistralai/mistral-vibe) |

#### Built-in Primitives
| **Tool** | **Purpose** | **Official Source** |
|---------|-------------|---------------------|
| `read` | Read file contents | [GitHub README](https://github.com/mistralai/mistral-vibe) |
| `write_file` | Create/overwrite files | [GitHub README](https://github.com/mistralai/mistral-vibe) |
| `edit` | Modify existing files | [GitHub README](https://github.com/mistralai/mistral-vibe) |
| `shell` / `!` | Execute shell commands (e.g., `!ls`) | [GitHub README](https://github.com/mistralai/mistral-vibe) |
| `grep` | Search files for regex patterns (ripgrep support) | [GitHub README](https://github.com/mistralai/mistral-vibe) |
| `todo` | Manage task list | [GitHub README](https://github.com/mistralai/mistral-vibe) |
| `ask_user_question` | Ask interactive questions to gather user input | [GitHub README](https://github.com/mistralai/mistral-vibe), [PyPI](https://pypi.org/project/mistral-vibe/) |
| `task` | Delegate tasks to subagents | [GitHub README](https://github.com/mistralai/mistral-vibe) |

#### Skill Format
| **Claim** | **Status** | **Official Source** |
|----------|------------|---------------------|
| Follows **Agent Skills specification** | ✅ Verified | [Mistral Docs](https://docs.mistral.ai/vibe/code/cli/skills) |
| Skills discovered in `.vibe/skills/` (project) and `~/.vibe/skills/` (user) | ✅ Verified | [Mistral Docs](https://docs.mistral.ai/vibe/code/cli/skills) |
| Frontmatter fields: `name`, `description`, `license`, `compatibility`, `user-invocable`, `allowed-tools` | ✅ Verified | [Mistral Docs](https://docs.mistral.ai/vibe/code/cli/skills) |
| `allowed-tools` acts as a **restriction array** (e.g., `- read_file`, `- grep`) | ✅ Verified | [Mistral Docs](https://docs.mistral.ai/vibe/code/cli/skills) |

#### Subagents
| **Claim** | **Status** | **Official Source** |
|----------|------------|---------------------|
| Configured as `.toml` files in `.vibe/agents/` (project) or `~/.vibe/agents/` (user) | ✅ Verified | [Mistral Docs](https://docs.mistral.ai/mistral-vibe/agents-skills), [GitHub](https://github.com/mistralai/mistral-vibe) |
| Schema fields: `agent_type`, `display_name`, `description`, `safety`, `enabled_tools`, `disabled_tools`, `system_prompt_id` | ✅ Verified | [Mistral Docs](https://docs.mistral.ai/mistral-vibe/agents-skills) |
| `agent_type = "subagent"` required for delegation-only agents | ✅ Verified | [GitHub README](https://github.com/mistralai/mistral-vibe) |
| Delegated via the `task` tool | ✅ Verified | [GitHub README](https://github.com/mistralai/mistral-vibe) |

> **💡 This Repo:** See [`.vibe/agents/codeberg.toml`](./.vibe/agents/codeberg.toml) and [`.vibe/agents/timestamp.toml`](./.vibe/agents/timestamp.toml) for examples of subagent configurations.

#### AGENTS.md Support
| **Claim** | **Status** | **Official Source** |
|----------|------------|---------------------|
| Natively reads `AGENTS.md` at user (`~/.vibe/AGENTS.md`) and project levels | ✅ Verified | [Mistral Docs](https://docs.mistral.ai/mistral-vibe/agents-skills), [DeepWiki](https://deepwiki.com/mistralai/mistral-vibe/3.8-skills-and-agent-profiles) |

#### Permissions
| **Claim** | **Status** | **Official Source** |
|----------|------------|---------------------|
| Built-in agent profiles: `default`, `plan` (read-only auto-approval), `accept-edits`, `auto-approve` | ✅ Verified | [GitHub README](https://github.com/mistralai/mistral-vibe), [Mistral Docs](https://docs.mistral.ai/mistral-vibe/agents-skills) |

---

## 📊 Comparison Tables

### Built-in Tools
| **Tool** | **Claude Code** | **Pi Agent** | **Vibe Code** |
|---------|----------------|--------------|---------------|
| Read | ✅ `Read` | ✅ `read` | ✅ `read` |
| Write | ✅ `Write` | ✅ `write` | ✅ `write_file` |
| Edit | ✅ `Edit` | ✅ `edit` | ✅ `edit` |
| Bash/Shell | ✅ `Bash` | ✅ `bash` | ✅ `shell` / `!` |
| Grep | ✅ `Grep` | ✅ `grep` | ✅ `grep` |
| Glob/Find | ✅ `Glob` | ✅ `find` | ❌ (uses `grep` + `read`) |
| List Directory | ✅ `ListDirectory`/`LS` | ✅ `ls` | ❌ |
| User Questions | ✅ `AskUserQuestion` | ❌ | ✅ `ask_user_question` |
| Subagent Delegation | ✅ `Agent` | ❌ (extensions only) | ✅ `task` |
| Artifacts | ✅ `Artifact` | ❌ | ❌ |
| Todo | ❌ | ❌ | ✅ `todo` |

### Skill Formats
| **Feature** | **Claude Code** | **Pi Agent** | **Vibe Code** |
|------------|----------------|--------------|---------------|
| **Standard** | Agent Skills + Proprietary | Agent Skills | Agent Skills |
| **File** | `SKILL.md` | `SKILL.md` | `SKILL.md` |
| **Discovery Paths** | `.claude/skills/`, `~/.claude/skills/` | `.agents/skills/`, `~/.pi/agent/skills/` | `.vibe/skills/`, `~/.vibe/skills/` |
| **Frontmatter Fields** | Standard + Proprietary | Standard | Standard + `allowed-tools` |
| **Override Behavior** | Project > User | Project > User | Project > User |

### AGENTS.md Support
| **Feature** | **Claude Code** | **Pi Agent** | **Vibe Code** |
|------------|----------------|--------------|---------------|
| **Native Support** | ❌ (Uses `CLAUDE.md`) | ✅ | ✅ |
| **Fallback** | `@AGENTS.md` import in `CLAUDE.md` | N/A | N/A |
| **Paths** | `.claude/rules/`, `CLAUDE.md` | `~/.pi/agent/`, cwd, ancestors | `~/.vibe/`, `.vibe/` |

### Subagents
| **Feature** | **Claude Code** | **Pi Agent** | **Vibe Code** |
|------------|----------------|--------------|---------------|
| **Native Support** | ✅ | ❌ | ✅ |
| **Config Format** | Markdown + YAML frontmatter | Extensions (`.ts`) | `.toml` files |
| **Config Paths** | `.claude/agents/`, `~/.claude/agents/` | N/A (extension-based) | `.vibe/agents/`, `~/.vibe/agents/` |
| **Delegation Tool** | `Agent` | N/A (via extensions) | `task` |
| **Isolation** | ✅ Separate context windows | ✅ (via `harness-v2` lanes) | ✅ Separate context windows |

---

## 🔍 Officially Undocumented Gaps

The following are **not covered in official documentation** as of August 21, 2026:

1. **Exact JSON Schemas for Built-in Primitives**
   - No official schemas exist for tool inputs/outputs in any of the three tools.
   - *Workaround:* Refer to [Claude Code System Prompts](https://github.com/Piebald-AI/claude-code-system-prompts) for tool descriptions.

2. **Vibe Code’s `SKILL.md` Argument-Passing Syntax**
   - The `allowed-tools` field syntax (e.g., `- read_file`) is undocumented.
   - *Workaround:* See [Vibe Skills Docs](https://docs.mistral.ai/vibe/code/cli/skills) for examples.

3. **MCP Scaling Limits**
   - The MCP specification **intentionally omits** hard numeric caps for tool counts, server limits, or context scaling.
   - *Workaround:* Monitor [MCP Spec Updates](https://modelcontextprotocol.io/specification/2026-07-28).

---

## 📚 Official Sources Summary

### Cross-Tool Standards
- [Agent Skills Specification](https://agentskills.io/specification)
- [AGENTS.md Specification](https://agents.md/)
- [Model Context Protocol (MCP) Specification](https://modelcontextprotocol.io/specification/2026-07-28)

### Claude Code
- [Claude Code Documentation](https://code.claude.com/docs)
- [Claude Platform Documentation](https://platform.claude.com/docs)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)
- [Claude Code System Prompts](https://github.com/Piebald-AI/claude-code-system-prompts)

### Pi Agent
- [Pi Documentation](https://pi.dev/docs/latest)
- [Pi GitHub](https://github.com/earendil-works/pi)
- [Pi Coding Agent README](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md)

### Mistral Vibe Code
- [Mistral Documentation](https://docs.mistral.ai)
- [Mistral Vibe GitHub](https://github.com/mistralai/mistral-vibe)
- [Mistral Vibe PyPI](https://pypi.org/project/mistral-vibe/)

---

## 🏗️ This Repository’s Implementation

### Skills
This repo implements **cross-agent skills** in [`skills/`](./skills/):
- [`codeberg/SKILL.md`](./skills/codeberg/SKILL.md): Codeberg API operations (compatible with Claude, Pi, Vibe).
- [`timestamp/SKILL.md`](./skills/timestamp/SKILL.md): UTC timestamp generation (compatible with Claude, Pi, Vibe).

Each skill includes:
```yaml
---
name: <skill_name>
description: <trigger description>
license: MIT
compatibility: [claude, pi, vibe]
---
```

### Subagents
This repo includes **Vibe Code subagent configurations** in [`.vibe/agents/`](./.vibe/agents/):
- [`codeberg.toml`](./.vibe/agents/codeberg.toml): Codeberg API operations subagent.
- [`timestamp.toml`](./.vibe/agents/timestamp.toml): Timestamp generation subagent.

Each subagent uses the schema:
```toml
agent_type = "subagent"
display_name = "<name>"
description = "<description>"
active_model = "mistral-small"

[tools.python]
enabled = true
```

---

## 📝 Changelog

| **Date** | **Change** | **Author** |
|----------|------------|------------|
| 2026-08-21 | Initial documentation based on validated research | Vibe Code |

---

## 🤝 Contributing

To add a new skill or subagent:
1. Follow the [Agent Skills Specification](https://agentskills.io/specification).
2. Add the skill to [`skills/<name>/SKILL.md`](./skills/).
3. For Vibe Code, add a subagent config to [`.vibe/agents/<name>.toml`](./.vibe/agents/).
4. Test compatibility across all three agents (Claude, Pi, Vibe).
5. Submit a PR with references to official documentation.

---

## 📄 License

This documentation is provided under the [MIT License](https://opensource.org/licenses/MIT).
