# Mailroom

> **Purpose:** Read-only staging area for content to be reviewed, remixed, and integrated into the main repository.

---

## 📦 What This Is

The **mailroom** is a **read-only archive** where content is dropped off for agents to:
- **Review** - Assess quality, relevance, and compatibility
- **Remix** - Adapt, combine, or transform for our needs
- **Harvest** - Extract useful patterns, skills, or documentation
- **Integrate** - Move validated content into the main repo structure

**Agents MUST NEVER write to this directory.** This is a one-way flow: content comes in, gets processed, and moves out to the appropriate location.

---

## 🎯 Workflow

### Step 1: Drop Off
Content is added to `mailroom/` by maintainers (human or automated). This can include:
- Skills from other repositories
- Documentation drops
- Research findings
- Experimental content
- Third-party content for review

### Step 2: Review
Agents read and assess content in the mailroom:
- Check for quality and relevance
- Verify licensing and attribution
- Assess compatibility with our standards
- Identify useful patterns or components

### Step 3: Process
Based on review, agents:
- **Accept as-is** - Move to appropriate location (skills/, docs/, etc.)
- **Adapt** - Modify for our conventions, then move
- **Extract** - Pull out useful parts, leave the rest
- **Reject** - Archive or delete if not useful

### Step 4: Integrate
Validated content is moved to its permanent home:
- Skills → `skills/` (library) or `.vibe/skills/` / `.claude/skills/` (live)
- Documentation → `docs/`
- Agents → `.vibe/agents/` or `.claude/agents/`
- Archive → `archive/`

### Step 5: Cleanup
After processing, the mailroom item is:
- **Deleted** - If fully processed
- **Archived** - If partially useful (moved to `archive/`)
- **Left for reference** - If it's a reference that should remain

---

## 📁 Current Contents

| Item | Type | Status | Notes |
|------|------|--------|-------|
| `SKILL.md` | Skill | Pending | challenge-my-thinking (duplicate of skills/) |
| `skill-extractor/` | Skill + refs | Pending | Skill extraction guidance |
| `skill-validator/` | Skill | Pending | SKILL.md validation |
| `multi-agent-drop-823/` | Documentation | **Priority** | Multi-agent standards from crispy-couscous |

---

## 🔍 Processing Priority

### High Priority (Process First)
1. **`multi-agent-drop-823/`** - Comprehensive multi-agent standards documentation
   - Contains verified research on cross-agent compatibility
   - Includes tool-specific behaviors (Claude, Pi, Vibe)
   - Has standards references (Agent Skills, AGENTS.md, MCP)
   - **Action:** Review, adapt for our repo, integrate into docs/

### Medium Priority
2. **`skill-extractor/`** - Skill extraction methodology
   - Contains quality guide, lifecycle, template
   - **Action:** Review for our skill-creation workflows

3. **`skill-validator/`** - SKILL.md validation
   - **Action:** Review, potentially add as a tool

### Low Priority
4. **`SKILL.md`** - challenge-my-thinking
   - Appears to be a duplicate of `skills/challenge-my-thinking/SKILL.md`
   - **Action:** Verify, delete if duplicate

---

## 📋 Review Guidelines

### For Skills
When reviewing a skill in the mailroom:

1. **Check frontmatter:**
   - Has `name`, `description`, `license`?
   - Has `compatibility` list?
   - Has `allowed-tools` (Vibe) or equivalent?

2. **Assess quality:**
   - Is the description specific and actionable?
   - Does it have clear "When to Use" section?
   - Are there concrete examples?
   - Is it under 500 lines?

3. **Check compatibility:**
   - Uses common tools (read_file, grep, bash)?
   - No agent-specific tool names?
   - Works in both Vibe and Claude?

4. **Verify licensing:**
   - Has clear license?
   - Third-party content attributed?
   - No proprietary content?

### For Documentation
When reviewing documentation:

1. **Check accuracy:**
   - Claims verified against official sources?
   - Has citations/references?
   - Up-to-date?

