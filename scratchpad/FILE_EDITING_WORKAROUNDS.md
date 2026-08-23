# File Editing Workarounds for Vibe Code

**Created:** 2026-08-24  
**Purpose:** Patch around file editing failures to restore functionality  
**Status:** Active workarounds documented

---

## Quick Reference: What Works vs What Doesn't

| Operation | Tool | Status | Notes |
|-----------|------|--------|-------|
| Read file | `read_file` | ✅ WORKS | Use this for all reads |
| Create new file | `write_file` | ✅ WORKS | Use this for new files |
| Modify existing | `search_replace` | ❌ BROKEN | Do not use |
| Modify existing | `bash` + `sed` | ⚠️ UNRELIABLE | Unicode issues |
| Modify existing | Python script | ⚠️ PARTIAL | Needs unicode normalization |
| List files | `bash` + `ls`/`find` | ✅ WORKS | Use for discovery |
| Git operations | `bash` + `git` | ✅ WORKS | Use for verification |

---

## Workaround 1: Create-Then-Replace Pattern

**Use Case:** Modifying existing files when `search_replace` fails

**Method:**
1. Read the original file
2. Create a NEW file with modifications
3. Replace the old file with the new one

**Template:**
```bash
# Step 1: Read original
read_file: /path/to/file.md

# Step 2: Create modified version
write_file: /tmp/file.md.new, "[modified content]"

# Step 3: Replace (using bash)
bash: "cp /tmp/file.md.new /path/to/file.md && rm /tmp/file.md.new"

# Step 4: Verify
git diff /path/to/file.md
```

**Example:**
```bash
# Modify AGENTS.md
read_file: AGENTS.md
write_file: /tmp/AGENTS.md.new, "[content with archive section added]"
bash: "cp /tmp/AGENTS.md.new AGENTS.md && rm /tmp/AGENTS.md.new"
git diff AGENTS.md
```

---

## Workaround 2: Python Script with Unicode Normalization

**Use Case:** String replacement in files with unicode characters

**Template:**
```python
#!/usr/bin/env python3
def normalize_text(text):
    """Normalize unicode characters to ASCII equivalents."""
    replacements = {
        '\u2014': '--',    # em dash
        '\u2013': '-',     # en dash
        '\u2192': '->',    # right arrow
        '\u2190': '<-',    # left arrow
        '\u0014': '-',     # various dashes
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def edit_file(path, old_text, new_text):
    """Safely edit a file with unicode normalization."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_normalized = normalize_text(old_text)
    new_normalized = normalize_text(new_text)
    content_normalized = normalize_text(content)
    
    if old_normalized in content_normalized:
        content = content.replace(old_normalized, new_normalized, 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Usage
if edit_file('AGENTS.md', 
             'it is for human-maintained drop-offs only.',
             'it is for human-maintained drop-offs only. **Agents should only read from mailroom/ when the user explicitly requests it.**'):
    print("Success")
else:
    print("Pattern not found")
```

**Save as:** `scratchpad/edit_file.py`

**Run with:**
```bash
bash: "python3 scratchpad/edit_file.py"
```

---

## Workaround 3: Full File Rewrite with Backup

**Use Case:** Complex modifications where line-by-line editing is needed

**Template:**
```python
#!/usr/bin/env python3
import sys

def backup_file(path):
    """Create backup before editing."""
    import shutil
    backup_path = f"{path}.backup"
    shutil.copy2(path, backup_path)
    return backup_path

def restore_file(path):
    """Restore from backup if edit fails."""
    backup_path = f"{path}.backup"
    import shutil
    shutil.copy2(backup_path, path)
    print(f"Restored {path} from backup")

def edit_file_lines(path, modifications):
    """
    Edit file by line modifications.
    modifications: list of (line_number, new_text) tuples
    """
    backup_file(path)
    
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Sort modifications by line number descending
    modifications.sort(key=lambda x: x[0], reverse=True)
    
    for line_num, new_text in modifications:
        if line_num < len(lines):
            lines[line_num] = new_text + '\n' if not new_text.endswith('\n') else new_text
        else:
            print(f"Warning: Line {line_num} out of range")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    # Verify
    import subprocess
    result = subprocess.run(['git', 'diff', path], capture_output=True, text=True)
    print(result.stdout)
    
    return True

# Usage example
edit_file_lines('AGENTS.md', [
    (121, 'The `mailroom/` directory is a **read-only** staging area for content to be reviewed,\nremixed, harvested, and integrated into the main repository. **Agents MUST NEVER write\nto this directory** -- it is for human-maintained drop-offs only. **Agents should only\nread from mailroom/ when the user explicitly requests it.**'),
])
```

**Save as:** `scratchpad/edit_file_lines.py`

---

## Workaround 4: Batch File Creation

**Use Case:** Creating multiple files with similar content

