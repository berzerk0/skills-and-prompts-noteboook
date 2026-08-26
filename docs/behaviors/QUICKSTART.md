# Behaviors: Quick Start Guide

Welcome to the foundation harness behaviors. This page helps you get started quickly.

## What Are Behaviors?

**Behaviors** are always-on enforcement mechanisms that prevent specific failures in your harness. Unlike skills (which you invoke), behaviors run automatically on events or schedules.

**Example:** B1 (Tool-Name Assertion) runs before you commit a skill file, checking that all declared tool names exist in both Claude Code and Vibe.

## The Three Tier 1 Behaviors

These have the strongest panel support and lowest implementation cost. Start here.

### 1️⃣ B1: Tool-Name Validation

**What it does:** Prevents skills from being committed with tool names that don't exist in one harness (e.g., `Read` in Vibe, where it's called `read_file`).

**Why it matters:** Mistral Vibe silently drops unrecognized tool names. A skill works in Claude Code but fails silently in Vibe.

**Quick start:**
```bash
# Check all skills
python3 scripts/validate-tool-names.py --harness claude-code --harness vibe

# Install pre-commit hook (optional)
cp docs/behaviors/B1-setup-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

**Documentation:** `docs/behaviors/B1-tool-name-validation.md`

**Status:** ✅ Implemented and tested

---

### 2️⃣ B2: Premise Re-Check on Tool-Not-Found

**What it does:** When a tool call fails (tool not found), injects the list of available tools into the error message, preventing the model from building elaborate wrong theories.

**Why it matters:** Without this, the model spends multiple turns explaining false hypotheses instead of re-checking the tool list.

**Real example from this repo:** Model tried to call `search_replace` (doesn't exist in Vibe), then invented a multi-tier architecture explanation instead of re-checking available tools.

**Quick start:**
```bash
# Verification needed first
# Check: Can Claude Code PreToolUse hook access tool-error events?
# Check: Can Vibe PRE_TOOL hook modify error messages before model sees them?
```

**Documentation:** `docs/behaviors/B2-premise-recheck.md`

**Status:** 📋 Documented, awaiting hook capability verification

---

### 3️⃣ B3: Retirement Sweep

**What it does:** Finds skills that haven't been invoked in 30 days, so you can decide whether to keep, archive, or delete them.

**Why it matters:** Dead skills consume tokens (their descriptions are always resident in your prompt). At n=1, removing dead weight saves real tokens.

**Quick start:**
```bash
# Check for unused skills (currently a template)
python3 scripts/find-unused-skills.py

# Full automation awaits hook-based logging
```

**Documentation:** `docs/behaviors/B3-retirement-sweep.md`

**Status:** 📋 Template implementation, awaiting hook logging

---

## Setup Instructions

### Minimum Setup (Recommended)

1. **Read the overview:**
   ```bash
   # Understand what behaviors do
   cat docs/behaviors/README.md
   ```

2. **Validate existing skills:**
   ```bash
   # Check your skills for tool-name issues
   python3 scripts/validate-tool-names.py --show-valid
   ```

3. **Fix any issues found:**
   - Edit skill files to use correct tool names
   - Reference: `docs/cross-tool-notes.md` for tool translations

4. **Review documentation:**
   - `docs/behaviors/B1-tool-name-validation.md` — Full B1 guide
   - `docs/behaviors/README.md` — Overview of all behaviors

### Optional: Install Pre-Commit Hook

For B1 enforcement at commit time:

```bash
cp docs/behaviors/B1-setup-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Test it
git add docs/behaviors/B1-tool-name-validation.md
git commit -m "test: verify pre-commit hook works"
# Hook should run and pass
```

### Optional: Start Override Log

For measuring whether behaviors actually help:

```bash
# Create a file to log when you override substrate recommendations
touch docs/override-log.md

# Add this header:
echo "# Override Log

Track decisions where you chose NOT to follow a behavior recommendation.

## Format
- Date: YYYY-MM-DD
- Behavior: (e.g., B1, B3)
- What you did: (e.g., committed tool 'Read' in Vibe skill)
- Why: (e.g., 'one-time script, not a reusable skill')
- Outcome: (e.g., 'script failed in Vibe as expected')
" > docs/override-log.md
```

---

## Common Tasks

### I Found a Skill With Invalid Tools

**Problem:** Running B1 validation found a skill with tools not available in Vibe.

**Solution:**
1. Edit the skill's SKILL.md file
2. Update `allowed-tools:` to use correct names
3. Reference `docs/cross-tool-notes.md` for translation
4. Re-run validation to verify

**Example:**
```yaml
# Before (Claude Code names)
allowed-tools:
  - Read
  - Write
  - Grep

# After (Vibe-compatible names)
allowed-tools:
  - read_file
  - write_file
  - grep
