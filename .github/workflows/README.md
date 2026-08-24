# GitHub Actions Workflows

This directory contains CI/CD workflows for the crispy-couscous repository.

## Workflows

### [symlink-guard.yml](symlink-guard.yml)
**Purpose:** Primary CI guard against symlink-related bugs

**Triggers:**
- Push to `main` or `fix/**` branches
- Pull requests targeting `main`

**Checks:**
1. Verifies all entries in `.claude/skills/`, `.pi/skills/`, `.vibe/skills/` are symlinks (not real directories)
2. Verifies symlinks point to `../../skills/<name>`
3. Verifies canonical `skills/<name>/SKILL.md` files are real files, not symlinks
4. Static analysis of generator scripts to ensure guardrails are present
5. Runs generators and verifies they don't modify canonical `skills/` directory

**Why:** Prevents the 2026-08-24 incident class of bugs where generators overwrote canonical SKILL.md files through symlinks.

---

### [pre-commit-check.yml](pre-commit-check.yml)
**Purpose:** Runs the same checks that should be in a local pre-commit hook

**Triggers:**
- Push to `main` or `fix/**` branches
- Pull requests targeting `main`

**Checks:**
1. Validates all symlinks in skill farms point to valid targets in `skills/`
2. Verifies skills directory structure (real dirs, real SKILL.md files)
3. Verifies generators have guardrails
4. Tests generators don't modify canonical skills

**Local Setup:**
To run these checks locally before commit:
```bash
# Make the hook executable
chmod +x .github/workflows/pre-commit-check.sh

# Create the pre-commit hook
ln -s ../../.github/workflows/pre-commit-check.sh .git/hooks/pre-commit
```

---

### [validate-symlinks.yml](validate-symlinks.yml)
**Purpose:** Scheduled validation of all symlinks

**Triggers:**
- Manual (workflow_dispatch)
- Daily at midnight UTC (schedule)

**Checks:**
- Lists all symlinks in the repository
- Verifies symlink farm integrity
- Reports broken symlinks

---

## Local Pre-commit Hook

For local development, you can install a pre-commit hook that runs the same checks as the CI:

```bash
# Create the hook script
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
set -euo pipefail

echo "Running pre-commit symlink safety checks..."

# Check 1: Verify symlink farms
echo "Check 1: Validating symlink farms..."
for farm in .claude/skills .pi/skills .vibe/skills; do
  if [ -d "$farm" ]; then
    for entry in "$farm"/*; do
      if [ -e "$entry" ] && [ ! -L "$entry" ]; then
        echo "ERROR: Non-symlink in symlink farm: $entry"
        exit 1
      fi
    done
  fi
done
echo "  OK: All entries in symlink farms are symlinks"

# Check 2: Verify generators have guardrails
echo "Check 2: Verifying generator guardrails..."
for gen in meta/generate_claude.py meta/generate_pi.py meta/generate_vibe.py; do
  if [ -f "$gen" ] && ! grep -q "canonical_skills" "$gen"; then
    echo "ERROR: Missing guardrail in $gen"
    exit 1
  fi
done
echo "  OK: All generators have guardrails"

# Check 3: Test generators
echo "Check 3: Testing generator safety..."
find skills -name "SKILL.md" -type f | sort | xargs md5sum > /tmp/before.md5
python meta/generate_all.py --all > /dev/null 2>&1
find skills -name "SKILL.md" -type f | sort | xargs md5sum > /tmp/after.md5
if ! diff /tmp/before.md5 /tmp/after.md5; then
  echo "ERROR: Generators modified canonical skills!"
  exit 1
fi
echo "  OK: Generators do not modify canonical skills"

echo "All pre-commit checks passed"
EOF

# Make it executable
chmod +x .git/hooks/pre-commit
```

---

## Windows Notes

On Windows, git requires `core.symlinks=true` for proper symlink handling:

```bash
# Enable symlinks in git config
git config --global core.symlinks true
```

The `.gitattributes` file also helps ensure symlinks are preserved correctly.
