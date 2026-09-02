# ADR-001: Canonical Skill Format

**Status:** PROPOSED  
**Date:** 2026-08-23  
**Author:** Vibe Code  
**Supersedes:** None

---

## Context

We need a **single source of truth** for skill definitions that works across Claude Code, Pi Agent, and Mistral Vibe Code. Previously, we used custom YAML files (`agents/<name>.yaml`) as the canonical source, with generation scripts creating framework-specific configs.

**Problem:** This approach has several issues:
1. The custom YAML format is **not part of any official standard**
2. It **reinvents** the Agent Skills spec frontmatter
3. Other tools cannot read our skill definitions
4. It adds unnecessary complexity

## Decision

**Use `SKILL.md` as the canonical skill format**, following the official [Agent Skills specification](https://agentskills.io/specification).

### Implementation

1. **Canonical source:** `skills/<name>/SKILL.md` with standard YAML frontmatter
2. **Custom metadata:** Use the `metadata:` section for internal fields (e.g., `requires_authentication`, `requires_network`)
3. **Agent configs:** Generate framework-specific agent configurations from SKILL.md files
4. **Symlinks:** Use symlinks in `.vibe/skills/`, `.claude/skills/`, `.pi/skills/` to point to canonical `skills/` directory

### Example Canonical SKILL.md

```yaml
---
name: repo-auditor
description: Audit repository structure, skills, and cross-agent compatibility
license: MIT
compatibility: [claude, pi, vibe]
metadata:
  requires_authentication: false
  requires_network: false
---

## Skill Instructions

This skill audits the repository...
```

## Consequences

### Positive
- ✅ **Portable:** Any Agent Skills-compliant tool can read our skills
- ✅ **Standard-compliant:** Follows official specification
- ✅ **Simpler:** No custom YAML format to maintain
- ✅ **Interoperable:** Other repositories can use our skills directly

### Negative
- ⚠️ **Agent configs still framework-specific:** We still need separate `.toml`/`.md` files for each agent framework
- ⚠️ **Generation scripts still needed:** For creating agent configs from SKILL.md

## Alternatives Considered

1. **Keep custom YAML (`agents/<name>.yaml`)**
   - ❌ Not portable
   - ❌ Reinvents the wheel
   - ❌ Other tools can't read it

2. **Use only framework-native formats**
   - ❌ Requires maintaining 3 separate skill definitions
   - ❌ No single source of truth
   - ❌ Changes don't propagate automatically

3. **Use MCP for everything**
   - ❌ MCP is for tools, not skills
   - ❌ Not all agents support MCP equally
   - ❌ Overkill for skill definitions

## Related

- [Agent Skills Specification](https://agentskills.io/specification)
- [ADR-002: Drop skill_type Classification](ADR-002-drop-skill-type.md)
- [docs/multi-agent/STANDARDS.md](../multi-agent/STANDARDS.md)

---

*Last updated: 2026-08-23*
