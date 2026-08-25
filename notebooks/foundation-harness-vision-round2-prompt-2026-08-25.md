# Foundation harness vision -- round 2 prompt (2026-08-25)

Round 1 responses live in
[`foundation-harness-vision-debates/`](foundation-harness-vision-debates/).
The original brain dump is
[`foundation-harness-vision-2026-08-25.md`](foundation-harness-vision-2026-08-25.md).

Ship the block below to every model that answered round 1. If the model is in
a fresh session, attach its own round 1 response and the original brain dump
first. Same XML-tag convention as round 1 so the replies file cleanly.

Design notes, so a future reader knows why this prompt looks like it does:

- Round 1 was a convergent prompt. Six models produced roughly four distinct
  ideas, because "here is an ambitious vision, challenge me" has one strong
  attractor. Round 2 forbids the consensus so the models have to spend the
  round somewhere new.
- Nearly every model read "harness" as "multi-agent framework in Python" and
  did not know the target harnesses already ship deny rules, hooks, subagent
  contracts, and two-stage skill loading. That inflated their "unsolved"
  verdicts. Round 2 supplies the missing facts and asks what changes.
- Round 1 produced four direct factual contradictions between models. Those
  are the only genuinely new information in the pile, so round 2 forces a
  commitment on each.
- The word cap is deliberate. Compression prevents restatement.

---

```
<ask and task>
This is round 2. In round 1 I sent you an unedited brain dump about a "foundation
harness" and asked you to stress-test it. You responded. Round 2 gives you a fact
you did not have, forbids the critiques the whole panel already made, and asks you
to commit to positions.

Hard limit: 1500 words. Compression is part of the test.

## The fact you did not have

Six models answered round 1. Nearly all of you read "foundation harness" as "build
a multi-agent orchestration framework." That is not what this is. The actual
conditions:

- The deliverable is markdown. Skills, prompt templates, and agent instruction
  files that load into coding agents that already exist. I am not building a
  framework. I am writing the content two existing harnesses read.
- The two target harnesses are Claude Code and Mistral Vibe Code. Both already
  ship: permission and deny rules enforced in the tool call path, below the model
  and outside its control; hooks that fire deterministically on tool events and
  write logs the model does not author; subagents with declared tool lists and
  isolated context; two-stage skill loading, where only a skill's name and
  description stay resident and the body loads on invocation; MCP connections;
  and session resume.
- Scale is one person and one repository. Every change is a git commit a human
  reads. There is no fleet, no unattended deployment, no second stakeholder.
- The two harnesses are not interchangeable. Tool names differ (Read vs read_file,
  Edit vs edit, and Glob has no equivalent at all). Vibe silently drops tool names
  it does not recognize from a skill's frontmatter -- no error, just a quietly
  crippled skill. Directives that exist in one do not exist in the other.
- One real failure from this repo, on record: an agent used a tool name that did
  not exist, and instead of re-checking that premise it invented a multi-tier
  architecture to explain the failure. Producing the elaborate wrong explanation
  was cheaper for it than running the correct check.

Under those conditions some of round 1 changes status. Part of what you called an
unsolved research problem is a configuration setting in software I already run.

## Spent arguments

The panel reached consensus on four points. They are accepted, and repeating any
of them wastes your round:

1. I anthropomorphized. "It knows" is not a mechanism.
2. Self-improvement from logs is a diary without an external verifier.
3. Safety belongs below the model, in enforced rules, not in prose.
4. Expansion without retirement accumulates skill debt.

"You are describing AGI" is also spent. Six models said these. Say something they
did not.

## Part A -- Corrections

1. Name the specific verdicts in your round 1 that drop from "unsolved" to
   "already configured" under the conditions above. If none do, say none and
   defend that.
2. Name one claim from your round 1 you now retract or weaken.
3. Go through every citation you gave in round 1. For each, give a working URL or
   an exact paper title, or mark it UNVERIFIED. One model in this panel cited a
   GitHub issue that does not exist, in my own repository. I check these.

## Part B -- Pick a side

The panel contradicted itself on four factual questions. Quotes are from round 1,
unattributed. Take a side on each in one paragraph, and name the evidence that
would flip you.

1. Self-authored skills.
   A: "Self-generated skills provide no benefit on average. Models cannot reliably
   author the procedural knowledge they benefit from consuming."
   B: "Self-improving coding agents already edit their own codebase and add their
   own tools. Dynamic skill and script generation is implementable today."

2. Multi-agent for coding work.
   A: "Most coding tasks are not well suited to multi-agent systems with current
   technology, since they require shared context and involve complex
   interdependencies."
   B: "Subagent delegation with defined contracts is established practice and the
   practical path forward."

3. Weak models.
   A: "Completely false. Metacognition requires frontier models. Weak models crater
   when asked to manage state and plan autonomously."
   B: "A good harness makes weak models useful on constrained tasks. Robustness
   should be stated per task class, not as a general property of the harness."

4. The categories.
   A: "Prompt, script, skill, subagent, and MCP are overlapping engineering labels,
   not natural kinds. The stable abstraction is a capability with an interface and
   a lifecycle."
   B: The five categories are the right decomposition and worth keeping distinct.

## Part C -- Three things you dismissed

Defend them or kill them, but on the right grounds.

1. Principles over specifics. Most of you read this as vagueness. It is a
   portability requirement: one file has to work in two harnesses with different
   tool names, one of which silently drops names it does not recognize. On those
   grounds, is principle-level instruction the right response to cross-harness
   drift, or is the right answer per-harness compilation from a single source?
   Argue portability, not whether "be efficient" is actionable.

2. Governance at n=1. Several of you asked for quarantine periods, artifact owners,
   expiration conditions, two-level supervisor architectures, and provenance
   chains. At one person and one repo, git log is the audit trail and I am the
   verifier. Name individually which of your round 1 recommendations you withdraw
   as overhead at this scale, and which survive.

3. The classification framework. The brain dump was raw material. The actual
   deliverable is the framework for deciding prompt vs script vs skill vs subagent
   vs MCP. One model attacked it. The rest critiqued my prose and did not notice
   the framework was there. Attack the framework.

## Part D -- The artifact

Give me at most seven always-on behaviors that survive your own round 1 critique.
For each, exactly four lines:

- Trigger: the observable condition that fires it. Countable or detectable, not a
  judgment call.
- Falsifier: the evidence that would show it failed to fire when it should have.
- Failure mode: loud, silent, or expensive.
- Enforced at: deny rule, hook, skill text, or model judgment. If the answer is
  model judgment, say why the other three cannot carry it.

Then one more thing: describe the experiment that would show this whole substrate
is net negative. Not how to prove it works. How I would catch it making things
worse.

Format your response exactly as in round 1:

<[model-name] round 2 response>
# Round 2 response from: [model-name]
[YOUR RESPONSE]
</[model-name] round 2 response>
</ask and task>
```
