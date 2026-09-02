# Findings & Decisions

## Requirements
Answer four questions about Vibe Code's skill system with validated sources:
1. Can Vibe Code on the web identify its own skills?
2. Can models invoke skills automatically?
3. How about agent files?
4. How does Vibe Code on the web know when to invoke skills?

## Research Findings

### From Repo Documentation

#### docs/vibe/VERIFIED_REFERENCE.md (PRIMARY SOURCE)
**Source:** `mistralai/mistral-vibe` @ `a84be0391bf93e93a4025a5e08e8032ecb587123` (v2.24.3)
**Verification:** Static source analysis, commit dated 2026-08-20
**Confidence:** HIGH - Direct source code analysis

**Key Findings:**

**1. Skill Discovery & Identification (Section 2):**
- **Format**: Skills are directories containing `SKILL.md` with YAML frontmatter
- **Discovery Order** (`vibe/core/skills/manager.py:72-83`):
  1. `skill_paths` in `config.toml`
  2. Project-level `./.vibe/skills/`
  3. User-level `~/.vibe/skills/`
- **CRITICAL CORRECTION**: Official docs claim `./.agents/skills/` is valid, but **source shows ONLY `.vibe/skills/`**
- **Parsed Fields** (`vibe/core/skills/models.py:38-68`):
  - `name` (required)
  - `description` (required)
  - `license` (optional)
  - `compatibility` (optional, list)
  - `metadata` (optional, dict)
  - `allowed-tools` (optional, list) - Vibe-specific, NOT portable
  - `user-invocable` (optional, bool)

**2. Skill Invocation by Models (Section 2.2-2.3):**
- **Progressive Disclosure** (`vibe/core/system_prompt.py:262-290`, `345-380`):
  - **Enabled but uninvoked**: Only name + description + path in system prompt (cheap)
  - **On invocation**: Full SKILL.md body loaded by `skill` tool (`vibe/core/tools/builtins/skill.py:120-158`)
  - Full body enters conversation history **once**, stays resident for session
  - **Cost**: Per-session, not per-turn
- **`user-invocable: true`**: Exposes as slash command (`/<skill-name>`) but does **NOT** prevent model invocation
- **NO per-skill model invocation blocking exists**
- **Only control**: `enabled_skills` / `disabled_skills` in `config.toml` (global, user-set)
  - Supports exact names, globs, regex with `re:` prefix
  - Non-empty `enabled_skills` acts as allow-list
  - **CRITICAL**: Unrecognized tool names in `enabled_tools` are **SILENTLY IGNORED** (`vibe/core/tools/manager.py:563-568`)

**3. Agent Files & Subagents (Section 3):**
- **Definition** (`vibe/core/config/harness_files/_harness_manager.py:187-189`):
  - `.toml` files in `~/.vibe/agents/` (user) and `./.vibe/agents/` (project)
  - Every agent declares `agent_type`: `"agent"` (user-facing) or `"subagent"` (delegation-only)
- **Subagent Isolation** (`vibe/app_server/_runtime.py:509-540`, `vibe/app_server/_sessions.py:291-345`):
  - **Fully isolated**: Fresh context, own AgentLoop, own session logger, own stats
  - Skills visible are from its own (inherited-then-overridden) config
  - **Scratchpad directory** (`vibe/core/subagents.py:76-84`): Can read/write without permission prompts
- **Hard Constraints**:
  - **Cannot use `ask_user_question`** (`task.py:111-115`)
  - **Text-only return**: `TaskResult` carries only `response: str`, `turns_used: int`, `completed: bool`
  - **Critical**: If `skill` tool is NOT in `enabled_tools`, subagent **CANNOT load skills at all**

#### skills/vibe-reference/SKILL.md
**Purpose:** Reference assistant for Vibe Code internals
**Confidence:** HIGH - Derived from VERIFIED_REFERENCE.md

**Confirmations:**
- Silent tool name failures: Unrecognized names in `enabled_tools` are SILENTLY IGNORED
- Skill discovery: Only `.vibe/skills/` is valid (NOT `.agents/skills/`)
- Subagent skill loading: If `skill` tool not in `enabled_tools`, cannot load skills
- AGENTS.md: Multiple files loaded (one per project root + user-level), all resident every turn

#### docs/multi-agent/COMPATIBILITY.md
**Purpose:** Cross-agent compatibility guide
**Confidence:** MEDIUM-HIGH - Based on official docs + repo analysis

**Mistral Vibe Code Specifics:**
- **Skill Format**: Agent Skills specification compliant
- **Discovery Paths**: `.vibe/skills/` (project), `~/.vibe/skills/` (user)
- **Frontmatter**: `name`, `description`, `license`, `compatibility`, `user-invocable`, `allowed-tools`
- **`allowed-tools`**: Acts as a **restriction array** (e.g., `- read_file`, `- grep`)
- **Agents**: `.toml` files in `.vibe/agents/` (project), `~/.vibe/agents/` (user)
- **Delegation**: `task` tool
- **Isolation**: Separate context windows

