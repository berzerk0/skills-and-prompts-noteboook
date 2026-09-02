# Vibe Tool Version & Behavior Inconsistency Audit

**Created:** 2026-08-24  
**Status:** Active Investigation  
**Priority:** HIGH  
**Scope:** SDK vs Core tool discrepancies, version mismatches, path resolution bugs

---

## Executive Summary

We discovered a **critical inconsistency** between:
1. **Runtime version** (was v2.9.4, now upgraded to v2.24.3)
2. **Documentation reference** (`docs/vibe/internals.md` verified against v2.24.3 source)
3. **Tool availability** (`search_replace` exists in SDK but not core, with path bugs)

This creates **unpredictable behavior** and explains many of the file editing failures.

---

## Version Timeline

| Date | Runtime Version | Docs Reference | Action |
|------|----------------|----------------|--------|
| 2026-08-24 (original) | **v2.9.4** | v2.24.3 | File editing failures, misdiagnosed |
| 2026-08-24 (discovery) | v2.9.4 | v2.24.3 | Identified version gap |
| 2026-08-24 (upgrade) | **v2.24.3** | v2.24.3 | Upgraded to match docs |

---

## Tool Architecture Discovery

### Core Vibe Tools vs SDK Tools

**Two separate tool systems exist:**

#### 1. Core Vibe Tools (vibe/core/tools/builtins/)
- **Verified against:** v2.24.3 source code
- **Discovered via:** Static source analysis
- **List in `docs/vibe/internals.md`:** Complete and accurate for v2.24.3
- **Tool names:** `edit`, `read_file`, `write_file`, `bash`, `grep`, etc.
- **`search_replace`:** **DOES NOT EXIST** in core tools

#### 2. SDK Tools (mistralai.vibe.sdk.capabilities.builtins/)
- **Discovered via:** Runtime inspection, file search
- **Location:** `/usr/local/lib/python3.12/site-packages/mistralai/vibe/sdk/capabilities/builtins/`
- **Tool names:** `search_replace`, `read_file`, `write_file`, etc.
- **`search_replace`:** **EXISTS** but has critical path resolution bug

### The Critical Distinction

```
┌─────────────────────────────────────────────────────────────┐
│                    VIBE TOOL ECOSYSTEM                           │
├─────────────────────────────────────────────────────────────┤
│                                                                  │
│  CORE TOOLS              SDK TOOLS                             │
│  ───────────             ──────────                             │
│  vibe/core/tools/       mistralai.vibe.sdk/                   │
│  builtins/               capabilities/builtins/                 │
│                                                                  │
│  ✅ edit                ❌ search_replace (path bug)            │
│  ✅ read_file           ✅ read_file                           │
│  ✅ write_file          ✅ write_file                          │
│  ✅ bash                ✅ bash                               │
│  ✅ grep                ✅ grep                               │
│                                                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## `search_replace` Deep Dive

### Existence
- **v2.9.4:** Exists in SDK (`mistralai.vibe.sdk.capabilities.builtins.search_replace_tool`)
- **v2.24.3:** Exists in SDK (same location, **same path bug**)
- **Core tools:** Does NOT exist in either version

### Path Resolution Bug

**Symptom:** All paths passed to `search_replace` get `/opt/app/vibe_agents/` prepended

```
Input:  "scratchpad/test.md"
Searched: "/opt/app/vibe_agents/scratchpad/test.md"

Input:  "/workspace/scratchpad/test.md"
Searched: "/opt/app/vibe_agents/workspace/scratchpad/test.md"
```

**Key Finding:** `/opt/app/vibe_agents/` does NOT exist on this system
- This is a **hardcoded or misconfigured base path** in the SDK tool
- The sandbox environment uses `/workspace/` as the workspace root
- The tool is looking in the wrong place

### Source Code Location
```
File: /usr/local/lib/python3.12/site-packages/mistralai/vibe/sdk/
  capabilities/builtins/search_replace_tool.py
```

---

## `edit` Tool Status

### Verification
- **v2.9.4:** Works correctly (no path issues)
- **v2.24.3:** Works correctly (no path issues)
- **Both versions:** Properly resolves relative and absolute paths

### Confirmed Functionality
```yaml
# Working example (both versions)
edit:
  file_path: "scratchpad/test.md"
  content:
    - old_str: "old text"
      new_str: "new text"
