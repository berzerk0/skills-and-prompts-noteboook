# Implementation Roadmap - crispy-couscous
## Comprehensive Plan for Repository Improvements

**Created:** 2026-08-22  
**Status:** PLANNING PHASE  
**Owner:** Vibe Code  

---

## 🎯 Executive Summary

This plan outlines the strategic improvements to make crispy-couscous a **first-class multi-agent skill repository** that works seamlessly with Vibe Code. We've already fixed the critical blocking issues. Now we build on that foundation.

**Current State:**
- ✅ 18 subagents configured, all with `skill` tool enabled
- ✅ 13 skills available and discoverable
- ✅ Cross-agent compatibility (Claude, Pi, Vibe)
- ✅ Router agent created (entry point)
- ⚠️ Mixed symlink/real directory structure in `.vibe/skills/`
- ⚠️ No user-selectable main agent yet
- ⚠️ Inconsistent tool availability across agents

---

## 📋 Phase Overview

| Phase | Priority | Duration | Dependencies |
|-------|----------|----------|--------------|
| Phase A: Symlink Standardization | HIGH | 15 min | None |
| Phase B: Router Agent & Routing Logic | HIGH | 30 min | Phase A |
| Phase C: Agent Type Refactoring | HIGH | 20 min | Phase B |
| Phase D: Tool Profile Standardization | MEDIUM | 20 min | Phase B |
| Phase E: JSON Return Convention | MEDIUM | 15 min | Phase C |
| Phase F: Model Selection Strategy | MEDIUM | 20 min | None |
| Phase G: Validation & Testing | HIGH | 30 min | All |

---

## Phase A: Symlink Standardization

**Objective:** Make all skill directories in `.vibe/skills/` symlinks for consistency.

### Current State
```
.vibe/skills/
├── challenge-my-thinking -> ../../skills/challenge-my-thinking (SYMLINK)
├── clarify (REAL DIR)
├── codeberg -> ../../skills/codeberg (SYMLINK)
├── escalate (REAL DIR)
├── modern-python (REAL DIR)
├── napkin (REAL DIR)
├── planning-with-files (REAL DIR)
├── repo-auditor -> ../../skills/repo-auditor (SYMLINK)
├── skill-extractor (REAL DIR)
├── skill-validator -> ../../skills/skill-validator (SYMLINK)
├── timestamp -> ../../skills/timestamp (SYMLINK)
├── vibe-reference -> ../../skills/vibe-reference (SYMLINK)
└── writing-for-agents (REAL DIR)
```

### Tasks
- [ ] Remove 7 real directories from `.vibe/skills/`
- [ ] Create symlinks pointing to `../../skills/<name>` for each
- [ ] Verify all symlinks resolve correctly
- [ ] Test that Vibe Code can still discover all skills

### Impact
- ✅ Single source of truth for all skills
- ✅ Consistency with `.claude/skills/` and `.pi/skills/`
- ✅ Eliminates drift risk

---

## Phase B: Router Agent & Routing Logic

**Objective:** Create a smart router that delegates to subagents based on intent.

### Router Agent Created
- `agent_type = "agent"` - User-selectable via `--agent router`
- All tools enabled for maximum flexibility
- Uses `mistral-medium` as default model

### Routing Logic (System Prompt Addition)

The router needs a **routing table** in its system prompt or a reference document:

```markdown
## Routing Rules

When user request matches:

### Direct Triggers (exact match)
- "audit this repo" / "audit repository" → spawn repo-auditor
- "validate skills" / "validate SKILL.md" → spawn skill-validator
- "what time is it" / "timestamp" → spawn timestamp
- "challenge my thinking" → spawn challenge-my-thinking
- "clarify" / "ask questions" → spawn clarify

### Domain-Based Routing
- Repository structure, skills, compatibility → repo-auditor
- SKILL.md, spec compliance, validation → skill-validator
- Time, date, timestamp → timestamp
- Python project setup, config, migration → modern-python
- Codeberg, Gitea, repository management → codeberg
- Architecture, design, review → architect
- Implementation, code changes → implementer
- Review, debugging → reviewer
- Planning, complex tasks → planning-with-files

### Fallback Behavior
- If no clear match, ask clarifying questions
- If ambiguous, present options to user
- If experimental, use napkin for runbook
```

### Tasks
- [ ] Create `prompts/router.md` with routing logic
- [ ] Update `router.toml` to reference `system_prompt_id = "router"`
- [ ] Create symlink: `.vibe/prompts/router.md -> ../../prompts/router.md`
- [ ] Test routing with sample requests

### Structured Return Convention
Router should expect and handle JSON-formatted returns from subagents:

```json
{
  "status": "success|error|partial",
  "task": "audit",
  "results": {...},
  "artifacts": ["/scratchpad/findings.md"],
  "stats": {"turns": 5, "tokens": 1500},
  "next_steps": ["review findings", "fix issues"]
}
```