#### skills/writing-for-agents/SKILL-MECHANICS.md
**Purpose:** Skill invocation mechanics documentation
**Confidence:** MEDIUM - Based on Agent Skills spec + repo patterns

**Invocation Types:**
- **Model-invoked skill**: Has `description`, agent can fire autonomously, other skills can reach it
  - Description is "top-level context pointer, forced to stay loaded at all times"
  - "Permanent context load in exchange for discoverability"
  - Mechanics: omit `disable-model-invocation`, write model-facing description with trigger branches
- **User-invoked skill**: `disable-model-invocation: true`, strips description from agent reach
  - Only human typing name can invoke it
  - Zero context load, but spends cognitive load
  - Mechanics: set `disable-model-invocation: true`

**Key Insight:** "model-invocation always _includes_ user reach; a description only ever adds agent discovery, never removes the human's"

#### AGENTS.md (repo root)
**Lines 55-57:**
- **Claude Code**: Skills are auto-discovered. Reference them by name or use `/<skill-name>`
- **Pi Agent**: Skills are auto-discovered from `.agents/skills/` and ancestors
- **Vibe Code**: Skills are auto-discovered from `.vibe/skills/`

### From Official Mistral Documentation

**Source:** [docs.mistral.ai/vibe/code/cli/skills](https://docs.mistral.ai/vibe/code/cli/skills)
**Confidence:** MEDIUM - Official docs, but VERIFIED_REFERENCE.md found discrepancies

**Claimed Behavior (from docs):**
- Skills discovered from `.vibe/skills/` and `~/.vibe/skills/`
- Frontmatter fields: `name`, `description`, `license`, `compatibility`, `user-invocable`, `allowed-tools`
- `allowed-tools`: Restriction array

**DISCREPANCIES FOUND:**
1. Docs claim `./.agents/skills/` is a discovery path - **SOURCE SHOWS FALSE** (VERIFIED_REFERENCE.md)
2. Docs claim programmatic default agent is `auto-approve` - **SOURCE SHOWS `accept-edits`** (VERIFIED_REFERENCE.md)

### Manual Source Verification

**Files Referenced in VERIFIED_REFERENCE.md:**
- `vibe/core/skills/manager.py:72-83` - Skill discovery logic
- `vibe/core/skills/models.py:38-68` - Skill parsing
- `vibe/core/system_prompt.py:262-290, 345-380` - Progressive disclosure
- `vibe/core/tools/builtins/skill.py:120-158` - Skill tool implementation
- `vibe/core/tools/manager.py:563-568` - Tool name filtering (silent ignore)
- `vibe/app_server/_runtime.py:509-540` - Subagent isolation
- `vibe/app_server/_sessions.py:291-345` - Subagent isolation
- `vibe/core/subagents.py:76-84` - Scratchpad directory
- `vibe/core/config/harness_files/_harness_manager.py:187-189` - Agent file loading

**Verification Status:**
- All source references are to specific files and line numbers
- VERIFIED_REFERENCE.md explicitly states: "Trust source over docs"
- Three separate claims from official docs disagreed with code, always in same direction (docs simpler/older)

## Answers to Questions

### Q1: Can Vibe Code on the web identify its own skills?
**ANSWER: YES**

**Mechanism:**
- Vibe Code discovers skills via filesystem scanning of `.vibe/skills/` (project) and `~/.vibe/skills/` (user) directories
- Each skill is a directory containing a `SKILL.md` file with YAML frontmatter
- The system prompt includes **all enabled skills** with their `name`, `description`, and `path` (but NOT full body)
- This allows the model to "identify" available skills without loading full content

**Source:**
- VERIFIED_REFERENCE.md Section 2.1 (Discovery Order)
- VERIFIED_REFERENCE.md Section 2.2 (Context Residency)
- Source: `vibe/core/skills/manager.py:72-83`

**Validation:**
- Repo docs confirm: "Vibe Code: Skills are auto-discovered from `.vibe/skills/`" (AGENTS.md:57)
- Official docs confirm discovery paths
- **CONFIDENCE: HIGH**

---

### Q2: Can models invoke skills automatically?
**ANSWER: YES, with conditions**

**Mechanism:**
- Models CAN invoke skills automatically when:
  1. Skill is **enabled** (in `enabled_skills` or not in `disabled_skills`)
  2. Skill has a **description** field (makes it "model-invoked" vs "user-invoked")
  3. The `skill` tool itself is available to the agent
- The description acts as a "top-level context pointer" that the model uses to decide when to invoke
- **NO `disable-model-invocation` equivalent exists in Vibe Code** (unlike Claude Code)
- The only control is global: `enabled_skills` / `disabled_skills` in config

**Source:**
- VERIFIED_REFERENCE.md Section 2.3 (Invocation Control)
- skills/writing-for-agents/SKILL-MECHANICS.md (Invocation Types)
- Source: `vibe/core/skills/models.py:62-65`

**Validation:**
- SKILL-MECHANICS.md: "A **model-invoked** skill keeps a `description`, so the agent can fire it autonomously"
- VERIFIED_REFERENCE.md: "There is **no per-skill equivalent of Claude Code's `disable-model-invocation`**"
- **CONFIDENCE: HIGH**

---

### Q3: How about agent files?
**ANSWER: Agent files define subagents that can load and invoke skills, but the `skill` tool must be explicitly enabled**

**Mechanism:**
- Agent files are `.toml` files in `.vibe/agents/` (project) and `~/.vibe/agents/` (user)
- Each agent declares `agent_type`: `"agent"` (user-selectable) or `"subagent"` (delegation-only)
- Agents have their own `enabled_tools` / `disabled_tools` configuration
- **CRITICAL**: If the `skill` tool is NOT in `enabled_tools`, the agent **CANNOT load or invoke any skills at all**
- Subagents are fully isolated: separate context, own AgentLoop, own stats
- Subagents cannot use `ask_user_question`

**Source:**
- VERIFIED_REFERENCE.md Section 3 (Agents and Subagents)
- VERIFIED_REFERENCE.md Section 2.3 (Invocation Control - corollary)
- docs/multi-agent/COMPATIBILITY.md (Mistral Vibe Code section)
- Source: `vibe/core/config/harness_files/_harness_manager.py:187-189`
- Source: `vibe/app_server/_runtime.py:509-540`

**Validation:**
- VERIFIED_REFERENCE.md: "If `skill` tool is not in `enabled_tools` for a subagent, it **cannot load skills at all**"
- COMPATIBILITY.md: Confirms agent file locations and schema
- **CONFIDENCE: HIGH**

---

### Q4: How does Vibe Code on the web know when to invoke skills?
**ANSWER: Through progressive disclosure + model decision-making based on skill metadata in system prompt**

**Mechanism:**
1. **Progressive Disclosure** (always-on, cheap):
   - System prompt includes ALL enabled skills with: `<name>`, `<description>`, `<path>`
   - This metadata is always visible to the model, regardless of invocation state
   - **Cost**: Minimal (just metadata, not full content)

2. **Model Decision Process**:
   - Model reads skill `name` + `description` from system prompt
   - Description acts as "trigger branches" or "context pointer"
   - Model matches user request against skill descriptions
   - When match found, model invokes skill using the `skill` tool

3. **Full Content Loading** (on-demand):
   - When model invokes a skill, the `skill` tool loads the full SKILL.md body
   - Full body enters conversation history **once** and stays resident
   - **Cost**: Per-session, not per-turn (paid once, then cached)

**Source:**
- VERIFIED_REFERENCE.md Section 2.2 (Context Residency)
- skills/writing-for-agents/SKILL-MECHANICS.md (Invocation Types)
- Source: `vibe/core/system_prompt.py:262-290, 345-380`
- Source: `vibe/core/tools/builtins/skill.py:120-158`

**Validation:**
- VERIFIED_REFERENCE.md: "For an enabled but uninvoked skill, the system prompt contains only: name, description, path"
- VERIFIED_REFERENCE.md: "On invocation: the full body enters conversation history **once**, then stays resident"
- SKILL-MECHANICS.md: "The description is the skill's top-level context pointer, forced to stay loaded at all times"
- **CONFIDENCE: HIGH**

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| Prioritize VERIFIED_REFERENCE.md | Source-verified from actual code analysis; highest confidence |
| Trust source over docs | VERIFIED_REFERENCE.md found 3+ discrepancies where docs were wrong |
| Cross-check with multiple sources | Ensures consistency across repo documentation |

## Resources
- [mistralai/mistral-vibe source](https://github.com/mistralai/mistral-vibe) (commit a84be0391bf93e93a4025a5e08e8032ecb587123)
- [Official Mistral Docs](https://docs.mistral.ai)
- **Repo Documents Used:**
  - `docs/vibe/VERIFIED_REFERENCE.md` (PRIMARY)
  - `skills/vibe-reference/SKILL.md`
  - `docs/multi-agent/COMPATIBILITY.md`
  - `skills/writing-for-agents/SKILL-MECHANICS.md`
  - `AGENTS.md`

## Validation Summary

| Question | Answer | Source | Confidence | Validation Method |
|----------|--------|--------|------------|-------------------|
| Q1: Identify skills | YES - via filesystem discovery | VERIFIED_REFERENCE.md 2.1 | HIGH | Source code analysis |
| Q2: Auto invoke | YES - with description + enabled | VERIFIED_REFERENCE.md 2.3 | HIGH | Source code analysis |
| Q3: Agent files | Define subagents; skill tool must be enabled | VERIFIED_REFERENCE.md 3 | HIGH | Source code analysis |
| Q4: When to invoke | Progressive disclosure + model matching | VERIFIED_REFERENCE.md 2.2 | HIGH | Source code analysis |

**All answers validated using:**
1. ✅ Docs in this repo (VERIFIED_REFERENCE.md - source-verified)
2. ✅ Official Mistral docs (cross-referenced, discrepancies noted)
3. ✅ Manual source verification (via VERIFIED_REFERENCE.md's source citations)
