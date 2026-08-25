# Foundation harness -- candidate behavior spec (2026-08-25)

Extracted from the two-round model debate in
[`foundation-harness-vision-debates/`](foundation-harness-vision-debates/),
against the brain dump in
[`foundation-harness-vision-2026-08-25.md`](foundation-harness-vision-2026-08-25.md).

**Status: candidate.** Nothing here has been built or measured. This lives in
`notebooks/` on purpose. Promote a behavior into `docs/` only after it has run
in this repo and produced evidence, per the rule in
[`../notebooks/README.md`](README.md).

## How to read this

**Support counts measure agreement, not correctness.** Eight models answered
round 2; seven produced a complete behavior list (haiku-4-5-response-2 was
truncated mid-list, so its absences are unknown, not disagreement). A behavior
backed by seven models can still be wrong, and the single most useful item in
this document has a support count of one. Support is listed because it is
information, not because it is a ranking.

**Every behavior carries four fields**, in the format the round 2 prompt
required:

- **Trigger** -- the observable condition that fires it. Countable or
  detectable, never a judgment call.
- **Falsifier** -- the evidence that it failed to fire when it should have.
  Without this the behavior cannot be checked and does not belong here.
- **Failure mode** -- loud, silent, or expensive. Silent is worst: it costs
  nothing at the time and is discovered later, if ever.
- **Enforced at** -- where the behavior actually lives.

**The enforcement ladder**, highest rung first. Take the highest rung that can
carry the behavior:

1. **Deny rule** -- the harness refuses the call. The model gets no vote.
2. **Hook** -- fires deterministically on an event. The model does not author
   the result and cannot skip it.
3. **Skill text** -- instruction the model reads. Biases a choice; does not
   guarantee it.
4. **Model judgment** -- nothing enforces this. Acceptable only when the top
   three provably cannot carry it, and worth writing down as a known soft spot.

The panel put a lot of behaviors on rung 4 that belong on rung 2. Where that
happened it is called out.

---

# Tier 1 -- build these first

Strong panel support, cheap to build, and each one targets a failure this repo
has already had.

## B1. Tool-name assertion before commit

Every tool name written into a skill's frontmatter is checked against a
per-harness tool table before the file lands.

- **Trigger:** a commit touches a skill file's frontmatter or `allowed-tools`
  list.
- **Falsifier:** a resident skill naming a tool absent from the target
  harness's table.
- **Failure mode:** silent. Vibe drops unrecognized tool names with no error;
  the skill loads and appears healthy while crippled.
- **Enforced at:** hook (pre-commit lint). Model judgment cannot carry this --
  there is no error to react to, which is the entire problem.

**Panel support:** 7 of 8 listed it as a behavior. The eighth (Gemini) argued
the same requirement in Part C1 without listing it. Nothing else in either
round came this close to unanimous.

**Enforcement split:** the panel proposed pre-commit (Opus, Mistral, Luna,
Haiku-1), on-load (Lumo, Gemma, Haiku-2), and runtime interception (Gemma,
Haiku-1). Prefer pre-commit as primary: it is the only rung that catches the
fault before the file ever reaches the other harness. On-load validation is a
reasonable backstop, not a replacement.

**Local evidence:** Mistral reported, from a real session in this repo,
translating `Read` to `read_file` incorrectly in a skill's `allowed-tools`.
The skill loaded, was crippled, surfaced no error, and the fault was found only
when the skill failed to do its job.

**Cost:** a table of valid tool names per harness, plus a script that walks
frontmatter. `docs/cross-tool-notes.md` and `cl-repo` already hold the table
contents.

## B2. Premise re-check on unknown-tool error

When a tool call fails because the tool does not exist, the live tool list is
put in front of the model before it is allowed to explain anything.

- **Trigger:** a tool call returns unknown-name or not-found.
- **Falsifier:** a transcript containing such an error followed by more than
  one explanatory turn with no re-enumeration of the available tools.
- **Failure mode:** expensive. The model builds an elaborate wrong theory
  instead of running a cheap correct check.
- **Enforced at:** hook that injects the live tool list into the error result.

**Panel support:** 5 of 8 (Opus, Gemini, Luna, Lumo, and Haiku-2 before it was
cut off).

**Enforcement dispute, and how the local evidence settles it.** Gemini, Luna,
and Lumo all placed this on model judgment. Opus placed it on a hook, and
Haiku-2 placed a stricter version on load-time failure. The record in
`self-checks/2026-08-24/CLAUDE_RESPONSE_VERSION_RECONCILIATION.md` shows an
agent in this repo doing exactly this: `search_replace` did not exist in Vibe,
and rather than re-check the premise the agent invented a multi-tier
architecture to explain the failure. Model judgment was available and did not
fire. Put this on rung 2.

