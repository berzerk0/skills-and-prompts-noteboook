# Foundation harness: wants and priorities

**What this is.** The output of the brain-dump-plus-committee exercise, which was
run as a *wants elicitation* — deliberately impractical, so that the wants would
surface without being pre-filtered by feasibility. This document extracts the
priority of principles from that dump by checking each want against what already
exists.

**What this is not.** A build plan. See the note at the bottom on why
[`VISION-ASSESSMENT.md`](VISION-ASSESSMENT.md) is premature.

---

## How priority was inferred

The dump was written unedited on purpose, which means it leaks emphasis. Four
signals, strongest first:

1. **Already solved before it was wished for.** If you built a thing and *then*
   wrote it on a wish list, you cared about it enough to act before articulating
   it. This is the strongest available signal and it dominates the ranking below.
2. **Recurrence.** Wants stated more than once in a single pass.
3. **Open-question phrasing.** "Where does that logfile go?" — a question mark in
   a wish list marks genuine uncertainty, not a want.
4. **Hedging and specificity.** The more carefully qualified, the more thought
   went in.

These are inferences from the text, not things you said. Correct them where they're
wrong — the ranking is the point of the exercise, so a wrong rank is worth fixing.

---

## Tier A — proven priorities (you built these before wishing for them)

Every row here is a want from the dump that already has a working implementation
in one of your two repos. This is not "could be built." It exists.

| Want (from the dump) | Already exists as | Where |
|---|---|---|
| "recognizes when to make a script... knows where output should go" | `script-it`, with a concrete threshold: 5+ items, or must be repeated to verify | crispy-couscous |
| "tell if it needs to expand... logfile? plan? skill? agent? script? mcp?" | `router` agent — "primary entry point, routes tasks to specialized subagents based on intent, domain, complexity" | crispy-couscous `.vibe/agents/router.toml` |
| "flexible between agents because it is based on principles more than specifics" | Per-harness compiler: `agents/*.yaml` → `.claude/`, `.pi/`, `.vibe/` | crispy-couscous `meta/generate_*.py` |
| "how those subagents best communicate... where does that logfile go?" | `SUBAGENT_RETURN_CONVENTION.md` — JSON schema, `status`/`task`, enum of success/error/partial/needs_input | crispy-couscous `docs/` |
| "knows when to sound the alarm if something breaks" | `escalate` — creates an escalation brief when stuck | crispy-couscous |
| "knows basic principles for the models it uses, they don't behave the same" | `MODEL_SELECTION_STRATEGY.md` | crispy-couscous `docs/` |
| "knows when contradictions between principles exist and how to balance them" | `pilot-preset` conflict-resolution section — explicit precedence rules between bundled skills | user-level skills |
| "when to be verbose and when to be direct" / "paragraphs vs bullet points" | `solus-skill` (three intensity levels) | user-level skills |
| "conflict between what is 'supposed to be' vs what it has evidence for" | The method in `cross-tool-notes.md`: trust source over docs, trust the artifact the tool parses over the one written for humans | notebook repo |
| "tell when the user needs assistance clarifying their ask" | `clarify` / `ask-questions-if-underspecified` | both repos |
| "isn't a gutless sycophant, without being obstinate" | `challenge-my-thinking` | both repos |
| "enough breadcrumbs for a session with 0 context to pick it back up" | `napkin` (curated runbook) + `planning-with-files` | both repos |
| "knows how to make a skill / prompt / agent" | `skill-creator`, `SKILL_DESIGN.md`, `prompt-pipeline` | both repos |
| "knows how to talk to other models, pass messages back and forth" | `prompt-committee` — and you just ran it, twice, at scale | notebook repo |
| "a single prompt or session can do too much" | `task-chunkdown` | both repos |
| "knows not to rm -rf or drop tables" | deny rules (harness) + `security-audit` | shipped + notebook repo |

**Read this table as the answer to "what am I really looking for."** You have been
building the foundation harness for months. The dump is a description of work
already substantially done, not a spec for work to start.

---

## Tier B — wished for, the harness already ships it

No action beyond configuration. The committee was unanimous on these once corrected.

- Destructive-command prevention → deny rules
- Deterministic logging → hooks
- Session resume from hard failure → shipped in both harnesses
- Subagent isolation with declared tool lists → a subagent definition, not architecture
- "doesn't try to load it all at once" → two-stage skill loading, already the default
- "connect to another source of information" → MCP

---

## Tier C — the actual gaps

Three, and only three, survive the audit.

### 1. The null branch

The router routes. `script-it` fires at 5+ items. Nothing in either repo makes
*"nothing is needed here, just answer"* an explicit, first-class output.

