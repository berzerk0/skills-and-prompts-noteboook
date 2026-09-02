# Model Selection Strategy

**Repository:** crispy-couscous  
**Objective:** Rationalize model assignments across agents for cost/quality balance  
**Status:** ACTIVE  
**Version:** 1.0.0

---

## Overview

This document defines the **model selection strategy** for crispy-couscous agents. The goal is to match each agent's model to its task complexity while optimizing for cost and performance.

**Key Principle:** Use the smallest model that can reliably perform the task.

---

## Model Tiers

| Tier | Model | Cost | Speed | Quality | Best For |
|------|-------|------|-------|---------|----------|
| **Small** | `mistral-small` | Low | Fast | Good | Simple tasks, pattern matching, validation |
| **Medium** | `mistral-medium` | Medium | Medium | Very Good | General purpose, implementation, review |
| **Large** | `mistral-large` | High | Slow | Excellent | Complex reasoning, architecture, escalation |

---

## Model Assignment Framework

### Decision Tree

```
Task Complexity?
├── Simple (pattern matching, validation, single-step)
│   └── mistral-small
├── Medium (multi-step, implementation, review)
│   └── mistral-medium
└── Complex (architecture, escalation, strategic decisions)
    └── mistral-large
```

### Task Complexity Definitions

| Complexity | Characteristics | Examples |
|------------|----------------|----------|
| **Simple** | Single-step, deterministic, pattern matching | Timestamp, validation, simple queries |
| **Medium** | Multi-step, requires judgment, file operations | Implementation, review, planning |
| **Complex** | Strategic, architectural, high-stakes | Architecture, escalation, fix-loop |

---

## Current Agent Assignments

### Small Model (`mistral-small`) - 12 agents

| Agent | Rationale | Tasks |
|-------|-----------|-------|
| **architect** | ❌ **REVIEW** - Architecture is complex, should be medium/large | Design, codebase understanding |
| **challenge-my-thinking** | ✅ Simple pattern: push back on assumptions | Critical feedback |
| **clarify** | ✅ Simple pattern: ask questions | Clarification |
| **escalate** | ❌ **REVIEW** - Creating escalation briefs needs judgment | Brief creation |
| **escalation-fixer** | ✅ Fix-loop: one tier above stuck model | Fix retries |
| **modern-python** | ✅ Pattern matching: config recommendations | Tooling advice |
| **napkin** | ✅ Simple: maintain runbook | Runbook curation |
| **planning-with-files** | ❌ **REVIEW** - Multi-step planning needs medium | Task planning |
| **repo-auditor** | ✅ Pattern matching: audit structure | Repository audit |
| **skill-extractor** | ✅ Pattern matching: extract from sessions | Skill extraction |
| **skill-validator** | ✅ Validation: check SKILL.md format | Validation |
| **transcription** | ✅ Simple: single-file tasks | Transcription |
| **vibe-reference** | ✅ Lookup: reference documentation | Reference queries |
| **writing-for-agents** | ✅ Pattern matching: writing guidance | Document writing |

### Medium Model (`mistral-medium`) - 3 agents

| Agent | Rationale | Tasks |
|-------|-----------|-------|
| **implementer** | ✅ Multi-step: prose-spec implementation | Code implementation |
| **reviewer** | ✅ Judgment: code review, debugging | Multi-file coordination |
| **router** | ✅ Complex routing decisions | Task delegation |

### Large Model (`mistral-large`) - 0 agents

Currently no agents use `mistral-large`.

---

## Recommended Changes

Based on the complexity analysis:

### Promote to Medium

| Agent | Current | Recommended | Rationale |
|-------|---------|-------------|-----------|
| **architect** | small | **medium** | Architecture requires broader context understanding |
| **escalate** | small | **medium** | Escalation briefs need nuanced judgment |
| **planning-with-files** | small | **medium** | Complex multi-step planning benefits from medium |

