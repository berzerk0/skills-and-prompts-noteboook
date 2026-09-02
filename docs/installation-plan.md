# Vibe Skills Installation Plan

**Repository:** crispy-couscous  
**Target:** Mistral Vibe Code  
**Date:** 2026-08-22  
**Companion Documents:**
- [Skill Action Plan v3](skill-action-plan-v3.md)
- [Cross-Agent Primitive Standardization](cross-agent-primitives.md)
- [Skill Design Guidelines](SKILL_DESIGN.md)
- [AGENTS.md](../AGENTS.md)

---

## Overview

This plan follows the **Suggested Order** from the action plan while incorporating the **Script-First Architecture** principle from this repository's documentation. All skills will follow the pattern:

```
Skill Request → Agent Wrapper → bash → Python Script → Result
```

**Key Constraints from Repository Docs:**
1. **Script-First**: All skills must have CLI-executable cores (Python/Bash)
2. **Tool-Agnostic Instructions**: Never reference specific tool names in SKILL.md
3. **Portable Frontmatter Only**: Use only the 6 Agent Skills spec fields
4. **bash/Bash is Universal**: The only consistent tool name across agents
5. **Vibe Tool Names**: `read_file`, `write_file`, `edit`, `grep`, `bash`, `search_replace`

---

## Prerequisites Checklist

- [ ] Read [Cross-Agent Primitive Standardization](cross-agent-primitives.md)
- [ ] Read [Skill Design Guidelines](SKILL_DESIGN.md)
- [ ] Verify Vibe Code is installed and accessible
- [ ] Verify `~/.vibe/skills/` directory exists
- [ ] Verify `~/.vibe/agents/` directory exists
- [ ] Verify `~/.vibe/hooks.toml` exists or can be created
- [ ] Verify `~/.vibe/prompts/` directory exists
- [ ] Verify Python 3.12+ is available
- [ ] Verify git is available

---

## Installation Phases

### Phase 1: Foundation (S Tier - Must Have)

#### Step 1.1: Install writing-for-agents (#1)
**Priority:** S Tier - Do this FIRST  
**Repository Docs Reference:** Script-First Architecture, Tool-Agnostic Instructions  

**Actions:**
- [ ] Clone source: `git clone --depth 1 https://github.com/mattpocock/skills`
- [ ] Copy `skills/productivity/writing-for-agents/` to `~/.vibe/skills/writing-for-agents/`
- [ ] **Convert for Vibe:**
  - [ ] Rewrite `allowed-tools` in SKILL.md frontmatter to: `read_file`, `grep`, `edit`, `write_file`
  - [ ] Remove `Glob` (no Vibe equivalent)
  - [ ] Add `user-invocable: true` to frontmatter
  - [ ] Update all path references from `~/.claude/skills/` to `~/.vibe/skills/`
- [ ] **Verify tool names:** Check against [cross-agent-primitives.md](cross-agent-primitives.md) table
- [ ] **Compress:** Reduce body from ~200 lines to ~40-60 lines using writing-for-agents itself
- [ ] Test: Invoke `/writing-for-agents` and verify it loads

**Checklist:**
- [ ] Source cloned
- [ ] Files copied to correct location
- [ ] allowed-tools rewritten for Vibe
- [ ] Paths updated
- [ ] user-invocable set
- [ ] Body compressed
- [ ] Tested and working

**Success Criteria:** `/writing-for-agents` slash command is available and functional

---

#### Step 1.2: Verify Transcript Format (#9 foundation)
**Priority:** S Tier - Required before #2, #4  
**Repository Docs Reference:** N/A (Vibe-specific)  

**Actions:**
- [ ] Create test `POST_AGENT` hook in `~/.vibe/hooks.toml`
- [ ] Trigger a Vibe session with the hook active
- [ ] Inspect `transcript_path` file contents
- [ ] Verify token usage data is present in transcript
- [ ] Document transcript format in a new file: `~/.vibe/docs/transcript-format.md`

**Checklist:**
- [ ] Hook created and registered
- [ ] Test session completed
- [ ] Transcript file located
- [ ] Token data confirmed present/absent
- [ ] Format documented

**Success Criteria:** Confirmed whether transcript contains token usage data

**Blocker for:** #2 (planning-with-files), #4 (escalate), #9 (token measurement)

---

#### Step 1.3: Install planning-with-files (#2)
**Priority:** S Tier  
**Repository Docs Reference:** Script-First Architecture  

**Actions:**
- [ ] **Source Decision:** Choose between:
  - [ ] `trailofbits/skills-curated` (vetted, frozen Feb 22)
  - [ ] `OthmanAdi/planning-with-files` (v2.32.x, active, has hooks)
