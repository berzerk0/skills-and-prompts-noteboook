> **⚠️ Thought exercise — not a work queue.**
> Nothing in this file has been run, measured, or committed to. Status markers,
> effort estimates, and "next steps" here were written *before* anything was
> verified, and several are known to be wrong. **Do not act on this file, install
> anything from it, or treat its statuses as current.**
> Start at [`../IDEAL.md`](../IDEAL.md) for what actually holds up; known-wrong claims are
> catalogued in [`../verified-defects-2026-08-25.md`](../verified-defects-2026-08-25.md).

---

# B3: Retirement Sweep

**Status:** Documented + Template Implementation

## Overview

Artifacts that nothing invokes get found and removed on a schedule. Dead skills consume tokens (their descriptions are always resident in every prompt) and can mislead the model's routing decisions, so finding and removing them is worth doing regularly.

## Problem This Solves

**Silent debt accumulation:** Skills that become obsolete remain resident:
- Their descriptions consume tokens on every turn
- The model wastes computation evaluating whether to invoke them
- Dead skills can mislead routing: if an old tool still has a description, the model might pick it over a new one
- No automatic signal that a skill is dead; must be found by inspection

**Why this matters at n=1:** With two-stage skill loading (descriptions resident, body loaded on invocation), every skill in the directory is a standing tax on context. A 1000-token description resident every turn across 100 turns costs 100K tokens even if never invoked.

**Example:** A skill written to handle "database schema migrations" stays resident even after the project adopts a new ORM that makes it obsolete. The model still evaluates it, still picks it in some cases, but it's been broken for months.

## Implementation

### Core Mechanism

A scheduled script (B3) that:
1. **Lists** all skills in `.claude/skills/` and `skills/`
2. **Checks** invocation logs (when available) or git history
3. **Reports** skills with zero invocations in the last N days
4. **Produces** a human-readable list for manual review

**Important:** The script does NOT delete skills. Deletion is a human decision.

### Trigger

- Scheduled: every 30 days (configurable)
- Manual: `python3 (removed, see verified-defects D5)`

### Falsifier

A skill that meets the zero-invocation criterion still exists after a sweep runs.

### Failure Mode

**Silent.** Dead skills keep consuming tokens and competing for model attention. The script catches it, but only if it runs.

### Enforcement Point

**Skill text (partially) + Scheduled script.** The script runs on schedule and produces a list. Whether you act on it is a human decision.

## Usage

### Check for unused skills
```bash
python3 (removed, see verified-defects D5)
```

### Check for skills unused in last 90 days
```bash
python3 (removed, see verified-defects D5) --days 90
```

### Show invocation counts for all skills
```bash
python3 (removed, see verified-defects D5) --show-all --verbose
```

## Workflow

1. **Script runs** (automatically via scheduled trigger, or manually)
2. **Report generated** listing zero-invocation skills
3. **Human review** — for each unused skill, decide:
   - **Keep:** Still valuable, might be used in future
   - **Archive:** Valuable but not currently in use; move to `archive/` with documentation
   - **Delete:** Obsolete; remove from repo
4. **Action taken** — human commits the cleanup

## Integration with B4: Null-First Expansion

B3 is downstream cleanup; B4 is upstream prevention.

- **B4:** When creating a skill, default to "don't create" (null branch)
- **B3:** When a skill exists but isn't used, default to "retire it" (cleanup)

Together they prevent skill debt accumulation.

## Integration with Hooks

**Future:** When invocation logging is implemented via hooks, B3 will have accurate data:
- Hook logs every skill invocation (name, timestamp, outcome)
- B3 script queries this log instead of guessing from git history
- Accuracy improves from "probably unused" to "definitely unused"

**Current state:** Placeholder implementation; script will be fully functional once hooks log skill invocations.

## Scheduling

### Option A: Manual Trigger (Easiest)
Run the script monthly as a reminder:
```bash
# In CLAUDE.md or workflow:
# "Run (removed, see verified-defects D5) monthly to audit dead skills"
```

### Option B: Scheduled Trigger (Automated)
```bash
# Register a routine to check every 30 days
python3 -c "from datetime import datetime, timedelta; print((datetime.now() + timedelta(days=30)).isoformat())"
# Then use that date with create_trigger or cron
```

### Option C: Git Hook (On-Demand)
Add to pre-push or post-merge hook:
```bash
python3 (removed, see verified-defects D5)
```

## Related Behaviors

- **B1 (Tool-Name Assertion):** Prevents bad skills from being committed
- **B4 (Null-First Expansion):** Prevents creation of unnecessary skills (upstream)
- **B3 (this behavior):** Removes unused skills (downstream cleanup)

### Skill Lifecycle

```
Create → Validate (B1) → Decide (B4 check) → Use → Review (B3) → Archive/Delete
```

## Measurement

**Metric:** Skill description tokens resident per turn

```
Before B3: N unused skills × avg_description_tokens × turns_per_session = wasted_tokens
After B3: (N - cleanup_count) × avg_description_tokens × turns = saved_tokens
```

## Design Notes

### Why not automatic deletion?

Deleting dead skills without human review risks:
- Losing valuable code that could be resurrected
- Deleting a skill that's not actually dead (false negative in detection)
- Orphaning downstream references or documentation

Human review is cheap at n=1.

### Why not keep them archived in the same directory?

Archived skills still consume tokens if resident. Moving them to `archive/` (excluded from skill discovery) reduces context weight.

### Why 30 days?

A skill that's not invoked for 30 days is likely either:
- Genuinely obsolete (safe to archive)
- Situational but not current (safe to archive, resurrect when needed)
- Long-tail use case (rare, but will surface if actually needed)

30 days balances signal (catching real dead weight) vs. noise (false positives on rare skills).

## Known Limitations

1. **Hook logs not yet in place:** Current implementation is a template. Accuracy depends on hook integration.
2. **Manual invocation not logged:** Skills invoked via slash commands may not be logged yet.
3. **Indirect invocation unclear:** If skill A invokes skill B internally, is B marked as invoked?
4. **Deleted skills still in git history:** The script only checks current state, not whether skills were active before.

## Panel Support

**Support:** 4 of 8 as an explicit behavior; 7 of 8 once Part C statements are counted.

**Panel reasoning:** At n=1 with two-stage skill loading, every skill's description is resident every turn whether invoked or not. Dead skills are not inert; they are a standing tax on context and a standing source of misrouting.

**Note:** Mistral answered Part C2 "Survive: none" but then listed retirement in its Part D. Treat as capitulation pressure; the core idea survives the debate.

## What was proposed (never done)

1. **Verify hook capability:** Confirm that invoking a skill can be logged automatically
2. **Implement logging:** Add hook to log skill invocations (name, timestamp, outcome)
3. **Test script:** Run against repo and verify detection of unused skills
4. **Schedule:** Set up recurring trigger to run B3 monthly or quarterly
5. **First sweep:** Run manually and review results

## Related Documentation

- `notebooks/behaviors/B1-tool-name-validation.md` — Validation of skills at creation
- `notebooks/behaviors/B4-null-first-expansion.md` — Prevention at creation time
- `notebooks/foundation-harness-behavior-spec-2026-08-25.md` — Full debate context
- `archive/README.md` — Where to move retired skills