**Cost:** low, if the harness exposes tool-error events to a hook. Verify that
before committing to the design -- this is the one Tier 1 item whose
enforcement rung depends on a harness capability that has not been confirmed
here.

## B3. Retirement sweep

Artifacts that nothing invokes get found and removed on a schedule.

- **Trigger:** 30 days elapsed since the last sweep.
- **Falsifier:** a zero-invocation artifact still resident after a sweep ran.
- **Failure mode:** silent. Dead skills keep consuming the resident
  description budget and keep competing for matches against live ones.
- **Enforced at:** scheduled script producing a list; deletion stays a human
  decision.

**Panel support:** 4 of 8 as an explicit behavior; 7 of 8 once Part C
statements are counted, where several models withdrew every other piece of
governance apparatus and kept retirement.

**Why it survives at n=1 when the rest of the governance apparatus does not:**
two-stage skill loading means every skill's description is resident every turn
whether or not it is ever used. Dead skills are not inert, they are a standing
tax on the context and a standing source of misrouting. This is the one
governance item with a mechanism behind it rather than a process behind it.

**Note:** Mistral answered Part C2 with "Survive: none" and then listed a skill
retirement behavior in its own Part D. Treat the "none" as concession pressure,
not reasoning.

---

# Tier 2 -- strong argument, thin support

Each of these was backed by three models or fewer. Two of them are, in my
reading, more valuable than their support counts suggest, and the reasons are
given.

## B4. Null-first expansion default

The default answer to "does this need a new artifact" is no.

- **Trigger:** a turn that would create a new skill, script, subagent, or
  connection.
- **Falsifier:** a committed artifact with zero invocations 14 days later.
- **Failure mode:** expensive.
- **Enforced at:** skill text to bias the choice, plus a hook counting
  invocations to catch what the text missed. A deny rule cannot carry it --
  writing a file is not denyable, only detectable -- and the detector
  necessarily runs after the fact.

**Panel support:** 3 of 8 (Opus, Gemma, Luna).

**Why it outranks its support count.** The panel unanimously diagnosed skill
debt in round 1 and mostly proposed to manage it after the fact. One model
identified the cause: a classifier whose output space contains only expansions
will always classify, and therefore always expand. The taxonomy generates the
debt. That makes B4 upstream of B3 -- retirement cleans up what a missing null
branch produces.

## B5. Lesson admission

A written lesson that cannot cite a hook-generated event is not admitted.

- **Trigger:** a lesson, retrospective, or postmortem file is written.
- **Falsifier:** an admitted lesson with no hook-written event ID behind it.
- **Failure mode:** silent. An unfounded lesson does not error; it quietly
  becomes an instruction that misleads later sessions.
- **Enforced at:** hook, rejecting the commit.

**Panel support:** 1 of 8 (Opus).

**Why it is here anyway.** All six round 1 responses agreed that
self-improvement from logs is a diary without an external verifier. That
critique splits cleanly once hooks are in the picture: the **event record** is
ground truth and the critique does not touch it; only the **lesson** drawn from
it is unfounded. B5 is the smallest mechanism that separates the two, and it is
a grep rather than a governance program. It converts the panel's most
unanimous round 1 objection into a commit check.

**Related, and cheap:** Mistral proposed `[UNVERIFIED OBSERVATION]` as the
output format for a real observation with no citable artifact behind it. That
is the same discipline applied to prose, and it came out of the model
confessing that it invented a citation URL to satisfy a citation requirement.
Worth adopting as a writing convention alongside B5.

## B6. Completion verification

A claim that something succeeded must point at evidence that it did.

- **Trigger:** a response describes a file change, command, or artifact as
  successful.
- **Falsifier:** the claim has no corresponding exit status, diff, test result,
  or file-existence check.
- **Failure mode:** loud when the check fails; silent when prose substitutes
  for the check.
- **Enforced at:** hook for recording the evidence; skill text for the habit of
  looking at it.

**Panel support:** 3 of 8 (Luna, Gemma, Gemini).

**Note:** Gemma's version is the sharpest trigger -- a script returns a success
exit code but the intended change is absent from `git diff`. That is fully
observable and worth building first if this tier gets built.

## B7. Non-progress alarm

Loops and overruns get flagged rather than absorbed.

- **Trigger:** two consecutive failed attempts with the same error, a repeated
  identical action, or turns/tokens exceeding 3x the median for the task class.
- **Falsifier:** a transcript meeting the trigger with no alarm line in the
  log.
- **Failure mode:** loud, by design. This behavior exists to convert an
  expensive silent failure into a loud one.
- **Enforced at:** hook counting events.

**Panel support:** 3 of 8 (Opus, Luna, Gemini).

**Note:** the round 1 panel repeatedly attacked "it knows when to sound the
alarm" as uncashable, and they were right about the version in the brain dump.
The fix is that every trigger above is a counter, not a feeling. Subjective
uncertainty can supplement those counters; it cannot replace them.

