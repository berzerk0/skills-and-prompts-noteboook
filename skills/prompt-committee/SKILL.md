---
name: prompt-committee
version: 1.2.0
description: Two-phase skill for getting structured feedback on prompts, guidelines, or rule sets from other AI models, then triaging the responses into actionable patches. Use when the user wants to validate a prompt, send design decisions to another model for review, or process feedback received from another model. Triggers on: "send this to [model]", "get another opinion", "run this by [model]", "what would [model] say", "committee review", "/prompt-committee", or when the user pastes a response from another model and asks what to do with it.
---

# Prompt Committee

Two phases, independent -- use either alone. Re-run Phase 2 each turn if feedback arrives in multiple turns.

---

## Phase 1 -- Outbound

Extract from context: artifact type, what changed since last review, what it runs on, what feedback is wanted. Ask if unclear.

Draft structure:

```
<context>
[1-2 sentences: what artifact is and what it does]
</context>

<changes>
[Bullets of changes since last review. Omit if first review.]
</changes>

<request>
[3-5 focused questions. Default if unspecified:
- Logic gaps or contradictions
- Ambiguous instructions
- Missing edge cases
- Unexpected model behavior risks]
</request>

<format>
Numbered list. Each item: Issue / Why it matters / Fix. No praise. No summary.
</format>

<artifact>
[Full artifact text]
</artifact>
```

End output with:
```
<artifact>
[paste here]
</artifact>
```

---

## Phase 2 -- Inbound

Strip all praise first. Identify distinct items: suggested change, flagged issue, question back to user, design tradeoff.

Auto-flag `USER CHOICE`: contradictions in feedback, unanswered review questions.

```
IMPLEMENT
- [item]: [change summary]

USER CHOICE
- [item]: [conflict, design decision, contradictory feedback, unanswered question, or style/scope tradeoff]

DEFER
- [item]: [valid but conditional -- revisit if X]

REJECT
- [item]: [misunderstands artifact purpose, adds bloat, or solves non-problem]

NO ACTION NEEDED
- [reason -- if nothing actionable after praise stripped]
```

Triage rules:
- **IMPLEMENT** -- unambiguous, aligns with artifact goals, no tradeoffs
- **USER CHOICE** -- requires a decision: conflicts, contradictions, unanswered questions, or style/compression/scope preference (artifact still works -- user preference only)
- **DEFER** -- valid but conditional or non-urgent
- **REJECT** -- misunderstands purpose, adds bloat, solves non-problem
- **NO ACTION NEEDED** -- nothing actionable remains after praise stripped
- All-IMPLEMENT is valid. Don't manufacture DEFER/REJECT to balance the list.
- Omit empty category headers from output.

Present action list. Wait for confirmation before patching.
