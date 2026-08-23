---
name: task-chunkdown
description: "Breaks large, ambiguous tasks into granular micro-steps to eliminate task paralysis and activation energy barriers. Trigger when user says 'task chunkdown', 'break this down', or 'chunk this'. Delivers first 3 steps upfront, then one step at a time. Use proactively whenever a user presents a large or overwhelming goal."
---

# Task Chunkdown

Removes activation energy barriers by decomposing tasks into small, immediately actionable steps. Delivers momentum before cognitive load sets in.

## Activation

On trigger phrase `task chunkdown` (or equivalent), ask granularity before decomposing:

```
How granular?
a) Quick tasks (~2 min each) — default
b) Deep work (~5 min each)
c) Full decomposition (~90 sec each)

Reply: defaults (or a/b/c)
```

Do not decompose until the user answers. If user says `defaults` or doesn't specify, use option a.

## Delivery cadence

1. **First response**: deliver steps 1, 2, and 3. End with: `Ready when you are.`
2. **Each subsequent response**: deliver one step only. Wait for user to confirm done (any acknowledgment: "done", "next", "ok", "✓") before giving the next.
3. **Final step**: close with `Task complete.` or `That's everything.` — no follow-up questions.

## Step format

Each step must be:
- A single, physical, immediately actionable action
- Completable without making any decisions
- Free of sub-steps or branching

**Good**: `Open a blank doc. Type the title.`
**Bad**: `Start drafting your introduction and think about your main argument.`

When solus-skill is active, apply compression to step labels — but never compress to the point of ambiguity:
- Full solus: `Step 1: Open doc. Type title.`
- Ultra solus: `1. open doc → type title`

## Mid-task interruption

If the user goes quiet, pivots, or says `pause` / `stop` / `end task`: stop delivering steps. Do not resume unless explicitly asked.

If the user says `restart` or `from the top`: re-ask granularity and start over.

## New goal while task is active

If the user introduces a new goal before the current one is complete, ask:

```
Finish current task first, or switch now?
a) Finish current — default
b) Switch now
```

If they choose b, drop the current task and begin activation flow for the new goal (re-ask granularity). Do not attempt to maintain both tasks simultaneously.

## Vague tasks

If the task has no clear first physical action (e.g. "get my life together", "fix everything"), scope-narrow before asking granularity:

```
What's the one area to tackle first?
a) Work / career
b) Finances
c) Health / routine
d) Something else — name it
```

Decompose only after the user picks a scope.

## Solus compatibility

Solus wins on format (compression, fragments, active voice). Task chunkdown wins on cadence (one step at a time after the first three). No conflict — they stack cleanly.
