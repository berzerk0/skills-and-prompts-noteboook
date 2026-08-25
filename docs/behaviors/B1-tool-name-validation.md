# B1: Tool-Name Assertion Before Commit

**Status:** Implemented (validation script + hook template)

## Overview

Every tool name written into a skill's frontmatter is checked against a per-harness tool table before the file lands. This prevents silent-drop failures where a tool name is unrecognized by one harness but the skill loads anyway, appearing healthy while being crippled.

## Problem This Solves

**Silent drop in Vibe:** Mistral Vibe silently drops unrecognized tool names with no error message. A skill written with `Read`, `Write`, `Glob` (Claude Code names) will load in Vibe, but the invocation of those tools will fail silently. The skill appears to work until actually tested.

**Example from this repo:**
- A skill declares `allowed-tools: [Read, Write, Glob, Grep, WebSearch]`
- Works perfectly in Claude Code
- In Vibe: skill loads, but `read_file`, `write_file`, `grep` are silently dropped
- No error at load time; errors only surface when the skill is actually invoked

## Implementation

### 1. Tool Registry (`.tools-registry.yaml`)

A YAML file listing valid tool names for each harness:

```yaml
harnesses:
  claude-code:
    name: "Claude Code"
    tools: [Read, Write, Edit, Grep, Glob, Bash, Task, ...]
  
  vibe:
    name: "Mistral Vibe Code"
    tools: [read_file, write_file, edit, grep, bash, task, ...]

translation:
  claude-code-to-vibe:
    Read: read_file
    Write: write_file
    # ... etc
```

Location: `./.tools-registry.yaml`

### 2. Validation Script (`scripts/validate-tool-names.py`)

A Python script that:
- Reads skill files and extracts `allowed-tools` from frontmatter
- Checks each tool against the registry for target harness(es)
- Reports violations with clear error messages
- Can be run manually or via pre-commit hook

Usage:
```bash
# Check all skills for both Claude Code and Vibe
python3 scripts/validate-tool-names.py --harness claude-code --harness vibe

# Check specific skills
python3 scripts/validate-tool-names.py skills/my-skill/SKILL.md

# Show both valid and invalid
python3 scripts/validate-tool-names.py --show-valid

# Fail if any errors (useful for CI)
python3 scripts/validate-tool-names.py --fail-on-error
```

### 3. Pre-Commit Hook (Optional but Recommended)

**Template:** See `docs/behaviors/B1-setup-hook.sh`

To install the pre-commit hook:
```bash
# Copy hook template to .git/hooks
cp docs/behaviors/B1-setup-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

The hook runs the validation script on any skill files staged for commit, preventing invalid tool names from being committed.

## Enforcement Ladder

**Primary (Pre-commit):** Hook runs before commit is created, catching faults before they reach other harnesses.

**Secondary (On-load):** If the hook is not installed, Vibe will silently drop unrecognized names on load. Watch for this when porting skills between harnesses.

**Tertiary (Runtime):** Hook-enforced error injection at tool-invocation time (future enhancement).

## Quick Start

### For single-harness skills (Claude Code only):
```yaml
---
name: my-skill
allowed-tools:
  - Read
  - Write
  - Grep
  - Bash
---
```

No validation needed; these tools exist in Claude Code.

### For multi-harness portable skills:

**Option A: Use only shared tools**
```yaml
allowed-tools:
  - Bash  # Exists in both harnesses
  - Edit  # Exists in both harnesses
```

**Option B: Declare per-harness tools with a comment**
```yaml
# Portable to: claude-code only
# In Vibe, would require: read_file, write_file, grep
allowed-tools:
  - Read
  - Write
  - Grep
  - WebSearch
```

### For Vibe-first or Vibe-only skills:

Use Vibe tool names directly:
```yaml
allowed-tools:
  - read_file
  - write_file
  - bash
  - grep
```

## Tool Name Translation Reference

| Claude Code | Vibe | Notes |
|---|---|---|
| Read | read_file | |
| Write | write_file | |
| Edit | edit | In Claude: `search_replace`, in Vibe: `edit` (different tools) |
| Grep | grep | Same name, different parameter names |
| Glob | *(none)* | No Vibe equivalent; use bash with find/ls |
| Bash | bash | |
| Task | task | |
| AskUserQuestion | ask_user_question | |
| WebSearch | *(none in Vibe)* | Use bash + curl for HTTP calls |
| Agent/Skill (invocation) | *(different)* | Invocation differs; not in allowed-tools |

## Detected Issues (from this repo)

Running the validator against existing skills found:

**High priority:**
- `skills/skill-extractor/SKILL.md`: declares tools not available in Vibe (WebSearch, Read, Write, Glob, Grep, AskUserQuestion will be silently dropped)

**Recommendation:** Mark this skill as Claude-Code-only or create a Vibe-compatible variant.

## Testing Validation

```bash
# Full validation
python3 scripts/validate-tool-names.py --show-valid --fail-on-error

# Test a specific skill
python3 scripts/validate-tool-names.py skills/skill-extractor/SKILL.md --harness vibe
```

## Related Behaviors

- **B2 (Premise re-check):** Handles the case where validation didn't catch a tool name issue and the tool fails at runtime.
- **B3 (Retirement sweep):** Cleans up skills that have tool issues and become broken.

## Future Enhancements

1. **Hook on other harnesses:** Add Vibe-side hook (in `hooks.toml`) that validates tool names at load time.
2. **Per-harness CI:** Check tool portability in CI before merging.
3. **Automatic translation:** Offer to auto-convert `allowed-tools` for portability.
4. **MCP tool registry:** Extend to validate MCP server tool availability.
