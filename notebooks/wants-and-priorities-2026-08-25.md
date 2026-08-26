# Foundation harness: ambitions, principles, and what's actually true

## Epistemic status — read this first

**This is not a plan and nothing here is committed to.** It is a set of ambitions
worth returning to, plus a record of what was verified when they were checked
against two real repos.

Three separate things got conflated in earlier drafts of this document. Keeping them
apart is the whole point:

| Layer | What it is | How much weight it carries |
|---|---|---|
| **The ambitions** | The brain dump. Written deliberately without regard to practicality, as a wants-elicitation exercise. | High as a statement of what you want. Zero as a spec. |
| **The committee** | 8 models, 2 rounds. | **Low.** Each model got essentially one shot per round, no iteration, no repo access, no ability to run anything. They were reasoning about a description, not a system. Useful for surfacing disagreement; not evidence about your code. |
| **The verification** | Files read and commands run in `crispy-couscous` on 2026-08-25. | Highest of the three, and still narrow — see the log at the bottom for exactly what was and wasn't checked. |

The committee's "reality check" deserves its scare quotes. Its main value was
*forcing variance* — round 1 produced convergent consensus that was mostly useless,
round 2 produced disagreement worth reading. It did not validate anything about the
repos, because it never saw them.

**History this sits on top of:** crispy-couscous was the first attempt. This notebook
repo was a semi-restart. The committee was an anti-over-engineering check on both.
None of the three has superseded the others, and that's the actual current state.

---

## The ambitions worth returning to

Stated as principles rather than features, because that's the form that survives
re-reading. These are the parts of the dump that still look right after the audit.

1. **Decide the shape of the work before doing the work.** Does this ask need a
   logfile, a plan, a script, a new skill, a subagent, an MCP connection — or
   nothing? Getting this wrong is more expensive than doing the work badly.

2. **"Nothing" must be an available answer.** A decision procedure whose output
   space contains only expansions will always expand. This was the single sharpest
   idea in the committee round and it came from one model, with a support count of
   one — so weigh it on its merits, not its backing.

3. **Artifacts need a declared home.** "Where does that logfile go?" appears twice
   in the dump, both times as a question. That's genuine uncertainty, not a want.

4. **Evidence beats documentation, including your own.** Where a tool's docs and its
   source disagree, the source wins. You already operationalized this in
   `cross-tool-notes.md` — and the audit below shows a case where your own system
   prompt was the thing that disagreed with reality.

5. **Triggers should be countable, not felt.** "Knows when to sound the alarm" is
   uncashable. "3 failed attempts" is not. The best existing work in either repo
   follows this rule; the weakest parts don't.

6. **Separate retrieval from judgment.** `escalate` does this explicitly and it's the
   best-designed thing in either repo — it gathers the transcript and formats a brief,
   and *deliberately refuses* to decide whether escalation is warranted or to
   summarize an attempted solution.

7. **Portability is a compilation problem, not a prose problem.** Committee voted 7-1
   here and the working compiler in crispy-couscous agrees with the majority. Note
   the one dissenter disclosed that its position favored its own harness.

8. **Dead artifacts are not inert.** Two-stage loading means every description is
   resident every turn. Unused skills cost tokens and cause misrouting.

9. **Best-effort, because models predict tokens.** The dump's closing line, and the
   right frame for all of the above.

---

## Verification log — 2026-08-25

Checked against `berzerk0/crispy-couscous` @ `4d2c23d`. Everything below was read or
run, not inferred.

### Verified true

- **The per-harness compiler works.** `python3 meta/generate_all.py --validate`
  returns clean on all 13 canonical YAMLs. `agents/*.yaml` → `.claude/agents/*.md`,
  `.pi/agents/*.md`, `.vibe/agents/*.toml`. This is the committee's 7-1
  recommendation, already built and functional.
- **`script-it` is substantive.** Counted trigger (5+ items, or must be repeated to
  verify), an explicit "when not to script" list, the mechanical/judgment split, and
  concrete authoring rules (dry-run first, print a verifiable N-found/N-changed
  summary, PEP 723 throwaway). It has its own null branch.
- **`escalate` is substantive.** Four steps, a fixed brief format, an explicit
  "deliberately does NOT" list, a route fork, and a return leg that appends a dated
  lesson to `napkin.md`.
- **The 3-strike counter exists.** `planning-with-files` defines attempts 1/2/3 and
  hands off to `/escalate` after three failures. Combined with `escalate`, the
  non-progress alarm is real and better-designed than what the committee proposed.
- **`SUBAGENT_RETURN_CONVENTION.md` exists** with a JSON schema
  (`status` ∈ success/error/partial/needs_input, `task`, artifacts, warnings, stats).
- **The router prompt is real** — 213 lines at `prompts/router.md`, with priority
  tiers, trigger tables, and domain keyword routing.

### Verified false — claims I made that were wrong