---

## Phase C: Agent Type Refactoring

**Objective:** Make key subagents callable as user-facing agents when needed.

### Current State
All 18 agents are `type = "subagent"`. This means:
- ❌ Cannot be selected with `--agent <name>`
- ✅ Can be spawned via `task` tool

### Strategy
Keep most as subagents, but make **high-value, frequently-used** ones also available as direct agents:

| Agent | Current Type | Proposed Type | Rationale |
|-------|--------------|---------------|-----------|
| router | agent | agent | Primary entry point |
| repo-auditor | subagent | **agent** | Common task |
| skill-validator | subagent | **agent** | Common task |
| timestamp | subagent | **agent** | Simple, frequent |
| codeberg | subagent | **agent** | Common task |
| challenge-my-thinking | subagent | subagent | Better as subagent |
| clarify | subagent | subagent | Better as subagent |
| ... | subagent | subagent | Keep as subagent |

### Tasks
- [ ] Create duplicate agent files for callable versions
- [ ] Or: Use `agent_type = "agent"` in primary configs
- [ ] Update documentation to show which are directly callable
- [ ] Test `--agent repo-auditor` works

### Naming Convention
```
.vibe/agents/
├── router.toml (agent) - main entry
├── repo-auditor.toml (agent) - directly callable
├── repo-auditor-sub.toml (subagent) - for delegation
├── skill-validator.toml (agent)
├── skill-validator-sub.toml (subagent)
└── ...
```

**OR simpler:** Just make the useful ones `type = "agent"` and keep subagent behavior via `task` tool.

---

## Phase D: Tool Profile Standardization

**Objective:** Define consistent tool profiles across agents.

### Current Inconsistencies
Some agents have `web_search`, some don't. Some have `todo`, some don't.

### Proposed Profiles

```toml
# Profile: Full (router, main agents)
[tools.task]
[tools.skill]
[tools.read_file]
[tools.write_file]
[tools.edit]
[tools.grep]
[tools.bash]
[tools.web_search]
[tools.web_fetch]
[tools.todo]
[tools.ask_user_question]

# Profile: Standard (most subagents)
[tools.skill]
[tools.read_file]
[tools.write_file]
[tools.edit]
[tools.grep]
[tools.bash]

# Profile: Read-Only (audit, validation)
[tools.skill]
[tools.read_file]
[tools.grep]
[tools.bash]

# Profile: Network-Enabled (add web tools)
[tools.skill]
[tools.read_file]
[tools.write_file]
[tools.edit]
[tools.grep]
[tools.bash]
[tools.web_search]
[tools.web_fetch]
```

### Tasks
- [ ] Define tool profile types
- [ ] Audit each agent's tool needs
- [ ] Apply consistent profiles
- [ ] Document profile definitions

---

## Phase E: JSON Return Convention

**Objective:** Standardize subagent return format for parseable results.

### Convention Document
Create `docs/SUBAGENT_RETURN_CONVENTION.md`:

```markdown
# Subagent Return Convention

All subagents SHOULD return structured JSON when possible.

## Response Schema

```json
{
  "status": "success" | "error" | "partial" | "needs_input",
  "task": "string - the task that was performed",
  "summary": "string - human-readable summary",
  "results": {
    // Task-specific data
  },
  "artifacts": [
    {
      "path": "/scratchpad/filename.ext",
      "type": "markdown" | "json" | "text" | "csv",
      "description": "what this file contains"
    }
  ],
  "warnings": ["string - non-blocking issues"],
  "errors": ["string - blocking issues"],
  "stats": {
    "turns_used": 5,
    "tokens_input": 1000,
    "tokens_output": 500
  },
  "next_steps": ["string - suggested follow-up actions"]
}
```

### Example: repo-auditor return
```json
{
  "status": "success",
  "task": "repository_audit",
  "summary": "Audit of crispy-couscous completed. 3 findings.",
  "results": {
    "skill_count": 13,
    "agent_count": 18,
    "findings": [
      {"severity": "critical", "description": "3 agents missing skill tool", "fixed": true},
      {"severity": "medium", "description": "inconsistent symlinks"}
    ]
  },
  "artifacts": [
    {"path": "/scratchpad/audit-report.md", "type": "markdown", "description": "Full audit report"}
  ],
  "stats": {"turns_used": 8, "tokens_input": 2500, "tokens_output": 1200}
}
```

### Tasks
- [ ] Create convention document
- [ ] Update subagent prompts to use JSON format
- [ ] Update router to parse JSON responses
- [ ] Test end-to-end structured flow

---

## Phase F: Model Selection Strategy

**Objective:** Rationalize `active_model` choices across agents.

### Current State
```
mistral-small: 14 agents
mistral-medium: 3 agents (implementer, reviewer, router)
mistral-large: 2 agents (architect, escalation-fixer)
```

### Model Selection Framework

| Model | Use Case | Cost | Speed | Quality |
|-------|----------|------|-------|---------|
| mistral-small | Simple tasks, validation, timestamps | Low | Fast | Good |
| mistral-medium | General purpose, implementation | Medium | Medium | Very Good |
| mistral-large | Architecture, complex reasoning | High | Slow | Excellent |

### Proposed Assignment

```toml
# mistral-small (fast, cheap - simple tasks)
timestamp.toml
codeberg.toml
skill-validator.toml
repo-auditor.toml
challenge-my-thinking.toml
clarify.toml
napkin.toml
planning-with-files.toml
skill-extractor.toml
vibe-reference.toml
writing-for-agents.toml
escalate.toml
transcription.toml

