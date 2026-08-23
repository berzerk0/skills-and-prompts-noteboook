# Mistral Vibe Code -- Complete Reference & Skill Builder Guide

> **Verified against:** `mistralai/mistral-vibe` @ `a84be0391bf93e93a4025a5e08e8032ecb587123` (2026-08-20), `pyproject.toml` version **2.24.3**
> **Verified:** 2026-08-22, two rounds, in a Vibe Code Web sandbox reading its own source
> **Method:** static source analysis (T2). Runtime testing was blocked by MCP/sentry import errors in the sandbox.

> **Standing rule discovered during verification: trust source over docs.** Three separate claims taken from official docs turned out to disagree with the code, always in the same direction -- docs describe something simpler or older. Where this file and `docs.mistral.ai` conflict, the code was checked more recently.

---

## Table of Contents

### Part A: Verified Internals Reference
1. [Tool Names](#1-tool-names)
2. [Skills](#2-skills)
3. [Agents and Subagents](#3-agents-and-subagents)
4. [AGENTS.md](#4-agentsmd)
5. [Hooks](#5-hooks)
6. [Token Accounting](#6-token-accounting)
7. [CLI Flags](#7-cli-flags)
8. [Known Unverified](#8-known-unverified)
9. [Docs-vs-Source Discrepancies](#9-docs-vs-source-discrepancies)

### Part B: Skill Building Workflows
- [Quick Start: Create a Skill](#quick-start-create-a-skill)
- [Skill Structure](#skill-structure)
- [Discovery & Enablement](#discovery--enablement)
- [Tool Access](#tool-access)
- [Invocation Patterns](#invocation-patterns)
- [Content Patterns](#content-patterns)
- [Testing Workflows](#testing-workflows)
- [Common Pitfalls & Fixes](#common-pitfalls--fixes)
- [Advanced Patterns](#advanced-patterns)
- [Deployment](#deployment)
- [Quick Checklist](#quick-checklist)

---

## Part A: Verified Internals Reference

---

## 1. Tool Names

Builtin tools live in `vibe/core/tools/builtins/*.py`. Each is a `BaseTool` subclass; the invocable name is derived from the class name by `BaseTool.get_name()` (`vibe/core/tools/base.py:424-426`), which converts PascalCase to snake_case. Discovery is `ToolManager._iter_tool_classes_with_origin()` (`vibe/core/tools/manager.py:165-178`), which walks `search_paths` -- note the plural.

### Complete Builtin List

`ask_user_question`, `bash`, `bash_log_file`, `bash_output`, `bash_sessions`, `bash_stdin`, `edit`, `exit_plan_mode`, `experimental_bash`, `git_bash`, `git_bash_log_file`, `git_bash_output`, `git_bash_sessions`, `git_bash_stdin`, `grep`, `powershell`, `powershell_log_file`, `powershell_output`, `powershell_sessions`, `powershell_stdin`, `read_file`, `skill`, `task`, `todo`, `web_fetch`, `web_search`, `write_file`

**Scope caveat:** exhaustive for *builtins only*. `search_paths` is plural -- user/project tool directories and MCP servers add names at runtime. Sufficient for translating imported skills; not a complete session inventory.

### Translation from Claude Code

| Claude Code | Vibe | Note |
|---|---|---|
| `Read` | `read_file` | |
| `Write` | `write_file` | |
| `Edit` | `edit` | **Not `search_replace`** -- no such tool exists |
| `Grep` | `grep` | |
| `Glob` | **-- none --** | No glob/list tool. Use `grep`, or `bash` running `find`/`ls` |
| `Bash` | `bash` | |
| `Task` | `task` | |
| `AskUserQuestion` | `ask_user_question` | Unavailable to subagents |

### Failure Mode

Unrecognized names in `enabled_tools` are **silently ignored** -- no match means not included in `available_tools` (`vibe/core/tools/manager.py:563-568`). A typo or a stale Claude Code name does not error; it quietly removes the capability. This is the single most dangerous behaviour in this document.

**Corollary:** a subagent whose `enabled_tools` omits `skill` cannot load skills at all.

---

## 2. Skills

### Format and Parsing

A skill is a directory containing `SKILL.md` with YAML frontmatter (`vibe/core/skills/manager.py:129-131`, `vibe/core/skills/parser.py`). Fields actually parsed (`vibe/core/skills/models.py:38-68`):

`name` · `description` · `license` · `compatibility` · `metadata` (dict) · `allowed-tools` (list) · `user-invocable` (bool)

### Discovery Order

`vibe/core/skills/manager.py:72-83`:

1. `skill_paths` in `config.toml`
2. Project-level `./.vibe/skills/`
3. User-level `~/.vibe/skills/`

**Docs are wrong here.** `docs.mistral.ai` lists `./.agents/skills/` as a discovery path. It is not one in source. Use `.vibe/skills/`.

### Context Residency -- Progressive Disclosure Holds

This was verified twice; round 1 got it wrong. The prompt-assembly path is `get_universal_system_prompt()` -> `_get_available_skills_section()` (`vibe/core/system_prompt.py:262-290`, `345-380`).

**For an enabled but uninvoked skill,** the system prompt contains only:

```xml
<skill>
  <name>...</name>
  <description>...</description>
  <path>...</path>
</skill>
```

**The full `SKILL.md` body is not in the system prompt.** It is loaded on demand by the **`skill` tool** (`vibe/core/tools/builtins/skill.py:120-158`), which returns `skill_info.prompt` as a **tool result**.

Cost model that follows:

- Per enabled skill, per turn: name + description + path. Cheap.
- On invocation: the full body enters conversation history **once**, then stays resident for the remainder of the session.
- So enabling many skills is cheap; invoking a bloated skill is expensive, and the cost is per-session not per-turn.

`user-invocable` does **not** change residency. The system prompt always lists all enabled skills.

### Invocation Control

`user-invocable: true` exposes the skill as a slash command. It does **not** prevent model invocation (`vibe/core/skills/models.py:62-65`, `manager.py:179-188`).

**There is no per-skill equivalent of Claude Code's `disable-model-invocation`.** The only lever is `enabled_skills` / `disabled_skills` in `config.toml` -- global, user-set, all-or-nothing per skill. Supports exact names, globs, and regex with an `re:` prefix (`manager.py:54-63`, `vibe_schema.py:395-405`). A non-empty `enabled_skills` acts as an allow-list.

### No Plugin System

Skills are directories on disk. No marketplace, no `/plugin install` (`vibe/core/skills/manager.py`). A separate opt-in registry exists but is not a plugin system.

**Installation is therefore:** clone or download -> copy the skill directory into `~/.vibe/skills/` or `./.vibe/skills/` -> rewrite `allowed-tools` -> adjust or remove anything harness-specific.

---

## 3. Agents and Subagents

### Definition

`.toml` files in `~/.vibe/agents/` (user) or `./.vibe/agents/` (project) -- `vibe/core/config/harness_files/_harness_manager.py:187-189`.

Every agent declares `agent_type` (`vibe/agents.py:1-17`):
- `"agent"` -- user-facing, selectable via `--agent <name>` or Shift+Tab
- `"subagent"` -- delegation-only, spawned by the model through the `task` tool

Subagents cannot be selected with `--agent`. Attempting it errors: *"Only agents of type 'agent' can be selected with --agent"* (`vibe/core/agents/manager.py:43-48`).

Builtin subagent `explore` is read-only (`vibe/core/agents/models.py:85-91`).

### Recognized `.toml` Keys

`vibe/core/agents/models.py:26-40`, `vibe/core/config/vibe_schema.py:367-405`:

| Key | Purpose |
|---|---|
| `active_model` | **Per-agent model routing.** The primary cost lever. |
| `allowed_models` | Restrict which models this agent may use |
| `providers` / `models` | Provider and model config overrides |
| `compaction_model` | Model used for context compaction -- separate from `active_model` |
| `bypass_tool_permissions` | Skip permission prompts |
| `enabled_tools` / `disabled_tools` | Tool scoping |
| `tools` | Dict with per-tool `permission`, `allowlist`, `denylist` |
| `system_prompt_id` | Points at a file in `~/.vibe/prompts/` |
| `safety` | **Cosmetic only** -- sets input border colour, enforces nothing (`vibe/agents.py:7-14`) |

### Subagent Isolation -- Confirmed Clean

`vibe/app_server/_runtime.py:509-540`, `vibe/app_server/_sessions.py:291-345`.

- **Fresh context.** `create_child()` builds a new `AgentLoop` with a copied config orchestrator. No parent conversation history is passed.
- The subagent's entire first message is `prepare_subagent_prompt(args.task, ctx)` and nothing else.
- Own `AGENTS.md` load, own `AgentLoop`, own `session_logger`, own stats.
- Skills visible are those from its own (inherited-then-overridden) config.

### `scratchpad_dir` -- Native File Handoff

`vibe/core/subagents.py:76-84`:

```python
def prepare_subagent_prompt(task: str, ctx: InvokeContext) -> str:
    if ctx.scratchpad_dir is None:
        return task
    return (
        f"Scratchpad directory: {ctx.scratchpad_dir}\n"
        "You can read and write files here without permission prompts.\n\n"
        f"{task}"
    )
```

Subagents are handed a scratchpad directory and told they may read and write there without permission prompts. **This is first-class support for the write-findings-to-a-file, return-a-path pattern.** Build handoff conventions on `scratchpad_dir` rather than inventing one.

### Return Channel

`TaskResult` carries only (`vibe/core/subagents.py:18-26`, `vibe/core/tools/builtins/task.py:30-118`):

```
response: str
turns_used: int
completed: bool
```

Text only. No structured payload, no file handles. A subagent returning a path returns it as a string the parent must parse.

### Hard Constraints

- **Subagents cannot ask the user questions.** No access to `ask_user_question` (`task.py:111-115`). Any clarification must happen in the parent agent. A subagent that hits ambiguity will guess or return partial results.
- Concurrency is real but **model-initiated only**; a user cannot directly force parallel dispatch (`task.py:80-118`).

---

## 4. AGENTS.md

`vibe/core/config/harness_files/_harness_manager.py:189-192`, `210-234`, `237-256`.

- **Not** limited to two files. Loads the user-level file plus **one per project root**, walking up to the trust root.
- Additional `AGENTS.md` files are auto-discovered for lazy injection when reading files below open project roots.
- Loaded at session start via `load_project_docs()` and **resident every turn**. Always-on cost -- budget every line.

---

## 5. Hooks

**Vibe has hooks.** (Assumed absent in early planning; that was wrong.)

`vibe/core/hooks/models.py`, `vibe/core/hooks/config.py`, `_harness_manager.py:109-114`.

- **Events:** `PRE_TOOL`, `POST_TOOL`, `POST_AGENT`
- **Config:** `hooks.toml` -- a `hooks` list with fields `name`, `type`, `command`, `match`, `timeout`, `strict`, `description`
- **Location:** `.vibe/hooks.toml` in project roots, and `~/.vibe/hooks.toml`
- **Rough Claude Code mapping:** `PRE_TOOL` ≈ `PreToolUse`, `POST_AGENT` ≈ `Stop`

### Hook Payloads (`vibe/core/hooks/models.py:85-165`)

| Event | Fields |
|---|---|
| `PostAgentInvocation` | `session_id`, `transcript_path`, `cwd`, `parent_session_id` |
| `PreToolInvocation` | above + `tool_name`, `tool_call_id`, `tool_input` |
| `PostToolInvocation` | above + `tool_status`, `tool_output`, `tool_output_text`, `tool_error`, `duration_ms` |

**No token counts are passed to hooks.** But `POST_AGENT` carries `transcript_path` -- which is the route to usage data (see below).

---

## 6. Token Accounting

### Where Counts Live

`vibe/app_server/models.py:293-343`, `870-882`.

```
TokenUsage:          input_tokens, output_tokens, total_tokens

AgentStatsSnapshot:  steps
                     session_prompt_tokens, session_completion_tokens, session_cached_tokens
                     last_turn_prompt_tokens, last_turn_completion_tokens, last_turn_cached_tokens
                     computed: session_total_llm_tokens(), last_turn_total_tokens(), session_cost()

PublicSession:       token_usage: TokenUsage | None
```

Tracked **per subagent** -- each has its own `AgentLoop` and stats.

### What `--output json` Actually Emits

`vibe/cli/programmatic.py:37-102`. The envelope is:

```json
{ "history": [ /* PublicHistoryEntry objects */ ] }
```

or, with teleport, `{"history": [...], "teleportUrl": "..."}`.

`PublicHistoryEntry` is a discriminated union of `message`, `reasoning`, `effect`, `callback`, `checkpoint`, `notice`. **None of them carry token counts.** `token_usage` lives on `PublicSession`, which is *not* in the programmatic output.

### Consequences for Measurement

- `--output json` -> **no usage data.** Dead end.
- Hooks -> **no token counts.** Dead end.
- No `/cost` command exists.
- **Viable route:** `POST_AGENT` hook receives `transcript_path`. Parse the transcript. This is the same technique Anthropic's `session-report` uses against Claude Code JSONL -- only the file format differs.

*Unverified at runtime.* Transcript format and contents were never inspected. Confirm before building.

---

## 7. CLI Flags

`vibe/cli/cli.py:174`, `vibe/cli/entrypoint.py:65-69`, `102-107`, `130-154`.

| Flag | Behaviour |
|---|---|
| `--agent NAME` | Select a user-facing agent. Subagents rejected. |
| `--prompt` / `-p` | Programmatic mode |
| `--output json` | History only, no usage |
| `--max-turns N` | Turn cap |
| `--max-tokens`, `--max-price` | Budget caps |
| `--worktree NAME` | Create or reuse a git worktree under `$VIBE_HOME/worktrees` |
| `--add-dir PATH` | Implicitly trusts the path; adds it to `workspace_roots` for config discovery (pulls its `AGENTS.md` and `.vibe/`) |

### Programmatic Mode Default Agent

**Docs are wrong here too.** `docs.mistral.ai` says programmatic mode falls back to `auto-approve`. Source shows it falls back to the `default_agent` config value, whose default is **`accept-edits`** (`vibe/cli/cli.py:174`, `entrypoint.py:105-124`).

Less dangerous than the docs imply -- `accept-edits` auto-approves file edits but still prompts for shell commands. **Still pass `--agent` explicitly when scripting.**

---

## 8. Known Unverified

| Item | Status | How to Settle |
|---|---|---|
| `--output json` real envelope | Source only; sandbox runtime broken | `vibe -p "say hi" --output json --max-turns 1 --agent plan` |
| Transcript file format | Never inspected | Trigger a `POST_AGENT` hook, read `transcript_path` |
| Subagent tool availability column | Partly inferred, not fully cited | Read `task.py` tool-filtering logic directly |
| User-forced parallel dispatch | Model-initiated confirmed; forcing untested | Have an agent call `task` twice in one response |
| Runtime-added tool names | Builtins exhaustive; MCP/user tools unknown | Inspect `search_paths` on a live session |

---

## 9. Docs-vs-Source Discrepancies Found

| Topic | Docs say | Source says |
|---|---|---|
| Skill discovery path | `./.agents/skills/` is valid | Only `./.vibe/skills/` |
| AGENTS.md count | At most two files | One per project root, plus user-level |
| Programmatic default agent | `auto-approve` | `default_agent`, default `accept-edits` |
| Tool name for editing | (example uses `read_file`, correct) | `edit`, and no `search_replace` anywhere |

**Pattern:** docs lag the code and describe a simpler model. Check source for anything load-bearing.

---

---

## Part B: Skill Building Workflows

---

## Quick Start: Create a Skill

```bash
# 1. Create skill directory structure
mkdir -p ~/.vibe/skills/my-skill

# 2. Create SKILL.md with frontmatter
cat > ~/.vibe/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: What this skill does
license: MIT
compatibility:
  - vibe: ">=2.24.0"
user-invocable: true
allowed-tools:
  - read_file
  - grep
  - bash
---

# My Skill Content

This skill helps with...
EOF

# 3. Enable the skill (add to config.toml)
echo 'enabled_skills = ["my-skill"]' >> ~/.vibe/config.toml
```

---

## Skill Structure

### Required Files
```
.vibe/skills/my-skill/
├── SKILL.md          # Main file with YAML frontmatter + content
└── (optional)       # Any supporting files referenced in content
```

### YAML Frontmatter Fields

| Field | Required | Type | Purpose |
|---|---|---|---|
| `name` | ✅ | string | Unique identifier (used in slash commands) |
| `description` | ✅ | string | Shown in system prompt and skill listings |
| `license` | ❌ | string | License for the skill content |
| `compatibility` | ❌ | list | Vibe version compatibility |
| `metadata` | ❌ | dict | Custom key-value pairs |
| `user-invocable` | ❌ | bool | If `true`, exposes as `/my-skill` slash command |
| `allowed-tools` | ❌ | list | Tools available when this skill is active |

### Minimal Valid Skill
```markdown
---
name: minimal-skill
description: A minimal working skill
---

This skill does something.
```

---

## Discovery & Enablement

### Where Vibe Looks for Skills

**Order of precedence** (first found wins for same name):

1. **`skill_paths` in `config.toml`** -- explicit paths
2. **Project-level:** `./.vibe/skills/` -- relative to current project
3. **User-level:** `~/.vibe/skills/` -- global skills

```toml
# config.toml - explicit skill paths
[skills]
skill_paths = [
  "/path/to/custom/skills",
  "./project-specific/skills"
]
```

### Enabling/Disabling Skills

```toml
# config.toml
[skills]
# Allow-list (only these skills are loaded)
enabled_skills = ["my-skill", "another-skill"]

# Block-list (disable specific skills)
disabled_skills = ["deprecated-skill"]

# Supports globs and regex
enabled_skills = ["my-*", "re:^audit-"]
```

**Critical:** A skill must be in `enabled_skills` (or not in `disabled_skills`) AND have correct `allowed-tools` to function.

---

## Tool Access

### Builtin Tools Available

| Category | Tools |
|---|---|
| **File I/O** | `read_file`, `write_file`, `edit` |
| **Search** | `grep` |
| **Shell** | `bash`, `bash_stdin`, `bash_log_file`, `bash_output`, `bash_sessions` |
| **Git** | `git_bash`, `git_bash_stdin`, `git_bash_log_file`, `git_bash_output`, `git_bash_sessions` |
| **Web** | `web_fetch`, `web_search` |
| **Code** | `todo`, `task`, `skill` |
| **PowerShell** | `powershell`, `powershell_stdin`, `powershell_log_file`, `powershell_output`, `powershell_sessions` |

### Specifying Allowed Tools

```yaml
# In SKILL.md frontmatter
allowed-tools:
  - read_file
  - write_file
  - grep
  - bash
  - todo
```

**Best practice:** Only include tools your skill actually needs. Fewer tools = smaller system prompt = more tokens for reasoning.

---

## Invocation Patterns

### User-Invocable vs Model-Invocable

```yaml
# Skill can be invoked by user AND model
user-invocable: true

# Skill can ONLY be invoked by model (not via slash command)
user-invocable: false
```

**Important:** `user-invocable: false` does NOT prevent model invocation. The only control is `enabled_skills`/`disabled_skills` in config.

### Slash Command Format

```
/user-invocable-skill-name [arguments]
```

### When Skills Load (Progressive Disclosure)

1. **Enabled but uninvoked:** Only name, description, path in system prompt (cheap)
2. **On first invocation:** Full `SKILL.md` body loaded, enters conversation history **once**
3. **Subsequent turns:** Full content remains in context (resident)

**Implications:**
- ✅ Safe to enable many skills (cheap until invoked)
- ⚠️ Keep skill bodies concise (invocation cost is per-session)
- ⚠️ First invocation adds ~full skill size to context

---

## Content Patterns

### Pattern 1: Instruction Skill

```markdown
---
name: security-audit
description: Security audit checklist and patterns
user-invocable: true
allowed-tools:
  - grep
  - read_file
  - bash
---

# Security Audit Skill

You are a security auditor. When invoked, analyze the current codebase for:

## High Priority Checks
1. **Hardcoded secrets** - grep for API keys, passwords, tokens
2. **Dangerous functions** - eval(), exec(), system(), pickle.loads()

## Usage
Call me when you need to perform a security review.
```

### Pattern 2: Tool Wrapper Skill

```markdown
---
name: git-expert
description: Advanced git operations helper
user-invocable: true
allowed-tools:
  - git_bash
  - bash
---

# Git Expert Skill

You have access to advanced git knowledge and operations.

## Common Operations
- Find recent changes: `git log --oneline --since="1 week ago"`
- Find who introduced a bug: `git blame -L /pattern/,+5 filename.py`
```

### Pattern 3: Agent Delegation Skill

```markdown
---
name: code-reviewer
description: Code review assistant that spawns subagents
user-invocable: true
allowed-tools:
  - task
  - read_file
  - grep
---

# Code Review Skill

When invoked on a PR or code change:

1. Spawn subagents for different review aspects
2. Each gets a scratchpad directory for findings
3. Combine all findings into final report

## Subagent Tasks
- Security: `task: "Perform security review..."`
- Performance: `task: "Analyze performance implications..."`
- Testing: `task: "Review test coverage..."`
```

---

## Testing Workflows

### Test 1: Verify Discovery
```bash
vibe -p "List all enabled skills" --output json | grep -i "my-skill"
```

### Test 2: Verify System Prompt Inclusion
```bash
vibe -p "What skills are available?" --max-turns 1
# Should see your skill in the <skill> tags
```

### Test 3: Invoke via Slash Command
```bash
# In an interactive Vibe session:
/my-skill
```

---

## Common Pitfalls & Fixes

### Pitfall 1: Skill Not Found

| Cause | Fix |
|---|---|
| Wrong directory `.agents/skills/` | Use `.vibe/skills/` |
| Missing frontmatter | Add YAML frontmatter with `name` |
| Not in enabled_skills | Add to config.toml |
| Typo in skill name | Check name field matches directory |

### Pitfall 2: Tools Not Available

| Cause | Fix |
|---|---|
| Tool not in allowed-tools | Add tool to allowed-tools list |
| Wrong tool name (search_replace) | Use `edit` not `search_replace` |
| Tool typo | Verify against builtin list |
| Subagent restriction | Subagents can't use ask_user_question |

### Pitfall 3: Skill Too Large

| Cause | Fix |
|---|---|
| Massive skill body | Split into multiple skills |
| Many large examples | Move examples to separate files |
| Unnecessary content | Keep only essential instructions |

### Pitfall 4: Silent Tool Name Errors

**Remember:** Unrecognized tool names in `enabled_tools` or `allowed-tools` are **silently ignored** -- no error, just removed. This is the most dangerous behavior.

---

## Advanced Patterns

### Skill Chaining
```markdown
Use the `skill` tool to invoke other skills:
```
skill: security-audit
skill: code-quality
```
```

### Restricted Tool Access
```markdown
allowed-tools:
  - read_file
  - grep
  # Intentionally NO bash for safety
```

### Scratchpad-Based Workflow
```markdown
# Spawn researchers
task: "Research topic A. Write findings to /tmp/topic-a.md"
task: "Research topic B. Write findings to /tmp/topic-b.md"

# Read and synthesize results
read_file: /tmp/topic-a.md
read_file: /tmp/topic-b.md
```

---

## Deployment

### Sharing Skills
```bash
# Package
tar czf my-skill.tar.gz -C ~/.vibe/skills my-skill

# Install
cd ~/.vibe/skills
tar xzf /path/to/my-skill.tar.gz
```

### Versioning
```
.vibe/skills/
├── my-skill@1.0/
│   └── SKILL.md
├── my-skill@2.0/
│   └── SKILL.md
└── my-skill -> my-skill@2.0  (symlink)
```

---

## Quick Checklist

Before deploying a skill:

- [ ] `name` field is unique and descriptive
- [ ] `description` clearly explains the skill's purpose
- [ ] `allowed-tools` contains only valid tool names
- [ ] Skill directory is in `.vibe/skills/`
- [ ] Skill is in `enabled_skills` in config.toml
- [ ] `user-invocable` is set appropriately
- [ ] Skill body is concise (under ~1000 tokens recommended)
- [ ] All tool names verified against builtin list
- [ ] Tested with `vibe -p` in programmatic mode
- [ ] Tested slash command invocation (if user-invocable)

---

## Summary Tables

### Internals Quick Reference

| Aspect | Key Insight |
|---|---|
| **Discovery** | `.vibe/skills/` not `.agents/skills/` |
| **Loading** | Progressive -- cheap until invoked |
| **Tools** | Verify names -- silent failures on typos |
| **Invocation** | `user-invocable` only affects slash commands |
| **Context** | Full body loaded once, stays resident |
| **Subagents** | Fresh context, scratchpad_dir, no ask_user_question |

### Workflow Quick Reference

| Task | Command/Pattern |
|---|---|
| Create skill | `mkdir -p ~/.vibe/skills/my-skill && touch SKILL.md` |
| Enable skill | Add to `enabled_skills` in config.toml |
| Test discovery | `vibe -p "List skills" --output json` |
| Invoke skill | `/my-skill` (if user-invocable) |
| Use tools | Verify in `allowed-tools` frontmatter |
| Debug | Check `~/.vibe/config.toml` and skill frontmatter |

---

## Related Resources

- [Mistral Vibe Docs](https://docs.mistral.ai/vibe/)
- [Source Code](https://github.com/mistralai/mistral-vibe)
- [vibe-container repo](https://github.com/berzerk0/vibe-container) -- This repo with additional migration docs