- [ ] Clone chosen source
- [ ] Copy to `~/.vibe/skills/planning-with-files/`
- [ ] **Convert for Vibe:**
  - [ ] Rewrite `allowed-tools` to: `read_file`, `write_file`, `edit`, `grep`
  - [ ] Remove `Glob`
  - [ ] Add `user-invocable: true`
  - [ ] Update paths to use `scratchpad_dir` (Vibe-specific, passed to subagents)
  - [ ] **Wire 3-strike exit:** Update to call `/escalate` (will be installed in Step 1.5)
- [ ] **Compress:** Reduce from ~200 lines to ~40 lines
  - [ ] Keep: filesystem-as-disk, save findings after 2 reads, re-read plan, log errors with attempt#, never repeat failed action, 3-strike then escalate
  - [ ] Drop: templates, 5-question reboot test, read/write matrix
- [ ] **Port hooks:** If using ToB version, port completion-check hook to `~/.vibe/hooks.toml` as `POST_AGENT`
- [ ] Test: Verify compressed skill works

**Checklist:**
- [ ] Source selected and cloned
- [ ] Files copied
- [ ] allowed-tools rewritten
- [ ] Paths updated to use scratchpad_dir
- [ ] 3-strike wired to /escalate
- [ ] Body compressed to ~40 lines
- [ ] Hooks ported (if applicable)
- [ ] Tested and working

**Success Criteria:** Compressed planning-with-files skill is functional and uses Vibe conventions

---

#### Step 1.4: Create Model Routing Agent Files (#3)
**Priority:** S Tier  
**Repository Docs Reference:** Subagent Design in SKILL_DESIGN.md  

**Actions:**
- [ ] Clone `obra/superpowers` repo
- [ ] Read `skills/subagent-driven-development/SKILL.md`, Model Selection section only
- [ ] **Create agent TOML files in `~/.vibe/agents/`:**
  - [ ] `transcription.toml` - cheapest tier model
  - [ ] `reviewer.toml` - mid-tier floor model
  - [ ] `implementer.toml` - mid-tier floor model
  - [ ] `architect.toml` - most capable model
  - [ ] `escalation-fixer.toml` - one tier above whatever got stuck
- [ ] **For each agent file:**
  - [ ] Set `active_model` appropriately
  - [ ] Set `compaction_model` (separate from active_model)
  - [ ] Set `allowed_models` as guardrail
  - [ ] Set `enabled_tools` scoped tight
  - [ ] **Include `skill` tool** in enabled_tools (required for subagents to load skills)
  - [ ] Set `agent_type = "subagent"`
  - [ ] Add appropriate descriptions
- [ ] **Apply principle:** "turn count beats token price" - note in comments
- [ ] **Define failure path:** Reference #4 escalate skill

**Checklist:**
- [ ] Source reviewed
- [ ] transcription.toml created
- [ ] reviewer.toml created
- [ ] implementer.toml created
- [ ] architect.toml created
- [ ] escalation-fixer.toml created
- [ ] All files have active_model, compaction_model, allowed_models
- [ ] All files have skill tool enabled
- [ ] Failure paths documented
- [ ] Tested: each agent can be invoked

**Success Criteria:** Agent files created and can be used for delegation

---

#### Step 1.5: Create /escalate Skill (#4)
**Priority:** S Tier  
**Repository Docs Reference:** Tool-Agnostic Instructions  

