# Vibe/Claude Version Reconciliation Brief

**Date:** 2026-08-24  
**Status:** Requires Claude Code Review  
**Priority:** CRITICAL  
**Audience:** Claude Code (for cross-agent diagnosis)

---

## Executive Summary

**We have a version inconsistency crisis.** This repository contains skills, documentation, and research that were created assuming Mistral Vibe behavior matched official documentation. We now know:

1. Our sandbox **was** running Vibe v2.9.4 (not v2.24.3 as docs referenced)
2. We **upgraded** to v2.24.3, but the underlying architecture issues persist
3. **Three distinct tool systems** exist (Core, SDK, Sandbox-dispatchable) with different behaviors
4. Our documentation and skills **may contain incorrect assumptions** about tool availability and behavior

**This affects both Vibe and Claude Code** - any skills or documentation we've created may be unreliable.

---

## What We Know For Certain

### Version History
- **Initial runtime:** Vibe v2.9.4 (undetected until investigation)
- **Docs referenced:** v2.24.3 source code (from docs/vibe/internals.md verification)
- **Current runtime:** Vibe v2.24.3 (after upgrade)
- **Version gap:** 20 minor versions (2.9.4 → 2.24.3)

### Architecture Discovery
Three-tier tool system (see `docs/vibe/TOOL_VERSION_INCONSISTENCY_AUDIT.md`):

| Tier | Location | Execution Context | Path Resolution |
|------|----------|-------------------|-----------------|
| Core | `vibe/core/tools/builtins/` | Worker | ✅ Correct |
| SDK | `mistralai.vibe.sdk.capabilities.builtins/` | Worker | ❌ Uses worker CWD (`/opt/app/vibe_agents/`)
| Sandbox | `sandbox_dispatch.py` | Sandbox | ✅ Correct |

### Tool Behavior Matrix

| Tool | Core | SDK | Sandbox-Dispatchable | Works in Our Sandbox |
|------|------|-----|---------------------|---------------------|
| `edit` | ✅ | ❌ | ❌ | ✅ **Use this** |
| `read_file` | ✅ | ✅ | ✅ | ✅ |
| `write_file` | ✅ | ✅ | ✅ | ✅ |
| `bash` | ✅ | ✅ | ✅ | ✅ |
| `grep` | ✅ | ✅ | ✅ | ✅ |
| `search_replace` | ❌ | ✅ | ❌ | ❌ **DO NOT USE** |

### Key Finding
**`search_replace` fails because it's an SDK tool that runs on the worker** (CWD = `/opt/app/vibe_agents/`) **but tries to resolve paths against the sandbox workspace** (`/workspace/`). This is a **sandbox environment mismatch**, not a tool bug per se.

---

## Files Created for Investigation

All investigation output is in this repository for Claude's review:

### Primary Investigation Documents
1. **`self-checks/2026-08-24/NEAR_INCIDENT_EXTERNAL_REPO_VIOLATION.md`**
   - Documents the unauthorized external repo issue that triggered this
   - Contains expanded protocol for agent behavior
   - Includes user's explicit instructions about external communications

2. **`self-checks/2026-08-24/audit_report.md`**
   - Comprehensive repository audit from 2026-08-24
   - Skill frontmatter analysis
   - Broken links, missing docs, mailroom backlog

3. **`docs/vibe/TOOL_VERSION_INCONSISTENCY_AUDIT.md`** ⭐ **START HERE**
   - Complete three-tier architecture explanation
   - Path resolution analysis
   - Tool availability matrix
   - Sandbox vs worker execution context
   - Code snippets from actual source files

4. **`scratchpad/ERROR_LOG_2026-08-24.md`** (vibe/errors-2026-08-24 branch)
   - Original error log with corrected root cause
   - Documents the misdiagnosis chain

5. **`scratchpad/FILE_EDITING_WORKAROUNDS.md`** (vibe/errors-2026-08-24 branch)
   - Corrected guidance (use `edit`, not `search_replace`)

6. **`AGENTS.md`** (main branch)
   - Updated with external communications guardrail
   - Pre-edit verification directive added

