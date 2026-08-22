# Mistral Vibe Code — Verified Reference

**Source:** `mistralai/mistral-vibe` @ `a84be0391bf93e93a4025a5e08e8032ecb587123` (2026-08-20)  
**Version:** pyproject.toml version **2.24.3**  
**Verification Date:** 2026-08-22  
**Verification Method:** Static source analysis (T2). Runtime testing was blocked by MCP/sentry import errors in sandbox.  
**Author:** Vibe Code (verified from own source)

> **Standing Rule:** **Trust source over docs.** Three separate claims taken from official docs disagreed with the code, always in the same direction — docs describe something simpler or older. Where this file and `docs.mistral.ai` conflict, **the code was checked more recently**.

---

## 📋 Table of Contents

1. [Tool Names](#1-tool-names)
2. [Skills](#2-skills)
3. [Agents and Subagents](#3-agents-and-subagents)
4. [AGENTS.md](#4-agentsmd)
5. [Hooks](#5-hooks)
6. [Token Accounting](#6-token-accounting)
7. [CLI Flags](#7-cli-flags)
8. [Known Unverified Items](#8-known-unverified-items)
9. [Docs vs Source Discrepancies](#9-docs-vs-source-discrepancies)

---

## 1. Tool Names

### Builtin Tools List

**Source:** `vibe/core/tools/builtins/*.py`  
**Discovery:** `ToolManager._iter_tool_classes_with_origin()` in `vibe/core/tools/manager.py:165-178`

Complete list of builtin tools (exhaustive for builtins only; MCP servers and user tools add names at runtime):

- `ask_user_question`
- `bash`
- `bash_log_file`
- `bash_output`
- `bash_sessions`
- `bash_stdin`
- `edit`
- `exit_plan_mode`
- `experimental_bash`
- `git_bash`
- `git_bash_log_file`
- `git_bash_output`
- `git_bash_sessions`
- `git_bash_stdin`
- `grep`
- `powershell`
- `powershell_log_file`
- `powershell_output`
- `powershell_sessions`
- `powershell_stdin`
- `read_file`
- `skill`
- `task`
- `todo`
- `web_fetch`
- `web_search`
- `write_file`

**Tool Name Derivation:** Class name converted from PascalCase to snake_case via `BaseTool.get_name()` (`vibe/core/tools/base.py:424-426`)

### Translation from Claude Code

| Claude Code | Vibe Code | Note |
|-------------|-----------|------|
| `Read` | `read_file` | |
| `Write` | `write_file` | |
| `Edit` | `edit` | **Not `search_replace`** — no such tool exists |
| `Grep` | `grep` | |
| `Glob` | **— none —** | No glob/list tool. Use `grep`, or `bash` running `find`/`ls` |
| `Bash` | `bash` | |
| `Task` | `task` | |
| `AskUserQuestion` | `ask_user_question` | **Unavailable to subagents** |

### ⚠️ Critical Failure Mode

**Unrecognized tool names in `enabled_tools` are SILENTLY IGNORED** — no match means not included in `available_tools` (`vibe/core/tools/manager.py:563-568`).

**A typo or a stale Claude Code name does not error; it quietly removes the capability.**

**Corollary:** A subagent whose `enabled_tools` omits `skill` **cannot load skills at all**.

---

## 2. Skills

### Format and Parsing

**Source:** `vibe/core/skills/manager.py:129-131`, `vibe/core/skills/parser.py`

A skill is a directory containing `SKILL.md` with YAML frontmatter.

**Fields Actually Parsed** (`vibe/core/skills/models.py:38-68`):
- `name` (required)
- `description` (required)
- `license` (optional)
- `compatibility` (optional, list)
- `metadata` (optional, dict)
- `allowed-tools` (optional, list) ← **Vibe-specific, NOT portable**
- `user-invocable` (optional, bool)

### Discovery Order

**Source:** `vibe/core/skills/manager.py:72-83`

1. `skill_paths` in `config.toml`
2. Project-level `./.vibe/skills/`
3. User-level `~/.vibe/skills/`

> **⚠️ Docs are WRONG here.** `docs.mistral.ai` lists `./.agents/skills/` as a discovery path. **It is NOT one in source.** Use `.vibe/skills/`.

### Context Residency — Progressive Disclosure Holds

**Verified twice.** Source: `vibe/core/system_prompt.py:262-290`, `345-380`

**For an enabled but uninvoked skill**, the system prompt contains only:

```xml
<skill>
  <name>...</name>
  <description>...</description>
  <path>...</path>
</skill>
```

**The full `SKILL.md` body is NOT in the system prompt.** It is loaded on demand by the **`skill` tool** (`vibe/core/tools/builtins/skill.py:120-158`), which returns `skill_info.prompt` as a **tool result**.

**Cost Model:**
- **Per enabled skill, per turn:** name + description + path. **Cheap.**
- **On invocation:** the full body enters conversation history **once**, then stays resident for the remainder of the session.
- **Conclusion:** Enabling many skills is cheap; invoking a bloated skill is expensive, and the cost is **per-session not per-turn**.

> `user-invocable` does **NOT** change residency. The system prompt **always** lists all enabled skills.

### Invocation Control

**Source:** `vibe/core/skills/models.py:62-65`, `manager.py:179-188`

`user-invocable: true` exposes the skill as a **slash command** (`/<skill-name>`).

It does **NOT** prevent model invocation. There is **no per-skill equivalent of Claude Code's `disable-model-invocation`**.

**The only lever is `enabled_skills` / `disabled_skills` in `config.toml`** — global, user-set, all-or-nothing per skill.

- Supports exact names, globs, and regex with an `re:` prefix (`manager.py:54-63`, `vibe_schema.py:395-405`)
- A non-empty `enabled_skills` acts as an **allow-list**

### No Plugin System

**Source:** `vibe/core/skills/manager.py`

Skills are **directories on disk**. No marketplace, no `/plugin install`.

A separate opt-in registry exists but is **not a plugin system**.

**Installation is therefore:**
1. Clone or download
2. Copy the skill directory into `~/.vibe/skills/` or `./.vibe/skills/`
3. Rewrite `allowed-tools` to use Vibe tool names
4. Adjust or remove anything harness-specific

---

## 3. Agents and Subagents

### Definition

**Source:** `vibe/core/config/harness_files/_harness_manager.py:187-189`

`.toml` files in:
- `~/.vibe/agents/` (user)
- `./.vibe/agents/` (project)

Every agent declares `agent_type` (`vibe/agents.py:1-17`):
- `"agent"` — user-facing, selectable via `--agent <name>` or Shift+Tab
- `"subagent"` — delegation-only, spawned by the model through the `task` tool

**Critical:** Subagents **cannot** be selected with `--agent`. Attempting it errors: *"Only agents of type 'agent' can be selected with --agent"* (`vibe/core/agents/manager.py:43-48`).

Builtin subagent `explore` is **read-only** (`vibe/core/agents/models.py:85-91`).

### Recognized `.toml` Keys

**Source:** `vibe/core/agents/models.py:26-40`, `vibe/core/config/vibe_schema.py:367-405`

| Key | Purpose |
|-----|---------|
| `active_model` | **Per-agent model routing.** The primary cost lever. |
| `allowed_models` | Restrict which models this agent may use |
| `providers` / `models` | Provider and model config overrides |
| `compaction_model` | Model used for context compaction — separate from `active_model` |
| `bypass_tool_permissions` | Skip permission prompts |
| `enabled_tools` / `disabled_tools` | Tool scoping |
| `tools` | Dict with per-tool `permission`, `allowlist`, `denylist` |
| `system_prompt_id` | Points at a file in `~/.vibe/prompts/` |
| `safety` | **Cosmetic only** — sets input border colour, enforces nothing (`vibe/agents.py:7-14`) |

### Subagent Isolation — Confirmed Clean

**Source:** `vibe/app_server/_runtime.py:509-540`, `vibe/app_server/_sessions.py:291-345`

- **Fresh context.** `create_child()` builds a new `AgentLoop` with a copied config orchestrator. No parent conversation history is passed.
- The subagent's entire first message is `prepare_subagent_prompt(args.task, ctx)` and nothing else.
- Own `AGENTS.md` load, own `AgentLoop`, own `session_logger`, own stats.
- Skills visible are those from its own (inherited-then-overridden) config.

**✅ Subagents are fully isolated.**

### `scratchpad_dir` — Native File Handoff

**Source:** `vibe/core/subagents.py:76-84`

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

Subagents are handed a **scratchpad directory** and told they may read and write there **without permission prompts**.

**This is first-class support for the write-findings-to-a-file, return-a-path pattern.** Build handoff conventions on `scratchpad_dir` rather than inventing one.

### Return Channel

**Source:** `vibe/core/subagents.py:18-26`, `vibe/core/tools/builtins/task.py:30-118`

`TaskResult` carries only:
- `response: str`
- `turns_used: int`
- `completed: bool`

**Text only.** No structured payload, no file handles. A subagent returning a path returns it as a string the parent must parse.

### Hard Constraints

- **❌ Subagents cannot ask the user questions.** No access to `ask_user_question` (`task.py:111-115`). Any clarification must happen in the parent agent. A subagent that hits ambiguity will guess or return partial results.
- **✅ Concurrency is real** but **model-initiated only**; a user cannot directly force parallel dispatch (`task.py:80-118`).

---

## 4. AGENTS.md

**Source:** `vibe/core/config/harness_files/_harness_manager.py:189-192`, `210-234`, `237-256`

- **NOT limited to two files.** Loads the user-level file plus **one per project root**, walking up to the trust root.
- Additional `AGENTS.md` files are **auto-discovered** for lazy injection when reading files below open project roots.
- Loaded at session start via `load_project_docs()` and **resident every turn**. **Always-on cost** — budget every line.

---

## 5. Hooks

**Vibe HAS hooks.** (Assumed absent in early planning; that was wrong.)

**Source:** `vibe/core/hooks/models.py`, `vibe/core/hooks/config.py`, `_harness_manager.py:109-114`

- **Events:** `PRE_TOOL`, `POST_TOOL`, `POST_AGENT`
- **Config:** `hooks.toml` — a `hooks` list with fields:
  - `name`
  - `type` (PRE_TOOL, POST_TOOL, POST_AGENT)
  - `command`
  - `match`
  - `timeout`
  - `strict`
  - `description`
- **Location:** `.vibe/hooks.toml` in project roots, and `~/.vibe/hooks.toml`
- **Rough Claude Code mapping:**
  - `PRE_TOOL` ≈ `PreToolUse`
  - `POST_AGENT` ≈ `Stop`

### Hook Payloads

**Source:** `vibe/core/hooks/models.py:85-165`

| Event | Fields |
|-------|--------|
| `PostAgentInvocation` | `session_id`, `transcript_path`, `cwd`, `parent_session_id` |
| `PreToolInvocation` | above + `tool_name`, `tool_call_id`, `tool_input` |
| `PostToolInvocation` | above + `tool_status`, `tool_output`, `tool_output_text`, `tool_error`, `duration_ms` |

**⚠️ No token counts are passed to hooks.**

But `POST_AGENT` carries `transcript_path` — which is the route to usage data.

---

## 6. Token Accounting

### Where Counts Live

**Source:** `vibe/app_server/models.py:293-343`, `870-882`

```python
# TokenUsage model
TokenUsage:          input_tokens, output_tokens, total_tokens

# AgentStatsSnapshot model  
AgentStatsSnapshot:  steps
                     session_prompt_tokens, session_completion_tokens, session_cached_tokens
                     last_turn_prompt_tokens, last_turn_completion_tokens, last_turn_cached_tokens
                     computed: session_total_llm_tokens(), last_turn_total_tokens(), session_cost()

# PublicSession model
PublicSession:       token_usage: TokenUsage | None
```

**Tracked per subagent** — each has its own `AgentLoop` and stats.

### What `--output json` Actually Emits

**Source:** `vibe/cli/programmatic.py:37-102`

The envelope is:
```json
{ "history": [ /* PublicHistoryEntry objects */ ] }
```
or, with teleport, `{"history": [...], "teleportUrl": "..."}`

`PublicHistoryEntry` is a discriminated union of `message`, `reasoning`, `effect`, `callback`, `checkpoint`, `notice`.

**⚠️ NONE of them carry token counts.** `token_usage` lives on `PublicSession`, which is *NOT* in the programmatic output.

### Consequences for Measurement

- `--output json` → **NO usage data.** Dead end.
- Hooks → **NO token counts.** Dead end.
- No `/cost` command exists.
- **✅ Viable route:** `POST_AGENT` hook receives `transcript_path`. Parse the transcript. This is the same technique Anthropic's `session-report` uses against Claude Code JSONL — only the file format differs.

> *Unverified at runtime.* Transcript format and contents were never inspected. Confirm before building.

---

## 7. CLI Flags

**Source:** `vibe/cli/cli.py:174`, `vibe/cli/entrypoint.py:65-69`, `102-107`, `130-154`

| Flag | Behaviour |
|------|------------|
| `--agent NAME` | Select a user-facing agent. **Subagents rejected.** |
| `--prompt` / `-p` | Programmatic mode |
| `--output json` | History only, **NO usage data** |
| `--max-turns N` | Turn cap |
| `--max-tokens`, `--max-price` | Budget caps |
| `--worktree NAME` | Create or reuse a git worktree under `$VIBE_HOME/worktrees` |
| `--add-dir PATH` | Implicitly trusts the path; adds it to `workspace_roots` for config discovery (pulls its `AGENTS.md` and `.vibe/`)

### ⚠️ Programmatic Mode Default Agent

**Docs are WRONG here too.** `docs.mistral.ai` says programmatic mode falls back to `auto-approve`.

**Source shows it falls back to the `default_agent` config value, whose default is `accept-edits`** (`vibe/cli/cli.py:174`, `entrypoint.py:105-124`).

Less dangerous than the docs imply — `accept-edits` auto-approves file edits but still prompts for shell commands. **Still pass `--agent` explicitly when scripting.**

---

## 8. Known Unverified Items

| Item | Status | How to Settle |
|------|--------|---------------|
| `--output json` real envelope | Source only; sandbox runtime broken | `vibe -p "say hi" --output json --max-turns 1 --agent plan` |
| Transcript file format | Never inspected | Trigger a `POST_AGENT` hook, read `transcript_path` |
| Subagent tool availability column | Partly inferred, not fully cited | Read `task.py` tool-filtering logic directly |
| User-forced parallel dispatch | Model-initiated confirmed; forcing untested | Have an agent call `task` twice in one response |
| Runtime-added tool names | Builtins exhaustive; MCP/user tools unknown | Inspect `search_paths` on a live session |

---

## 9. Docs vs Source Discrepancies Found

| Topic | Docs Say | Source Says |
|-------|----------|-------------|
| Skill discovery path | `./.agents/skills/` is valid | **Only `./.vibe/skills/`** |
| AGENTS.md count | At most two files | **One per project root, plus user-level** |
| Programmatic default agent | `auto-approve` | `default_agent`, **default `accept-edits`** |
| Tool name for editing | (example uses `read_file`, correct) | `edit`, and **no `search_replace` anywhere** |

**Pattern:** Docs lag the code and describe a simpler model. **Check source for anything load-bearing.**

---

## 📚 References

- **Source Repository:** [mistralai/mistral-vibe](https://github.com/mistralai/mistral-vibe)
- **Official Docs:** [docs.mistral.ai](https://docs.mistral.ai)
- **Verification Commit:** `a84be0391bf93e93a4025a5e08e8032ecb587123`
- **Version:** 2.24.3

---

## 📝 Changelog

| Date | Change | Author |
|------|--------|--------|
| 2026-08-22 | Initial verified reference based on source code analysis | Vibe Code |
