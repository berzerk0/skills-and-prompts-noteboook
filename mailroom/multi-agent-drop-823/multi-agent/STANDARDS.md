# Multi-Agent Standards Reference

**Last Updated:** August 21, 2026  
**Repository:** [berzerk0/crispy-couscous](https://github.com/berzerk0/crispy-couscous)  
**Purpose:** Canonical reference for cross-platform agent compatibility standards: Agent Skills, AGENTS.md, and Model Context Protocol (MCP).

---

## 📋 Overview

This document consolidates the **official standards** adopted by Claude Code, Pi Agent, and Mistral Vibe Code. These standards enable **portable skills**, **consistent instruction files**, and **interoperable tool integrations** across multiple agent frameworks.

---

## 🔗 Agent Skills Specification

**Standard:** [agentskills.io/specification](https://agentskills.io/specification) | [GitHub](https://github.com/agentskills/agentskills)

### Core Concepts
| **Aspect** | **Specification** | **Official Source** |
|-----------|------------------|---------------------|
| **Definition** | A skill is a directory containing a `SKILL.md` file with YAML frontmatter + Markdown instructions. | [Agent Skills Spec](https://agentskills.io/specification) |
| **Structure** | Required: `SKILL.md`; Optional: `scripts/`, `references/`, `assets/` | [Agent Skills Spec](https://agentskills.io/specification) |
| **Frontmatter** | Required: `name`, `description`; Optional: `license`, `compatibility`, `user-invocable`, `allowed-tools` | [Agent Skills Spec](https://agentskills.io/specification), [SKILL.md Format Reference](https://www.agensi.io/learn/agent-skills-open-standard) |

### Progressive Disclosure
- **Startup**: Only `name` + `description` load (~30-50 tokens/skill).
- **Activation**: Full `SKILL.md` body loads when the skill is triggered.
- **Referenced Files**: Loaded only when explicitly requested.

*Source: [Agent Skills Spec](https://agentskills.io/specification), [Agentman Guide](https://agentman.ai/blog/build-your-first-agent-skill-skillmd-anatomy)*

### Best Practices
- Keep `SKILL.md` body **under 5,000 tokens**.
- Keep skill directories **under 500 lines**.
- Split long instructions into `references/` or `scripts/`.

*Source: [Agent Skills Spec](https://agentskills.io/specification), [Firecrawl Blog](https://www.firecrawl.dev/blog/agent-skills)*

### Adoption
- **27+ agents** support the standard: Claude Code, Cursor, Codex CLI, Pi, Vibe, etc.
- **Portable**: Write once, run on any compliant agent.

*Source: [agentskills.io](https://agentskills.io), [mdskills.ai](https://www.mdskills.ai/specs/skill-md)*

---

## 📄 AGENTS.md Specification

**Standard:** [agents.md](https://agents.md/) | [GitHub](https://github.com/agentsmd/agents.md)

### Core Concepts
| **Aspect** | **Specification** | **Official Source** |
|-----------|------------------|---------------------|
| **Purpose** | "README for agents"—predictable location for project-specific instructions. | [AGENTS.md Site](https://agents.md/) |
| **Format** | Standard Markdown; **no required fields or rigid schema**. | [AGENTS.md Spec](https://deepwiki.com/agentsmd/agents.md/7-agents.md-specification) |
| **Content** | Build commands, test instructions, conventions, guardrails, boundaries. | [AGENTS.md DeepWiki](https://deepwiki.com/agentsmd/agents.md/7-agents.md-specification) |
| **Nested Files** | Subdirectory `AGENTS.md` overrides parent rules for that subtree. | [AGENTS.md DeepWiki](https://deepwiki.com/openai/agents.md/5-agents.md-format-documentation) |

### Design Principles
- **Explicitly advises against** enforcing deterministic tooling/formatting constraints.
- **No validation**: Agents parse natural language instructions intelligently.
- **Complements README.md**: Focuses on **operational context** (e.g., how to run tests), not human onboarding.

*Source: [AGENTS.md Spec](https://agents.md/), [ASDLC Guide](https://asdlc.io/practices/agents-md-spec/), [MorphLLM Guide](https://www.morphllm.com/agents-md-guide)*

### Adoption
- Used by **60,000+ open-source projects**.
- Stewarded by the **Agentic AI Foundation** under the Linux Foundation.

*Source: [AGENTS.md Site](https://agents.md/)*

---

## 🔌 Model Context Protocol (MCP) Specification

**Standard:** [modelcontextprotocol.io/specification/2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28) | [GitHub](https://github.com/modelcontextprotocol/modelcontextprotocol)

### Core Concepts
| **Aspect** | **Specification** | **Official Source** |
|-----------|------------------|---------------------|
| **Purpose** | Standardizes integration between LLMs and external data/tools. | [MCP Spec](https://modelcontextprotocol.io/specification/2026-07-28) |
| **Protocol** | **JSON-RPC 2.0** for all messages (requests, responses, notifications). | [MCP Spec](https://modelcontextprotocol.io/specification/2026-07-28), [MCP Blog](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/) |
| **Capabilities** | **Prompts**, **Resources**, **Tools** exposed via MCP servers. | [MCP Spec](https://modelcontextprotocol.io/specification/2026-07-28) |
| **Transports** | **stdio** (local), **Streamable HTTP** (remote). | [MCP Cheat Sheet](https://www.webfuse.com/mcp-cheat-sheet) |

### Design Principles
- **No hard numeric caps**: Intentionally omits limits for tool counts, server limits, or context scaling.
- **Stateless architecture**: Supports load balancing and horizontal scaling.
- **Extensible**: Capabilities like **Tasks** and **MCP Apps** ship on their own timeline.

*Source: [MCP Spec](https://modelcontextprotocol.io/specification/2026-07-28), [Latenode Blog](https://latenode.com/blog/model-context-protocol-json-rpc)*

### Ecosystem
- **500M+ SDK downloads/month** (TypeScript + Python).
- **Adopted by Fortune 500 companies** (~28% within 18 months of availability).

*Source: [MCP Blog](https://blog.modelcontextprotocol.io/posts/2026-07-28/)*

---

## 📚 Official Sources

| **Standard** | **Primary Documentation** | **GitHub** | **Additional Resources** |
|-------------|---------------------------|------------|-------------------------|
| **Agent Skills** | [agentskills.io/specification](https://agentskills.io/specification) | [agentskills/agentskills](https://github.com/agentskills/agentskills) | [mdskills.ai](https://www.mdskills.ai/specs/skill-md) |
| **AGENTS.md** | [agents.md](https://agents.md/) | [agentsmd/agents.md](https://github.com/agentsmd/agents.md) | [ASDLC Guide](https://asdlc.io/practices/agents-md-spec/) |
| **MCP** | [modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2026-07-28) | [modelcontextprotocol/spec](https://github.com/modelcontextprotocol/modelcontextprotocol) | [MCP Blog](https://blog.modelcontextprotocol.io/) |

---

## 🏗️ This Repository’s Usage

This repo uses these standards to enable **cross-agent compatibility**:
- **Skills**: See [`../../skills/`](../../skills/) for examples following the Agent Skills spec.
- **AGENTS.md**: Not yet implemented (Claude Code uses `CLAUDE.md`; Pi/Vibe support `AGENTS.md` natively).
- **MCP**: Not yet implemented (future consideration for external tool integrations).

---

## 📝 Changelog

| **Date** | **Change** | **Author** |
|----------|------------|------------|
| 2026-08-21 | Initial documentation | Vibe Code |