# mistral-medium (balanced - general purpose)
router.toml (main entry)
implementer.toml
timestamp.toml (if needs more nuance)
reviewer.toml

# mistral-large (high quality - complex reasoning)
architect.toml
escalation-fixer.toml
modern-python.toml (complex config decisions)
```

### Cost Optimization
- Router uses medium: good balance for routing decisions
- Most subagents use small: they do focused tasks
- Large reserved for: architecture, escalation, complex config

### Tasks
- [ ] Audit each agent's actual needs
- [ ] Rebalance model assignments
- [ ] Document model selection rationale
- [ ] Add cost estimates per agent type

---

## Phase G: Validation & Testing

**Objective:** Verify all improvements work correctly.

### Test Cases

1. **Symlink Test**
   ```bash
   ls -la .vibe/skills/ | grep -v '^d' | wc -l  # Should be 0 real dirs
   ```

2. **Router Test**
   ```bash
   vibe --agent router "audit this repository"
   ```

3. **Direct Agent Test**
   ```bash
   vibe --agent repo-auditor "audit this"
   ```

4. **JSON Return Test**
   - Spawn subagent via task
   - Verify return is parseable JSON
   - Verify artifacts exist in scratchpad

5. **Skill Discovery Test**
   - Start Vibe Code session
   - Verify all 13 skills are discoverable
   - Verify skill descriptions appear in context

### Validation Checklist
- [ ] All symlinks valid
- [ ] Router agent selectable
- [ ] Router correctly delegates
- [ ] Direct agents work
- [ ] JSON returns parseable
- [ ] No regressions in existing functionality

---

## 📊 Implementation Priority Matrix

| Item | Impact | Effort | Priority | Phase |
|------|--------|--------|----------|-------|
| Router agent + routing logic | HIGH | Medium | **P0** | B |
| Symlink standardization | HIGH | Low | **P0** | A |
| Agent type refactoring | HIGH | Medium | **P0** | C |
| JSON return convention | MEDIUM | Low | **P1** | E |
| Model selection strategy | MEDIUM | Medium | **P1** | F |
| Tool profile standardization | LOW | Medium | **P2** | D |

---

## 🎯 Recommended Execution Order

1. **Phase A: Symlink Standardization** (15 min, quick win)
2. **Phase B: Router Agent** (30 min, core functionality)
3. **Phase C: Agent Type Refactoring** (20 min, unlocks direct access)
4. **Phase E: JSON Convention** (15 min, improves reliability)
5. **Phase F: Model Strategy** (20 min, cost optimization)
6. **Phase D: Tool Profiles** (20 min, consistency)
7. **Phase G: Validation** (30 min, ensure everything works)

---

## ⏱️ Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| A | 15 min | 15 min |
| B | 30 min | 45 min |
| C | 20 min | 65 min |
| E | 15 min | 80 min |
| F | 20 min | 100 min |
| D | 20 min | 120 min |
| G | 30 min | 150 min |

**Total: ~2.5 hours** for full implementation

---

## 📝 Success Criteria

- [ ] All skills in `.vibe/skills/` are symlinks
- [ ] Router agent works as primary entry point
- [ ] At least 4 agents are directly callable with `--agent`
- [ ] Subagents return parseable JSON
- [ ] Model assignments are rationalized and documented
- [ ] All existing functionality still works

---

## 🚀 Quick Wins (Can Do Now)

1. **Symlink standardization** - 15 min, immediate benefit
2. **Router agent** - Already created, just needs routing logic
3. **Make router default** - Configure as default_agent in config

---

## ❓ Open Questions

1. Should we make router the `default_agent` in config.toml?
2. Should callable agents have separate configs or dual-type configs?
3. Should we add a `config.toml` at repo level for Vibe Code settings?
4. Should we document the routing rules in AGENTS.md?

---

*Plan created: 2026-08-22*  
*Ready for execution*