**Actions:**
- [ ] Create directory: `~/.vibe/skills/escalate/`
- [ ] **Write SKILL.md** (~30 lines, using #1 writing-for-agents):
  - [ ] Frontmatter: name, description, user-invocable: true
  - [ ] allowed-tools: read_file, write_file, grep
  - [ ] **Four steps (retrieval only, zero self-assessment):**
    1. Halt - stop troubleshooting
    2. Read session transcript from `transcript_path` (from POST_AGENT hook)
    3. Write brief to `.escalation/brief-<timestamp>.md` or `scratchpad_dir`
    4. Output: `Brief at <path>. <route>.`
  - [ ] Include brief format template
  - [ ] **Route fork logic:**
    - Self-contained → dispatch subagent with stronger model
    - Needs dialogue → open fresh session
    - Never Shift+Tab
  - [ ] **Return leg:** Append lesson to napkin.md in required format
- [ ] **Reuse transcript reader** from Step 1.2
- [ ] Test: Verify `/escalate` command works

**Checklist:**
- [ ] Directory created
- [ ] SKILL.md written with proper frontmatter
- [ ] allowed-tools set correctly
- [ ] Four steps documented
- [ ] Brief format included
- [ ] Route fork logic documented
- [ ] Return leg to napkin documented
- [ ] Transcript reader reused
- [ ] Tested and working

**Success Criteria:** `/escalate` slash command creates proper brief and routes correctly

---

### Phase 2: High Value (A Tier)

#### Step 2.1: Create karpathy-guidelines Prompt Files (#5)
**Priority:** A Tier  
**Repository Docs Reference:** Per-Agent Wrappers in SKILL_DESIGN.md  

**Actions:**
- [ ] Clone `multica-ai/andrej-karpathy-skills`
- [ ] Review `skills/karpathy-guidelines/SKILL.md`
- [ ] **Create prompt file:** `~/.vibe/prompts/implementer.md`
- [ ] **Compress** from ~60 lines to ~15:
  - [ ] Keep four headers, one bullet each
  - [ ] Add ambiguous-verb rule: "validate", "check", "process", "handle" have multiple meanings — ask
- [ ] **Create implementer.toml agent file** (if not done in Step 1.4):
  - [ ] Reference `system_prompt_id: implementer`
- [ ] **Do NOT add to AGENTS.md** (per action plan: constraints backfire)

**Checklist:**
- [ ] Source reviewed
- [ ] implementer.md created with compressed content
- [ ] Ambiguous-verb rule added
- [ ] implementer.toml references prompt
- [ ] Not added to AGENTS.md
- [ ] Tested: implementer agent uses prompt

**Success Criteria:** Implementer agent uses karpathy guidelines without global constraints

---

#### Step 2.2: Create Merged Clarify Skill (#6)
**Priority:** A Tier  
**Repository Docs Reference:** Tool-Agnostic Instructions  

**Actions:**
- [ ] **Source Decision:** Choose philosophy:
  - [ ] ask-questions: cap at 1-5 questions
  - [ ] grill-me: reject caps, one question at a time
- [ ] Review `trailofbits.com/skills/ask-questions-if-underspecified/` (web page only)
- [ ] Review `mattpocock/skills/grill-me`
- [ ] Create directory: `~/.vibe/skills/clarify/`
- [ ] **Write SKILL.md** (~25 lines):
  - [ ] Frontmatter: name, description, user-invocable: true
  - [ ] allowed-tools: read_file, grep, ask_user_question
  - [ ] From ask-questions: six-dimension underspecification test
  - [ ] From grill-me: one question at a time, supply recommended answer, facts vs decisions
  - [ ] Drop question-formatting guidance (Vibe has ask_user_question natively)
  - [ ] **Hard constraint:** main-agent only (subagents can't use ask_user_question)
- [ ] Test: Verify `/clarify` command works

**Checklist:**
- [ ] Philosophy chosen
- [ ] Sources reviewed
- [ ] Directory created
- [ ] SKILL.md written
- [ ] allowed-tools set correctly
- [ ] Six-dimension test included
- [ ] Grill-me principles included
- [ ] Formatting guidance dropped
- [ ] Main-agent only constraint documented
- [ ] Tested and working

**Success Criteria:** `/clarify` slash command helps catch ambiguity in main agent

---

#### Step 2.3: Install skill-extractor (#7)
**Priority:** A Tier  
**Repository Docs Reference:** Script-First Architecture  

**Actions:**
- [ ] Clone `trailofbits/skills-curated`
- [ ] Copy `plugins/skill-extractor/skills/skill-extractor/` to `~/.vibe/skills/skill-extractor/`
- [ ] **Convert for Vibe:**
  - [ ] Rewrite `allowed-tools` to: read_file, write_file, grep, web_search, ask_user_question
  - [ ] Remove `Glob`
  - [ ] Add `user-invocable: true`
  - [ ] Update save paths from `~/.claude/skills/` to `~/.vibe/skills/`
- [ ] Test: Verify `/skill-extractor` command works

**Checklist:**
- [ ] Source cloned
- [ ] Files copied
- [ ] allowed-tools rewritten
- [ ] Glob removed
- [ ] user-invocable set
- [ ] Paths updated
- [ ] Tested and working

**Success Criteria:** `/skill-extractor` slash command can capture knowledge

---

#### Step 2.4: Install modern-python (#8)
**Priority:** A Tier  
**Repository Docs Reference:** Script-First Architecture  

**Actions:**
- [ ] Clone `trailofbits/skills` (NOT agenticskills.io mirror)
- [ ] Copy `plugins/modern-python/skills/modern-python/` to `~/.vibe/skills/modern-python/`
- [ ] **Verify license:** Should be CC-BY-SA-4.0 (not AGPL-3.0)
- [ ] Include `references/` directory
- [ ] **Convert for Vibe:**
  - [ ] Rewrite `allowed-tools` to: read_file, write_file, edit, grep, bash
  - [ ] Add `user-invocable: true`
  - [ ] Keep references intact (loaded on demand)
- [ ] Test: Verify `/modern-python` command works

**Checklist:**
- [ ] Source cloned from correct repo
- [ ] Files and references copied
- [ ] License verified
- [ ] allowed-tools rewritten
- [ ] user-invocable set
- [ ] References preserved
- [ ] Tested and working

**Success Criteria:** `/modern-python` slash command promotes modern Python stack

---

### Phase 3: Worth Doing (B Tier)

#### Step 3.1: Build Token Measurement Hook (#9)
**Priority:** B Tier  
**Repository Docs Reference:** N/A (Vibe-specific)  

**Actions:**
- [ ] Review `anthropics/claude-plugins-official/plugins/session-report/skills/session-report/analyze-sessions.mjs`
- [ ] **Create script:** `~/.vibe/scripts/token-measurement.py`
- [ ] **Steal metrics:** tokens by skill, tokens by subagent type, cache-hit rate, cache-break clustering, single prompts exceeding 2% of total
- [ ] **Reuse transcript reader** from Step 1.2
- [ ] **Register hook** in `~/.vibe/hooks.toml`:
  ```toml
  [hooks]
  post_agent = ["python ~/.vibe/scripts/token-measurement.py"]
  ```
- [ ] **Output:** Write metrics to `~/.vibe/logs/token-metrics-<date>.json`
- [ ] Test: Run a session and verify metrics are captured

**Checklist:**
- [ ] Source reviewed
- [ ] Script created
- [ ] Metrics list incorporated
- [ ] Transcript reader reused
- [ ] Hook registered
- [ ] Output path configured
- [ ] Tested and working

**Success Criteria:** Token metrics are captured per session

---

#### Step 3.2: Harvest Parallel-Dispatch Doctrine (#10)
**Priority:** B Tier  
**Repository Docs Reference:** Tool-Agnostic Instructions  

**Actions:**
- [ ] Clone `obra/superpowers`
- [ ] Review `skills/dispatching-parallel-agents/SKILL.md`
- [ ] **Harvest ~20 lines** into prompt files:
  - [ ] Independence test: truly separate domains, or would fixing one fix the others?
  - [ ] Prompt-construction discipline: focused scope, self-contained context, explicit constraints, specified return format
  - [ ] **Rewrite for Vibe:** return format writes to `scratchpad_dir`, return the path, not prose
- [ ] **Add to existing prompt files:**
  - [ ] `~/.vibe/prompts/implementer.md`
  - [ ] Or create new `~/.vibe/prompts/parallel-dispatch.md`
- [ ] **Do NOT install as skill** (Vibe concurrency is model-initiated, not forced)

**Checklist:**
- [ ] Source reviewed
- [ ] Doctrine harvested
- [ ] Vibe-specific return format applied
- [ ] Added to prompt files
- [ ] Not installed as skill

**Success Criteria:** Parallel dispatch doctrine is available in prompts

---

#### Step 3.3: Install napkin (#11)
**Priority:** B Tier  
**Repository Docs Reference:** N/A  

**Actions:**
- [ ] Clone `git clone --depth 1 https://github.com/blader/napkin`
- [ ] **Read SKILL.md, NOT README** (they contradict)
- [ ] Verify version: v6.0.0, commit "Update napkin skill to v6 curated runbook model"
- [ ] Copy to `~/.vibe/skills/napkin/`
- [ ] **Convert for Vibe:**
  - [ ] Change `.claude/napkin.md` → `.vibe/napkin.md` throughout
  - [ ] No `allowed-tools` to rewrite (has none)
  - [ ] Add `user-invocable: true`
- [ ] **Understand model:** curated runbook, NOT chronological log
  - [ ] Excludes: one-off timeline notes, verbose postmortems without reusable action, pure mistake logs without `Do instead:` line
  - [ ] Max 10 items per category, re-prioritised and pruned on every read
- [ ] **Add to .gitignore:** `.vibe/napkin.md`
- [ ] Test: Verify `/napkin` command works

**Checklist:**
- [ ] Source cloned
- [ ] SKILL.md read (not README)
- [ ] Version verified
- [ ] Files copied
- [ ] Paths updated
- [ ] user-invocable set
- [ ] Model understood
- [ ] Added to .gitignore
- [ ] Tested and working

**Success Criteria:** `/napkin` slash command maintains curated runbook

---

### Phase 4: Optional (C Tier)

#### Step 4.1: handoff (#12)
**Priority:** C Tier - Only when need appears  
**Repository Docs Reference:** N/A  

**Actions:**
- [ ] **Wait for need:** Revisit when #9 shows context loss patterns
- [ ] Review `mattpocock/skills/handoff` or ToB `productivity` fork
- [ ] **Re-author in ~20 lines** when actual cross-session transfer problem exists
- [ ] Note: #4 already covers failure handoff case

**Checklist:**
- [ ] Need identified
- [ ] Source reviewed
- [ ] Custom implementation created

**Success Criteria:** Handoff skill available when needed

---

## Cross-Cutting Rules Checklist (Apply to EVERY skill)

For each skill installed, verify:

### Rule 1: Rewrite allowed-tools
- [ ] `Edit` → `edit` (NOT `search_replace`)
- [ ] `Glob` → removed (no Vibe equivalent)
- [ ] All tool names checked against [cross-agent-primitives.md](cross-agent-primitives.md) table
- [ ] Unrecognized names removed (they fail silently)

### Rule 2: Rewrite paths
- [ ] `~/.claude/skills/` → `~/.vibe/skills/`
- [ ] `.claude/skills/` → `.vibe/skills/`
- [ ] `./.agents/skills/` → NOT used (per source, doesn't work)

### Rule 3: user-invocable
- [ ] Set `user-invocable: true` on slash-invoked skills
- [ ] Understand: does NOT hide skill from model
- [ ] `enabled_skills` in `config.toml` is the only reach control

### Rule 4: Port hooks
- [ ] `PRE_TOOL` → `PreToolUse` in `hooks.toml`
- [ ] `POST_AGENT` → `Stop` in `hooks.toml`
- [ ] Config format: `hooks.toml`, NOT `hooks.json`

### Rule 5: Compress
- [ ] Body compressed before installing
- [ ] Body cost paid at invocation, stays in history
- [ ] A 200-line skill called once costs 200 lines for rest of session

### Rule 6: Budget AGENTS.md
- [ ] AGENTS.md loads every turn
- [ ] One per project root + user-level (not two as docs claim)
- [ ] Keep lean

### Rule 7: Script invocations
- [ ] Pass `--agent` explicitly when scripting
- [ ] Programmatic mode falls back to `default_agent` (default `accept-edits`)
- [ ] NOT `auto-approve` as docs claim

### Rule 8: Read SKILL.md, not README
- [ ] SKILL.md and README may contradict (e.g., napkin)
- [ ] Assume README may describe superseded version

---

## Final Verification Checklist

### All Skills
- [ ] All S Tier skills installed and tested
- [ ] All A Tier skills installed and tested
- [ ] All B Tier skills installed and tested
- [ ] C Tier skills deferred until needed

### Documentation
- [ ] All skills documented in appropriate locations
- [ ] Cross-references between skills documented
- [ ] Failure paths and escalation routes clear

### Testing
- [ ] Each skill tested individually
- [ ] Skill interactions tested (e.g., planning-with-files → escalate)
- [ ] Token measurement baseline established
- [ ] Model routing effectiveness measurable

### Repository Integration
- [ ] All files in correct locations per [Repository Structure in AGENTS.md](../AGENTS.md)
- [ ] Symlinks maintained where appropriate
- [ ] No duplication between `.vibe/skills/` and `skills/`
- [ ] Python implementations in root, referenced by skills

---

## Execution Summary

**Total Steps:** 12 skill installations + foundation work  
**Estimated Order:**
1. writing-for-agents (#1)
2. Verify transcript format (#9 foundation)
3. planning-with-files (#2)
4. Model routing agent files (#3)
5. /escalate (#4)
6. karpathy-guidelines (#5)
7. clarify (#6)
8. skill-extractor (#7)
9. modern-python (#8)
10. Token measurement hook (#9)
11. Parallel-dispatch doctrine (#10)
12. napkin (#11)
13. handoff (#12) - when needed

**Dependencies:**
- #9 foundation (transcript format) must be done before #2, #4, #9
- #4 (escalate) should be done after #3 (model routing) to have escalation targets
- #1 (writing-for-agents) should be done first to improve all subsequent work

---

## Notes

1. **Rejected Skills:** See action plan for list of rejected skills and reasons
2. **Open Questions:** See action plan for unresolved decisions
3. **Repository Conventions:** All installations must follow [SKILL_DESIGN.md](SKILL_DESIGN.md) and [cross-agent-primitives.md](cross-agent-primitives.md)
4. **Porting Guidance:** Use [AGENTS.md](../AGENTS.md) repository structure as template

---

*Plan generated from Skill Action Plan v3 and crispy-couscous repository documentation*