```

---

## Version-Specific Behavior Matrix

| Tool | v2.9.4 | v2.24.3 | Core | SDK | Notes |
|------|--------|---------|------|-----|-------|
| `edit` | ✅ Works | ✅ Works | ✅ | ❌ | Use this for file edits |
| `read_file` | ✅ | ✅ | ✅ | ✅ | Both work |
| `write_file` | ✅ | ✅ | ✅ | ✅ | Both work |
| `search_replace` | ❌ Path bug | ❌ Path bug | ❌ | ✅ | **DO NOT USE** |
| `bash` | ✅ | ✅ | ✅ | ✅ | Both work |
| `grep` | ✅ | ✅ | ✅ | ✅ | Both work |

---

## Root Cause Analysis

### Why the Confusion?

1. **Version Mismatch:** Runtime was v2.9.4, docs referenced v2.24.3
2. **Dual Tool Systems:** Core vs SDK tools have different implementations
3. **Path Bug:** SDK `search_replace` has hardcoded `/opt/app/vibe_agents/` prefix
4. **Documentation Gap:** `docs/vibe/internals.md` only covers core tools, not SDK

### The Original 2026-08-24 Incident

```
Agent called: search_replace (SDK tool, exists but broken)
Got error: "File not found at: /workspace/..."
Misdiagnosed: Thought tool didn't exist
Actual: Tool exists but looks in /opt/app/vibe_agents/...
```

---

## Impact Assessment

### What's Broken
- `search_replace` tool is **non-functional** in this sandbox environment
- Version mismatch caused **misdiagnosis** of the actual problem
- Documentation doesn't cover **SDK-level tools**

### What Works
- `edit` tool (core) - fully functional
- `read_file` tool - fully functional  
- `write_file` tool - fully functional
- All other core tools - functional

### Risk Level
- **HIGH** for agents that try to use `search_replace`
- **MEDIUM** for version consistency
- **LOW** for agents using `edit`/`read_file`/`write_file`

---

## Recommended Actions

### Immediate (This Repo)
1. **Update AGENTS.md** to explicitly state:
   - Use `edit` for file modifications, NOT `search_replace`
   - Document the SDK vs Core tool distinction
   - Add version check to session startup

2. **Update docs/vibe/internals.md** header to note:
   - "Verified against v2.24.3 source (core tools only)"
   - "SDK tools may differ - see TOOL_VERSION_INCONSISTENCY_AUDIT.md"

3. **Add to self-checks/2026-08-24/:**
   - Version discrepancy findings
   - Tool behavior verification results

### Medium Term
1. **Verify with Mistral:** Is `/opt/app/vibe_agents/` the intended SDK base path?
2. **Check other SDK tools:** Do they have similar path issues?
3. **Document SDK tools:** Create a complementary reference for SDK-level tools

### Long Term
1. **Sandbox configuration:** Can we align sandbox paths with SDK expectations?
2. **Version pinning:** Should this repo pin to a specific Vibe version?
3. **Tool deprecation:** Should `search_replace` be removed from SDK or fixed?

---

## Test Results (v2.24.3 Upgrade)

### Upgrade Performed
```bash
pip install --upgrade mistral-vibe
# Before: 2.9.4
# After: 2.24.3
```

### Verification
- ✅ `edit` tool: Works correctly
- ❌ `search_replace` tool: Still has path bug (same as v2.9.4)
- ✅ `read_file` tool: Works correctly
- ✅ `write_file` tool: Works correctly

### Conclusion
**The path bug in `search_replace` is NOT version-specific.** It exists in both v2.9.4 and v2.24.3, confirming it's a **sandbox environment issue**, not a Vibe version issue.

---

## Files for Investigation

### To Review
1. `/usr/local/lib/python3.12/site-packages/mistralai/vibe/sdk/capabilities/builtins/search_replace_tool.py`
2. SDK tool manager vs Core tool manager
3. Path resolution logic in both systems
4. Sandbox workspace configuration

### To Create
1. Test script to verify all tools in both systems
2. Version detection script for session startup
3. Tool capability matrix (core vs SDK)

---

## Next Steps

### Phase 1: Documentation (This Week)
- [ ] Update AGENTS.md with tool usage guidance
- [ ] Update docs/vibe/internals.md with version context
- [ ] Create tool comparison table

### Phase 2: Verification (Next Session)
- [ ] Test all core tools systematically
- [ ] Test all SDK tools systematically
- [ ] Document any other inconsistencies

### Phase 3: External Coordination (Pending User Approval)
- [ ] Report SDK `search_replace` path bug to Mistral
- [ ] Verify if this affects other sandbox environments
- [ ] Check if there's a configuration option to fix the path

---

## References

- `docs/vibe/internals.md` - Core tools reference (v2.24.3)
- `self-checks/2026-08-24/NEAR_INCIDENT_EXTERNAL_REPO_VIOLATION.md` - Original incident
- `self-checks/2026-08-24/audit_report.md` - Repository audit
- [mistralai/mistral-vibe GitHub](https://github.com/mistralai/mistral-vibe) - Source repository

---

*Document created: 2026-08-24*
*Last updated: 2026-08-24*
*Status: Active investigation*

---

## CRITICAL UPDATE: Three-Tier Tool Architecture

### The Full Picture (Discovered 2026-08-24)

There are **THREE distinct tool execution contexts**, not two:

#### 1. Core Vibe Tools
- **Location:** `vibe/core/tools/builtins/` (in source repo)
- **Execution:** Worker process
- **Path resolution:** Uses worker's CWD
- **Tools:** `edit`, `read_file`, `write_file`, `bash`, `grep`, `task`, etc.
- **Sandbox:** NO - runs on worker, not in sandbox

#### 2. SDK Builtin Tools  
- **Location:** `mistralai.vibe.sdk.capabilities.builtins/`
- **Execution:** Worker process
- **Path resolution:** Uses worker's CWD (`/opt/app/vibe_agents/`)
- **Tools:** `search_replace`, `read_file`, `write_file`, `bash`, `grep`, etc.
- **Sandbox:** NO - runs on worker, not in sandbox

#### 3. Sandbox-Dispatchable Tools
- **Location:** `mistralai.vibe.sdk.capabilities.builtins.sandbox_dispatch.py`
- **Execution:** Sandbox process (`/workspace/`)
- **Path resolution:** Uses sandbox's CWD
- **Tools:** `bash`, `grep`, `read_file`, `write_file`
- **Sandbox:** YES - explicitly dispatched into sandbox

### The Key Code from sandbox_dispatch.py

```python
_SANDBOX_TOOLS: tuple[SandboxTool, ...] = (bash, grep, read_file, write_file)

