# ADR-002: Drop skill_type Classification

**Status:** PROPOSED  
**Date:** 2026-08-23  
**Author:** Vibe Code  
**Supersedes:** None

---

## Context

We previously used a `skill_type` classification system with three categories:
- **type_a:** Pure function (no external dependencies)
- **type_b:** API client (external service calls)
- **type_c:** File operations (local filesystem access)

This classification was used in `agents/<name>.yaml` files to auto-generate tool assignments for each framework.

**Problem:** As identified by Claude's review:
1. **Lossy proxy:** The categories don't accurately represent actual tool requirements
2. **Not portable:** External tools don't understand our custom classification
3. **Overlapping:** Most skills fall into multiple categories
4. **Duplicates information:** The tool requirements are already in `allowed-tools`

## Decision

**Drop the `skill_type` classification system.**

### Implementation

1. **Remove** `skill_type` field from all YAML files
2. **Replace** with explicit boolean flags in `metadata:` section:
   - `requires_authentication: true/false`
   - `requires_network: true/false`
3. **Derive** tool assignments from `allowed-tools` in SKILL.md frontmatter
4. **Update** generation scripts to use `allowed-tools` directly

### Example Migration

**Before (agents/repo-auditor.yaml):**
```yaml
name: repo-auditor
skill_type: type_c  # File operations
...
```

**After (skills/repo-auditor/SKILL.md):**
```yaml
---
name: repo-auditor
description: Audit repository...
license: MIT
compatibility: [claude, pi, vibe]
allowed-tools:
  - read
  - write
  - edit
  - grep
  - bash
metadata:
  requires_authentication: false
  requires_network: false
---
```

## Consequences

### Positive
- ✅ **Simpler:** One less abstraction layer
- ✅ **More accurate:** Tool assignments based on actual requirements
- ✅ **Portable:** No custom classification to explain to others
- ✅ **Maintainable:** Less code to keep in sync

### Negative
- ⚠️ **Need to update** all existing YAML files
- ⚠️ **Need to update** generation scripts
- ⚠️ **Lose** the classification for reporting (but it was lossy anyway)

## Alternatives Considered

1. **Keep skill_type**
   - ❌ Maintains unnecessary complexity
   - ❌ Not portable
   - ❌ Lossy classification

2. **Use a better classification system**
   - ❌ Still adds abstraction
   - ❌ Still not portable
   - ❌ Still duplicates information in `allowed-tools`

3. **Derive classification from allowed-tools programmatically**
   - ✅ This is the chosen approach
   - ✅ Always accurate
   - ✅ No manual classification needed

## Related

- [ADR-001: Canonical Skill Format](ADR-001-canonical-skill-format.md)
- [Claude's Review](https://github.com/berzerk0/crispy-couscous/pull/9) - Identified the issues with skill_type
- [docs/multi-agent/GAPS.md](../multi-agent/GAPS.md) - Documents framework differences

---

*Last updated: 2026-08-23*
