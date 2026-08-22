# Repository Bug & Problem Audit Plan
## crispy-couscous

**Objective:** Systematically identify bugs, problems, and issues in the repository that could cause silent failures, compatibility issues, or degraded performance.

**Scope:** Full repository audit with focus on Vibe Code compatibility, cross-agent portability, and configuration correctness.

**Reference Materials:**
- `/docs/vibe/VERIFIED_REFERENCE.md` - Vibe Code source-verified behavior
- `/docs/audit-report-2026-08-22.md` - Previous audit findings
- `/AGENTS.md` - Repository context for agents
- `/README.md` - Repository structure and purpose

---

## Plan Overview

This plan follows a **progressive discovery** approach:
1. **Known Issues Validation** - Verify and prioritize existing audit findings
2. **Configuration Audit** - Check all agent/subagent configs for correctness
3. **Skill Validation** - Validate each skill's structure and compatibility
4. **Cross-Agent Compatibility** - Verify portability across Claude, Pi, Vibe
5. **Path & Reference Audit** - Find stale paths and broken references
6. **Security & Permissions** - Check for overly permissive or restrictive configs
7. **Performance & Cost** - Identify context bloat and inefficient patterns
8. **Tool Name Consistency** - Ensure correct tool names per agent
9. **Symlink Integrity** - Verify all symlinks point to valid targets
10. **Synthesis & Prioritization** - Compile findings with severity ratings

---

## Detailed Execution Plan

### Phase 0: Preparation
- [ ] Create working directory for audit outputs: `main/audit-results/`
- [ ] Initialize audit log file: `main/audit-results/audit-log.md`
- [ ] Set up tracking file for findings: `main/audit-results/findings.md`
- [ ] Record start time and initial git state

### Phase 1: Known Issues Validation (Priority: CRITICAL)
**Objective:** Verify and expand on findings from `docs/audit-report-2026-08-22.md`

- [ ] **Issue 1.1: Agents missing `skill` tool**
  - [ ] Review each of the 7 agents missing `skill` tool in enabled_tools
  - [ ] Confirm these agents CANNOT load or invoke any skills
  - [ ] Check if this affects subagent delegation patterns
  - [ ] List all affected agent files
  - [ ] Document impact: silent failure mode

- [ ] **Issue 1.2: Stale path references**
  - [ ] Inspect `skills/skill-extractor/references/skill-lifecycle.md` for `.claude/` references
  - [ ] Inspect `skills/writing-for-agents/SKILL.md` for `CLAUDE.md` references
  - [ ] Search for all `.claude/`, `~/.claude/`, `CLAUDE.md` patterns in skills/
  - [ ] Document each occurrence with line numbers
  - [ ] Assess impact: broken references in Vibe Code context

- [ ] **Issue 1.3: Prompt path resolution**
  - [ ] Verify `implementer.toml` references `system_prompt_id='implementer'`
  - [ ] Check if `prompts/implementer.md` exists at repo root
  - [ ] Test if Vibe Code can find prompts at repo root vs `.vibe/prompts/`
  - [ ] Document expected vs actual behavior

### Phase 2: Configuration Audit (Priority: HIGH)
**Objective:** Audit all `.vibe/agents/*.toml` files for correctness and completeness

- [ ] **Config Structure Validation**
  - [ ] List all 14 agent TOML files in `.vibe/agents/`
  - [ ] Verify each has required fields: `agent_type`, `display_name`, `description`
  - [ ] Check for valid `agent_type` values ("agent" or "subagent")
  - [ ] Document any missing required fields

- [ ] **Tool Configuration Audit**
  - [ ] For each agent, extract enabled_tools list
  - [ ] Cross-reference with Vibe Code builtin tools from VERIFIED_REFERENCE.md
  - [ ] Flag any non-existent tool names (silently ignored)
  - [ ] Flag any Claude Code tool names used in Vibe configs
  - [ ] Check for `skill` tool presence in each agent

- [ ] **Model Configuration Check**
  - [ ] Verify `active_model` field exists in each agent
  - [ ] Check if model names are valid (mistral-small, etc.)
  - [ ] Flag any agents without model configuration

- [ ] **System Prompt Resolution**
  - [ ] Identify all agents with `system_prompt_id` field
  - [ ] For each, check if referenced prompt file exists
  - [ ] Test resolution path: `.vibe/prompts/` vs repo root `prompts/`

### Phase 3: Skill Validation (Priority: HIGH)
**Objective:** Validate each skill's structure, frontmatter, and content

- [ ] **Skill Inventory**
  - [ ] List all skill directories in `skills/`
  - [ ] Count total skills and categorize by type
  - [ ] Verify each has `SKILL.md` file

