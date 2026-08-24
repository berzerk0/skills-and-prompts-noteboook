---
name: cross-agent-compat
description: Cross-agent compatibility helper for Mistral Vibe and Claude Code. Provides tool translation, pattern guidance, and dual-agent workflows.
license: MIT
compatibility: [claude, pi, vibe]
metadata:
  author: "berzerk0"
  repository: "https://github.com/berzerk0/skills-and-prompts-notebook"
  tags: ["compatibility", "claude", "cross-agent", "translation"]
user-invocable: true
---

# Cross-Agent Compatibility Skill

> **Purpose:** Enable seamless collaboration between Mistral Vibe Code and Claude Code. This skill provides tool translation, pattern guidance, and best practices for building artifacts that work in both agents.

---

## 🎯 When to Use This Skill

Invoke this skill when:
- You need to create content that works in both Vibe and Claude
- You're translating between agent-specific formats
- You want to follow cross-compatible patterns
- You need to understand the differences between the two agents

**Invocation:** `/cross-agent-compat` or let the model invoke it automatically.

---

## 📋 Tool Translation Table

### File Operations

| Action | Vibe | Claude | Notes |
|--------|------|--------|-------|
| Read file | `read_file: path` | `Read: path` | Direct equivalent |
| Write file | `write_file: path, content` | `Write: path, content` | Direct equivalent |
| Edit file | `edit: old, new` | `Edit: path, old, new` | Vibe: `edit` NOT `search_replace` |
| Create file | `write_file: path, content` | `Write: path, content` | Both create if not exists |

### Search Operations

| Action | Vibe | Claude | Notes |
|--------|------|--------|-------|
| Search files | `grep: pattern, path` | `Grep: pattern, path` | Direct equivalent |
| List files | `bash: "ls -la path"` | `Bash: "ls -la path"` | Use shell commands |
| Find files | `bash: "find path -name pattern"` | `Bash: "find path -name pattern"` | No native glob |

### Shell Operations

| Action | Vibe | Claude | Notes |
|--------|------|--------|-------|
| Run command | `bash: "command"` | `Bash: "command"` | Direct equivalent |
| Stdin input | `bash_stdin: "command", "input"` | `Bash: "echo input | command"` | Vibe has dedicated tool |
| Log file | `bash_log_file: "command", "logfile"` | `Bash: "command > logfile 2>&1"` | Vibe has dedicated tool |

### Code Operations

| Action | Vibe | Claude | Notes |
|--------|------|--------|-------|
| Task delegation | `task: "description"` | `Task: "description"` | Both spawn subagents |
| Todo management | `todo: [{"content": "task", "status": "in_progress"}]` | `Task: "description"` | Vibe has structured todo |
| Invoke skill | `skill: skill-name` | N/A | Claude uses commands |

### Web Operations

| Action | Vibe | Claude | Notes |
|--------|------|--------|-------|
| Fetch URL | `web_fetch: url` | `Fetch: url` | Direct equivalent |
| Web search | `web_search: query` | `WebSearch: query` | Direct equivalent |

---

## 🏗️ Cross-Compatible Patterns

### Pattern 1: Universal File Reader

```python
# This pattern works in both Vibe and Claude

# Read a file
read_file: path/to/file.txt

# Process content
# ... your logic here

# Write result
write_file: path/to/result.txt, "processed content"
```

### Pattern 2: Safe Directory Listing

```bash
# Works in both - use bash for directory operations
bash: "ls -la /path/to/directory"

# For recursive listing
bash: "find /path/to/directory -type f -name '*.py'"

# For filtering
bash: "ls /path/to/directory | grep pattern"
```

### Pattern 3: Multi-File Search

```bash
# Search across multiple files - works in both
grep: "search_pattern", "/path/to/directory"

# For more complex searches
bash: "rg 'pattern' /path/to/directory"
```

### Pattern 4: Task Delegation

```bash
# Spawn a subagent/task for complex work
task: "Analyze the codebase for security issues. Focus on: hardcoded secrets, dangerous functions, and permission issues. Write findings to /tmp/security-audit.md"

# Then read the results
read_file: /tmp/security-audit.md
```

**Vibe-specific:** Subagents receive a `scratchpad_dir` for file handoff
**Claude-specific:** Tasks run in isolated contexts with their own tool access

---

## ⚠️ Critical Differences to Remember

### 1. Tool Name: Edit vs Search/Replace

**Vibe:** Uses `edit` tool
```
edit:
  file_path: "file.py"
  old_str: "old_code()"
  new_str: "new_code()"
```

