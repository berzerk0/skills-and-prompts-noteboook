#!/bin/bash
# Pre-commit hook: Tool-Name Validation (B1)
#
# Prevents skills with invalid tool names from being committed.
# Catches silent-drop failures (e.g., Vibe silently dropping unrecognized tools).
#
# Installation:
#   cp docs/behaviors/B1-setup-hook.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
# To bypass (emergency only):
#   git commit --no-verify
#
# See docs/behaviors/B1-tool-name-validation.md for details.

set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
VALIDATION_SCRIPT="$REPO_ROOT/scripts/validate-tool-names.py"

if [ ! -f "$VALIDATION_SCRIPT" ]; then
    echo "Warning: Tool validation script not found at $VALIDATION_SCRIPT"
    exit 0
fi

if ! command -v python3 &> /dev/null; then
    echo "Warning: python3 not found, skipping tool validation"
    exit 0
fi

# Get staged skill files
SKILL_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E 'skills/.*SKILL\.md$' || true)

if [ -z "$SKILL_FILES" ]; then
    exit 0
fi

echo "🔧 Validating tool names in skill files..."

if python3 "$VALIDATION_SCRIPT" \
    --harness claude-code \
    --harness vibe \
    --fail-on-error \
    $SKILL_FILES; then
    echo "✓ Tool name validation passed"
    exit 0
else
    echo ""
    echo "❌ Tool name validation FAILED"
    echo ""
    echo "You have skill files with tool names that don't exist in one or both target harnesses."
    echo "This would cause silent failures in Mistral Vibe Code (silent-drop behavior)."
    echo ""
    echo "Quick fixes:"
    echo "  • For Vibe portability: Use read_file, write_file, bash, grep, edit, task, ask_user_question"
    echo "  • For Claude Code: Use Read, Write, Edit, Grep, Glob, Bash, Task, etc."
    echo "  • See .tools-registry.yaml for the complete tool list per harness"
    echo "  • See docs/cross-tool-notes.md for translation table"
    echo ""
    echo "Options:"
    echo "  1. Fix the tool names in the skill(s) and try again: git add ... && git commit"
    echo "  2. Bypass validation (emergency only): git commit --no-verify"
    echo "  3. Mark skill as single-harness only (add comment in frontmatter)"
    echo ""
    exit 1
fi
