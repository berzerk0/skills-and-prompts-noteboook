---
name: vibe-internals
description: Complete guide to Mistral Vibe Code internals and skill-building workflows. Includes verified source analysis of tool names, skill system, agents/subagents, hooks, token accounting, CLI flags, plus actionable patterns for building effective skills.
license: MIT
compatibility: [claude, pi, vibe]
metadata:
  verified_against: mistralai/mistral-vibe@a84be0391bf93e93a4025a5e08e8032ecb587123
  verified_date: 2026-08-22
  verification_method: static source analysis
  source: https://github.com/berzerk0/vibe-container/blob/main/docs/vibe-internals-22Aug.md
user-invocable: true
---

# Mistral Vibe Code — Complete Reference & Skill Builder Guide

> **Standing rule:** Trust source over docs. Multiple discrepancies found where official docs describe a simpler or older model. This guide is based on verified source analysis of `mistralai/mistral-vibe@a84be03` (v2.24.3, 2026-08-22).

---

## Table of Contents

### Part A: Verified Internals Reference
- [Tool Names & Translation from Claude Code](#tool-names--translation-from-claude-code)
- [Skills System](#skills-system)
- [Agents and Subagents](#agents-and-subagents)
- [AGENTS.md Behavior](#agentsmd-behavior)
- [Hooks System](#hooks-system)
- [Token Accounting](#token-accounting)
- [CLI Flags](#cli-flags)
- [Known Discrepancies](#known-discrepancies)

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

### Tool Names & Translation from Claude Code

#### Complete Builtin Tool List
`ask_user_question`, `bash`, `bash_log_file`, `bash_output`, `bash_sessions`, `bash_stdin`, `edit`, `exit_plan_mode`, `experimental_bash`, `git_bash`, `git_bash_log_file`, `git_bash_output`, `git_bash_sessions`, `git_bash_stdin`, `grep`, `powershell`, `powershell_log_file`, `powershell_output`, `powershell_sessions`, `powershell_stdin`, `read_file`, `skill`, `task`, `todo`, `web_fetch`, `web_search`, `write_file`

#### Claude Code → Vibe Translation

| Claude Code | Vibe | Note |
|---|---|---|
| `Read` | `read_file` | |
| `Write` | `write_file` | |
| `Edit` | `edit` | **Not `search_replace`** — no such tool exists |
| `Grep` | `grep` | |
| `Glob` | **— none —** | Use `grep` or `bash` with `find`/`ls` |
| `Bash` | `bash` | |
| `Task` | `task` | |
| `AskUserQuestion` | `ask_user_question` | Unavailable to subagents |

#### Critical Warning
Unrecognized tool names in `enabled_tools` are **silently ignored** — no error, just removed from available tools. A typo or stale Claude Code name quietly disables the capability.

**Action:** Always verify tool names exist in the builtin list above or your custom tool paths.

---

### Skills System

#### Format
- A skill is a **directory** containing a `SKILL.md` file
- `SKILL.md` must have YAML frontmatter
- Parsed fields: `name`, `description`, `license`, `compatibility`, `metadata` (dict), `allowed-tools` (list), `user-invocable` (bool)

#### Discovery Order
1. `skill_paths` in `config.toml`
2. Project-level `./.vibe/skills/`
3. User-level `~/.vibe/skills/`

**Correction:** Docs claim `./.agents/skills/` is valid — it is **not** in source. Use `.vibe/skills/`.

#### Context Residency (Progressive Disclosure)
- **Enabled but uninvoked:** Only name, description, and path appear in system prompt (cheap)
- **On invocation:** Full `SKILL.md` body loaded via the `skill` tool and enters conversation history **once**
- **Cost model:** Enabling many skills is cheap; invoking a bloated skill is expensive (per-session cost)

#### Invocation Control
- `user-invocable: true` → exposes as slash command
- `user-invocable: false` → **still invocable by model** (no `disable-model-invocation` equivalent)
- Only global levers: `enabled_skills` / `disabled_skills` in `config.toml` (supports exact names, globs, regex with `re:` prefix)

#### No Plugin System
Skills are directories on disk. No marketplace, no `/plugin install`. Installation: clone → copy to `.vibe/skills/` → rewrite `allowed-tools` → remove harness-specific parts.

---

### Agents and Subagents

#### Definition
- `.toml` files in `~/.vibe/agents/` (user) or `./.vibe/agents/` (project)
- Every agent declares `agent_type`:
  - `"agent"` — user-facing, selectable via `--agent <name>` or Shift+Tab
  - `"subagent"` — delegation-only, spawned via `task` tool

**Constraint:** Subagents cannot be selected with `--agent`. Error: *"Only agents of type 'agent' can be selected with --agent"*

#### Key Configuration Options

| Key | Purpose |
|---|---|
| `active_model` | **Primary cost lever** — per-agent model routing |
| `allowed_models` | Restrict models this agent may use |
| `providers` / `models` | Provider and model config overrides |
| `compaction_model` | Model for context compaction (separate from `active_model`) |
| `bypass_tool_permissions` | Skip permission prompts |
| `enabled_tools` / `disabled_tools` | Tool scoping |
| `tools` | Per-tool `permission`, `allowlist`, `denylist` |
| `system_prompt_id` | Points to file in `~/.vibe/prompts/` |
| `safety` | **Cosmetic only** — sets input border color, enforces nothing |

#### Subagent Isolation
- **Fresh context:** New `AgentLoop` with copied config, no parent history
- **Own resources:** Own `AGENTS.md` load, `AgentLoop`, `session_logger`, stats
- **Skills:** From own (inherited-then-overridden) config

#### Scratchpad Directory
Subagents receive a `scratchpad_dir` and are told:
> "You can read and write files here without permission prompts."

This is **first-class support** for the write-findings-to-file, return-path pattern. Build handoff conventions on this.

#### Return Channel
`TaskResult` carries only:
- `response: str` — text only
- `turns_used: int`
- `completed: bool`

No structured payload, no file handles. Paths must be parsed from text.

#### Hard Constraints
- **Subagents cannot ask user questions** — no access to `ask_user_question`
- **Concurrency is model-initiated only** — cannot force parallel dispatch via CLI

---

### AGENTS.md Behavior

- **Not limited to two files** — loads user-level file plus **one per project root**, walking up to trust root
- **Auto-discovery:** Additional `AGENTS.md` files found for lazy injection when reading files below open project roots
- **Residency:** Loaded at session start via `load_project_docs()`, resident every turn
- **Cost:** Always-on — budget every line

---

### Hooks System

**Vibe has hooks** (often assumed absent — this assumption is wrong).

#### Events
- `PRE_TOOL` ≈ Claude Code's `PreToolUse`
- `POST_TOOL`
- `POST_AGENT` ≈ Claude Code's `Stop`

#### Configuration
- `hooks.toml` with a `hooks` list
- Fields: `name`, `type`, `command`, `match`, `timeout`, `strict`, `description`
- Location: `.vibe/hooks.toml` in project roots, and `~/.vibe/hooks.toml`

#### Hook Payloads

| Event | Fields |
|---|---|
| `PostAgentInvocation` | `session_id`, `transcript_path`, `cwd`, `parent_session_id` |
| `PreToolInvocation` | above + `tool_name`, `tool_call_id`, `tool_input` |
| `PostToolInvocation` | above + `tool_status`, `tool_output`, `tool_output_text`, `tool_error`, `duration_ms` |

**Note:** No token counts passed to hooks. But `POST_AGENT` carries `transcript_path` — route to usage data.

---

### Token Accounting

#### Where Counts Live
```
TokenUsage:          input_tokens, output_tokens, total_tokens
AgentStatsSnapshot:  session_prompt_tokens, session_completion_tokens, session_cached_tokens
                     last_turn_prompt_tokens, last_turn_completion_tokens, last_turn_cached_tokens
                     computed: session_total_llm_tokens(), last_turn_total_tokens(), session_cost()
PublicSession:       token_usage: TokenUsage | None
```

Tracked **per subagent** — each has its own `AgentLoop` and stats.

#### Programmatic Output
`--output json` emits:
```json
{ "history": [ /* PublicHistoryEntry objects */ ] }
```
**None of the history entries carry token counts.** `token_usage` lives on `PublicSession`, which is *not* in programmatic output.

#### Measurement Options
- `--output json` → **no usage data** (dead end)
- Hooks → **no token counts** (dead end)
- No `/cost` command exists
- **Viable route:** `POST_AGENT` hook receives `transcript_path` — parse the transcript

*Unverified at runtime.* Transcript format never inspected. Confirm before building.

---

### CLI Flags

| Flag | Behavior |
|---|---|
| `--agent NAME` | Select user-facing agent (subagents rejected) |
| `--prompt` / `-p` | Programmatic mode |
| `--output json` | History only, no usage |
| `--max-turns N` | Turn cap |
| `--max-tokens`, `--max-price` | Budget caps |
| `--worktree NAME` | Create/reuse git worktree under `$VIBE_HOME/worktrees` |
| `--add-dir PATH` | Trust path, add to `workspace_roots` for config discovery |

#### Programmatic Mode Default
**Docs are wrong:** Docs claim fallback to `auto-approve`. Source shows fallback to `default_agent` config value, whose default is **`accept-edits`**.

`accept-edits` auto-approves file edits but still prompts for shell commands. **Recommendation:** Pass `--agent` explicitly when scripting.

---

### Known Discrepancies (Docs vs Source)

| Topic | Docs Say | Source Says |
|---|---|---|
| Skill discovery path | `./.agents/skills/` is valid | Only `./.vibe/skills/` |
| AGENTS.md count | At most two files | One per project root, plus user-level |
| Programmatic default agent | `auto-approve` | `default_agent`, default `accept-edits` |
| Tool name for editing | (example uses `read_file`) | `edit`, and no `search_replace` anywhere |

**Pattern:** Docs lag the code and describe a simpler model. **Check source for anything load-bearing.**

---

---

## Part B: Skill Building Workflows

---

### Quick Start: Create a Skill

```bash
# 1. Create skill directory structure
mkdir -p ~/.vibe/skills/my-skill

# 2. Create SKILL.md with frontmatter
cat > ~/.vibe/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: What this skill does
license: MIT
compatibility: [claude, pi, vibe]
user-invocable: true
---

# My Skill Content

This skill helps with...
EOF

# 3. Enable the skill (add to config.toml)
echo 'enabled_skills = ["my-skill"]' >> ~/.vibe/config.toml
```

---

### Skill Structure

#### Required Files
```
.vibe/skills/my-skill/
├── SKILL.md          # Main file with YAML frontmatter + content
└── (optional)       # Any supporting files referenced in content
```

#### YAML Frontmatter Fields

| Field | Required | Type | Purpose |
|---|---|---|---|
| `name` | ✅ | string | Unique identifier (used in slash commands) |
| `description` | ✅ | string | Shown in system prompt and skill listings |
| `license` | ❌ | string | License for the skill content |
| `compatibility` | ❌ | list | Vibe version compatibility |
| `metadata` | ❌ | dict | Custom key-value pairs |
| `user-invocable` | ❌ | bool | If `true`, exposes as `/my-skill` slash command |
| `allowed-tools` | ❌ | list | Tools available when this skill is active |

#### Minimal Valid Skill
```markdown
---
name: minimal-skill
description: A minimal working skill
---

This skill does something.
```

---

### Discovery & Enablement

#### Where Vibe Looks for Skills

**Order of precedence** (first found wins for same name):

1. **`skill_paths` in `config.toml`** — explicit paths
2. **Project-level:** `./.vibe/skills/` — relative to current project
3. **User-level:** `~/.vibe/skills/` — global skills

```toml
# config.toml - explicit skill paths
[skills]
skill_paths = [
  "/path/to/custom/skills",
  "./project-specific/skills"
]
```

#### Enabling/Disabling Skills

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

### Tool Access

#### Builtin Tools Available

| Category | Tools |
|---|---|
| **File I/O** | `read_file`, `write_file`, `edit` |
| **Search** | `grep` |
| **Shell** | `bash`, `bash_stdin`, `bash_log_file`, `bash_output`, `bash_sessions` |
| **Git** | `git_bash`, `git_bash_stdin`, `git_bash_log_file`, `git_bash_output`, `git_bash_sessions` |
| **Web** | `web_fetch`, `web_search` |
| **Code** | `todo`, `task`, `skill` |
| **PowerShell** | `powershell`, `powershell_stdin`, `powershell_log_file`, `powershell_output`, `powershell_sessions` |

#### Specifying Allowed Tools

```yaml
# In SKILL.md frontmatter
```

**Best practice:** Only include tools your skill actually needs. Fewer tools = smaller system prompt = more tokens for reasoning.

---

### Invocation Patterns

#### User-Invocable vs Model-Invocable

```yaml
# Skill can be invoked by user AND model
user-invocable: true

# Skill can ONLY be invoked by model (not via slash command)
user-invocable: false
```

**Important:** `user-invocable: false` does NOT prevent model invocation. The only control is `enabled_skills`/`disabled_skills` in config.

#### Slash Command Format

```
/user-invocable-skill-name [arguments]
```

#### When Skills Load (Progressive Disclosure)

1. **Enabled but uninvoked:** Only name, description, path in system prompt (cheap)
2. **On first invocation:** Full `SKILL.md` body loaded, enters conversation history **once**
3. **Subsequent turns:** Full content remains in context (resident)

**Implications:**
- ✅ Safe to enable many skills (cheap until invoked)
- ⚠️ Keep skill bodies concise (invocation cost is per-session)
- ⚠️ First invocation adds ~full skill size to context

---

### Content Patterns

#### Pattern 1: Instruction Skill

```markdown
---
name: security-audit
description: Security audit checklist and patterns
user-invocable: true
---

# Security Audit Skill

You are a security auditor. When invoked, analyze the current codebase for:

## High Priority Checks
1. **Hardcoded secrets** - grep for API keys, passwords, tokens
2. **Dangerous functions** - eval(), exec(), system(), pickle.loads()

## Usage
Call me when you need to perform a security review.
```

#### Pattern 2: Tool Wrapper Skill

```markdown
---
name: git-expert
description: Advanced git operations helper
user-invocable: true
---

# Git Expert Skill

You have access to advanced git knowledge and operations.

## Common Operations
- Find recent changes: `git log --oneline --since="1 week ago"`
- Find who introduced a bug: `git blame -L /pattern/,+5 filename.py`
```

#### Pattern 3: Agent Delegation Skill

```markdown
---
name: code-reviewer
description: Code review assistant that spawns subagents
user-invocable: true
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

### Testing Workflows

#### Test 1: Verify Discovery
```bash
vibe -p "List all enabled skills" --output json | grep -i "my-skill"
```

#### Test 2: Verify System Prompt Inclusion
```bash
vibe -p "What skills are available?" --max-turns 1
# Should see your skill in the <skill> tags
```

#### Test 3: Invoke via Slash Command
```bash
# In an interactive Vibe session:
/my-skill
```

---

### Common Pitfalls & Fixes

#### Pitfall 1: Skill Not Found

| Cause | Fix |
|---|---|
| Wrong directory `.agents/skills/` | Use `.vibe/skills/` |
| Missing frontmatter | Add YAML frontmatter with `name` |
| Not in enabled_skills | Add to config.toml |
| Typo in skill name | Check name field matches directory |

#### Pitfall 2: Tools Not Available

| Cause | Fix |
|---|---|
| Tool not in allowed-tools | Add tool to allowed-tools list |
| Wrong tool name (search_replace) | Use `edit` not `search_replace` |
| Tool typo | Verify against builtin list |
| Subagent restriction | Subagents can't use ask_user_question |

#### Pitfall 3: Skill Too Large

| Cause | Fix |
|---|---|
| Massive skill body | Split into multiple skills |
| Many large examples | Move examples to separate files |
| Unnecessary content | Keep only essential instructions |

#### Pitfall 4: Silent Tool Name Errors

**Remember:** Unrecognized tool names in `enabled_tools` or `allowed-tools` are **silently ignored** — no error, just removed. This is the most dangerous behavior.

---

### Advanced Patterns

#### Skill Chaining
```markdown
Use the `skill` tool to invoke other skills:
```
skill: security-audit
skill: code-quality
```
```

#### Restricted Tool Access
```markdown
  # Intentionally NO bash for safety
```

#### Scratchpad-Based Workflow
```markdown
# Spawn researchers
task: "Research topic A. Write findings to /tmp/topic-a.md"
task: "Research topic B. Write findings to /tmp/topic-b.md"

# Read and synthesize results
read_file: /tmp/topic-a.md
read_file: /tmp/topic-b.md
```

---

### Deployment

#### Sharing Skills
```bash
# Package
tar czf my-skill.tar.gz -C ~/.vibe/skills my-skill

# Install
cd ~/.vibe/skills
tar xzf /path/to/my-skill.tar.gz
```

#### Versioning
```
.vibe/skills/
├── my-skill@1.0/
│   └── SKILL.md
├── my-skill@2.0/
│   └── SKILL.md
└── my-skill -> my-skill@2.0  (symlink)
```

---

### Quick Checklist

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
| **Loading** | Progressive — cheap until invoked |
| **Tools** | Verify names — silent failures on typos |
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
- [vibe-container repo](https://github.com/berzerk0/vibe-container) — This repo with additional migration docs