**Claude:** Uses `Edit` tool (which is search/replace)
```
Edit: file.py, "old_code()", "new_code()"
```

**⚠️ DANGER:** Vibe has **NO** `search_replace` tool. Using it will **silently fail**.

### 2. Silent Tool Name Failures

**Vibe behavior:** If you specify a tool name that doesn't exist in `allowed-tools` or `enabled_tools`, it is **silently ignored** - no error, no warning, just removed from available tools.

**Claude behavior:** Similar silent failure for unrecognized tools.

**Best practice:** Always verify tool names against the official lists.

### 3. Skill vs Command System

**Vibe:** Skills are directories with `SKILL.md` files, discovered from `.vibe/skills/`
**Claude:** Skills are installed from marketplace or defined via MCP servers

**Cross-agent approach:** Document your capabilities in both formats.

### 4. Subagent Capabilities

**Vibe subagents:**
- Cannot use `ask_user_question`
- Have access to `scratchpad_dir`
- Fresh context, no parent history
- Can use all tools except those explicitly restricted

**Claude tasks:**
- Cannot ask user questions
- Run in isolated contexts
- Can use tools based on parent configuration

### 5. Configuration Locations

| Config | Vibe | Claude |
|--------|------|--------|
| User config | `~/.vibe/config.toml` | `~/.claude/settings.json` |
| Project config | `./.vibe/` | `./.claude/` |
| Skills | `~/.vibe/skills/` or `./.vibe/skills/` | Marketplace or `~/.claude/skills/` |
| Agents | `~/.vibe/agents/*.toml` | N/A (uses commands) |

---

## 📁 Repository Structure Guide

This repository follows a dual-compatibility structure:

```
skills-and-prompts-notebook/
├── AGENTS.md                    # Shared compatibility layer (read by both)
├── CLAUDE.md                    # Pointer to AGENTS.md for Claude
├── README.md                    # Repository overview
│
├── .vibe/                       # Mistral Vibe configuration
│   ├── skills/                 # Vibe skills (SKILL.md format)
│   │   ├── cross-agent-compat/ # This skill
│   │   ├── vibe-internals/    # Vibe internals reference
│   │   └── ...
│   ├── agents/                 # Vibe agent configs
│   │   └── default.toml
│   └── prompts/                 # Custom system prompts
│
├── .claude/                     # Claude Code configuration
│   ├── skills/                 # Claude skills (future)
│   └── commands/               # Custom Claude commands
│
├── docs/                        # Documentation
│   ├── shared/                 # Cross-agent docs
│   ├── vibe/                   # Vibe-specific docs
│   │   └── internals.md        # Vibe internals deep dive
│   └── claude/                 # Claude-specific docs
│
├── skills/                      # Portable skill library (NOT live path)
│   ├── ask-questions-if-underspecified/
│   ├── challenge-my-thinking/
│   └── ...
│
└── notebooks/                   # Working documents
    └── ...
```

**Key insight:** `skills/` is a **library** of portable SKILL.md files. To use them, copy or symlink to `.vibe/skills/` (Vibe) or `.claude/skills/` (Claude).

---

## 🔧 Workflow: Creating Cross-Compatible Content

### Step 1: Define the Capability

```markdown
# My New Capability

## Purpose
What this does and why it's useful.

## Tools Required
- read_file
- write_file
- grep
- bash

## Usage Examples
```

### Step 2: Create Vibe Skill

```bash
# Create skill directory
mkdir -p .vibe/skills/my-capability

# Create SKILL.md
cat > .vibe/skills/my-capability/SKILL.md << 'EOF'
---
name: my-capability
description: Description here
user-invocable: true
---

# My Capability

[Content from Step 1]
EOF
```

### Step 3: Create Claude Equivalent

```bash
# Create Claude command/skill
mkdir -p .claude/commands
cat > .claude/commands/my-capability.md << 'EOF'
# My Capability

## Tools
- Read
- Write
- Grep
- Bash

## Usage
[Adapted content for Claude]
EOF
```

### Step 4: Add to Library (Optional)

```bash
# Add to skills/ library for sharing
cp -r .vibe/skills/my-capability skills/
# Update skills/README.md with source/license info
```

### Step 5: Test in Both Agents

```bash
# Test with Vibe
vibe -p "test my-capability" --max-turns 1

# Test with Claude
claude "test my-capability"
```

---

## 🎓 Best Practices

### 1. Always Use Common Tools

