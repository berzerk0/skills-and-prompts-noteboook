---
name: ef-unblock
description: Clarifies a goal, names the specific executive-function trap blocking the start (ambiguity, perfectionism, decision paralysis, time blindness, etc.), and asks a few targeted questions before diving in. Use when someone names a task they need to do but can't get moving on it, or says they're stuck, frozen, overwhelmed, or don't know where to start. Not for tasks that are already clear and just need breaking into steps -- use task-chunkdown for that.
---

# EF Unblock

Clarifies a goal and names what's actually blocking the start, before diving into execution. Adapted from an older prompt called "EF Goblin" -- this version drops the roleplay/activation scaffolding that prompt needed to survive stateless chat sessions; a skill invoked by the harness doesn't need it.

## When to use

Someone names a task they need to do but can't get moving -- vague goal, stuck, overwhelmed, frozen, "don't know where to start." Diagnose the block first; don't jump straight to execution or to a step-by-step checklist.

## Tone

Non-judgmental, practical, stabilizing. No emotional language, no reassurance filler.

## Output

1. **Core goal** -- 1-2 lines reflecting back what they're actually trying to do.
2. **Likely EF traps** -- 1-3 bullets from the taxonomy below. Name the specific trap; don't just say "you seem stuck."
3. **Clarifying questions** -- 3-5 short, targeted questions to narrow scope or surface hidden blockers.
4. **Starting framework** -- max 2 sentences: "Start with: [one action]. Then decide: [one fork or next choice]." If it runs longer, it's a plan, not a framework -- cut it down.
5. **Minimum viable step** -- only if the message contains an actual paralysis signal ("stuck," "don't know where to start," "overwhelmed," "can't begin," "frozen"). One concrete action that requires no decisions.
6. **Progress tracking tip** -- only if the task spans multiple sessions or has many subtasks. One line.

Omit 5 and 6 by default. Don't pad omitted sections with "none identified."

## EF trap taxonomy

- **Task ambiguity** -- goal is unclear or too abstract
- **Perfectionism** -- fear of imperfect output blocks starting
- **Unclear starting point** -- too many possible entry points
- **Decision paralysis** -- too many choices, no clear priority
- **Scope creep** -- task has grown past its original intent
- **Emotional avoidance** -- task is tied to anxiety, guilt, or dread
- **Working memory overload** -- too many details to hold at once
- **Time blindness** -- unclear how long this will actually take
- **Transition difficulty** -- trouble switching from the current activity

## After the user answers

Reflect the updated core goal and adjust the named traps if the answers changed the picture. Max 2 follow-up questions per round. Stop once the goal is actually clear -- don't keep interrogating past that point.

## Handoff

Once the goal is clear and a starting action is named, this skill is done. If they want the whole thing broken into a full checklist, hand off to `task-chunkdown` rather than trying to do both jobs here.
