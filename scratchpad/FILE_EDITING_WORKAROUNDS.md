# File Editing Guidance for Vibe Code

**Created:** 2026-08-24  
**Purpose:** Accurate guidance for file editing in Vibe Code  
**Status:** Corrected guidance

---

## Quick Reference: File Editing in Vibe

| Operation | Tool | Status | Notes |
|-----------|------|--------|-------|
| Read file | `read_file` | ✅ WORKS | Use this for all reads |
| Create new file | `write_file` | ✅ WORKS | Use this for new files |
| Modify existing | `edit` | ✅ WORKS | **Use this for all file modifications** |
| List files | `bash` + `ls`/`find` | ✅ WORKS | Use for discovery |
| Git operations | `bash` + `git` | ✅ WORKS | Use for verification |

**Note:** The tool `search_replace` does NOT exist in Vibe. This was the root cause
of the file editing failures in the 2026-08-24 session. The correct tool is `edit`.

---

## Primary Method: Use `edit` Tool

The `edit` tool is Vibe's built-in file editing tool and should be used for all
file modifications. It supports:
- String replacement (old_str -> new_str)
- Multiple search/replace blocks in a single call
- Unicode characters (no normalization needed)

**Template:**
```
edit: {
  "file_path": "path/to/file.md",
  "content": [
    {
      "old_str": "text to replace",
      "new_str": "new text"
    },
    {
      "old_str": "another pattern",
      "new_str": "another replacement"
    }
  ]
}
```

**Example:**
```
edit: {
  "file_path": "AGENTS.md",
  "content": [
    {
      "old_str": "it is for human-maintained drop-offs only.",
      "new_str": "it is for human-maintained drop-offs only. **Agents should only read from mailroom/ when the user explicitly requests it.**"
    }
  ]
}
```

---

## Known Limitations of `edit` Tool

### Unicode Handling
The `edit` tool handles unicode natively. If you encounter string matching issues:
- Ensure the `old_str` exactly matches the file content (including unicode characters)
- Use `read_file` first to see the exact content
- Copy the exact text from the file for `old_str`

### Large Files
For very large files, the `edit` tool may hit context limits. In this case:
- Break edits into smaller chunks
- Use line-specific edits where possible
- Consider using `read_file` with offset/limit to work on sections

### Partial Matches
The `edit` tool performs exact string matching. If `old_str` appears multiple
times and you only want to replace one occurrence, ensure `old_str` includes
enough surrounding context to be unique.

---

## Fallback Methods (If `edit` Fails)

### Method 1: Create-Then-Replace Pattern
Use when `edit` fails for any reason:

```bash
# Step 1: Read original
read_file: AGENTS.md

# Step 2: Create modified version in /tmp
write_file: /tmp/AGENTS.md.new, "[full modified content]"

# Step 3: Replace (using bash)
bash: "cp /tmp/AGENTS.md.new AGENTS.md && rm /tmp/AGENTS.md.new"

# Step 4: Verify
git diff AGENTS.md
```

**Warning:** This method uses `write_file`, which has a confirmed bug (issue #667):
when context fills mid-edit, `write_file` produces a partial file rewrite, silently
drops the rest, and reports success. To avoid this:
- Keep file content under context limits
- Verify the file after writing with `read_file` or `git diff`

---

### Method 2: Python Script with Backup

For complex edits where `edit` tool fails, use a Python script with proper
backup and verification:

```python
#!/usr/bin/env python3
import shutil
from pathlib import Path

def safe_edit(path, old_text, new_text):
    """Safely edit a file with backup."""
    path = Path(path)
    backup_path = Path(f"{path}.backup")
    
    # Create backup
    shutil.copy2(path, backup_path)
    
    try:
        # Read
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace
        if old_text in content:
            content = content.replace(old_text, new_text, 1)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Success: {path}")
            backup_path.unlink()  # Remove backup on success
            return True
        else:
            print(f"Pattern not found in {path}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        # Restore from backup
        shutil.copy2(backup_path, path)
        return False

# Usage
safe_edit('AGENTS.md', 'old text', 'new text')
```

**Save as:** `scratchpad/safe_edit.py`

---

## Verification Checklist

After ANY file modification, run these checks:

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
```

---

## Common Pitfalls and Solutions

### Pitfall 1: Using Wrong Tool Name
**Symptom:** "File not found at: [path]" error when file exists
**Cause:** Using `search_replace` (doesn't exist) instead of `edit`
**Solution:** Always use `edit` for file modifications

### Pitfall 2: Unicode Mismatch
**Symptom:** Pattern not found, even though text appears in file
**Cause:** Unicode characters in file don't match ASCII in search pattern
**Solution:** Use `read_file` to see exact content, copy exact text for `old_str`

### Pitfall 3: Context Overflow in write_file
**Symptom:** File appears to write successfully but content is truncated
**Cause:** write_file bug (issue #667) - context fills mid-edit
**Solution:** Use `edit` instead, or keep content under context limits and verify

### Pitfall 4: Partial String Matching
**Symptom:** Replaces wrong occurrence of text
**Cause:** `old_str` matches multiple places in file
**Solution:** Include more surrounding context in `old_str` to make it unique

---

## Summary: Recommended Workflow

1. **Primary method:** Use `edit` tool for all file modifications
2. **If `edit` fails:** Use create-then-replace pattern with `write_file` + `bash cp`
3. **For complex edits:** Use Python script with backup (safe_edit.py)
4. **After every edit:** Run verification checklist
5. **Never assume:** Always verify the tool name before starting

---

## Pre-Edit Verification

**Before using any file-editing tool, confirm the tool name exists in the
builtin list in `docs/vibe/internals.md`.** Do not guess tool names or carry
over names from Claude Code. Vibe silently drops unrecognized tool names
with no error.

The correct file editing tools in Vibe are:
- `read_file` - Read file content
- `write_file` - Create new files or overwrite existing
- `edit` - Modify existing files (search and replace)

The tool `search_replace` does NOT exist in Vibe.

---

*Document created: 2026-08-24*
*Last updated: 2026-08-24 (corrected guidance)*