- [ ] **Frontmatter Validation**
  - [ ] For each SKILL.md, parse YAML frontmatter
  - [ ] Verify required fields: `name`, `description`
  - [ ] Check for non-portable fields (e.g., `allowed-tools`)
  - [ ] Validate `compatibility` lists contain valid agent names
  - [ ] Flag any skills missing required fields

- [ ] **Content Analysis**
  - [ ] Check for tool-specific language in SKILL.md bodies
  - [ ] Search for hardcoded tool names (Read, Write, Edit, etc.)
  - [ ] Search for hardcoded paths (.claude/, .pi/, .vibe/)
  - [ ] Check for agent-specific assumptions

- [ ] **Line Count & Complexity**
  - [ ] Measure each SKILL.md line count
  - [ ] Flag skills exceeding 200 lines (context cost concern)
  - [ ] Calculate total always-on cost (sum of all descriptions)

### Phase 4: Cross-Agent Compatibility (Priority: HIGH)
**Objective:** Verify portability across Claude Code, Pi Agent, and Vibe Code

- [ ] **Agent Directory Structure**
  - [ ] Verify `.claude/agents/` exists and has agent files
  - [ ] Verify `.pi/agents/` exists and has agent files
  - [ ] Verify `.vibe/agents/` exists and has agent files
  - [ ] Compare agent lists across all three platforms

- [ ] **Skill Directory Symlinks**
  - [ ] Check `.claude/skills/` -> `../skills/` symlink
  - [ ] Check `.pi/skills/` -> `../skills/` symlink
  - [ ] Check `.vibe/skills/` -> `../skills/` symlink
  - [ ] Verify all symlinks are valid and point to correct targets

- [ ] **Tool Name Translation**
  - [ ] Build tool name mapping table (from AGENTS.md)
  - [ ] Verify Vibe Code uses correct names: `read_file`, `write_file`, `edit`, `bash`, `grep`
  - [ ] Verify Claude Code uses: `Read`, `Write`, `Edit`, `Bash`, `Grep`
  - [ ] Verify Pi Agent uses: `read`, `write`, `edit`, `bash`, `grep`
  - [ ] Check for inconsistencies in agent configs

- [ ] **Agent Type Consistency**
  - [ ] Compare agent_type across all three platforms
  - [ ] Flag any agents that are "agent" in one platform but "subagent" in another

### Phase 5: Path & Reference Audit (Priority: MEDIUM)
**Objective:** Find all stale, broken, or non-portable path references

- [ ] **Repository-Wide Path Search**
  - [ ] Search for `.claude/` references outside `.claude/` directory
  - [ ] Search for `.pi/` references outside `.pi/` directory
  - [ ] Search for `.vibe/` references outside `.vibe/` directory
  - [ ] Search for `~/.claude/`, `~/.pi/`, `~/.vibe/` patterns
  - [ ] Search for `CLAUDE.md`, `PI.md`, `VIBE.md` patterns

- [ ] **File Reference Validation**
  - [ ] Extract all file paths from markdown files
  - [ ] Test if each referenced file exists
  - [ ] Flag broken links with severity
  - [ ] Document relative vs absolute path usage

- [ ] **URL Validation**
  - [ ] Extract all URLs from markdown files
  - [ ] Test if each URL is reachable (for docs links)
  - [ ] Flag broken URLs

### Phase 6: Security & Permissions (Priority: MEDIUM)
**Objective:** Check for security issues and permission problems

- [ ] **Bash Tool Permissions**
  - [ ] Check which agents have `bash` tool enabled
  - [ ] Flag agents with bash enabled but no restrictions
  - [ ] Check for `bypass_tool_permissions` usage

- [ ] **Python Tool Permissions**
  - [ ] Check which agents have `python` tool enabled
  - [ ] Flag agents with python enabled (code execution risk)

- [ ] **File Write Permissions**
  - [ ] Check which agents have `write_file` or `edit` enabled
  - [ ] Document potential for unintended file modifications

- [ ] **Scratchpad Directory Usage**
  - [ ] Check if any agents reference scratchpad_dir
  - [ ] Verify scratchpad is used for safe file operations

### Phase 7: Performance & Cost Analysis (Priority: MEDIUM)
**Objective:** Identify context bloat and performance issues

- [ ] **Always-On Context Cost**
  - [ ] Calculate sum of all skill descriptions (from frontmatter)
  - [ ] Calculate AGENTS.md character count
  - [ ] Calculate total always-on cost
  - [ ] Compare with Vibe Code context limits

- [ ] **Per-Skill Invocation Cost**
  - [ ] Calculate line count for each SKILL.md body
  - [ ] Identify skills with highest invocation cost
  - [ ] Flag skills exceeding recommended size limits

