---
name: outside-perspective-session
description: >-
  Get cold-read feedback on a document, prompt, plan, or design via a
  separate session, chat, or model instance -- not an in-process subagent.
  Use when: reviewing something this session wrote or iterated on; checking
  whether it reads clearly to someone with zero context; the user asks for
  "fresh eyes," "outside perspective," or "cold read"; a repeat review round
  would be biased by earlier findings; or you want a genuinely different
  model or vendor's read, not just a fresh window on the same one.
author: Claude Code
version: 1.0.0
date: 2026-08-27
---

# Outside Perspective (Session)

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
- You have no way to spawn an in-process subagent (a chat product without
  that feature, a host that doesn't expose it) but do have a way to start a
  second, independent conversation -- a new chat tab, a separate session, a
  different model or vendor entirely

## When NOT to Use

- The review doesn't depend on the reviewer being naive -- e.g. checking code
  compiles, running tests, verifying a fact against a source. Just do it
  directly.
- The task requires the reviewer to already share your context (e.g. "does
  this match what we discussed") -- a fresh session can't do that by
  definition.
- Your host *does* support spawning an in-process subagent and you have no
  reason to prefer a fully separate session (a different vendor, a human in
  the loop, a product without subagent support) -- use `outside-perspective`
  instead. It gets you the same isolation with less manual handoff: you
  dispatch and read the result back automatically, instead of copying text
  between two chats yourself.

## Problem

Self-review of your own artifact silently fails at exactly the thing it's
supposed to catch. If you wrote or have been fixing a document across several
turns, you already know what its undefined terms mean, what its citations
point to, and which past round's finding to route around -- none of which a
genuinely new reader has. Asking yourself to "read this as if you'd never
seen it" doesn't work: you can't unlearn context already in your window. The
review still looks thorough -- specific, quote-anchored, plausible -- and
still misses the exact class of problem, "does this communicate to someone
with nothing else to go on," that motivated running it in the first place.

This skill covers the case where you can't (or don't want to) solve that with
an in-process subagent: no subagent tool available, or you specifically want
the isolation to also cross a model/vendor boundary.

## Solution

### Step 1: Recognize when a review's value depends on naivety

Ask: does this review need the reviewer to *not* know what I know? Checking a
document's clarity to an uninitiated reader, checking whether a plan
communicates on its own, or repeating a cold-read review that's already had
prior rounds -- yes. If not, skip this skill and do the check directly.

### Step 2: Start a genuinely separate session

Any of these satisfy "separate" -- pick based on what's available and what
kind of independence you want:

- A new chat/conversation in the same product, with no shared history
- A different Claude Code session (new terminal, new session id)
- A different model in the same family (e.g. a larger or smaller model than
  the one that produced the artifact)
- A different vendor entirely (another AI product) -- useful when you want
  the review to not share even training-level blind spots with the author

What makes it work is the same in every case: the reviewing session must
start with nothing except what you deliberately give it.

### Step 3: Hand it an exclusion list, not just the artifact

Two things make the handoff actually isolated instead of only nominally so:

- **Don't paste your own analysis, summaries, or prior findings into the
  prompt.** Give the reviewing session the source file(s) or text and the
  review instructions, and let it work from those alone. Anything you
  summarize for it is context it wouldn't otherwise have -- and defeats the
  point.
- **If the reviewing session can browse or has access reaching beyond the
  one artifact under review** (a repo, a shared drive, search), explicitly
  tell it not to go looking for background docs, prior review rounds,
  related design notes, or history. A capable reviewer left to wander will
  often go find the very things that would contaminate it, out of ordinary
  thoroughness. Naming what's off-limits is the only reliable guard --
  "don't look at anything you don't need" is too vague to hold.

Example prompt shape, to paste into the fresh session:

```
You are being given exactly one task, with no other context on this project.
Read the attached/pasted material and follow the review instructions below
exactly.
Do not search for or assume any background beyond what's given here -- the
whole point is answering as someone who has never seen this project before.
If the material references something you don't have, treat that exactly as
a real cold reader would: note it as undecodable, don't guess at it.

[review instructions]

[artifact under review]
```

### Step 4: Bring the result back and treat it as the actual review

Resist the urge to "clean up" or re-derive its findings using your own
contaminated knowledge -- that reintroduces the bias you sought a separate
session to avoid. If a finding recurs across independent rounds (different
sessions, different models or vendors), that convergence is itself evidence
the finding is real rather than one reviewer's blind spot.

### Step 5: Report results plainly, including where they surprised you

A finding an isolated session produces that you, with full context, would
not have flagged (or would have argued yourself out of) is the actual signal
this technique exists for. Don't average it away.

## Verification

1. Spot-check one or two of the reviewing session's specific claims (quote,
   line reference) against the source -- a genuine cold read still has to be
   *accurate*, not just naive.
2. If two independent sessions (different chats, different models, or a
   session and a prior human review) converge on the same finding without
   having seen each other's output, that's strong evidence the finding
   reflects the artifact, not the reviewer.

## References

- Related: `outside-perspective` -- the same technique via an in-process
  subagent (the `Agent` tool) instead of a manually-run separate session.
  Prefer it when your host supports subagents and you don't specifically
  need a different vendor or a human in the loop -- it dispatches and
  collects the result automatically instead of requiring manual copy/paste
  between sessions.