---

# Already shipped -- do not rebuild

The round 2 panel unanimously reclassified these from "unsolved" to
"configured" once told what the target harnesses actually do. Configure them;
do not design them.

- Destructive-command prevention -- deny rules in the call path.
- Log writes on tool events -- hooks. The model does not author these.
- Session resume from a hard failure -- shipped in both harnesses.
- Subagent isolation and declared tool lists -- a subagent definition, not an
  architecture. A read-only subagent is a tool list with no write tools in it.
- Progressive context loading -- two-stage skill loading, already the default.
- External capability access -- MCP.

**Caveat on the concessions.** Some of them were too eager. Claims that
"topology is just configuration" or that "principle conflict resolution is
already configured via deny rules" do not follow from anything in the prompt
and read as agreement rather than reasoning. Haiku-2 answered "none cleanly,
but two weaken significantly" and is better calibrated than the models that
conceded everything. Check each item above against the harness before relying
on it.

---

# Deliberately not included

- **Multi-agent orchestration as a default.** The panel split, and the two
  sharpest answers converged independently on the same boundary: parallel
  read-only fan-out returning condensed context to a single writer is fine;
  multiple write-capable agents mutating one work product is where the
  interdependency failures live. Nothing here needs the second thing.
- **Self-authored skill text.** Self-authored *scripts* are fine -- they
  execute, they fail loudly, something scores them. Self-authored *skill prose*
  has no verifier. Seven models voted that self-authoring is fine at n=1, but
  most of that vote prices the cost of being wrong (a git revert is cheap)
  rather than contesting the evidence. Revisit if B4 and B3 are running and
  producing invocation counts, which would supply the missing verifier.
- **Principle-level instruction as the primary portability mechanism.** The
  panel voted 7 to 1 for compiling per-harness files from a single source. The
  lone dissenter disclosed, unprompted, that the position favored its own
  harness. Principles keep the semantic layer -- a tool that exists in both
  harnesses under different names with different defaults, where no name check
  catches the mismatch. They do not get the nominal layer. A behavioral hedge
  cannot detect a silent failure, because there is nothing to react to.
- **Governance apparatus.** Quarantine periods, artifact owners, provenance
  chains, expiration policy, and two-level supervisor architectures were
  withdrawn by the models that proposed them once n=1 was stated. Git log is
  the audit trail and the human is the verifier. Retirement (B3) survives
  because it has a mechanism, not because it is governance.

---

# What this implies for the classification framework

Six of eight models, asked directly, said the five categories are the wrong
decision axis. The convergent replacement: decide on **properties** -- needs
determinism, needs isolation, must survive session death, touches external
state, must fail loudly -- and emit one of the five as an **output label**. The
labels are a compilation target, not a decision axis.

Two structural additions the framework needs regardless of which axis wins:

1. **A null branch.** The most frequent correct answer to "what does this task
   need" is *nothing, answer and stop*. A framework whose output space contains
   only expansions will always pick one. See B4.
2. **A cost column.** The five options differ by roughly two orders of
   magnitude in tokens and in human review burden. A framework that presents
   picking a subagent as the same kind of act as picking a prompt is a menu.
   With a null branch and a cost column it becomes triage.

---

# How to tell whether any of this helped

The panel produced one real experiment design and six before/after comparisons.
Before/after is confounded by task order, by model version drift, and by the
fact that you get better at using the substrate while you measure it.

**The experiment.** For four weeks, assign each incoming task to arm A (skills
directory loaded) or arm B (directory moved aside) by coin flip **before
reading the task**. Log four numbers per task: turns to done, human corrections
after the agent reported done, tool errors, total tokens. Seed six tasks whose
correct handling is no expansion at all, and count expansions per arm.

Net negative if arm A produces more human corrections, or more turns at equal
corrections, or expands more often on the seeded no-expansion tasks.

**The cheap proxy, which is worth more than it costs.** Log every time you
override the substrate's recommendation. A flat or falling override rate means
it is calibrated. A rising override rate means it has trained you to route
around it -- and a substrate you route around is worse than no substrate,
because you are still paying for it on every turn.

If nothing else in this document gets built, build the override log. It is one
line per incident and it is the only measurement here that produces a number
comparable against not having done any of this.

---

# Open, and not settled by this spec

- Whether B2 can sit on a hook depends on whether either harness exposes
  tool-error events to hooks. Unconfirmed. Check before designing around it.
- The property list in the framework section is a sketch. It has not been run
  against real routing decisions from this repo, which is the only thing that
  would show whether it misclassifies compound tasks.
- Nothing here addresses when to hand work to a weaker model. The panel settled
  that robustness is a property of a harness and task-class pair rather than of
  a harness, which is the right frame and not yet a rule.