SANDBOX_DISPATCHABLE_TOOLS: Mapping[str, SandboxTool] = {tool.name: tool for tool in _SANDBOX_TOOLS}
```

**`search_replace` is NOT in this list.**

### Why search_replace Fails

1. **`search_replace` is an SDK tool** that runs on the **worker**
2. **Worker's CWD is `/opt/app/vibe_agents/`** (not `/workspace/`)
3. **`resolve_path()` in SDK uses `Path.cwd()`** which returns the worker's CWD
4. **Result:** All paths get resolved relative to `/opt/app/vibe_agents/` instead of `/workspace/`

### Why edit Works

1. **`edit` is a Core tool** that runs on the **worker**
2. **But it has its own path handling** that doesn't use the SDK's `resolve_path()`
3. **It correctly resolves paths** relative to the actual workspace

### The Path Resolution Functions

**SDK utils.py:**
```python
def resolve_path(path: str) -> Path:
    file_path = Path(path).expanduser()
    if not file_path.is_absolute():
        file_path = Path.cwd() / file_path  # <-- Uses worker's CWD!
    return file_path.resolve()
```

**Core tool handling:**
- Different implementation, doesn't rely on SDK's resolve_path
- Correctly handles workspace paths

### Tool Availability Matrix

| Tool | Core | SDK | Sandbox-Dispatchable | Works in Sandbox |
|------|------|-----|---------------------|------------------|
| `edit` | ✅ | ❌ | ❌ | ✅ (worker, correct paths) |
| `read_file` | ✅ | ✅ | ✅ | ✅ (both work) |
| `write_file` | ✅ | ✅ | ✅ | ✅ (both work) |
| `bash` | ✅ | ✅ | ✅ | ✅ (both work) |
| `grep` | ✅ | ✅ | ✅ | ✅ (both work) |
| `search_replace` | ❌ | ✅ | ❌ | ❌ (worker, wrong paths) |

### The Fix

**DO NOT USE `search_replace` in sandbox environments.**
- It runs on the worker, not in the sandbox
- It uses the worker's filesystem view, not the sandbox's
- There is no configuration to change this behavior

**USE `edit` instead** for all file modifications.

### Implications for This Repo

1. **docs/vibe/internals.md** only covers Core tools - it's still accurate
2. **SDK tools are a separate system** with different behavior
3. **Sandbox-dispatchable tools** are a subset that work correctly in the sandbox
4. **The version gap (v2.9.4 → v2.24.3)** didn't matter - the architecture is the same

### Open Questions

1. Why does `edit` (Core) work correctly when it also runs on the worker?
2. Is there a way to make `search_replace` sandbox-dispatchable?
3. Should Mistral add `edit` to the sandbox-dispatchable list?
4. Can the SDK `resolve_path` be fixed to handle sandbox paths?

