---
name: subagent-skill-patterns
description: >-
  Reference for building a skill whose steps dispatch subagents via the Agent
  tool -- how to structure the role prompt, pick a subagent_type for its tool
  access, choose foreground/background and one-shot/resumable, and fan out
  parallel workers with machine-readable output. Use when: (1) writing or
  editing a skill that needs to spawn subagents, (2) the user says "make this
  a skill that uses subagents," "parallelize this with subagents," or asks
  for a template/pattern for subagent-based skills, (3) deciding between a
  single isolated read, a fan-out grading/comparison pattern, or a long-lived
  collaborator agent.
author: Claude Code
version: 1.0.0
date: 2026-08-26
---

# Subagent Skill Patterns

## When to Use

- Writing a new skill (or a step within one) that should dispatch a subagent
  rather than do the work inline
- Deciding whether a task needs one isolated subagent, several parallel ones,
  or an agent you'll keep talking to across multiple turns
- The user asks for a "template" or "pattern" for subagent-based skills

## When NOT to Use

- The task doesn't need a separate context, isolation, or parallelism --
  just do it inline. Spawning a subagent for something you could do directly
  adds latency and a report-back step for no benefit.
- You specifically need the subagent to *not* know what you know (isolation
  is the whole point) -- see `outside-perspective` instead, which is this
  pattern applied to that one case.

## Problem

The `Agent` tool's own description covers mechanics (parameters, foreground
vs background) but not the design decisions that make a subagent-dispatching
skill actually work: how to write a reusable role prompt, which
`subagent_type` to pick and why it matters for tool access, whether a given
step should be one-shot or resumable, and how to fan out several subagents
so their results can be aggregated mechanically instead of re-read as free
text. Getting these wrong produces skills that either can't isolate context
when isolation was the point, spawn agents with the wrong tool access, or
fan out work that comes back in a shape nothing downstream can consume.

## Solution

### Step 1: Decide the dispatch shape first

- **Single isolated read** -- one subagent, no shared context, final report
  is the answer. (Pattern: `outside-perspective`.)
- **Fan-out workers** -- several subagents in parallel doing structurally
  identical work (grade N outputs, compare A vs B, run N eval cases), each
  writing a machine-readable result a later step aggregates.
- **Long-lived collaborator** -- one subagent you'll message more than once
  via `SendMessage`, because it should remember its own earlier work rather
  than have everything re-supplied each time.

These need different wiring below -- pick before writing the prompt.

### Step 2: Write the role as its own file, not inline in SKILL.md

Put it at `<skill-dir>/agents/<role>.md` (a skill-authored convention --
distinct from `.claude/agents/*.md`, which registers a new subagent *type*
with the harness and may not be supported on every host). A role file gets
*read and passed as the `prompt` parameter* at dispatch time, so it's
portable across any host that has the `Agent` tool at all. See
`references/role-template.md` in this skill for the skeleton, and
`skills/skill-creator/agents/{grader,comparator,analyzer}.md` in this repo
for three fully worked examples.

Shape: **Title**, **Role** (one paragraph -- mission, and what judgment calls
this role owns), **Inputs** (bullet list of parameters that get interpolated
into the prompt at dispatch time -- name each one, the caller fills them in),
**Process** (numbered steps), **Output Format** (the exact shape of the
final report -- a JSON schema with field descriptions if a later step
consumes it mechanically, plain prose if it's the final human-facing
answer), **Guidelines** (do/don't list -- this is where you encode tone and
the traps specific to this role, e.g. "stay blind: do not infer which skill
produced which output").

### Step 3: Pick subagent_type for its tool access, not its name

- `general-purpose` -- full tools. Default for anything that reads, writes,
  greps, and runs commands.
- `Explore` -- read-only, fast, cheap. Locating code only. Its own
  description says not to use it for review, audits, or open-ended analysis
  -- respect that even when it's tempting for speed.
- `Plan` -- read-only, for producing implementation plans.
- Narrower built-ins (e.g. `claude-code-guide`) -- use when the task is
  squarely inside their one stated domain; their tool list is fixed and
  won't stretch to cover anything else.

A project-defined `.claude/agents/*.md` type (frontmatter `tools:`
allowlist) scopes access tighter than any built-in, but registration support
is host-dependent -- confirm it works in your target environment before
relying on it; the role-file-as-prompt pattern above works everywhere the
`Agent` tool exists.

### Step 4: Assemble the dispatch prompt

`prompt` = the role file's full content + the actual values for this call's
Inputs, written in. If isolation matters and the subagent has filesystem
access reaching beyond what it should see, explicitly name and forbid the
files it shouldn't read (see `outside-perspective` for why naming them
beats a vague "don't look at anything you don't need").

### Step 5: Foreground vs background

Background (the default) for fan-out -- launch every worker in the same
message, let completion notifications land, aggregate once they're all in.
Foreground (`run_in_background: false`) only when your very next action
depends on this one result and there's nothing else useful to do meanwhile.

### Step 6: One-shot vs resumable

Default to one-shot: spawn, get the final report, done -- this is correct
for grading, comparison, review, and eval-running steps, where each call is
structurally independent. Reach for `SendMessage` to the same agent id only
when the task is genuinely iterative with one collaborator ("revise given
this new info") and re-supplying full context each time would be wasteful
or would lose state the agent built up on its own.

### Step 7: Make fan-out results aggregable

Have each worker write a structured file (JSON, with a field-descriptions
section in the role file itself, per `agents/grader.md`'s convention) rather
than returning free text. A later step should be able to read N result
files and produce an aggregate without re-parsing prose.

## Verification

1. Spot-check one subagent's output against the source material it was
   given -- isolation and cheap tool access don't guarantee accuracy.
2. For fan-out, confirm all N workers actually returned before aggregating
   -- a partial set silently treated as complete will skew results.
3. If two independently-dispatched subagents converge on the same finding
   without seeing each other's output, that convergence is itself evidence
   the finding is real.

## References

- `outside-perspective` -- this pattern applied specifically to isolated
  cold-read review (single dispatch, explicit exclusion list, why
  contamination defeats the point).
- `skills/skill-creator/agents/grader.md`, `comparator.md`, `analyzer.md` --
  worked examples of the role-file convention: fan-out grading, blind
  A/B comparison, and post-hoc analysis, each with a full Output Format
  section worth copying the shape of.
- `references/role-template.md` (this skill) -- blank skeleton for a new
  role file.