2. **Assess relevance:**
   - Applies to our repo's scope?
   - Cross-agent compatible?
   - Actionable?

3. **Check organization:**
   - Well-structured?
   - Easy to navigate?
   - Consistent style?

---

## 🛡️ Rules for Agents

### ❌ NEVER Do These
- **Write to mailroom/** - This is READ-ONLY
- **Modify mailroom contents** - Even "fixing typos"
- **Delete from mailroom/** - Only maintainers clean up
- **Assume content is production-ready** - Always review first

### ✅ DO These
- **Read mailroom contents** - For review and processing
- **Copy from mailroom/** - To appropriate locations
- **Reference mailroom/** - In documentation
- **Report issues** - With mailroom content
- **Suggest processing** - To maintainers

---

## 🎯 Processing Decisions

### Accept as-is
Content that:
- Follows our conventions
- Has proper licensing
- Is cross-agent compatible
- Fits our structure

**Action:** Copy to appropriate location, add to index

### Adapt
Content that:
- Is useful but needs modification
- Uses wrong tool names
- Has formatting issues
- Needs restructuring

**Action:** Create adapted version, note original source

### Extract
Content that:
- Has useful parts among irrelevant material
- Contains patterns worth preserving
- Has examples we can learn from

**Action:** Extract useful parts, create new content

### Reject
Content that:
- Is low quality
- Has licensing issues
- Is not relevant
- Is duplicate

**Action:** Archive to `archive/` or delete

---

## 📊 Integration Locations

| Content Type | Destination | Example |
|--------------|-------------|---------|
| Portable skills | `skills/<name>/` | `skills/code-review/` |
| Vibe live skills | `.vibe/skills/<name>/` | `.vibe/skills/cross-agent-compat/` |
| Claude commands | `.claude/commands/<name>.md` | `.claude/commands/code-review.md` |
| Cross-agent docs | `docs/shared/` | `docs/shared/workflows.md` |
| Vibe-specific docs | `docs/vibe/` | `docs/vibe/internals.md` |
| Claude-specific docs | `docs/claude/` | `docs/claude/README.md` |
| Reference material | `docs/` | `docs/cross-tool-notes.md` |
| Archive | `archive/` | `archive/old-goblins.txt` |

---

## 🔗 Related Files

- [AGENTS.md](../AGENTS.md) - Shared agent instructions
- [skills/README.md](../skills/README.md) - Skill library index
- [docs/shared/README.md](../docs/shared/README.md) - Shared docs index
- [archive/README.md](../archive/README.md) - Archive index

---

## 📝 Template: Processing a Mailroom Item

```markdown
# Processing: [Item Name]

**Location:** mailroom/[path]
**Type:** [skill/docs/research]
**Date Added:** [date]

## Assessment

### Quality
- [ ] Follows conventions
- [ ] Well-structured
- [ ] Actionable content

### Compatibility
- [ ] Cross-agent compatible
- [ ] Uses common tools
- [ ] No agent-specific dependencies

### Licensing
- [ ] Has license
- [ ] Third-party attributed
- [ ] No proprietary content

### Relevance
- [ ] Fits repo scope
- [ ] Useful for our workflows
- [ ] Not duplicate

## Decision

**Action:** [Accept/Adapt/Extract/Reject]
**Destination:** [path]
**Notes:** [any notes]

## Processing Steps

1. [ ] Review content
2. [ ] Make decision
3. [ ] Copy/adapt/extract
4. [ ] Place in destination
5. [ ] Update indexes
6. [ ] Test if applicable
```

---

## 🏁 Quick Reference

```bash
# List mailroom contents
ls -la mailroom/

# Read a mailroom item
read_file: mailroom/[path]/[file]

# Copy to skills library
cp -r mailroom/[skill] skills/[skill]

# Copy to live Vibe skills
cp -r mailroom/[skill] .vibe/skills/[skill]

# Move to docs
cp mailroom/[doc] docs/[category]/[doc]
```

---

*Directory purpose: Read-only staging area*
*Maintainer: @berzerk0*
*Last updated: 2026-08-23*