```

### I Want to Create a New Skill

**Use this checklist:**

1. [ ] Check B4 (Null-First Expansion): Do I really need a new skill, or can I use existing ones?
2. [ ] Decide: Single-harness (Claude Code only) or multi-harness (portable)?
3. [ ] If multi-harness: Use tool names from BOTH harnesses (or only shared tools)
4. [ ] If single-harness: Add comment `# Portable to: claude-code only`
5. [ ] Create skill file in `skills/my-skill/SKILL.md`
6. [ ] Run validation: `python3 scripts/validate-tool-names.py skills/my-skill/SKILL.md`
7. [ ] Commit (hook will validate again if installed)

### I Want to Fix Tool-Name Issues in My Skills

**Workflow:**
1. Run validation with verbose output:
   ```bash
   python3 scripts/validate-tool-names.py --show-valid --harness claude-code --harness vibe
   ```

2. For each error, check the translation:
   ```bash
   # See tool names for both harnesses
   grep -A 50 "Tool name translation" docs/cross-tool-notes.md
   ```

3. Edit the skill:
   ```bash
   # Edit the problematic skill
   vim skills/skill-name/SKILL.md
   # Update allowed-tools: list
   ```

4. Re-validate:
   ```bash
   python3 scripts/validate-tool-names.py skills/skill-name/SKILL.md --harness vibe
   ```

5. Commit when clean:
   ```bash
   git add skills/skill-name/SKILL.md
   git commit -m "fix(skill-name): make vibe-compatible"
   ```

---

## Tool Name Reference

Quick translation for the most common tools:

| Claude Code | Vibe | Use in Both |
|---|---|---|
| Read | read_file | ❌ |
| Write | write_file | ❌ |
| Edit | edit | ❌ (different tool) |
| Grep | grep | ✅ (same name) |
| Glob | *(none)* | ❌ (use bash find) |
| Bash | bash | ✅ (same name) |
| Task | task | ✅ (same name) |

**For portable skills:** Prefer bash, task (shared names). Or use principles: "use the read tool, whatever its name".

---

## Next: Understanding the Full Debate

After setup, read these for context:

1. **5-minute version:** `notebooks/DEBATE-SUMMARY.md` (what we learned, decisions, next steps)
2. **30-minute version:** `notebooks/foundation-harness-behavior-spec-2026-08-25.md` (all 7 behaviors, reasoning)
3. **Deep dive:** `notebooks/foundation-harness-vision-debates/` (individual model responses, round 1 & 2)

---

## Getting Help

### Understanding a Specific Behavior

- B1 (Tool-Name Validation): `docs/behaviors/B1-tool-name-validation.md`
- B2 (Premise Re-Check): `docs/behaviors/B2-premise-recheck.md`
- B3 (Retirement Sweep): `docs/behaviors/B3-retirement-sweep.md`

### Tool Translations

- `docs/cross-tool-notes.md` — Complete translation table (Claude Code ↔ Vibe)
- `.tools-registry.yaml` — Machine-readable tool registry

### Running Scripts

```bash
# See all options
python3 scripts/validate-tool-names.py --help
python3 scripts/find-unused-skills.py --help
```

### Understanding the Debate

```bash
# Read the summary
cat notebooks/DEBATE-SUMMARY.md

# See the full spec
cat notebooks/foundation-harness-behavior-spec-2026-08-25.md

# Check the methodology
grep "Why Two Rounds" notebooks/DEBATE-SUMMARY.md -A 15
```

---

## Measurement: Catch Net Negatives Early

Once you're running B1-B3, track whether they actually help:

### Cheap Proxy (Recommended)

Log every time you decide NOT to follow a behavior. Example:

```
# docs/override-log.md

2026-08-25: B3 recommended retiring skill X. I kept it anyway because I might use it in 3 months.
2026-08-26: B1 flagged tool 'Read' in Vibe skill. I ignored it because this is Claude-Code-only.
```

- **Flat/falling override rate** → behaviors are calibrated
- **Rising override rate** → you're routing around them (not good)

### Full Experiment (After 4 Weeks)

See `notebooks/DEBATE-SUMMARY.md` section "Measurement Strategy" for the controlled experiment design.

---

## FAQ

**Q: Do I have to use these behaviors?**  
A: No. They're optional. Start with B1 (validation script) to see if it catches issues you already have.

**Q: Can I disable the pre-commit hook?**  
A: Yes. Either don't install it, or run `git commit --no-verify` to bypass.

**Q: What if a tool is valid in both harnesses but named differently?**  
A: Avoid it in portable skills. Use bash (shared name). Or use principles: "use the read tool" (works in both).

**Q: I have a skill that's intentionally Claude-Code-only. Will B1 complain?**  
A: Yes. Add a comment in the frontmatter to document this. See B1-tool-name-validation.md for examples.

**Q: When will B2 and B3 be fully working?**  
A: B2 needs hook capability verification. B3 needs hook-based invocation logging. Both are blocked on harness integration, not on the behavior design.

---

## What's Next?

1. **Run B1 validation:** `python3 scripts/validate-tool-names.py --show-valid`
2. **Fix any issues found** (if any)
3. **Read the full summary:** `notebooks/DEBATE-SUMMARY.md`
4. **Wait for B2/B3 implementation:** Both depend on hook integration

Questions? See `docs/behaviors/README.md` or individual behavior docs.
