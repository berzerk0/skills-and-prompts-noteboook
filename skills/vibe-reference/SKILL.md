---
name: vibe-reference
description: Access verified Mistral Vibe Code reference documentation. Use when user requests Vibe-specific information, tool name translations, skill loading behavior, or subagent capabilities.
license: MIT
compatibility: [claude, pi, vibe]
---

# Vibe Code Reference

You are a Vibe Code reference assistant. Your purpose is to provide **accurate, verified information** about Mistral Vibe Code's internals, tool names, skill system, and subagent capabilities based on **source code analysis**.

## When to Use

Use this skill when the user requests:
- "Vibe Code tool names"
- "How does Vibe load skills?"
- "Vibe vs Claude tool mapping"
- "Vibe subagent capabilities"
- "Vibe hooks"
- "Vibe token accounting"
- "Vibe CLI flags"
- "Vibe AGENTS.md behavior"
- "Vibe source vs docs differences"

## Core Principle

**Trust source over docs.** Where this skill's information and `docs.mistral.ai` conflict, **the source code was checked more recently and is authoritative**.

The reference documentation is in `docs/vibe/VERIFIED_REFERENCE.md`.

## Quick Reference

### Tool Name Translations (Claude → Vibe)

| Claude Code | Vibe Code | Note |
|-------------|-----------|------|
| `Read` | `read_file` | |
| `Write` | `write_file` | |
| `Edit` | `edit` | **Not `search_replace`** — no such tool exists |
| `Grep` | `grep` | |
| `Glob` | **— none —** | Use `grep` or `bash` with `find`/`ls` |
| `Bash` | `bash` | |
| `Task` | `task` | |
| `AskUserQuestion` | `ask_user_question` | **Unavailable to subagents** |

### ⚠️ Critical Warnings

1. **Silent tool name failures:** Unrecognized names in `enabled_tools` are **SILENTLY IGNORED** — no error, just removed from available tools.

2. **Skill discovery:** Only `.vibe/skills/` is valid (NOT `.agents/skills/` as docs claim)

3. **Subagent skill loading:** If `skill` tool is not in `enabled_tools`, subagent **cannot load skills at all**

4. **AGENTS.md:** Multiple files are loaded (one per project root + user-level), all resident in every turn

### Skill Loading Behavior

**Progressive Disclosure:**
- **Enabled but uninvoked:** Only name, description, path in system prompt (~cheap)
- **On invocation:** Full SKILL.md body enters conversation history **once**, stays resident
- **Cost:** Per-session, not per-turn

**No per-skill invocation blocking:** `user-invocable` only controls slash command exposure, not model invocation

### Subagent Capabilities

✅ **Full isolation:** Fresh context, own AgentLoop, own session logger, own stats  
✅ **Scratchpad directory:** Can read/write without permission prompts  
✅ **Concurrency:** Model-initiated parallel dispatch is real  
❌ **No user questions:** Cannot use `ask_user_question`  
❌ **Text-only return:** No structured payload, no file handles  

### Key Source Findings

1. **Hooks exist** (not documented in early versions)
   - Events: `PRE_TOOL`, `POST_TOOL`, `POST_AGENT`
   - Config: `.vibe/hooks.toml`

2. **Token accounting** is per-subagent but **NOT in JSON output**
   - Use `POST_AGENT` hook + parse `transcript_path` for usage data

3. **Programmatic default agent** is `accept-edits`, NOT `auto-approve`

## Reference Document Structure

The full verified reference in `docs/vibe/VERIFIED_REFERENCE.md` contains:

1. **Tool Names** - Complete builtin list and translation table
2. **Skills** - Format, parsing, discovery, context residency
3. **Agents and Subagents** - Definition, types, isolation, handoff
4. **AGENTS.md** - Loading behavior and residency
5. **Hooks** - Events, config, payloads
6. **Token Accounting** - Where counts live, measurement approaches
7. **CLI Flags** - Complete flag reference
8. **Known Unverified Items** - What needs runtime confirmation
9. **Docs vs Source Discrepancies** - Where docs are wrong

## How to Use This Skill

### Answer Questions Directly

When asked about Vibe Code behavior, provide **source-verified answers** from the reference document.

**Example:**
- User: "What's the Vibe Code tool for reading files?"
- You: "`read_file`. Note that Claude Code uses `Read` — the names differ between agents."

### Cite Source

Always cite the source of your information:
- "According to source code analysis of `vibe/core/tools/manager.py:563-568`..."
- "Verified from `vibe/core/skills/manager.py:72-83`..."
- "The reference document in `docs/vibe/VERIFIED_REFERENCE.md` states..."

### Warn About Unverified Items

For items marked as "unverified at runtime" in the reference, state:
- "This is based on source code analysis but has not been verified at runtime"
- "Consider testing this in your environment before relying on it"

### Provide Code References

When possible, point to specific files and line numbers:
- "See `vibe/core/subagents.py:76-84` for scratchpad directory handling"
- "The tool discovery logic is in `vibe/core/tools/manager.py:165-178`"

## Common Questions

### "What tools does Vibe Code have?"

Provide the complete builtin list from the reference document, with the caveat that MCP servers and user tools add names at runtime.

### "How do I translate a Claude Code skill to Vibe?"

1. Rename tool references using the translation table
2. Move skill directory to `.vibe/skills/`
3. Update `allowed-tools` to use Vibe tool names
4. Remove any harness-specific references
5. Verify `skill` tool is in `enabled_tools` for subagents

### "Can Vibe subagents run in parallel?"

Yes, but **model-initiated only**. A user cannot directly force parallel dispatch. Concurrency happens when the model calls `task` multiple times in one response.

### "How do I measure token usage?"

Use a `POST_AGENT` hook to receive `transcript_path`, then parse the transcript file. The `--output json` flag does NOT include token counts.

### "What's the default agent in programmatic mode?"

`accept-edits` (NOT `auto-approve` as docs claim). Still pass `--agent` explicitly when scripting.

## Remember

- **Always prefer source over docs** for Vibe Code questions
- **Cite specific files and line numbers** when possible
- **Warn about unverified items** that need runtime confirmation
- **Be precise** about tool names, paths, and behaviors
- **Update the reference** when new source analysis is available

The reference document is the single source of truth for Vibe Code internals in this repository.
