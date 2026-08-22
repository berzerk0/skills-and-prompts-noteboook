---
name: planning-with-files
description: Implements file-based planning for complex multi-step tasks. Creates task_plan.md, findings.md, and progress.md as persistent working memory. Use when starting tasks requiring multi-phase projects, research, or any work where losing track of goals and progress would be costly.
license: MIT
compatibility: [claude, pi, vibe]
---

Use persistent markdown files as working memory on disk.

## When to Use

- Multi-step tasks (3+ phases)
- Research projects requiring many searches
- Building or creating projects with multiple files
- Tasks spanning many tool calls
- Any work where losing track of goals would be costly

## When NOT to Use

- Simple questions or quick lookups
- Single-file edits with obvious scope
- Tasks completable in few tool calls

## Core Pattern

Anything important gets written to disk. After many tool calls, the original goal drifts out of the attention window. Reading the plan brings it back.

## File Purposes

- **task_plan.md**: Phases, progress, decisions. Update after each phase.
- **findings.md**: Research, discoveries, decisions. Update after ANY discovery.
- **progress.md**: Session log, test results. Update throughout.

All files go in **scratchpad_dir** (Vibe) or project root.

## Critical Rules

1. **Create Plan First**: Never start a complex task without task_plan.md.
2. **The 2-Action Rule**: After every 2 read operations, save key findings to findings.md.
3. **Read Before Decide**: Before any major decision, re-read task_plan.md.
4. **Update After Act**: Mark phase status, log errors, note files changed.
5. **Log ALL Errors**: Every error goes in task_plan.md with attempt number.
6. **Never Repeat Failures**: If an action failed, next action must be different.

## 3-Strike Error Protocol

**ATTEMPT 1**: Diagnose & Fix - Read error, identify root cause, apply targeted fix.

**ATTEMPT 2**: Alternative Approach - Try different method, different tool.

**ATTEMPT 3**: Broader Rethink - Question assumptions, search for solutions.

**AFTER 3 FAILURES**: Run /escalate - Explain what tried, share error, ask for guidance.

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| State goals once and forget | Re-read plan before decisions |
| Hide errors and retry silently | Log every error to plan file |
| Stuff everything in context | Store large content in files |
| Start executing immediately | Create plan file FIRST |
| Repeat failed actions | Track attempts, mutate approach |
