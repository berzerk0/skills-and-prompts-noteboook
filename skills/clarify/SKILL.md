---
name: clarify
description: Ask clarifying questions when task is underspecified. Use when user request is ambiguous, lacks constraints, or has unclear scope.
license: MIT
compatibility: [claude, pi, vibe]
---

## Underspecification Test

Check these six dimensions. If any are unclear, ask:

1. **Objective**: What is the desired outcome?
2. **Done**: What does success look like?
3. **Scope**: What is in and out of scope?
4. **Constraints**: What limitations or requirements exist?
5. **Environment**: Where does this run or apply?
6. **Safety**: What should be avoided or protected?

## Question Discipline

- **One question at a time** - Focus on one dimension per question
- **Always supply your recommended answer** - Provide a suggested path
- **Look up facts** - Verify information before asking
- **Put decisions to the user** - Don't decide, ask
- **Don't ask what a cheap read answers** - If information is easily accessible, retrieve it first

## Hard Constraint

**Main-agent only.** Subagents have no access to `ask_user_question` and will guess or return partial results.

## Philosophy Choice

This skill merges two approaches:
- **ask-questions**: Cap at 1-5 questions to avoid overwhelming user
- **grill-me**: No caps, focus on quality over quantity

**Decision**: Use uncapped approach - ask until ambiguity is resolved, but always one at a time with recommended answers.

## When to Use

- User request is vague or ambiguous
- Multiple interpretations are possible
- Constraints or requirements are unclear
- Scope is not well-defined
- Safety concerns need clarification
