---
name: time-estimate
description: Produces a realistic time range (never a single number) for a task, with the reasoning and estimation traps that justify it. Use when someone needs to plan, schedule, or reality-check how long a task or project will actually take.
---

# Time Estimate

Produces a realistic time range for a task, with just enough reasoning to trust it. Adapted from an older prompt called "Time Goblin" — the estimation logic held up; the roleplay/activation scaffolding around it didn't need to survive the port.

## Output

1. **Scope** — one line echoing back what's being estimated.
2. **Assumptions** — only if they'd change the estimate.
3. **Time estimate** — range only, never a single number. Format: `[lower]-[upper] [unit]`.
4. **Rationale** — max 3 bullets, only material factors, no filler.
5. **Parallelization** — only if it meaningfully changes total time.
6. **Tracking tip** — one line, simplest viable method for checking estimate against actual.

Omit 2 and 5 when not material. Don't pad omitted sections with "none identified."

## Range sizing

- Small (under 1 hr): 1.5-2x spread — e.g. 20-40 min
- Medium (1-4 hr): ~1.5x spread — e.g. 2-3 hr
- Large (over 4 hr): 1.3-1.5x spread — e.g. 6-8 hr
- Multi-day: express in days, ~1.5x spread — e.g. 2-3 days

## Widens the range

Unfamiliar domain or tools, dependencies on other people, unclear requirements, creative or open-ended work, first time doing this kind of task.

## Narrows the range

Routine/repeated task, clear requirements, no dependencies, familiar tools and domain.

## Estimation traps to catch

- Forgetting setup/teardown time
- Ignoring context-switching cost
- Assuming zero interruptions
- Conflating hands-on time with elapsed time
- Underestimating review/revision cycles

## Clarifying questions

Ask at most 3, only if the ambiguity would actually distort the estimate:
- Rough draft or polished final version?
- Waiting on input from anyone else?
- Done this type of task before?
- What tools/systems are involved?

Wait for answers before producing the estimate. Re-ask only if an answer introduces new ambiguity.
