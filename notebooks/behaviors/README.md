> **⚠️ Thought exercise — not a work queue.**
> Nothing in this file has been run, measured, or committed to. Status markers,
> effort estimates, and "next steps" here were written *before* anything was
> verified, and several are known to be wrong. **Do not act on this file, install
> anything from it, or treat its statuses as current.**
> Start at [`../IDEAL.md`](../IDEAL.md) for what actually holds up; known-wrong claims are
> catalogued in [`../verified-defects-2026-08-25.md`](../verified-defects-2026-08-25.md).

---

# Behaviors: Foundation Harness Implementation

This directory contains the implementation of "behaviors" — always-on enforcement mechanisms extracted from the two-round model debate on the foundation harness vision.

## Reference Documents

- **Debate source:** `notebooks/foundation-harness-vision-debates/` (round 1 & 2 responses from 8 models)
- **Extracted behaviors:** `notebooks/foundation-harness-behavior-spec-2026-08-25.md` (candidate behaviors, Tier 1-2)
- **Vision context:** `notebooks/foundation-harness-vision-2026-08-25.md` (original brain dump)

## Behaviors by Tier

### Tier 1: Build First (High Panel Support + Local Evidence)

| Behavior | Status | Purpose | Enforcement |
|----------|--------|---------|-------------|
| **B1: Tool-Name Assertion** | ✅ Implemented | Prevent silent-drop failures (e.g., Vibe silently dropping unrecognized tool names) | Pre-commit hook + validation script |
| **B2: Premise Re-Check** | 📋 Planned | Inject live tool list when tool-not-found error occurs | Hook on tool-error events |
| **B3: Retirement Sweep** | 📋 Planned | Find and list zero-invocation skills every 30 days | Scheduled script |

### Tier 2: Stronger Argument, Thin Support

| Behavior | Status | Purpose | Notes |
|----------|--------|---------|-------|
| **B4: Null-First Expansion** | 📋 Planned | Default to not creating new skills | Upstream prevention of skill debt |
| **B5: Lesson Admission** | 📋 Planned | Only accept lessons backed by hook-generated events | Prevents unfounded lessons |
| **B6: Completion Verification** | 📋 Planned | Claims of success must point to evidence | Catches silent failures |
| **B7: Non-Progress Alarm** | 📋 Planned | Flag loops and overruns instead of absorbing them | Loud failure for expensive mistakes |

## B1: Tool-Name Assertion Before Commit

**Status:** ✅ Implemented (validated against existing skills)

**Files:**
- `notebooks/behaviors/tools-registry.yaml` — Registry of valid tool names per harness
- `notebooks/behaviors/validate-tool-names.py` — Validation script (can run standalone or via hook)
- `notebooks/behaviors/B1-tool-name-validation.md` — Full documentation
- `notebooks/behaviors/B1-setup-hook.sh.txt` — Pre-commit hook template (optional)

**Quick start:**
```bash
# Validate all skills
python3 notebooks/behaviors/validate-tool-names.py --harness claude-code --harness vibe

# Install optional pre-commit hook
cp notebooks/behaviors/B1-setup-hook.sh.txt .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

**Issues found in this repo:**
- `skills/skill-extractor/SKILL.md` declares tools (Read, Write, Glob, Grep, WebSearch, AskUserQuestion) that don't exist in Vibe and would be silently dropped

**Panel support:** 7 of 8 models (only unanimous support besides Gemma's indirect mention)

**Local evidence:** Mistral reported a real session error where `Read` was mistranslated to `read_file` in a skill's `allowed-tools`, the skill loaded without error, and the failure was discovered only when the skill was invoked and Read/read_file lookup failed.

---

## Testing Behaviors

See `notebooks/foundation-harness-behavior-spec-2026-08-25.md` section "How to tell whether any of this helped" for experiment design.

**Cheapest metric:** Log every time you override the substrate's recommendation. A flat/falling override rate means it's calibrated. A rising rate means you're routing around it.

---

## How Behaviors Differ From Skills

- **Skills** (in `.claude/skills/`) are reusable procedural knowledge for the agent
- **Behaviors** (in `notebooks/behaviors/`) are always-on enforcement mechanisms that constrain what the agent can do
- **Skills** are invoked; **behaviors** run automatically on events or schedules
- **Skills** can be disabled; **behaviors** (especially Tier 1) should be hard to bypass

---

## Contributing New Behaviors

Before implementing a new behavior:

1. ✅ **Has it passed the debate?** Check `notebooks/foundation-harness-behavior-spec-2026-08-25.md`
2. ✅ **Do you have local evidence** of the failure it prevents?
3. ✅ **Can it sit on the enforcement ladder?** (deny rule > hook > skill text > model judgment)
4. ✅ **Is the trigger countable?** (never "the model should know better")

---

## Enforcement Ladder (Highest Rung First)

1. **Deny rule** — harness refuses the call; model has no vote
2. **Hook** — fires deterministically on an event; model doesn't author the result
3. **Skill text** — instruction the model reads; biases choice but doesn't guarantee it
4. **Model judgment** — nothing enforces this; acceptable only when top three cannot carry it

Most Tier 1 behaviors should sit on rung 1 or 2. Rung 4 is a known soft spot, not a strategy.

---

## Related Documents

- `docs/cross-tool-notes.md` — Tool name translation table (Claude Code ↔ Vibe)
- `AGENTS.md` — Shared harness configuration (applies to both Claude Code and Vibe)
- `notebooks/foundation-harness-behavior-spec-2026-08-25.md` — Complete behavior specification from debate
