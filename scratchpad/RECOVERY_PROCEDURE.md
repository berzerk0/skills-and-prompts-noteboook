# Recovery Procedure: Restoring File Editing Functionality

**Created:** 2026-08-24  
**Status:** Functional with workarounds  
**Priority:** HIGH - Required for repository maintenance

---

## Immediate Status

**Current State:**
- ✅ Can READ all files reliably
- ✅ Can CREATE new files reliably  
- ❌ Cannot MODIFY existing files with ``edit``
- ⚠️ Can MODIFY with workarounds (python scripts)

**Workarounds Available:**
- `scratchpad/edit_file.py` - Unicode-aware file editor
- `scratchpad/FILE_EDITING_WORKAROUNDS.md` - Complete guide
- `scratchpad/ERROR_LOG_2026-08-24.md` - Error documentation

---

## Step 1: Verify Current State

Run these commands to confirm the issue:

```bash
# Test 1: Can we read files?
read_file: AGENTS.md

# Test 2: Can we create files?
write_file: /tmp/test_file.md, "# Test\nThis is a test file."

# Test 3: Can we use `edit`? (Expected: FAIL)
`edit`: {"file_path": "AGENTS.md", "content": [{"old_str": "it is for human-maintained drop-offs only.", "new_str": "it is for human-maintained drop-offs only. TEST"}]}

# Test 4: Can we use python workaround?
bash: "python3 scratchpad/edit_file.py AGENTS.md 'it is for human-maintained drop-offs only.' 'it is for human-maintained drop-offs only. TEST'"

# Test 5: Check git status
git status
```

---

## Step 2: Restore From Backups (If Needed)

If files were corrupted during editing attempts:

```bash
# List any backup files
bash: "find . -name '*.backup' -o -name '*.bak' -o -name '*.orig'"

# Restore AGENTS.md from git
git checkout AGENTS.md

# Restore all modified files
git checkout .

# Or restore from specific backup
bash: "cp /tmp/agents_backup.md AGENTS.md"
```

---

## Step 3: Implement Workarounds

### For Single File Edits

Use the python editor script:

```bash
# Edit a single occurrence
bash: "python3 scratchpad/edit_file.py AGENTS.md 'OLD_TEXT' 'NEW_TEXT'"

# Edit all occurrences
bash: "python3 scratchpad/edit_file.py --all AGENTS.md 'OLD_TEXT' 'NEW_TEXT'"

# Append to file
bash: "python3 scratchpad/edit_file.py --append AGENTS.md 'NEW_CONTENT'"

# Prepend to file
bash: "python3 scratchpad/edit_file.py --prepend AGENTS.md 'NEW_CONTENT'"
```

### For Batch Operations

Use the specialized scripts:

```bash
# Fix all skill frontmatter
bash: "python3 scratchpad/fix_skills.py"

# Create all missing READMEs
bash: "python3 scratchpad/create_readmes.py"
```

### For Symlink Creation

```bash
# Create symlinks for .vibe/skills/
bash: "mkdir -p .vibe/skills && cd .vibe/skills && for dir in ../../skills/*/; do ln -sf \"$dir\" .; done"

# Create symlinks for .claude/skills/
bash: "mkdir -p .claude/skills && cd .claude/skills && for dir in ../../skills/*/; do ln -sf \"$dir\" .; done"
```

---

## Step 4: Verify Workarounds Work

Test each workaround before using it on important files:

```bash
# Test 1: Create a test file
write_file: /tmp/test_edit.md, "# Test\nLine 1\nLine 2\nLine 3"

# Test 2: Edit with python
bash: "python3 scratchpad/edit_file.py /tmp/test_edit.md 'Line 2' 'Line 2 MODIFIED'"

# Test 3: Verify the edit
read_file: /tmp/test_edit.md

# Test 4: Check git diff
git diff /tmp/test_edit.md

# Test 5: Clean up
bash: "rm /tmp/test_edit.md /tmp/test_edit.md.backup"
```

If all tests pass, workarounds are functional.

---

## Step 5: Implement User's Directives

Now that workarounds are verified, implement the 4 directives:

### Directive 0: Clarify archive vs mailroom

```bash
# Add archive section to AGENTS.md
python3 scratchpad/edit_file.py AGENTS.md \
  'current contents inventory, and priority list.' \
  'current contents inventory, and priority list.\n\n---\n\n## Archive (Read-Only Deprecated Content)\n\nThe `archive/` directory is a **read-only** storage area...'

# Update mailroom section
python3 scratchpad/edit_file.py AGENTS.md \
  'it is for human-maintained drop-offs only.' \
  'it is for human-maintained drop-offs only. **Agents should only read from mailroom/ when the user explicitly requests it.**'

# Update CLAUDE.md
python3 scratchpad/edit_file.py CLAUDE.md \
  'for processing guidelines.' \
  'for processing guidelines.\n\n## Archive\n\nBoth `mailroom/` and `archive/` are **read-only**...'
```