- [ ] **Agent Configuration Bloat**
  - [ ] Count tools enabled per agent
  - [ ] Flag agents with excessive tool lists
  - [ ] Check for duplicate or redundant tool configurations

### Phase 8: Tool Name Consistency (Priority: HIGH)
**Objective:** Ensure correct tool names are used throughout

- [ ] **Vibe Code Tool Names** (from VERIFIED_REFERENCE.md)
  - [ ] Builtin tools: ask_user_question, bash, edit, grep, read_file, search_replace, todo, web_fetch, web_search, write_file
  - [ ] Note: `search_replace` exists (contrary to VERIFIED_REFERENCE.md note)
  - [ ] Wait - VERIFIED_REFERENCE.md says no `search_replace`, only `edit`

- [ ] **Agent Config Tool Names**
  - [ ] For each `.vibe/agents/*.toml`, extract tool names from `[toolname]` sections
  - [ ] Verify each tool name matches Vibe Code builtin list
  - [ ] Flag any mismatches or typos

- [ ] **Skill Content Tool References**
  - [ ] Search SKILL.md files for tool-specific language
  - [ ] Flag any direct tool name references (should be tool-agnostic)

### Phase 9: Symlink Integrity (Priority: MEDIUM)
**Objective:** Verify all symlinks are valid and point to correct targets

- [ ] **Skill Directory Symlinks**
  - [ ] Check `.claude/skills/` symlink target
  - [ ] Check `.pi/skills/` symlink target
  - [ ] Check `.vibe/skills/` symlink target
  - [ ] Verify targets exist and are accessible

- [ ] **Individual Skill Symlinks**
  - [ ] For each agent directory, check if skills are symlinked individually
  - [ ] Verify symlink targets for: timestamp, codeberg, etc.
  - [ ] Flag any broken symlinks

### Phase 10: Synthesis & Prioritization (Priority: CRITICAL)
**Objective:** Compile all findings into prioritized action items

- [ ] **Finding Compilation**
  - [ ] Aggregate all findings from Phases 1-9
  - [ ] Remove duplicates
  - [ ] Group by category (Configuration, Compatibility, Security, etc.)

- [ ] **Severity Classification**
  - [ ] CRITICAL: Causes silent failures, breaks functionality
  - [ ] HIGH: Causes errors, degrades performance significantly
  - [ ] MEDIUM: Causes warnings, minor degradation
  - [ ] LOW: Cosmetic, documentation issues

- [ ] **Impact Assessment**
  - [ ] For each finding, document affected components
  - [ ] Document user impact
  - [ ] Document fix complexity

- [ ] **Remediation Plan**
  - [ ] Create prioritized list of fixes
  - [ ] Estimate effort for each fix
  - [ ] Identify dependencies between fixes

---

## Validation Checklist

After executing the plan:

- [ ] All phases completed with checkboxes marked
- [ ] Findings file created: `main/audit-results/findings.md`
- [ ] Each finding has: ID, Severity, Description, Location, Impact, Fix
- [ ] Audit log created: `main/audit-results/audit-log.md`
- [ ] Summary report created: `main/audit-results/summary.md`
- [ ] Git diff reviewed for any accidental changes
- [ ] All generated files committed or documented

---

## Success Criteria

1. **Completeness:** All 10 phases executed
2. **Accuracy:** Findings verified against source code where possible
3. **Actionability:** Each finding has clear remediation steps
4. **Prioritization:** Findings ranked by severity and impact
5. **Reproducibility:** Process documented so it can be repeated

---

## Estimated Timeline

- Phase 0: 5 minutes
- Phase 1: 15 minutes (known issues validation)
- Phase 2: 20 minutes (configuration audit)
- Phase 3: 20 minutes (skill validation)
- Phase 4: 20 minutes (cross-agent compatibility)
- Phase 5: 15 minutes (path & reference audit)
- Phase 6: 10 minutes (security & permissions)
- Phase 7: 10 minutes (performance & cost)
- Phase 8: 10 minutes (tool name consistency)
- Phase 9: 10 minutes (symlink integrity)
- Phase 10: 20 minutes (synthesis)
- **Total Estimated: ~2.5 hours**

---

## Notes

- Reference VERIFIED_REFERENCE.md for Vibe Code specific behaviors
- The audit from 2026-08-22 found 7 agents missing `skill` tool - this is CRITICAL
- Stale path references are PORTABILITY issues
- Always verify findings against actual source code when possible
- Document assumptions and uncertainties for later validation

---

*Plan created: 2026-08-22*  
*Based on: docs/vibe/VERIFIED_REFERENCE.md, docs/audit-report-2026-08-22.md*  
*Repository: berzerk0/crispy-couscous*
