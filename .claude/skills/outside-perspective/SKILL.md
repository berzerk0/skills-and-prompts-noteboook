---
name: outside-perspective
description: >-
  Dispatches an isolated subagent with no memory of this conversation to
  review a doc, prompt, or plan for clarity and internal consistency --
  genuine cold-read feedback, not self-review. Use when: reviewing something
  this session wrote or iterated on; checking if it reads clearly to a
  zero-context reader; user asks "fresh eyes," "outside perspective," "cold
  read"; or a repeat review round would be biased by earlier findings.
metadata:
  author: Claude Code
  version: 1.0.0
  date: 2026-08-26
---

# Outside Perspective

## When to Use

- Iterating on a doc/prompt/plan across turns? Check it still reads clearly outside this conversation.
- User asks "fresh eyes," "cold read," "outside perspective," "how would someone unfamiliar read this."
- Reviewing something you wrote/edited/deeply know — review's value depends on the reviewer *not* sharing that background.
- Round 2+ review of the same artifact — round 1's findings are now things you "already know," can't un-know.

## When NOT to Use

- Review doesn't need naivety — checking code compiles, running tests, verifying a fact. Just do it directly.
- Want a second *opinion* from a different model/vendor (e.g. send the prompt to another AI) — that's `prompt-committee`, not this.
- Reviewer needs to already share your context (e.g. "does this match what we discussed") — a fresh subagent can't, by definition.

## Problem

Self-review fails at exactly what it's meant to catch. Write or fix a doc across turns and you already know its undefined terms, its citations, which past round's finding to route around — none of which a genuinely new reader has. "Read this as if you'd never seen it" doesn't work: you can't unlearn context already in your window. The review still looks thorough — specific, quote-anchored, plausible — and still misses "does this communicate to someone with nothing else to go on." Output format gives no signal the reviewer wasn't actually naive.

## Solution

### Step 1: Recognize when naivety matters

Ask: does this review need the reviewer to *not* know what you know? Clarity to an uninitiated reader, whether a plan communicates alone, a repeat cold-read after prior rounds — yes. Otherwise skip this skill, check directly.

### Step 2: Dispatch with an exclusion list, not just an inclusion list

Use the `Agent` tool, `subagent_type: general-purpose`, for open-ended analysis. Skip `Explore` — read-only search agent, own description warns against design-doc audits or open-ended analysis.

Two things make isolation real, not nominal:

- **Don't paste your own analysis, summaries, or findings into the prompt.** Point the subagent at the source file(s) and instructions, let it read them. Anything you summarize is context it wouldn't otherwise have — defeats the point.
- **If the subagent's filesystem/repo access reaches beyond the one artifact, name and forbid the off-limits files** — background docs, prior rounds, design notes, git log. Left to wander, a subagent often finds the very things that contaminate it, out of ordinary thoroughness. Naming them explicitly is the only reliable guard; "don't read anything you don't need" is too vague.

Example prompt shape:

```
You are being given exactly one task, with no other context on this project.
Read <review-instructions-file> first and follow it exactly.
Do NOT read <background-file-1>, <background-file-2>, prior review rounds,
git log, or commit history — the whole point is answering as someone who has
never seen this project before. If the reviewed document references those
files, treat that exactly as a real cold reader would (per whatever the
review instructions ask about undecodable references).
Report your answer back in full as your final response.
```

### Step 3: Treat the subagent's output as the real review, not a draft

Resist "cleaning up" or re-deriving findings with your own contaminated knowledge — that reintroduces the bias you dispatched the subagent to avoid. A finding recurring across independent rounds (different subagents, tools, models) is itself evidence it's real.

### Step 4: Report plainly, including surprises

A finding you, with full context, wouldn't have flagged (or would've argued away) — that's the actual signal this technique exists for. Don't average it away.

## Verification

1. Spot-check one or two subagent claims (quote, line reference) against the source — a cold read must be *accurate*, not just naive.
2. Two independent subagents (or a subagent and a prior human/other-model round) converge without seeing each other's output? Strong evidence the finding's real.
3. Exact counts (chars, lines, words): run the actual command (`wc -c`, `wc -l`) — don't eyeball.

## References

- `outside-perspective-session` — same technique, no subagent tool: a separate chat, session, or model/vendor instance you hand the artifact to manually. Prefer it when the host lacks subagent dispatch, or isolation needs to cross a model/vendor boundary.
- `prompt-committee` — feedback from an actual different AI model or vendor, copy-pasted manually, not an in-session subagent.