- **`skill-validator` does not validate anything.** 25 lines: frontmatter, a restated
  description, and a list of trigger phrases. No spec definition, no checks, no logic.
  It names an intent. It is a routing shim, not an implementation. My earlier claim
  that it duplicated `notebooks/behaviors/validate-tool-names.py` was wrong — those are not the
  same kind of object.
- **`repo-auditor` is the same shape.** 26 lines, trigger phrases only.
- **"~85% built" was fabricated.** I inferred it from directory listings and two file
  heads. There is no defensible single number; the per-item log is the honest form.
- **The router does not answer the dump's first question.** It dispatches among
  *existing* subagents by keyword match. The dump asks whether the ask requires
  creating a *new* skill / agent / prompt template / script. No branch in the router
  covers "the needed capability doesn't exist yet."

### Verified false — claims the repo makes about itself

These matter more than my errors, because they live in a system prompt an agent will
act on.

- **`prompts/router.md`: "All skills have Python implementations. Use `bash` to
  execute them when appropriate."** There are **zero** `.py` files across all 13
  skills. An agent running this prompt will look for implementations that do not
  exist.
- **`prompts/router.md`: "You have access to 17 specialized subagents and 11
  skills."** Actual: 19 vibe agents, 13 claude agents, 13 canonical YAMLs, 13 skills.
  No reading of the repo produces either number.

### Verified — structural gap

- **The router is outside the single source of truth.** 19 vibe agents vs. 13
  canonical YAMLs. Six orchestration agents — `router`, `architect`, `implementer`,
  `reviewer`, `escalation-fixer`, `transcription` — exist only under `.vibe/` and are
  not compiled from `agents/*.yaml`. The component implementing the most-wanted
  capability is the least portable thing in the repo.

### Not checked

- Whether the generators produce *correct* output, only that they validate input.
- Whether the router has ever been run, or routes well in practice.
- Any of `.pi/`, `docs/architecture/`, `docs/multi-agent/`, `main/`.
- The notebook repo's own skills against the same standard — several are likely
  thin in the same way `skill-validator` is.
- Drift: your own `docs/audit-report-2026-08-22.md` lists `challenge-my-thinking` at
  182 lines; it is 26 today. The repo has changed shape recently and I did not trace
  what happened.

---

## What's genuinely open

Stated as questions, because they are questions.

1. **Does anything decide whether a *new* capability is needed?** The router
   dispatches; `script-it` decides one narrow case (script vs. no script) well. The
   general version of the dump's first line is unbuilt in both repos.

2. **Is "nothing needed" reachable?** The router's Priority 4 handles meta-questions
   ("what skills are available?"), and Priority 5 falls back to clarifying questions.
   Neither is "this task needs no artifact, just answer it."

3. **What audits usage?** Nothing in either repo asks whether a skill still earns its
   residency. `repo-auditor` would be the natural home if it did anything.

4. **What is the relationship between the three attempts?** crispy-couscous,
   this notebook, and the user-level `~/.claude/skills/synced/` set all hold pieces.
   `skills/README.md` here records `pilot-preset`, `karpathy-guidelines`, and
   `solus-skill` as deliberately removed — while they remain live at user level and
   carry real weight. No single place answers "what is the substrate."

5. **How much of the existing surface is stubs?** Two of the four crispy-couscous
   skills I read closely were trigger-phrase shims. That rate, if it holds, changes
   what "already built" means substantially — and it is cheap to measure.

---

## Where the committee's verdicts land after verification

Two verdicts read as rejections of *wants* but were rejections of *mechanisms*:

| Want | Your proposed mechanism | Committee | Where it actually lands |
|---|---|---|---|
| Portability across agents | Principle-level instruction | Rejected 7-1 | The want is satisfied by the compiler you already built. The mechanism lost; the want didn't. |
| Don't repeat mistakes | Agent reads its own logs and self-improves | Rejected unanimously | Satisfied by `escalate`'s return leg — a dated lesson appended to `napkin.md` by hand. Only *automatic* lesson-drawing was rejected. |

And one verdict the verification undercuts: the committee treated tool-name
validation as the highest-consensus behavior (7 of 8). That consensus was formed
about a two-harness world with silent drops. It is still right for Vibe — but the
committee never saw that a compiler already existed, so it was answering a question
that had been partly solved before it was asked.

---

## Status of the other documents here

- [`foundation-harness-vision-2026-08-25.md`](foundation-harness-vision-2026-08-25.md) — the dump. The source. Unchanged and still worth re-reading directly.
- [`foundation-harness-behavior-spec-2026-08-25.md`](foundation-harness-behavior-spec-2026-08-25.md) — B1-B7. Valid as behavior *descriptions*; its "build this" framing is wrong for the alarm (exists, better than proposed) and partly wrong for validation.
- [`DEBATE-SUMMARY.md`](DEBATE-SUMMARY.md) — accurate on method. Its "already exists" and "next steps" sections predate this verification.
- [`VISION-ASSESSMENT.md`](VISION-ASSESSMENT.md) — **superseded.** A build roadmap written before priorities were extracted and before either repo was inspected. Its phase structure and timelines were invented, and it is kept only as a record of that error.