**Template:**
```python
#!/usr/bin/env python3

# Define the standard frontmatter template
FRONTMATTER_TEMPLATE = """---
name: {name}
description: {description}
license: {license}
compatibility:
  - vibe: ">=2.24.0"
  - claude: ">=1.0.0"
user-invocable: {user_invocable}
allowed-tools:
  - read_file
  - write_file
  - grep
  - bash
---

"""

# List of skills to fix
SKILLS_TO_FIX = [
    {
        'path': 'skills/ask-questions-if-underspecified/SKILL.md',
        'name': 'ask-questions-if-underspecified',
        'description': 'Clarify requirements before implementing. Use when serious doubts arise.',
        'license': 'MIT',
        'user_invocable': 'true',
    },
    # Add all other skills here
]

def fix_skill_frontmatter(skill_info):
    """Add standard frontmatter to a skill."""
    import os
    
    # Read existing file
    with open(skill_info['path'], 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has frontmatter
    if content.startswith('---'):
        # Has frontmatter, need to merge
        print(f"{skill_info['path']} already has frontmatter - manual merge needed")
        return False
    
    # Add frontmatter
    frontmatter = FRONTMATTER_TEMPLATE.format(**skill_info)
    new_content = frontmatter + content
    
    # Write back
    with open(skill_info['path'], 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Fixed: {skill_info['path']}")
    return True

# Fix all skills
for skill in SKILLS_TO_FIX:
    fix_skill_frontmatter(skill)
```

**Save as:** `scratchpad/fix_skills.py`

---

## Workaround 5: Symlink Creation

**Use Case:** Creating symlinks for cross-agent skill sharing

**Template:**
```bash
# Create all symlinks for .vibe/skills/
bash: "mkdir -p .vibe/skills && cd .vibe/skills && for dir in ../../skills/*/; do ln -sf "$dir" .; done"

# Create all symlinks for .claude/skills/
bash: "mkdir -p .claude/skills && cd .claude/skills && for dir in ../../skills/*/; do ln -sf "$dir" .; done"

# Verify symlinks
bash: "ls -la .vibe/skills/ && ls -la .claude/skills/"
```

**Note:** This assumes all skills in `skills/` should be symlinked. Adjust as needed.

---

## Workaround 6: README Creation Helper

**Use Case:** Creating multiple README.md files with consistent format

**Template:**
```python
#!/usr/bin/env python3

README_TEMPLATE = """# {title}

{purpose}

## Usage
{usage}

## Related Files
{related}

*Last updated: 2026-08-24*
"""

READMES = [
    {
        'path': '.vibe/prompts/README.md',
        'title': 'Vibe Prompts',
        'purpose': 'Custom system prompts for Mistral Vibe Code.',
        'usage': 'Prompts in this directory are loaded by Vibe\'s configuration.',
        'related': '- [.vibe/config.toml](../config.toml)\n- [AGENTS.md](../../AGENTS.md)',
    },
    # Add other READMEs here
]

def create_readme(readme_info):
    """Create a README.md file."""
    import os
    
    content = README_TEMPLATE.format(**readme_info)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(readme_info['path']), exist_ok=True)
    
    with open(readme_info['path'], 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Created: {readme_info['path']}")

# Create all READMEs
for readme in READMES:
    create_readme(readme)
```

**Save as:** `scratchpad/create_readmes.py`

---

## Verification Checklist

After any file modification, run these checks:

```bash
# Check 1: Git status
git status

# Check 2: Git diff for specific file
git diff /path/to/file.md

# Check 3: Line count
wc -l /path/to/file.md

# Check 4: Beginning of file
head -5 /path/to/file.md

# Check 5: End of file
tail -5 /path/to/file.md

# Check 6: File encoding
file /path/to/file.md

# Check 7: Unicode check
grep -P '\p{Em}' /path/to/file.md  # Check for em dashes
```

---

## Recovery Procedures

### If File Becomes Corrupted

```bash
# Step 1: Restore from git
git checkout /path/to/file.md

# Step 2: If git checkout fails
cp /path/to/file.md.backup /path/to/file.md

# Step 3: Verify restoration
git diff /path/to/file.md  # Should be empty
```

### If All Else Fails

```bash
# Reset entire repository
git reset --hard HEAD

# Or restore from backup
cp -r /tmp/repo_backup/* /workspace/github__berzerk0__skills-and-prompts-noteboook/
```

---

## Summary: Recommended Workflow

1. **For simple modifications:** Use Workaround 1 (create-then-replace)
2. **For string replacements:** Use Workaround 2 (python with unicode normalization)
3. **For line-by-line edits:** Use Workaround 3 (full file rewrite with backup)
4. **For batch skill fixes:** Use Workaround 4 (batch file creation)
5. **For symlinks:** Use Workaround 5 (bash symlink creation)
6. **For READMEs:** Use Workaround 6 (README creation helper)
7. **After every edit:** Run verification checklist

---

## Files Created for Workarounds

- ✅ `scratchpad/edit_file.py` - Unicode-aware file editor
- ✅ `scratchpad/edit_file_lines.py` - Line-by-line file editor
- ✅ `scratchpad/fix_skills.py` - Batch skill frontmatter fixer
- ✅ `scratchpad/create_readmes.py` - README creation helper
- ✅ `scratchpad/FILE_EDITING_WORKAROUNDS.md` - This document
- ✅ `scratchpad/ERROR_LOG_2026-08-24.md` - Error documentation

---

*Document created: 2026-08-24*
*Next update: As new workarounds are discovered*
