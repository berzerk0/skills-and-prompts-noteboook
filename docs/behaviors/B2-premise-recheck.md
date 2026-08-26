# B2: Premise Re-Check on Unknown-Tool Error

**Status:** Documented (awaiting hook integration)

## Overview

When a tool call fails because the tool does not exist, the live tool list is injected into the error result before the model is allowed to explain anything. This prevents expensive hypothesis-building based on a false premise.

## Problem This Solves

**Expensive hypothesis chains:** When a tool call fails with "tool not found" or similar, the model often:
1. Invents elaborate explanations (multi-tier architecture failures, system state issues)
2. Proposes complex solutions to false premises
3. Consumes many turns and tokens before the real issue is discovered

**Real example from this repo:**
- Agent called `search_replace` (Claude Code tool)
- Mistral Vibe doesn't have `search_replace`; it uses `edit`
- Result: "tool not found"
- Model response: invented a multi-tier architecture to explain the failure, rather than re-checking the premise
- Cost: multiple turns, false diagnosis, wasted exploration
- Root cause: available tools were not in context when interpreting the error

**Why it's expensive:** The model has one action available (re-check the tool list), but instead spends multiple turns explaining a false premise, then eventually discovers the real issue by accident.

## Implementation

### Core Mechanism

When a tool call fails with error code indicating the tool is not found:

1. **Capture** the error response
2. **Inject** the current list of available tools into the error message
3. **Deliver** to the model before it attempts explanation

Example before:
```
Error: Tool 'search_replace' not found
```

Example after:
```
Error: Tool 'search_replace' not found

Available tools in this harness:
- Read / read_file
- Write / write_file
- Edit (Vibe: 'edit', not 'search_replace')
- Bash / bash
- Grep / grep
- Task / task
[...full list...]

Did you mean one of these tools instead?
```

### Enforcement Point

**Primary:** Hook that intercepts tool-error events and re-formats the error message

**Trigger:** Tool call returns:
- "Tool not found"
- "Unknown tool"
- Tool name not in harness's available tool list
- Any other unrecognized-tool error

**Falsifier:** A transcript where such an error is followed by multiple explanatory turns with no enumeration of available tools.

**Failure mode:** Expensive (token waste, delayed diagnosis, false theories)

### Required Capabilities

This behavior depends on:
1. **Hook access to tool-error events** — Claude Code has `PreToolUse` hook; verify Vibe has `PRE_TOOL` equivalent
2. **Ability to modify error message before model sees it** — hooks must run before model processes the result
3. **Access to current harness tool list** — registry must be readable from hook context

### Hook Integration Checklist

- [ ] Claude Code: Verify `PreToolUse` hook can access tool error results
- [ ] Vibe: Verify `PRE_TOOL` hook (if it exists) fires on tool-not-found
- [ ] Vibe: Confirm error message can be modified before model ingestion
- [ ] Registry: Move `.tools-registry.yaml` to location readable by hooks
- [ ] Testing: Create test case with deliberately wrong tool name

## Related Behaviors

- **B1 (Tool-Name Assertion):** Prevents the problem upstream by validating at commit time
- **B2 (this behavior):** Handles the case where B1 didn't catch it or a tool is truly unavailable
- **B7 (Non-Progress Alarm):** Flags expensive loops; would catch this if the hook didn't prevent it

## Design Decision: Why Not B1 Alone?

B1 catches tool names at skill-creation time, but doesn't address:
1. **Typos in skill invocations** — A skill declares `Read` (valid), but the body calls `read` (typo)
2. **Tool availability changes** — A tool is valid when the skill is created but removed later
3. **Harness-specific code paths** — A skill has fallback logic for when a tool doesn't exist
4. **Manual intervention** — A user manually invokes a tool directly (not through a skill)

B2 is the runtime safety net for these cases.

## Implementation Priority

- **Tier:** 1 (high support, but depends on harness capability that's unconfirmed)
- **Dependency:** Hook access to tool-error events must be verified first
- **Effort:** Medium (requires hook configuration + test case)

## Testing Strategy

### Manual test (before implementing hook):
```bash
# In Claude Code session
# Attempt to call a non-existent tool
# Observe: current behavior (no premise re-check)

# After hook implementation:
# Attempt to call a non-existent tool
# Observe: available tools injected into error
# Measure: turns to diagnosis (should drop significantly)
```

### Automated test:
```bash
# Create skill that deliberately uses wrong tool name
# Invoke skill in both harnesses
# Verify: error message includes tool list in both
# Verify: model's response references available tools, not false premises
```

## Open Questions

1. **Hook capability:** Does Claude Code `PreToolUse` fire on tool-not-found, or only on successful tool calls?
2. **Vibe behavior:** Vibe has `PRE_TOOL` hook; does it fire before tool name validation?
3. **Error context:** Can hooks modify the error message, or only log/deny?
4. **Performance:** What's the cost of injecting a full tool list into every error?

**Resolution:** Check harness source code or ask in respective communities before implementing.

## Related Documentation

- `docs/behaviors/B1-tool-name-validation.md` — Upstream prevention via validation
- `docs/cross-tool-notes.md` — Tool name differences between harnesses
- `notebooks/foundation-harness-behavior-spec-2026-08-25.md` — Original debate and panel consensus

## Panel Support

**Support:** 5 of 8 models (Opus, Gemini, Luna, Lumo, and Haiku-2 before truncation)

**Enforcement split:** Opus placed on hook, others on model judgment. **Local evidence (CLAUDE_RESPONSE_VERSION_RECONCILIATION.md) shows model judgment failed** — the model had the error but didn't re-check the premise. Enforce on hook.

**Quote from debate:** "Expensive. The model builds an elaborate wrong theory instead of running a cheap correct check." — Exactly what happened in this repo with `search_replace` vs `edit`.