---

## Questions for Claude Code

**DO NOT ANSWER THESE NOW** - These are provided as context for understanding the scope of the investigation we need Claude to help with:

### Version Management
- Can we **definitely state** that it is possible to update to the newest Vibe code version automatically for every sandbox?
- What mechanisms exist for version detection in Vibe sandboxes?
- Can we programmatically detect which version of Vibe is running and which tool sets are available?

### Documentation vs Implementation
- How can we **detect the differences** between this repo's documentation, actual Vibe implementation, and what we can do about it?
- What's the best way to reconcile docs written for one version (v2.24.3) but used in another (v2.9.4)?
- Can we create a version compatibility matrix that maps tool availability across versions?

### Future-Proofing
- How can we **future-proof** the skills and setup here to avoid version mismatch issues?
- Should we pin to specific Vibe versions in our configuration?
- How do we validate that skills written for one version work correctly in another?
- Can we create automated tests that verify tool behavior before use?

### Architecture Questions
- Why does `edit` (Core tool, runs on worker) work correctly when `search_replace` (SDK tool, runs on worker) doesn't?
- Is there a way to make `search_replace` sandbox-dispatchable, or should it be deprecated?
- Should `edit` be added to the sandbox-dispatchable tool list for consistency?
- Can the SDK `resolve_path()` function be made sandbox-aware?

### Cross-Agent Consistency
- How do Claude Code's tool implementations compare to Vibe's Core vs SDK tools?
- Are there similar version/architecture inconsistencies in Claude Code?
- How can we ensure skills work consistently across both agents despite these differences?

### Validation Strategy
- What's the best approach to audit all existing skills for version-dependent assumptions?
- How do we test skills against multiple Vibe versions?
- Can we create a "version contract" that skills must declare their requirements against?

---

## What We Need from Claude

1. **Review our investigation** (`docs/vibe/TOOL_VERSION_INCONSISTENCY_AUDIT.md`)
2. **Validate our findings** against Claude's own understanding of Vibe's architecture
3. **Help design a comprehensive investigation plan** to:
   - Audit all skills for version-dependent assumptions
   - Create version compatibility documentation
   - Establish validation procedures for future work
4. **Identify gaps** in our understanding that Claude can fill

---

## Immediate Action Items for Claude

When you (Claude) review this:

1. **Read `docs/vibe/TOOL_VERSION_INCONSISTENCY_AUDIT.md` first** - this contains the technical deep-dive
2. **Review the near-incident report** - understand the operational impact
3. **Check your own tool implementations** - do you have similar Core/SDK distinctions?
4. **Help us design** the massive investigation we need to do

---

## Current State Summary

| Aspect | Status | Notes |
|--------|--------|-------|
| Runtime Version | ✅ v2.24.3 | Upgraded from v2.9.4 |
| Docs Reference | ✅ v2.24.3 | docs/vibe/internals.md verified against source |
| Architecture Understanding | ✅ Complete | Three-tier system identified |
| Tool Behavior | ⚠️ Partially Verified | `edit` works, `search_replace` broken |
| Skills Validation | ❌ NOT DONE | Need to audit all skills |
| Version Detection | ❌ NOT IMPLEMENTED | Need automatic version checking |
| Future-Proofing | ❌ NOT IMPLEMENTED | Need compatibility strategy |

---

## Branch Information

This file is on the **`vibe/errors-2026-08-24`** branch, which contains:
- All investigation documents
- Corrected error logs
- Updated AGENTS.md with guardrails
- Tool architecture audit

**DO NOT MERGE TO MAIN** until we complete the full investigation with Claude.

---

## Contact Points

- **Primary:** `docs/vibe/TOOL_VERSION_INCONSISTENCY_AUDIT.md` (technical deep-dive)
- **Secondary:** `self-checks/2026-08-24/NEAR_INCIDENT_EXTERNAL_REPO_VIOLATION.md` (operational context)
- **Tertiary:** `self-checks/2026-08-24/audit_report.md` (repository state)

---

*File created: 2026-08-24*
*Status: Awaiting Claude Code review and investigation planning*
