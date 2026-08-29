---
name: outside-perspective-session
description: >-
  Gets cold-read feedback on a doc, prompt, plan, or design via a separate
  session, chat, or model instance -- not an in-process subagent. Use when:
  reviewing something this session wrote or iterated on; checking if it
  reads clearly to a zero-context reader; user asks "fresh eyes," "outside
  perspective," "cold read"; a repeat review round would be biased by
  earlier findings; or you want a genuinely different model/vendor's read,
  not just a fresh window on the same one.
metadata:
  author: Claude Code
  version: 1.0.0
  date: 2026-08-27
---

# Outside Perspective (Session)

## When to Use

- Iterating on a doc/prompt/plan across turns? Check it still reads clearly outside this conversation.
- User asks "fresh eyes," "cold read," "outside perspective," "how would someone unfamiliar read this."
- Reviewing something you wrote/edited/deeply know — review's value depends on the reviewer *not* sharing that background.
- Round 2+ review of the same artifact — round 1's findings are now things you "already know," can't un-know.
- No way to spawn an in-process subagent (chat product lacks it, host doesn't expose it) but can start a second, independent conversation — new chat tab, separate session, different model or vendor.

## When NOT to Use

- Review doesn't need naivety — checking code compiles, running tests, verifying a fact. Just do it directly.
- Reviewer needs to already share your context (e.g. "does this match what we discussed") — a fresh session can't, by definition.
- Host supports in-process subagents and there's no reason to prefer a separate session (no different vendor, no human in the loop) — subagent dispatch gives the same isolation with less manual handoff: it collects the result automatically instead of you copying text between chats.

## Problem

Self-review fails at exactly what it's meant to catch. Write or fix a doc across turns and you already know its undefined terms, its citations, which past round's finding to route around — none of which a genuinely new reader has. "Read this as if you'd never seen it" doesn't work: you can't unlearn context already in your window. The review still looks thorough — specific, quote-anchored, plausible — and still misses "does this communicate to someone with nothing else to go on."

This skill covers the case you can't (or won't) solve with an in-process subagent: none available, or isolation needs to cross a model/vendor boundary too.

## Solution

### Step 1: Recognize when naivety matters

Ask: does this review need the reviewer to *not* know what you know? Clarity to an uninitiated reader, whether a plan communicates alone, a repeat cold-read after prior rounds — yes. Otherwise skip this skill, check directly.

### Step 2: Start a genuinely separate session

Any of these count as "separate" — pick by availability and independence wanted:

- New chat/conversation, same product, no shared history
- Different Claude Code session (new terminal, new session id)
- Different model, same family (larger or smaller than the one that produced the artifact)
- Different vendor entirely — useful when the review shouldn't share even training-level blind spots with the author

What makes it work: the reviewing session starts with nothing except what you deliberately give it.

### Step 3: Hand it an exclusion list, not just the artifact

Two things make the handoff actually isolated:

- **Don't paste your own analysis, summaries, or findings into the prompt.** Give the session the source file(s)/text and review instructions, let it work from those alone. Anything you summarize is context it wouldn't otherwise have — defeats the point.
- **If the session can browse beyond the one artifact** (repo, shared drive, search), tell it not to hunt for background docs, prior rounds, design notes, history. Left to wander, a capable reviewer often finds the very things that contaminate it, out of ordinary thoroughness. Naming what's off-limits is the only reliable guard.

Example prompt shape, paste into the fresh session:

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

### Step 4: Bring the result back, treat it as the real review

Resist "cleaning up" or re-deriving findings with your own contaminated knowledge — that reintroduces the bias you sought isolation to avoid. A finding recurring across independent rounds (different sessions, models, vendors) is itself evidence it's real.

### Step 5: Report plainly, including surprises

A finding you, with full context, wouldn't have flagged (or would've argued away) — that's the actual signal this technique exists for. Don't average it away.

## Verification

1. Spot-check one or two session claims (quote, line reference) against the source — a cold read must be *accurate*, not just naive.
2. Two independent sessions (different chats/models, or a session and a prior human review) converge without seeing each other's output? Strong evidence the finding's real.
3. Exact counts (chars, lines, words): run the actual command (`wc -c`, `wc -l`) — don't eyeball.
