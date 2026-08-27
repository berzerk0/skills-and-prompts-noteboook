---
name: outside-perspective
description: >-
  Dispatches an isolated subagent with no memory of the current conversation
  to review a document, prompt, plan, or design for clarity and internal
  consistency, producing genuine cold-read feedback instead of self-review.
  Use when: (1) reviewing a prompt or plan this session authored or has been
  iterating on, (2) checking whether a document communicates clearly to a
  reader with zero prior context, (3) the user asks for "fresh eyes," "outside
  perspective," "cold read," or "someone with no context" on something already
  in this session's context, (4) running a repeated review round on the same
  artifact where the session's own accumulated knowledge from earlier rounds
  would bias the read.
author: Claude Code
version: 1.0.0
date: 2026-08-26
---

# Outside Perspective

## When to Use

- You've been iterating on a document/prompt/plan across multiple turns and
  need to check whether it still reads clearly to someone who wasn't in this
  conversation
- The user explicitly asks for "fresh eyes," "a cold read," "outside
  perspective," or "how would someone unfamiliar read this"
- You're about to review something you wrote, edited, or have deep background
  context on, and the review's value depends on the reviewer *not* having
  that background
- Running a second or later round of review on the same artifact, where round
  1's findings are now things you "already know" and can no longer un-know

## When NOT to Use

- The review doesn't depend on the reviewer being naive — e.g. checking code
  compiles, running tests, verifying a fact against a source. Just do it
  directly.
- You want a second *opinion* from a different model or vendor entirely (e.g.
  sending a prompt to another AI for comparison) — that's `prompt-committee`,
  not this.
- The task requires the reviewer to already share your context (e.g. "does
  this match what we discussed") — a fresh subagent can't do that by
  definition.

## Problem

Self-review of your own artifact silently fails at exactly the thing it's
supposed to catch. If you wrote or have been fixing a document across several
turns, you already know what its undefined terms mean, what its citations
point to, and which past round's finding to route around — none of which a
genuinely new reader has. Asking yourself to "read this as if you'd never
seen it" doesn't work: you can't unlearn context already in your window. The
review still looks thorough — specific, quote-anchored, plausible — and still
misses the exact class of problem, "does this communicate to someone with
nothing else to go on," that motivated running it in the first place. Nothing
about the output format signals that the reviewer wasn't actually naive.

## Solution

### Step 1: Recognize when a review's value depends on naivety

Ask: does this review need the reviewer to *not* know what I know? Checking a
document's clarity to an uninitiated reader, checking whether a plan
communicates on its own, or repeating a cold-read review that's already had
prior rounds — yes. If not, skip this skill and do the check directly.

### Step 2: Dispatch a subagent with an explicit exclusion list, not just an inclusion list

Use the `Agent` tool with `subagent_type: general-purpose` for open-ended
analysis. Do not use `Explore` — it's a read-only search agent, and its own
description says not to use it for design-doc auditing or open-ended
analysis.

Two things make the dispatch actually isolated instead of only nominally so:

- **Don't paste your own analysis, summaries, or prior findings into the
  prompt.** Point the subagent at the source file(s) and instructions and let
  it read them itself. Anything you summarize for it is context it wouldn't
  otherwise have — and defeats the point.
- **If the subagent has filesystem or repo access reaching beyond the one
  artifact under review, explicitly name and forbid the files you don't want
  it reading** — background docs, prior review rounds, related design notes,
  git log. A subagent left to wander a repo it can read will often go read
  the very things that would contaminate it, out of ordinary thoroughness.
  Naming them explicitly is the only reliable guard; "don't read anything you
  don't need" is too vague to hold.

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

### Step 3: Treat the subagent's output as the actual review, not a rough draft to rewrite

Resist the urge to "clean up" or re-derive its findings using your own
contaminated knowledge — that reintroduces the bias you dispatched the
subagent to avoid. If a finding recurs across independent rounds (different
subagents, different tools or models), that convergence is itself evidence
the finding is real rather than one reviewer's blind spot.

### Step 4: Report results plainly, including where they surprised you

A finding an isolated subagent produces that you, with full context, would
not have flagged (or would have argued yourself out of) is the actual signal
this technique exists for. Don't average it away.

## Verification

1. Spot-check one or two of the subagent's specific claims (quote, line
   reference) against the source file — a genuine cold read still has to be
   *accurate*, not just naive.
2. If two independent subagents (or a subagent and a prior human/other-model
   round) converge on the same finding without having seen each other's
   output, that's strong evidence the finding reflects the artifact, not the
   reviewer.

## References

- Related: `outside-perspective-session` — the same technique without a
  subagent tool: a separate chat, session, or model/vendor instance you hand
  the artifact to manually. Prefer it when your host has no subagent
  dispatch, or when you specifically want the isolation to cross a
  model/vendor boundary.
- Related: `prompt-committee` — for feedback from an actual different AI
  model or vendor, copy-pasted manually, rather than an in-session subagent.
