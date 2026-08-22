# Skill Action Plan v3 — Vibe Build

**Date:** 2026-08-22 · **Target:** Mistral Vibe Code (primary), Claude Code (secondary)
**Baseline:** nothing installed anywhere · **Companion:** `vibe-code-reference.md`
**Tiers:** S = blocks everything else · A = high value · B = worth doing · C = only when the need is real

**Changed from v2:** added `/escalate` (new #4) and `napkin` (new #11). `/escalate` closes two holes v2 left open — item #2's 3-strike protocol had no defined escalation target, and item #3 routed cheap models with no failure path. Karpathy shifts from #4 to #5; everything below renumbers.

---

## Read this before installing anything

Two facts drive most of the reasoning below.

**Enabling a skill is cheap. Invoking one is not.** Vibe's system prompt carries only `<name>`, `<description>`, `<path>` per enabled skill. The body loads via the `skill` tool on demand, as a tool result, and then stays in conversation history for the rest of the session. So breadth costs almost nothing and **bloat costs a lot, once, at the moment of use**. This is why every item below says compress: you are not paying for the file sitting there, you are paying the day you call it.

**Wrong tool names fail silently.** Unrecognized entries in `enabled_tools` are dropped with no error. A stale Claude Code name doesn't break loudly — it quietly removes a capability, and you find out three sessions later when a skill can't write a file. Every port needs its `allowed-tools` rewritten, and the rewrite has to be checked.

---

## S Tier — Must have

### 1. writing-for-agents

**Get:** `git clone --depth 1 https://github.com/mattpocock/skills`
**Place:** copy `skills/productivity/writing-for-agents/` → `~/.vibe/skills/writing-for-agents/`
**Convert:** rewrite `allowed-tools` → `read_file`, `grep`, `edit`, `write_file`. Drop `Glob` (no equivalent). Set `user-invocable: true`.
**Not from Trail of Bits:** their fork is the pre-rename `writing-great-skills`, frozen 2026-07-14. Upstream v1.1 renamed it and expanded scope to cover AGENTS.md and CLAUDE.md — which item #5 needs.

**Why the ROI is highest here:** you are about to author a dozen `.toml` agent files, several prompt files, multiple AGENTS.md, and a set of compressed skills. Every one is a chance to bake in a mistake you'll pay for on every future session. This is the only item that improves *the quality of everything else on this list*, and it's user-invoked, so it costs nothing until you type it. Its author reports it as his own most-invoked skill — rare direct evidence of dogfooding.

**Do this first. Items 2 through 12 are all better if this comes first.**

### 2. planning-with-files — compressed

**Get:** `git clone --depth 1 https://github.com/trailofbits/skills-curated` (vetted, hooks removed, frozen Feb 22)
*or* `OthmanAdi/planning-with-files` (v2.32.x, active, ships hooks)
**Place:** `~/.vibe/skills/planning-with-files/`
**Convert:** compress ~200 lines to ~40. Keep only: filesystem-as-disk; save findings after every 2 reads; re-read the plan before deciding; log every error with attempt number; never repeat a failed action; 3-strike then escalate. Drop the templates, the 5-question reboot test, the read/write matrix. `allowed-tools`: `read_file`, `write_file`, `edit`, `grep`.
**Rewrite for Vibe:** point the file convention at **`scratchpad_dir`**, which subagents already receive and may write to without permission prompts. Don't invent a directory convention when the runtime hands you one.
**Wire the 3-strike exit to #4.** v2 left "escalate" undefined. It now means: run `/escalate`.
**Hook:** if you take the ToB version, its completion-check hook is portable — port it to `hooks.toml` as `POST_AGENT` rather than discarding it.

**Why the ROI is high:** `TaskResult` returns text only, so whatever a subagent says lands whole in the parent's context. Without file-handoff discipline, every delegation pollutes the controller — defeating the reason to delegate. This is what makes subagents actually pay off rather than just moving cost around. It's also the cheapest possible intervention: a behavioural rule, not machinery, working identically in Claude Code.

**Compressing it is itself the first `writing-for-agents` exercise.** Two returns from one task.

### 3. Model routing → `.toml` agent files

**Get:** `git clone --depth 1 https://github.com/obra/superpowers`, read `skills/subagent-driven-development/SKILL.md`, **Model Selection section only**
**Place:** nothing. This is harvest, not install.
**Convert:** write `~/.vibe/agents/*.toml` files with `active_model` set per role:
- transcription / single-file mechanical → cheapest tier
- reviewers, prose-spec implementers → mid-tier **floor**
- architecture, final review → most capable
- fix-loop escalation → one tier above whatever got stuck

Carry over verbatim: *"turn count beats token price"* — cheap models take 2–3× the turns on multi-step work and cost more overall.
**Also set, per agent:** `compaction_model` (separate from `active_model`), `allowed_models` as a guardrail, `enabled_tools` scoped tight — and **remember `skill` is a tool.** A subagent without it can't load skills at all.
**Define the failure path.** Cheap-model routing is only safe with a defined exit when the cheap model can't do the job. That exit is #4.
**Ignore:** the Mondoo "potentially malicious" badge. Its scripts are clean git plumbing; the scan is stale and you're taking prose anyway.

**Why the ROI is highest of the three cost levers:** you named token cost, wall-clock, and context pollution as all three being bottlenecks. Subagents fix context pollution and wall-clock but *raise* token cost. Model routing is the only lever that lowers spend directly, and Vibe exposes it as plain config — no framework, no orchestration layer, a handful of `.toml` files written once. Highest saving per hour of effort on the list.

---

## A Tier — High value

### 4. `/escalate` — write it yourself *(new in v3)*

**Get:** nothing external. ~30 lines, authored with #1.
**Place:** `~/.vibe/skills/escalate/` — `user-invocable: true`
**`allowed-tools`:** `read_file`, `write_file`, `grep`

**The four steps — every one retrieval and formatting, zero self-assessment:**

1. **Halt.** Stop troubleshooting. No apology, no final attempt, no "let me just try one thing."
2. **Read** the session transcript. In Vibe, get the path from the `POST_AGENT` hook payload (`transcript_path`) — same plumbing as #9. Also read `.vibe/napkin.md` if #11 is installed, but expect little from it (see below).
3. **Write** `.escalation/brief-<timestamp>.md`, or into `scratchpad_dir` when a subagent is what failed.
4. **Output one line:** `Brief at <path>. <route>.`

**Brief format:**

```markdown
# Escalation Brief — <timestamp>
## Goal
<original ask, one paragraph, from the first user turn>

## Current state
<what works, what's broken, exact repro command>

## Errors (verbatim)
<exact stderr/stack, unedited, deduplicated>

## Attempted and failed
- <approach> → <why it failed>

## Files touched
<paths + one-line what changed>

## Uncertain / unverified
<anything assumed but never confirmed>
```

**Deliberately does not:** count attempts · decide whether escalation is warranted · attempt a solution summary · clean up the record to look competent. Failed approaches stay raw — the strong model needs the dead ends in order to skip them.

**Why retrieval-only, correctly stated:** since *you* type `/escalate`, the model isn't being asked to self-assess anyway. The real risk is **editorializing** — a model summarizing its own failures will smooth them, drop the embarrassing dead end, and produce a tidy narrative. Retrieval-only prevents that. The `## Uncertain / unverified` section is the highest-value one and the hardest to get filled honestly; it's where the assumption that caused the spiral usually hides.

**The route fork — Vibe-specific:**

- **Self-contained problem → dispatch a subagent** with a stronger `active_model` and the brief path. Subagents start with *fresh, empty context* (verified: `create_child()` passes no parent history; the first message is only `prepare_subagent_prompt`). You get the clean-context benefit without opening a new session.
- **Might need dialogue → open a fresh session.** Subagents cannot use `ask_user_question`. A strong model that needs to ask something will guess instead.
- **Never Shift+Tab.** Agent switching swaps the model but keeps the polluted context, which defeats the entire point. The fresh-context requirement is real, not a Claude Code habit.

**The return leg — do not skip this.** After the strong model solves it, append the lesson to napkin **in napkin's required format**, or its own curation will prune it as a mistake log:

```markdown
1. **[2026-08-22] Devstral loops on multi-file async refactors**
   Do instead: route async refactors to Mistral Large from the start.
```

**Why the ROI is high:** this closes two holes at once — #2's 3-strike protocol had no target, and #3 routed cheap models with no failure path. It also fixes the *cost* of escalating. Today a handoff means re-explaining hours of context to a fresh session, expensive enough that fighting the weak model keeps looking cheaper. Drop that to one command and the calculus flips. And the return-leg entries accumulate into the empirical answer to the question underneath your whole routing strategy: **which task classes does the cheap model actually fail at.** Ten entries and you have data instead of guesses.

**What it does not fix:** you still have to notice and type it. No hook, no automatic trigger. That's fine — lowering friction beats requiring discipline, and `/escalate` reads as *routing a task* rather than *giving up*.

### 5. karpathy-guidelines → per-agent prompt files

**Get:** `multica-ai/andrej-karpathy-skills/skills/karpathy-guidelines/SKILL.md`
**Place:** `~/.vibe/prompts/implementer.md`, referenced by `system_prompt_id` in your implementer subagent `.toml`
**Convert:** compress ~60 lines to ~15 — four headers, one bullet each. Add your own ambiguous-verb rule ("validate", "check", "process", "handle" have multiple meanings — ask). That bullet is yours, not upstream's.
**Not AGENTS.md.** Community reports say the constraints backfire — agents refusing warranted refactors, skipping needed infrastructure updates, writing lazily. AGENTS.md is resident every turn for every agent; a contested rule is the worst thing to make unconditional.

**Why per-agent is the higher-ROI placement:** "don't touch unrelated code" is *correct* for an implementer working a narrow task and *wrong* for a main agent you're asking for architectural judgment. `system_prompt_id` per agent costs nothing extra and converts a globally contested rule into a locally correct one. Same content, none of the downside.
**Note:** upstream repo stale since 2026-04-20. Harvest, don't depend.

### 6. Merged clarify skill

**Get:** `trailofbits.com/skills/ask-questions-if-underspecified/` — **the web page is the only surviving copy**, the GitHub plugin was deleted. Plus `mattpocock/skills` → `grill-me`.
**Place:** `~/.vibe/skills/clarify/` — write it yourself, ~25 lines.
**Convert:**
- From ask-questions: the six-dimension underspecification test (objective / done / scope / constraints / environment / safety), and don't-ask-what-a-cheap-read-answers
- From grill-me: one question at a time, always supply your recommended answer, look up *facts* but put *decisions* to the user
- Drop all question-formatting guidance — Vibe has `ask_user_question` natively
- `allowed-tools`: `read_file`, `grep`, `ask_user_question`

**Decide first:** ask-questions caps at 1–5 questions; grill-me ships a design doc explicitly rejecting caps. Opposed philosophies. Pick one.
**Hard constraint:** main-agent only. **Subagents have no access to `ask_user_question`** — a subagent hitting ambiguity will guess or return partial results rather than ask.

**Why the ROI is high:** the cheapest bug is the one never written. Every wrong assumption at the top of a task propagates through the subagents beneath it, and with subagents structurally unable to ask, the parent is your *only* place to catch ambiguity. ~25 lines guarding the most expensive failure mode in the system.

### 7. skill-extractor

**Get:** `trailofbits/skills-curated/plugins/skill-extractor/skills/skill-extractor/`
**Place:** `~/.vibe/skills/skill-extractor/`
**Convert:** `allowed-tools` → `read_file`, `write_file`, `grep`, `web_search`, `ask_user_question`. **Drop `Glob`.** Rewrite save paths from `~/.claude/skills/` to `~/.vibe/skills/`. Set `user-invocable: true`.

**Why the ROI is high:** you're about to spend real hours learning Vibe's quirks — silent tool-name failures, docs-vs-source drift, what compresses well. That knowledge either becomes reusable skills or evaporates. This is the capture mechanism, and it pairs with #1 (which tells it *how* to write what it captures) and sits at the top of the memory ladder described under #11.
**Caveat:** thinnest sentiment signal on the list — 2 commits, frozen February, no discussion either direction. Adopt on merit, not evidence.

### 8. modern-python — full plugin

**Get:** `trailofbits/skills/plugins/modern-python/skills/modern-python/` — **not** the agenticskills.io mirror, three months stale and misreporting the license as AGPL-3.0 (actual: CC-BY-SA-4.0)
**Place:** `~/.vibe/skills/modern-python/` including its `references/` directory
**Convert:** `allowed-tools` → `read_file`, `write_file`, `edit`, `grep`, `bash`. Leave references intact — loaded on demand, not resident.

**Why it's in A tier:** the value isn't setup convenience, it's **anti-drift** — stopping agents defaulting to `pip`, `flake8`, `virtualenv`, `mypy` when the modern stack is `uv`, `ruff`, `ty`. That drift is expensive because it's invisible; you get working code with outdated tooling and only notice at integration.
**Fit bonus:** Vibe itself is a Python 3.12+ uv-managed project. Your agents work in the same idiom as the tool running them.
**Structural bonus:** best-structured skill on this list — thin SKILL.md, nine on-demand reference files. Exactly right for Vibe's cost model, and a working example to imitate in #2.
**Signal:** most actively maintained Trail of Bits plugin — 17 commits, last 2026-08-18.

---

## B Tier — Worth doing

### 9. Token measurement via transcript parsing

**Get:** `anthropics/claude-plugins-official/plugins/session-report/skills/session-report/` — read `analyze-sessions.mjs` for **technique**, not reuse
**Place:** your own script; register a `POST_AGENT` hook in `~/.vibe/hooks.toml`
**Convert:** `--output json` emits `{"history": [...]}` with **no token data**, and hooks carry **no token counts**. But `POST_AGENT` receives **`transcript_path`** — so the approach transfers and only the file format differs.
**Steal the metric list:** tokens by skill, tokens by subagent type, cache-hit rate, cache-break clustering, single prompts exceeding 2% of total.
**Shares plumbing with #4** — both read `transcript_path`. Build the reader once.
**Verify first:** the transcript format was never inspected. Fire a `POST_AGENT` hook, read the file, confirm it carries usage before building.

**Why the ROI is high despite tier B:** you have no token baseline for Vibe, which means every optimisation is unmeasurable and you can't tell a win from a regression. Arguably run this *before* #3 so you can prove the routing worked. Tier B only because it's build-your-own with an unverified dependency — if the transcript lacks usage data, the item needs rethinking.

### 10. Parallel-dispatch prompt discipline

**Get:** `obra/superpowers/skills/dispatching-parallel-agents/SKILL.md`
**Place:** `~/.vibe/prompts/*.md` — harvest ~20 lines into your subagent prompt files
**Convert:** keep the independence test (truly separate domains, or would fixing one fix the others?) and the prompt-construction discipline — focused scope, self-contained context, explicit constraints, specified return format. **Rewrite the return format for Vibe:** write to `scratchpad_dir`, return the path, not prose.
**Do not install.** Its core mechanic — multiple dispatches in one response equals parallel — assumes a controller that fans out on demand. In Vibe concurrency is real but **model-initiated**; you can't force it.

**Why the ROI is moderate:** the doctrine is good and it's twenty lines, but you can't drive Vibe's dispatch directly, so it shapes *how well* subagents work rather than *whether* they run.
**Corroboration:** Mondoo independently flags this skill for description mismatch — claims to dispatch, actually just describes. Same conclusion reached independently: doctrine, not machinery.

### 11. napkin *(new in v3)*

**Get:** `git clone --depth 1 https://github.com/blader/napkin` — MIT, single 3.2KB SKILL.md, v6.0.0
**Place:** `~/.vibe/skills/napkin/`
**Convert:** change `.claude/napkin.md` → `.vibe/napkin.md` throughout. No `allowed-tools` to rewrite — it has none. Trivial port.

**Read the SKILL.md, not the README — they contradict each other.** The README describes continuous journal-style logging. SKILL.md v6.0.0 (commit *"Update napkin skill to v6 curated runbook model"*) says the opposite: a **continuously curated runbook, not a chronological log**, with *"do not use raw journal-style entries."* It explicitly excludes one-off timeline notes, verbose postmortems without reusable action, and pure mistake logs without a `Do instead:` line. Max 10 items per category, re-prioritised and pruned on every read.

**Consequence for #4:** napkin is **not** the input layer for escalation briefs. Your spiral today is a one-off timeline note and a pure mistake log — exactly what napkin discards, and it prunes on every read. `/escalate` leans on the transcript. Napkin contributes at most one line, and only if the failure was recurring.

**Where it does fit — the third rung of a memory ladder you already have:**

| Horizon | Skill | Content | Lifetime |
|---|---|---|---|
| Task | #2 planning-with-files | Working memory, findings, error log | Disposable |
| Repo | #11 napkin | Recurring lessons, curated, capped | Permanent, per repo |
| Global | #7 skill-extractor | Generalisable lessons promoted to skills | Permanent, cross-repo |

No redundancy — three different horizons. Napkin is the cheap capture; skill-extractor promotes the ones worth generalising.

**Why B and not A:** it's `always active, every session, no trigger` — so its body loads every session plus the napkin file contents. Unavoidable recurring cost in a setup you're building to be lean. Modest (3.2KB skill plus a capped file), real, and permanent. Worth paying; not urgent.
**Gitignore `.vibe/napkin.md` for now.** Commit it later if the lessons turn out to be team-shaped rather than personal.

---

## C Tier — Only when the need is real

### 12. handoff

**Get:** `mattpocock/skills` → `handoff` (or the ToB `productivity` fork)
**Do:** nothing yet. Re-authorable in ~20 lines when you actually have a cross-session transfer problem. Note that #4 already covers the *failure* handoff case; this is for the ordinary one. Revisit once #9 shows you where context is being lost.

---

## Rejected

| Item | Reason |
|---|---|
| `session-report` as install | Parses `~/.claude/projects/**.jsonl` only. Technique transfers (#9); code doesn't. |
| `skill-improver` | Needs `plugin-dev` from another marketplace — and Vibe has no marketplace at all. Its `Stop` hook drives a 20-iteration autonomous loop gated on a literal string match. Actively maintained (8 commits); the objection is design, not neglect. |
| `code-simplifier` | Hardcoded TypeScript/React/ES-module conventions. Auto-triggers on every edit. 1 commit, zero discussion. Also **directly contradicts #5** — "proactively refine recently modified code" vs "don't refactor what isn't broken." |
| `python-code-simplifier` | Same agent with Python standards. Code clarity isn't the bottleneck. |
| `teach` | Multi-session teaching workspace. No fit. |
| `subagent-driven-development` as install | Hard-depends on three sibling superpowers skills; mandates worktrees, ledger, 5-round fix loop. HN reports it's stripped to ~30% in practice. Harvest only — see #3. |
| `pilot-preset` | Bundling in Vibe is the `enabled_skills` allow-list. Becomes a config stanza, not a skill. |
| `solus-skill` / `caveman` | Compresses output *to you*. Upstream's own `HONEST-NUMBERS.md` says it adds ~1–1.5k input tokens per turn, saves nothing on input, and goes net-negative on terse workloads. Readability preference, not a spend lever. Keep for claude.ai if you like it. |
| `copilot-preset`, `prompt-committee`, `prompt-pipeline`, `task-chunkdown` | Chat-shaped. Don't belong in a coding agent. |
| `prompt-master` | claude.ai only. ~6,800 tokens to load — token-negative for one-off prompts. Use once to author `~/.vibe/prompts/*.md`, then dormant. Ignore its Claude block: names Opus 4.8 as current; flagship is Opus 5. |

---

## Cross-cutting rules for every port

**1. Rewrite `allowed-tools`.** See `vibe-code-reference.md` §1 for the full table. The three that bite: `Edit` → **`edit`** (not `search_replace`, which does not exist), `Glob` → **no equivalent**, and unrecognized names are **silently dropped**.

**2. Rewrite paths.** Imported skills hardcode `~/.claude/skills/` and `.claude/skills/`. Vibe wants `~/.vibe/skills/` and `./.vibe/skills/`. Docs claim `./.agents/skills/` works — it does not, per source.

**3. Set `user-invocable: true`** on anything you'll call by name. It adds a slash command. It does **not** hide the skill from the model — no such per-skill control exists. `enabled_skills` in `config.toml` is your only reach lever, and it's global.

**4. Don't strip hooks — port them.** `PRE_TOOL` ≈ `PreToolUse`, `POST_AGENT` ≈ `Stop`. Config is `hooks.toml`, not `hooks.json`.

**5. Compress before installing.** Body cost is paid at invocation, in full, and stays in history. A 200-line skill you call once costs 200 lines for the rest of that session.

**6. Budget AGENTS.md hard.** Resident every turn, and it loads one per project root plus user-level — not the two the docs claim.

**7. Pass `--agent` explicitly when scripting.** Programmatic mode falls back to `default_agent` (default `accept-edits`), not the `auto-approve` the docs claim. Less dangerous than documented, still not what you want unattended.

**8. Read SKILL.md, not README.** Napkin's disagree by a whole design model. Assume any imported skill's README may describe a superseded version.

---

## Suggested order

1. **#1** — writing-for-agents. Everything downstream is better authored with it.
2. **#9 + hooks foundation** — get a baseline *before* optimising, or you can't tell a win from a regression. Build the `transcript_path` reader once; #4 reuses it.
3. **#2** — compress planning-with-files. First authoring exercise, graded by #1.
4. **#3 + #5** — the `.toml` agent files and their prompt files, together. Measure against the #9 baseline.
5. **#4** — `/escalate`, once #3 gives you something to escalate *to*.
6. **#6, #7, #8, #10, #11** — any order.
7. **#12** — when the need appears.

---

## Still open

1. **Question cap in #6** — ask-questions caps at 1–5; grill-me rejects caps. Unresolved.
2. **planning-with-files source** — ToB (vetted, frozen) vs upstream (current, hooks). Unresolved.
3. **Transcript format** — never inspected. Blocks #9 and step 2 of #4.
4. **claude.ai hard reset** — separate exercise. Survivors from the current set: `prompt-master` (dormant), optionally `caveman`/`solus`. Everything else is Vibe-side or chat-shaped.