Prefer tools that exist in both agents:
- ✅ `read_file` / `Read`
- ✅ `write_file` / `Write`
- ✅ `grep` / `Grep`
- ✅ `bash` / `Bash`
- ✅ `web_fetch` / `Fetch`
- ✅ `web_search` / `WebSearch`

Avoid agent-specific tools when possible.

### 2. Document Tool Requirements

Always explicitly state which tools your skill/prompt requires:

```markdown
## Required Tools
- read_file
- write_file
- grep
- bash
```

### 3. Handle Missing Tools Gracefully

```python
# Check if a tool is available before using it
# In Vibe, you can check available tools via the skill system
# In both, you can use bash as a fallback

# Instead of:
grep: "pattern", "file"

# Use:
bash: "grep 'pattern' file || echo 'grep not available, using alternative'"
```

### 4. Keep Content Modular

- Small, focused skills > monolithic skills
- Single-purpose prompts > multi-purpose prompts
- Easy to test, easy to maintain

### 5. Test Early and Often

Test in both agents before committing:
- Vibe: `vibe -p "test" --max-turns 1`
- Claude: `claude "test"`

---

## 🐛 Common Pitfalls and Fixes

### Pitfall 1: Using `search_replace` in Vibe

**Symptom:** Edit operations silently fail
**Cause:** Vibe has no `search_replace` tool
**Fix:** Use `edit` tool instead

### Pitfall 2: Silent Tool Name Typos

**Symptom:** Tools don't work, no error message
**Cause:** Unrecognized tool names are silently ignored
**Fix:** Verify all tool names against official lists

### Pitfall 3: Assuming Agent-Specific Features

**Symptom:** Works in one agent, fails in another
**Cause:** Using agent-specific features without fallbacks
**Fix:** Use common denominator tools and patterns

### Pitfall 4: Large Skill Files

**Symptom:** High token usage, context limits
**Cause:** Skill content loaded into context on invocation
**Fix:** Keep skill bodies concise, move examples to separate files

### Pitfall 5: Missing Frontmatter in Vibe Skills

**Symptom:** Skill not discovered or loaded
**Cause:** Missing or malformed YAML frontmatter
**Fix:** Ensure SKILL.md has valid frontmatter with `name` and `description`

---

## 📊 Performance Optimization

### Vibe-Specific

1. **Progressive Skill Loading:**
   - Enabled but uninvoked: Only name, description, path in system prompt (cheap)
   - On invocation: Full content loaded once, then resident
   - **Action:** Keep descriptions concise, skill bodies focused

2. **AGENTS.md Cost:**
   - Loaded every turn, resident in context
   - **Action:** Keep AGENTS.md concise, budget every line

3. **Tool Verification:**
   - Unrecognized tools silently ignored
   - **Action:** Always verify tool names

### Claude-Specific

1. **MCP Server Overhead:**
   - Each MCP server adds to context
   - **Action:** Only enable necessary servers

2. **Marketplace Skills:**
   - Installed skills add to system prompt
   - **Action:** Only install needed skills

---

## 🔗 Related Resources

### Internal
- [AGENTS.md](../../AGENTS.md) - Repository compatibility layer
- [docs/cross-tool-notes.md](../../docs/cross-tool-notes.md) - Tool translation reference
- [skills/README.md](../../skills/README.md) - Skill library index

### External
- [Mistral Vibe Docs](https://docs.mistral.ai/vibe/)
- [Claude Code Docs](https://docs.claude.com/en/docs)
- [Mistral Vibe Source](https://github.com/mistralai/mistral-vibe)
- [vibe-container](https://github.com/berzerk0/vibe-container) - Sandboxed Vibe devcontainer
- [cl-repo](https://github.com/berzerk0/cl-repo) - Verified Vibe internals reference

---

## 🏁 Quick Checklist

Before deploying cross-compatible content:

- [ ] Uses only common tools (read_file, write_file, grep, bash, etc.)
- [ ] No `search_replace` in Vibe content (use `edit`)
- [ ] All tool names verified against official lists
- [ ] Vibe skill has proper frontmatter (name, description, allowed-tools)
- [ ] Claude equivalent created (command or skill)
- [ ] Documentation added to docs/shared/
- [ ] Tested with Vibe: `vibe -p "test" --max-turns 1`
- [ ] Tested with Claude: `claude "test"`
- [ ] Token usage is reasonable
- [ ] Error handling is graceful

---

*Skill version: 1.0.0*
*Last updated: 2026-08-23*
*Compatibility: Mistral Vibe >=2.24.0, Claude Code >=1.0*