### Keep as Small

All other `mistral-small` agents have appropriate assignments:
- Validation tasks (skill-validator, repo-auditor)
- Pattern matching (modern-python, writing-for-agents)
- Simple operations (challenge-my-thinking, clarify, napkin)

### Consider Large for Special Cases

No current agents warrant `mistral-large`. However, consider for:
- **architect** if doing large-scale system design
- **escalation-fixer** if fixing very complex issues

For now, **medium is sufficient** for all our use cases.

---

## Cost Analysis

### Token Costs (Estimated)

| Model | Input Token Cost | Output Token Cost | Notes |
|-------|------------------|-------------------|-------|
| mistral-small | $0.25/M | $0.25/M | Cheap for simple tasks |
| mistral-medium | $0.70/M | $0.70/M | Good balance |
| mistral-large | $2.00/M | $2.00/M | Expensive, use sparingly |

### Cost per Agent Type

| Agent Type | Avg Turns | Model | Est. Cost/Turn |
|------------|-----------|-------|----------------|
| Simple (small) | 3-5 | mistral-small | ~$0.0025 |
| Medium (medium) | 5-10 | mistral-medium | ~$0.0070 |
| Complex (large) | 10+ | mistral-large | ~$0.0200 |

### Repository-Wide Impact

With current distribution (12 small, 3 medium, 0 large):
- **Average cost per session:** ~$0.02-0.05
- **With recommended changes** (9 small, 6 medium): ~$0.03-0.08
- **If all medium:** ~$0.07-0.15

**Conclusion:** The recommended changes add minimal cost for significant quality improvement.

---

## Implementation

### Apply Recommended Changes

```bash
# architect.toml
sed -i 's/active_model = "mistral-small"/active_model = "mistral-medium"/' .vibe/agents/architect.toml

# escalate.toml  
sed -i 's/active_model = "mistral-small"/active_model = "mistral-medium"/' .vibe/agents/escalate.toml

# planning-with-files.toml
sed -i 's/active_model = "mistral-small"/active_model = "mistral-medium"/' .vibe/agents/planning-with-files.toml
```

### Verification

```bash
# Check all model assignments
for f in .vibe/agents/*.toml; do
    echo "$(basename $f): $(grep active_model $f | cut -d= -f2 | tr -d ' "')"
done
```

---

## Model Selection Cheat Sheet

| If the agent... | Use Model |
|----------------|-----------|
| Validates format, checks compliance | small |
| Matches patterns, provides recommendations | small |
| Asks questions, clarifies | small |
| Maintains simple records | small |
| Implements code, creates files | medium |
| Reviews code, debugs | medium |
| Routes tasks, makes decisions | medium |
| Designs architecture | medium |
| Creates escalation briefs | medium |
| Plans complex tasks | medium |
| Does strategic reasoning | large |
| Handles high-stakes decisions | large |

---

## Monitoring and Iteration

### Track Model Performance

For each agent, track:
- Success rate (tasks completed without error)
- User satisfaction (if feedback available)
- Token usage (cost efficiency)
- Turn count (efficiency)

### Review Cadence

- **Monthly:** Review model assignments based on usage data
- **Quarterly:** Re-evaluate cost/quality tradeoffs
- **As needed:** When new models are released

### Adjustment Criteria

**Promote model if:**
- Success rate < 80%
- User complaints about quality
- Tasks frequently require rework

**Demote model if:**
- Success rate > 95% with current model
- Tasks are consistently simple
- Cost savings justify quality tradeoff

---

## References

- [Mistral AI Pricing](https://mistral.ai/pricing/)
- [Vibe Code Model Configuration](https://docs.mistral.ai/capabilities/code_generation)
- [Model Selection Best Practices](https://github.com/JSON-AGENTS/Standard)

---

*Document created: 2026-08-22*  
*Version: 1.0.0*  
*Status: Ready for implementation*
