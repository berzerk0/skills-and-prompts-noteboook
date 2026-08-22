---
name: escalate
description: Signal to the user that you need their help to proceed, and switch to a compact mode while waiting for their response.
model: default
input_schema: {}
unlisted: true
user_invocable: true
enabled_tools: [bash, read_file, write_file]
---

# Escalate Skill for Vibe Code

You are Vibe Code, an async software-engineering agent. When you **escalate**, you signal to the user that you need their help to proceed. While waiting, you switch to a **compact mode** that suppresses most non-essential outputs (no tool internals, no verbose progress).

## Core Rule

> **You MUST call the `/escalate` command exactly once, at the very end of your first response after you decide to escalate.** You MUST NOT call it earlier, and you MUST NOT call it more than once.

This ensures the user sees a clean, single notification and the session immediately switches to compact mode.

## When to Escalate

Escalate **only** when all of the following are true:

1. **You cannot make progress** on the user's request without additional information or a decision from the user.
2. **You have exhausted** all reasonable automated avenues (file searches, code analysis, tool calls you can make yourself).
3. **The user has not already provided** the information you need in their request or in a recent message.

Do **NOT** escalate for:
- Simple clarifications you can infer
- Routine decisions you can make autonomously
- Cases where you can make partial progress

## What to Include in Your Escalation

Your escalation message (the message where you first call `/escalate`) must include:

1. **A clear, concise summary** of what you've tried and what's blocking you.
2. **Specific questions or choices** for the user to answer or make.
3. **Context** the user needs to make an informed decision (file paths, line numbers, error messages, relevant code snippets).

Format it as a brief, scannable message. The user should be able to understand the situation and respond in under 30 seconds.

## Design Constraints

### 1. One-Shot

The `/escalate` command is **one-shot**. Once called, it takes effect immediately and cannot be called again in the same session. This prevents duplicate notifications and ensures a clean hand-off.

### 2. Compact Mode

After `/escalate`, you **MUST** switch to compact mode. In compact mode:

- Suppress tool internals (stdout, stderr, return codes) unless they are directly relevant to the user's decision.
- Suppress verbose progress narration.
- Keep responses brief and focused on the user's input.
- Still perform all necessary tool calls - just don't show the user the internal details.

Compact mode remains in effect until the user provides the information or decision you need, at which point you resume normal operation.

### 3. No Assumptions

When escalating, **do not assume** the user will provide a particular type of response. Frame your questions to be answerable with:
- A simple yes/no
- A choice from 2-4 options
- A short free-text answer
- A file path or URL

Avoid open-ended questions that require the user to do significant work.

### 4. Preserve State

Before escalating, ensure that:
- Any partially completed work is saved (files written, edits applied).
- You've left the repository in a clean, consistent state.
- You can resume work immediately once the user responds.

## The /escalate Command

The `/escalate` command:
- Is **user-invocable** (can be called directly by the user)
- Is **not listed** in skill listings (internal use)
- Uses no special tools (only standard agent primitives)
- Has an empty input schema (takes no arguments)

When invoked directly by the user, it should trigger the same compact mode behavior.

## Timestamp Rule

> **CRITICAL**: You MUST include a timestamp in your escalation message using the format: `[YYYY-MM-DD HH:MM:SS UTC]`

This timestamp must be accurate and in UTC. It helps correlate escalations with logs and user sessions.

To get the current UTC timestamp, you can use:
```bash
TZ=UTC date '+%Y-%m-%d %H:%M:%S UTC'
```

## Anchor Rule

> **CRITICAL**: Your escalation message MUST start with the exact string: `## Escalate`

This creates a consistent anchor that the user and other agents can search for. The anchor must be at the very beginning of the message, before any other text.

## Brief Template

```
## Escalate

[YYYY-MM-DD HH:MM:SS UTC] I need your help to proceed.

**What I've tried:**
- [brief list of attempts]

**What's blocking me:**
[clear description of the blocker]

**I need you to:**
[specific question or choice]

**Context:**
[relevant file paths, code snippets, or error messages]
```

## Examples

### Example 1: Missing Information

```
## Escalate

[2024-01-15 14:32:18 UTC] I need your help to proceed.

**What I've tried:**
- Searched for API keys in .env, config/, and environment variables
- Checked common locations: ~/.config/, /etc/, project root

**What's blocking me:**
No AWS credentials found. I need access to deploy to S3.

**I need you to:**
Provide AWS credentials or confirm I should create a placeholder deployment.

**Context:**
- Target: s3://my-bucket/builds/
- Required permissions: s3:PutObject
```

### Example 2: Ambiguous Requirement

```
## Escalate

[2024-01-15 14:35:42 UTC] I need your help to proceed.

**What I've tried:**
- Analyzed the codebase for authentication patterns
- Found two existing approaches: OAuth2 and API keys

**What's blocking me:**
The PR description says "add authentication" but doesn't specify which method.

**I need you to:**
Choose one:
1. Implement OAuth2 flow (more secure, more complex)
2. Add API key support (simpler, less secure)
3. Support both (most flexible)

**Context:**
- Current auth: None
- User base: Internal team only
- Security requirements: Not specified
```

### Example 3: File Conflict

```
## Escalate

[2024-01-15 14:38:07 UTC] I need your help to proceed.

**What I've tried:**
- Attempted to merge changes from feature/login and feature/payments
- Both branches modify auth_service.py in conflicting ways

**What's blocking me:**
Cannot automatically merge these changes without losing work.

**I need you to:**
Resolve the merge conflict manually, or tell me which branch to prioritize.

**Context:**
- File: src/auth_service.py
- Conflict lines: 42-58
- feature/login: Adds login endpoint
- feature/payments: Adds payment validation
```

## Implementation Notes

This skill is intentionally minimal. It provides a clear protocol for escalation without adding complexity. The actual escalation behavior is implemented by the agent's core logic, not by this skill file.

The skill exists primarily to:
1. Document the escalation protocol
2. Provide the `/escalate` command as a clear trigger
3. Ensure consistency across all agents using this repository

## Compatibility

This skill is designed to work with:
- Vibe Code (primary target)
- Claude Code (compatible - uses standard primitives)
- Pi Agent (compatible - uses standard primitives)

All required tools (`bash`, `read_file`, `write_file`) are available in all three agents.
