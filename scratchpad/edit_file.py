#!/usr/bin/env python3
"""
Safe file editor for Vibe Code with unicode normalization.

Usage:
    python3 edit_file.py <path> <old_text> <new_text>
    
Or import and use edit_file() function directly.

Created: 2026-08-24
Purpose: Unicode-aware file editing helper

WARNING: This script performs ASCII normalization on write, which changes
file content beyond the requested edit. Em dashes (—) become --, smart
quotes become straight quotes, etc. Use only if ASCII normalization is
acceptable for your use case. For most cases, use Vibe's built-in `edit` tool
instead, which handles unicode natively without normalization.
"""

import sys
import os
import shutil
from pathlib import Path


def normalize_text(text):
    """
    Normalize unicode characters to ASCII equivalents.
    
    This handles the common unicode characters found in markdown files
    that cause string matching to fail.
    """
    replacements = {
        # Em dash and variants
        '\u2014': '--',
        '\u2015': '--',
        # En dash
        '\u2013': '-',
        # Arrows
        '\u2192': '->',
        '\u2190': '<-',
        '\u2194': '<->',
        # Smart quotes
        '\u2018': "'",
        '\u2019': "'",
        '\u201c': '"',
        '\u201d': '"',
        # Ellipsis
        '\u2026': '...',
        # Non-breaking space
        '\u00a0': ' ',
        # Various dashes
        '\u2010': '-',
        '\u2011': '-',
        '\u2012': '-',
        '\u2013': '-',
        '\u2014': '--',
        '\u2015': '--',
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text


def backup_file(path):
    """Create backup of file before editing."""
    path = Path(path)
    backup_path = path.with_suffix(path.suffix + '.backup')
    shutil.copy2(str(path), str(backup_path))
    return str(backup_path)


def restore_file(path):
    """Restore file from backup."""
    path = Path(path)
    backup_path = path.with_suffix(path.suffix + '.backup')
    if backup_path.exists():
        shutil.copy2(str(backup_path), str(path))
        backup_path.unlink()  # Remove backup after restore
        return True
    return False


def edit_file(path, old_text, new_text, create_backup=True):
    """
    Safely edit a file with unicode normalization.
    
    Args:
        path: Path to file to edit
        old_text: Text to replace (can contain unicode)
        new_text: Replacement text (can contain unicode)
        create_backup: Whether to create backup before editing
    
    Returns:
        True if edit was successful, False otherwise
    """
    path = Path(path)
    
    # Validate file exists
    if not path.exists():
        print(f"Error: File not found: {path}")
        return False
    
    # Create backup
    backup_path = None
    if create_backup:
        backup_path = backup_file(path)
        print(f"Backup created: {backup_path}")
    
    try:
        # Read file
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Normalize all text
        old_normalized = normalize_text(old_text)
        new_normalized = normalize_text(new_text)
        content_normalized = normalize_text(content)
        
        # Check if pattern exists
        if old_normalized not in content_normalized:
            print(f"Error: Pattern not found in {path}")
            print(f"Looking for: {repr(old_normalized)}")
            # Try to find similar patterns
            if old_text in content:
                print("Note: Pattern found with original unicode encoding")
            return False
        
        # Replace (only first occurrence by default)
        content = content.replace(old_normalized, new_normalized, 1)
        
        # Write back
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Successfully edited: {path}")
        return True
        
    except Exception as e:
        print(f"Error editing {path}: {e}")
        # Attempt restore
        if backup_path and restore_file(path):
            print(f"Restored from backup: {backup_path}")
        return False


def edit_file_all(path, old_text, new_text):
    """
    Edit all occurrences of old_text in file.
    
    Same as edit_file but replaces ALL occurrences, not just first.
    """
    path = Path(path)
    
    if not path.exists():
        print(f"Error: File not found: {path}")
        return False
    
    backup_path = backup_file(path)
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        old_normalized = normalize_text(old_text)
        new_normalized = normalize_text(new_text)
        content_normalized = normalize_text(content)
        
        if old_normalized not in content_normalized:
            print(f"Error: Pattern not found in {path}")
            return False
        
        # Replace all occurrences
        content = content.replace(old_normalized, new_normalized)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Successfully edited all occurrences in: {path}")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        restore_file(path)
        return False


def append_to_file(path, text):
    """
    Append text to end of file.
    
    Args:
        path: Path to file
        text: Text to append
    """
    path = Path(path)
    
    if not path.exists():
        print(f"Error: File not found: {path}")
        return False
    
    backup_path = backup_file(path)
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ensure proper newline separation
        if not content.endswith('\n'):
            content += '\n'
        content += text
        if not text.endswith('\n'):
            content += '\n'
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Successfully appended to: {path}")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        restore_file(path)
        return False


def prepend_to_file(path, text):
    """
    Prepend text to beginning of file.
    
    Args:
        path: Path to file
        text: Text to prepend
    """
    path = Path(path)
    
    if not path.exists():
        print(f"Error: File not found: {path}")
        return False
    
    backup_path = backup_file(path)
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ensure proper newline separation
        text = text.rstrip() + '\n\n'
        content = text + content
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Successfully prepended to: {path}")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        restore_file(path)
        return False


if __name__ == '__main__':
    # Command line usage
    if len(sys.argv) < 4:
        print("Usage: python3 edit_file.py <path> <old_text> <new_text>")
        print("Or: python3 edit_file.py --append <path> <text>")
        print("Or: python3 edit_file.py --prepend <path> <text>")
        sys.exit(1)
    
    if sys.argv[1] == '--append':
        if len(sys.argv) < 4:
            print("Usage: python3 edit_file.py --append <path> <text>")
            sys.exit(1)
        path = sys.argv[2]
        text = sys.argv[3]
        append_to_file(path, text)
    elif sys.argv[1] == '--prepend':
        if len(sys.argv) < 4:
            print("Usage: python3 edit_file.py --prepend <path> <text>")
            sys.exit(1)
        path = sys.argv[2]
        text = sys.argv[3]
        prepend_to_file(path, text)
    else:
        path = sys.argv[1]
        old_text = sys.argv[2]
        new_text = sys.argv[3]
        edit_file(path, old_text, new_text)