### Directive 1: Fix skills with symlink solution

```bash
# First, standardize all skill frontmatter
python3 scratchpad/fix_skills.py

# Then create symlinks
bash: "mkdir -p .vibe/skills .claude/skills"
bash: "cd .vibe/skills && for dir in ../../skills/*/; do ln -sf \"$dir\" .; done"
bash: "cd .claude/skills && for dir in ../../skills/*/; do ln -sf \"$dir\" .; done"

# Update config
python3 scratchpad/edit_file.py .vibe/config.toml \
  '  \"./skills\",  # Portable skill library' \
  '  # \"./skills\",  # Portable skill library (now using symlinks)'
```

### Directive 2: Work in the docs

```bash
# Fix broken links in docs/shared/README.md
python3 scratchpad/edit_file.py docs/shared/README.md \
  '| [workflows.md](workflows.md) | Cross-agent workflow patterns |' \
  ''

python3 scratchpad/edit_file.py docs/shared/README.md \
  '| [patterns.md](patterns.md) | Reusable code patterns for both agents |' \
  ''

python3 scratchpad/edit_file.py docs/shared/README.md \
  '| [best-practices.md](best-practices.md) | General best practices |' \
  ''

# Add self-checks reference to AGENTS.md
python3 scratchpad/edit_file.py AGENTS.md \
  'See [self-checks/README.md](self-checks/README.md) for audit format and structure.' \
  'See [self-checks/README.md](self-checks/README.md) for audit format and structure.\n\n**Agents should check self-checks/ regularly to understand repository health.**'
```

### Directive 3: Add all missing READMEs

```bash
# Create all missing READMEs
python3 scratchpad/create_readmes.py
```

---

## Step 6: Final Verification

After implementing all directives:

```bash
# Check git status
git status

# Review all changes
git diff

# Check for any corrupted files
git diff --check

# Verify symlinks work
bash: "ls -la .vibe/skills/ && ls -la .claude/skills/"

# Test a symlinked skill
read_file: .vibe/skills/ask-questions-if-underspecified/SKILL.md
```

---

## Step 7: Commit Changes (If All Verified)

```bash
# Add all changes
git add -A

# Commit with descriptive message
git commit -m "Fix skills, docs, and add archive/mailroom clarification

- Add Archive section to AGENTS.md clarifying read-only nature
- Standardize all skill frontmatter with proper fields
- Implement symlink solution for cross-agent skill sharing
- Fix broken links in documentation
- Add missing README.md files to all directories
- Update CLAUDE.md with archive reference

Closes: User directives 0-3"

# Push if authorized
git push
```

---

## Emergency Recovery

If something goes wrong:

```bash
# Full reset to last known good state
git reset --hard HEAD

# Or reset specific files
git checkout AGENTS.md CLAUDE.md README.md

# Or restore from backups
bash: "cp /tmp/*.backup . 2>/dev/null || echo 'No backups found'"
```

---

## Summary Checklist

| Task | Command | Status |
|------|---------|--------|
| Verify current state | `read_file`, `write_file`, ``edit`` tests | ⬜ |
| Restore from backups | `git checkout .` or `cp *.backup` | ⬜ |
| Test workarounds | python scripts, bash commands | ⬜ |
| Implement Directive 0 | archive/mailroom clarification | ⬜ |
| Implement Directive 1 | skills + symlinks | ⬜ |
| Implement Directive 2 | docs fixes | ⬜ |
| Implement Directive 3 | READMEs | ⬜ |
| Final verification | `git diff --check` | ⬜ |
| Commit changes | `git add -A && git commit` | ⬜ |

---

## Files Created for Recovery

| File | Purpose |
|------|---------|
| `scratchpad/RECOVERY_PROCEDURE.md` | This document |
| `scratchpad/ERROR_LOG_2026-08-24.md` | Error documentation |
| `scratchpad/FILE_EDITING_WORKAROUNDS.md` | Complete workaround guide |
| `scratchpad/edit_file.py` | Unicode-aware file editor |
| `scratchpad/fix_skills.py` | Batch skill frontmatter fixer |
| `scratchpad/create_readmes.py` | README creation helper |

---

*Document created: 2026-08-24*
*Follow this procedure to restore full functionality*
