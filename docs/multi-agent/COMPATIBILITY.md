# Multi-Agent Compatibility Guide

**Last Updated:** August 21, 2026  
**Repository:** [berzerk0/crispy-couscous](https://github.com/berzerk0/crispy-couscous)  
**Purpose:** Tool-specific behaviors for Claude Code, Pi Agent, and Mistral Vibe Code, including built-in primitives, skill formats, subagents, and instruction files.

---

## 📌 Overview

This document details how **Claude Code**, **Pi Agent**, and **Mistral Vibe Code** implement the cross-tool standards (Agent Skills, AGENTS.md, MCP) and their **unique behaviors**. Use this to ensure **portability** when developing skills or subagents for this repo.

---

## 🛠️ Built-in Primitives

### Claude Code (Anthropic)
**Official Docs:** [code.claude.com/docs](https://code.claude.com/docs) | [GitHub](https://github.com/anthropics/claude-code)

| **Tool** | **Purpose** | **Official Source** |
|---------|-------------|---------------------|
| `Agent` | Spawn subagents for parallel/delegated tasks | [Tools Reference](https://code.claude.com/docs/en/tools-reference) |
| `Artifact` | Publish HTML/Markdown as shareable pages on claude.ai | [Tools Reference](https://code.claude.com/docs/en/tools-reference) |
| `AskUserQuestion` | Ask multiple-choice questions to gather requirements/clarifications | [Tools Reference](https://code.claude.com/docs/en/tools-reference) |
| `Bash` | Execute shell commands | [Tools Reference](https://code.claude.com/docs/en/tools-reference) |
| `Read` | Read file contents | [Tools Reference](https://code.claude.com/docs/en/tools-reference) |
| `Grep` | Search file contents for regex patterns (ripgrep-backed) | [Tools Reference](https://code.claude.com/docs/en/tools-reference) |
| `Glob` | Find files by name patterns | [Tools Reference](https://code.claude.com/docs/en/tools-reference) |
| `ListDirectory` / `LS` | List files/directories | [Tools Reference](https://code.claude.com/docs/en/tools-reference) |
| `Write` | Create/overwrite files | [Tools Reference](https://code.claude.com/docs/en/tools-reference) |
| `Edit` | Modify existing files | [Tools Reference](https://code.claude.com/docs/en/tools-reference) |

#### Bash Timeouts
- **Default**: `BASH_DEFAULT_TIMEOUT_MS` = **120,000ms (2 minutes)**
- **Hard Ceiling**: `BASH_MAX_TIMEOUT_MS` = **600,000ms (10 minutes)**
- **Configurable**: Set in `~/.claude/settings.json` under `env`.

*Source: [Env Vars Docs](https://code.claude.com/docs/en/env-vars), [Issue #25881](https://github.com/anthropics/claude-code/issues/25881)*

---

### Pi Agent (earendil-works/pi)
**Official Docs:** [pi.dev/docs](https://pi.dev/docs) | [GitHub](https://github.com/earendil-works/pi)

| **Tool** | **Purpose** | **Official Source** |
|---------|-------------|---------------------|
| `read` | Read file contents (truncates to 2,000 lines by default) | [Pi Skills Docs](https://pi.dev/docs/latest/skills) |
| `bash` | Execute shell commands | [Pi Skills Docs](https://pi.dev/docs/latest/skills) |
| `edit` | Patch files | [Pi Skills Docs](https://pi.dev/docs/latest/skills) |
| `write` | Create/overwrite files | [Pi Skills Docs](https://pi.dev/docs/latest/skills) |
| `grep` | Search files for regex patterns | [Pi Skills Docs](https://pi.dev/docs/latest/skills) |
| `find` | Find files/directories | [Pi Skills Docs](https://pi.dev/docs/latest/skills) |
| `ls` | List directory contents | [Pi Skills Docs](https://pi.dev/docs/latest/skills) |

#### Version
- **v0.80.6** (Published ~August 19–20, 2026)

*Source: [GitHub Release v0.80.6](https://github.com/earendil-works/pi/releases/tag/v0.80.6)*

---

### Mistral Vibe Code (mistralai/mistral-vibe)
**Official Docs:** [docs.mistral.ai](https://docs.mistral.ai) | [GitHub](https://github.com/mistralai/mistral-vibe) | [PyPI](https://pypi.org/project/mistral-vibe/)

| **Tool** | **Purpose** | **Official Source** |
|---------|-------------|---------------------|
| `read` | Read file contents | [GitHub README](https://github.com/mistralai/mistral-vibe) |
| `write_file` | Create/overwrite files | [GitHub README](https://github.com/mistralai/mistral-vibe) |
| `edit` | Modify existing files | [GitHub README](https://github.com/mistralai/mistral-vibe) |
| `shell` / `!` | Execute shell commands (e.g., `!ls`) | [GitHub README](https://github.com/mistralai/mistral-vibe) |
| `grep` | Search files for regex patterns (ripgrep support) | [GitHub README](https://github.com/mistralai/mistral-vibe) |
| `todo` | Manage task list | [GitHub README](https://github.com/mistralai/mistral-vibe) |
| `ask_user_question` | Ask interactive questions to gather user input | [GitHub README](https://github.com/mistralai/mistral-vibe) |
| `task` | Delegate tasks to subagents | [GitHub README](https://github.com/mistralai/mistral-vibe) |

#### Version
- **v2.24.2** (Released **August 20, 2026**)

*Source: [PyPI](https://pypi.org/project/mistral-vibe/), [GitHub](https://github.com/mistralai/mistral-vibe)*

---

## 📚 Skill Formats

### Claude Code
| **Aspect** | **Behavior** | **Official Source** |
|-----------|--------------|---------------------|
| **Standard** | Agent Skills + **proprietary Anthropic extensions** | [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) |
| **Discovery Paths** | `.claude/skills/` (project), `~/.claude/skills/` (user) | [Skills Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) |
| **Frontmatter** | Standard + proprietary fields (e.g., `allowed-tools`) | [Skills Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) |
| **Hot-Loading** | Skills/subagents **hot-loaded** by CLI upon detection | [Claude Code Docs](https://code.claude.com/docs/en/sub-agents) |

---

### Pi Agent
| **Aspect** | **Behavior** | **Official Source** |
|-----------|--------------|---------------------|
| **Standard** | Agent Skills (`SKILL.md` + frontmatter) | [Pi Skills Docs](https://pi.dev/docs/latest/skills) |
| **Discovery Paths** | `.pi/skills/` (cwd and ancestors), `~/.pi/agent/skills/` | [Pi Skills Docs](https://pi.dev/docs/latest/skills) |
| **Override** | Project-scope skills **override** user-global skills | [Pi Skills Docs](https://pi.dev/docs/latest/skills) |
| **Validation** | Warns about violations but remains **lenient** | [Pi Skills Docs](https://pi.dev/docs/latest/skills) |

---

### Mistral Vibe Code
| **Aspect** | **Behavior** | **Official Source** |
|-----------|--------------|---------------------|
| **Standard** | Agent Skills specification | [Mistral Docs](https://docs.mistral.ai/vibe/code/cli/skills) |
| **Discovery Paths** | `.vibe/skills/` (project), `~/.vibe/skills/` (user) | [Mistral Docs](https://docs.mistral.ai/vibe/code/cli/skills) |
| **Frontmatter** | `name`, `description`, `license`, `compatibility`, `user-invocable`, `allowed-tools` | [Mistral Docs](https://docs.mistral.ai/vibe/code/cli/skills) |
| **`allowed-tools`** | Acts as a **restriction array** (e.g., `- read_file`, `- grep`) | [Mistral Docs](https://docs.mistral.ai/vibe/code/cli/skills) |

---

## 🎭 Subagents

### Claude Code
| **Aspect** | **Behavior** | **Official Source** |
|-----------|--------------|---------------------|
| **Native Support** | ✅ Built-in | [Subagents Docs](https://code.claude.com/docs/en/sub-agents) |
| **Config Format** | Markdown + YAML frontmatter | [Claude Code Docs](https://code.claude.com/docs/en/sub-agents) |
| **Config Paths** | `.claude/agents/` (project), `~/.claude/agents/` (user) | [Subagents Docs](https://code.claude.com/docs/en/sub-agents) |
| **Delegation** | `Agent` tool | [Tools Reference](https://code.claude.com/docs/en/tools-reference) |
| **Isolation** | Separate context windows | [Claude Code Docs](https://code.claude.com/docs/en/sub-agents) |
| **Nesting** | Supported up to **depth 5** | [Claude Code Docs](https://code.claude.com/docs/en/sub-agents) |

---

### Pi Agent
| **Aspect** | **Behavior** | **Official Source** |
|-----------|--------------|---------------------|
| **Native Support** | ❌ **Not built into core** | [Pi README](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md) |
| **Implementation** | Via **extensions** (e.g., `examples/extensions/subagent.ts`) | [Pi README](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md) |
| **API** | `harness-v2` lanes API for parallel sessions | [Pi README](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md) |
| **Isolation** | Separate context windows (via extensions) | [Pi README](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md) |

---

### Mistral Vibe Code
| **Aspect** | **Behavior** | **Official Source** |
|-----------|--------------|---------------------|
| **Native Support** | ✅ Built-in | [Mistral Docs](https://docs.mistral.ai/vibe/code/cli/skills) |
| **Config Format** | `.toml` files | [GitHub README](https://github.com/mistralai/mistral-vibe) |
| **Config Paths** | `.vibe/agents/` (project), `~/.vibe/agents/` (user) | [Mistral Docs](https://docs.mistral.ai/vibe/code/cli/skills) |
| **Schema** | `agent_type`, `display_name`, `description`, `safety`, `enabled_tools`, `disabled_tools`, `system_prompt_id` | [Mistral Docs](https://docs.mistral.ai/vibe/code/cli/skills) |
| **Delegation** | `task` tool | [GitHub README](https://github.com/mistralai/mistral-vibe) |
| **Isolation** | Separate context windows | [Mistral Docs](https://docs.mistral.ai/vibe/code/cli/skills) |
| **Built-in Subagents** | `explore` (read-only for codebase exploration) | [GitHub README](https://github.com/mistralai/mistral-vibe) |

> **💡 This Repo:** See [`../../.vibe/agents/timestamp.toml`](../../.vibe/agents/timestamp.toml) for examples.

---

## 📄 AGENTS.md Support

| **Tool** | **Native Support** | **Paths** | **Fallback** | **Official Source** |
|---------|-------------------|----------|--------------|---------------------|
| **Claude Code** | ❌ No | `CLAUDE.md`, `.claude/rules/` | `@AGENTS.md` import in `CLAUDE.md` | [AGENTS.md](https://agents.md/) |
| **Pi Agent** | ✅ Yes | `~/.pi/agent/`, cwd, ancestors | N/A | [Pi Skills Docs](https://pi.dev/docs/latest/skills) |
| **Vibe Code** | ✅ Yes | `~/.vibe/AGENTS.md`, `.vibe/AGENTS.md` | N/A | [Mistral Docs](https://docs.mistral.ai/vibe/code/cli/skills) |

---

## 🏆 Permissions & Profiles

### Mistral Vibe Code
| **Profile** | **Behavior** | **Official Source** |
|------------|--------------|---------------------|
| `default` | Standard agent with full tool access | [GitHub README](https://github.com/mistralai/mistral-vibe) |
| `plan` | **Read-only** auto-approval mode | [GitHub README](https://github.com/mistralai/mistral-vibe) |
| `accept-edits` | Auto-approves edits | [GitHub README](https://github.com/mistralai/mistral-vibe) |
| `auto-approve` | Auto-approves all actions | [GitHub README](https://github.com/mistralai/mistral-vibe) |

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
| Glob/Find | ✅ `Glob` | ✅ `find` | ❌ |
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
| **Discovery Paths** | `.claude/skills/`, `~/.claude/skills/` | `.pi/skills/`, `~/.pi/agent/skills/` | `.vibe/skills/`, `~/.vibe/skills/` |
| **Frontmatter** | Standard + Proprietary | Standard | Standard + `allowed-tools` |
| **Override** | Project > User | Project > User | Project > User |

### Subagents
| **Feature** | **Claude Code** | **Pi Agent** | **Vibe Code** |
|------------|----------------|--------------|---------------|
| **Native Support** | ✅ | ❌ | ✅ |
| **Config Format** | Markdown + YAML | Extensions (`.ts`) | `.toml` |
| **Config Paths** | `.claude/agents/`, `~/.claude/agents/` | N/A | `.vibe/agents/`, `~/.vibe/agents/` |
| **Delegation** | `Agent` | N/A (via extensions) | `task` |

---

## 📚 Official Sources Summary

| **Tool** | **Documentation** | **GitHub** | **PyPI** |
|---------|-------------------|------------|---------|
| **Claude Code** | [code.claude.com/docs](https://code.claude.com/docs) | [anthropics/claude-code](https://github.com/anthropics/claude-code) | ❌ |
| **Pi Agent** | [pi.dev/docs](https://pi.dev/docs) | [earendil-works/pi](https://github.com/earendil-works/pi) | ❌ |
| **Vibe Code** | [docs.mistral.ai](https://docs.mistral.ai) | [mistralai/mistral-vibe](https://github.com/mistralai/mistral-vibe) | [mistral-vibe](https://pypi.org/project/mistral-vibe/) |

---

## 🏗️ This Repository’s Implementation

### Skills
This repo implements **cross-agent skills** in [`../../skills/`](../../skills/):
- [`timestamp/SKILL.md`](../../skills/timestamp/SKILL.md): UTC timestamp generation (compatible with Claude, Pi, Vibe).

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
This repo includes **Vibe Code subagent configurations** in [`../../.vibe/agents/`](../../.vibe/agents/):
- [`timestamp.toml`](../../.vibe/agents/timestamp.toml): Timestamp generation subagent.

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
| 2026-08-21 | Initial documentation | Vibe Code |
