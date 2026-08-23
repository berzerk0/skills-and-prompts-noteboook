---
name: braindump-triage
description: Converts unstructured brain-dump text (a stream-of-consciousness list of worries, tasks, ideas) into an actionable list, triaged into do-now / do-later / delegate / drop rather than just tagged by topic. Use when someone needs to get everything out of their head and organized fast, or says "brain dump," "let me just dump everything," or similar.
---

# Braindump Triage

Converts an unstructured brain dump into an actionable list. Adapted from an older prompt called "Braindump Goblin," sharpened against real brain-dump/mind-sweep practice (GTD's mind sweep, ADHD brain-dump guidance) rather than just reskinned: the original only tagged items by topic; this version triages by what to actually do with each item, and makes dropping low-value items an explicit option instead of converting everything into a task.

## When to use

Someone has a lot of raw, unfiltered thoughts (tasks, worries, ideas, commitments) and needs them out of their head and organized fast. Not for a task that's already clear and scoped -- use `task-chunkdown` for that.

## Core moves

- **Capture first, organize second.** Don't ask clarifying questions before producing a first pass -- that defeats the point of a dump. Only ask afterward, and only for items that are genuinely unconvertible.
- **Not everything becomes a task.** Venting, narrative, and trivial mentions get stripped or dropped outright -- they don't need a home. Resist the pull to dignify every sentence with a checkbox.
- **Triage by action, not just topic.** A bare topic tag ([work], [home]) doesn't say what to actually do with an item. Sort into buckets instead.
- **Give it a destination.** A dump that doesn't feed into something -- a task list, a calendar, an explicit delete -- gets re-dumped next time with the same items still on it.

## Output

1. **Do now** -- quick, unblocked, or time-sensitive items. Checkable markdown bullets, imperative verbs, deadline or priority in **bold** first if present.
2. **Do later** -- real tasks, not urgent. Same format.
3. **Delegate / waiting on** -- only if an item depends on someone else. Note who or what it's waiting on.
4. **Drop** -- items with no real action behind them: venting, trivia, things resolved just by writing them down. List briefly so the user can confirm nothing got lost -- not to relitigate them.
5. **Open questions** -- only if no action can be inferred at all. Format: `? [item]` + one-line inferred meaning. If an action can be inferred, it's a task, not a question.
6. **Destination note** -- one line: where should this list live now (today's task list, calendar, `task-chunkdown`, delete)? Only if not obvious.

Omit 3 and 5 when nothing qualifies. Don't pad omitted sections with "none identified."

## Conversion rules

- Each task starts with an imperative verb.
- Deadline first in **bold** if present (e.g. "**Friday:** Call dentist").
- Strip venting, narrative, and emotional processing unless a task is implied.
- Only surface as an Open Question when truly ambiguous -- if the action can be inferred, just convert it.

## Focus narrowing

If the combined Do-now/Do-later list runs 7+ items, suggest picking no more than 3 to actually act on today rather than treating the whole list as today's plan. Long lists left untriaged are exactly what sends people back to re-dumping the same items next time.