This is the single most valuable thing identified in the whole committee exercise,
and it came from one model with a support count of one: **a classifier whose output
space contains only expansions will always classify, and therefore always expand.**
The taxonomy generates the skill debt.

Cost to fix: one row in the router's decision table. Highest value-to-effort ratio
in this document.

### 2. Retirement

Nothing in either repo finds artifacts that nothing invokes. With two-stage loading,
every skill description is resident every turn whether or not it is ever used —
dead skills are a standing tax on context and a standing source of misrouting.

`repo-auditor` audits structure and compatibility, not usage. Closest existing thing,
but it doesn't answer "is this still earning its residency."

### 3. Consolidation

Two repos, overlapping skills, divergent conventions. `challenge-my-thinking`,
`clarify`/`ask-questions-if-underspecified`, `planning-with-files`, and
`skill-extractor` exist in both, and the notebook repo's `skills/README.md` records
`pilot-preset`, `karpathy-guidelines`, and `solus-skill` as *deliberately removed* —
while they remain live at user level and carry three Tier A wants between them.

That's not a bug, but it does mean no single place answers "what is the substrate."

---

## Want vs. mechanism — where the committee's rejections don't land

Two committee verdicts read as rejections of wants but are actually rejections of
*mechanisms*. The wants survive; they route elsewhere.

| Want | Mechanism you proposed | Committee verdict | Where the want actually lands |
|---|---|---|---|
| Portability across agents | Principle-level instruction ("based on principles more than specifics") | Rejected 7-1 — silent tool-drop means a behavioral hedge has nothing to react to | Satisfied already by `meta/generate_*.py`. The want was right; the mechanism was the thing that lost. |
| Don't repeat mistakes | "leaves logs for itself... can improve itself as a result" | Rejected unanimously — a lesson drawn from a log has no verifier | Satisfied by `napkin` + manual AGENTS.md edits. The event record is ground truth; only the *automatic* lesson-drawing was rejected. |

Worth keeping straight, because "the committee rejected that" is otherwise the wrong
takeaway on both.

---

## What was genuinely surprising

1. **You built the committee's top recommendation before the committee met.** The
   panel voted 7-1 for per-harness compilation from a single source. `meta/generate_all.py`
   already does exactly that, across three agents rather than two.

2. **The #1 line of the dump has an implementation.** "Tell if it needs to expand"
   is the first sentence of the brain dump and the thing I described as the one real
   gap. There is a `router` agent whose description is nearly a paraphrase of it.

3. **The hardest-to-cash-out line has the most concrete implementation.** "Knows when
   to make a script" sounds unfalsifiable. `script-it` cashes it out as a counted
   threshold: 5+ items, or repeated to verify. That is a trigger, not a feeling —
   exactly the standard the committee demanded and mostly failed to meet itself.

4. **Two wants were already solved twice.** Clarification and anti-sycophancy exist
   independently in both repos. Convergent invention across your own projects is a
   strong priority signal.

5. **The exercise's premise held.** Writing it impractically did surface the wants —
   but what it surfaced most clearly is that the wants were already being acted on.
   The dump reads less like a wish list and more like an inventory written from memory.

---

## What this implies

**Stop building. Start consolidating.** The substrate is roughly 85% built and split
across two repos plus a user-level skills directory. The remaining work is one router
row (null branch), one usage audit (retirement), and a merge.

**Corollary, and I'm the example:** earlier this session I built
`scripts/validate-tool-names.py` to satisfy B1. `skill-validator` and `repo-auditor`
already do that job in crispy-couscous. Check the other repo before building — the
duplication risk here is real and immediate, not hypothetical.

**On single-agent-first:** deferred, correctly. But note what the audit changes about
that decision — crispy-couscous is already tri-agent (Claude/Pi/Vibe) with a working
compiler. "Start with one agent" would mean *giving up* capability you have, not
avoiding work you'd otherwise take on. The reason to go single-agent was to harvest
rather than reinvent; the harvest already happened.

---

## Status of the other documents in this folder

- [`foundation-harness-vision-2026-08-25.md`](foundation-harness-vision-2026-08-25.md) — the dump. Unchanged, still the source.
- [`foundation-harness-behavior-spec-2026-08-25.md`](foundation-harness-behavior-spec-2026-08-25.md) — B1-B7. Still valid as *behavior specifications*; the "build this" framing is now wrong for B1 and B7, which exist.
- [`DEBATE-SUMMARY.md`](DEBATE-SUMMARY.md) — accurate on method and findings; its "next steps" predate the crispy-couscous audit.
- [`VISION-ASSESSMENT.md`](VISION-ASSESSMENT.md) — **premature.** Written as a build roadmap before the wants were prioritized and before the other repo was inspected. Its "what already exists" section is materially incomplete. Superseded by this document.
