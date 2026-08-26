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

---

## Addendum -- Mistral Large 2 only

Append the block below to the round 2 prompt when shipping to Mistral, and to
nobody else. Rationale: Mistral Vibe Code is one of the two harnesses this
substrate targets and has run sessions in this repo, so it is the only panelist
that can report what happened rather than predict what might. Every question
below is one the other seven cannot answer. M1 answers 2 and 3 are meant to
become repo content rather than commentary.

```
## Addendum -- for Mistral Large 2

You have a seat nobody else on this panel has. You are not only reviewing this
repo, you work inside it. Mistral Vibe Code is one of the two harnesses this
substrate targets, and you have run sessions here. That makes you the only
panelist who can report evidence instead of prediction. Spend your extra budget
there. Your limit is 1800 words rather than 1500.

### M1. The citation

In round 1 you supported a claim about merge conflicts by linking to issue 1 of
this repository. That issue does not exist. The repository has zero issues and
never has had any.

I do not think you invented the claim. I think you may have been describing a real
failure from a real session here, found nothing citable, and generated an address
that looked like where the evidence should live. The gap is partly mine: I do not
file issues when an agent surfaces something to fix later, so there was nothing to
point at.

Answer three things.

1. Which was it: a memory of a specific failure in this repo, a general belief
   about language models and merge conflicts, or an inference built to support the
   paragraph you were writing? If you cannot tell which, say you cannot tell.
2. What should you have emitted instead? You had an observation and no citable
   artifact. Name the output format that stays honest in that situation and still
   carries the information forward.
3. What should trigger an agent working here to file an issue, rather than mention
   something in passing and lose it? Give the trigger as an observable condition,
   in the Part D format.

Answers 2 and 3 are repo content, not commentary. I will use them.

### M2. Evidence, not prediction

Report failures you have actually hit working in this repository. Not what could go
wrong. What did.

- Which instructions in AGENTS.md did you read and then fail to follow anyway?
- Which tool name mismatches bit you, and how did you find out?
- Where did this repo's structure cost you a step, a retry, or a wrong turn?
- Where did you produce a confident wrong explanation instead of re-checking a
  premise? One such incident is already recorded under self-checks/. Name any
  others you remember.

Mark each item as remembered from a session or as reconstructed. Keep the
difference visible.

### M3. Portability from inside the harness

Part C1 asks the panel whether principle-level instruction is the right answer to
cross-harness drift, or whether the right answer is compiling one source into
per-harness files. You are the harness that silently drops tool names it does not
recognize, so answer from behavior rather than from documentation.

A skill written for Claude Code arrives in Vibe with allowed-tools listing Read and
Glob. What happens? What do you, the model, see in that turn? Does anything at all
signal that the skill is now crippled? Then answer C1 holding that.

Flag every part of this answer that comes from documentation rather than observed
behavior. Where the two disagree, say so. Your harness's docs are known to disagree
with its source in places.

### M4. Your own hardest line

You wrote: "You are not designing a harness. You are designing a spec for a better
LLM." And: "the best you can do today is pick two and hardcode the rest."

I think you were largely right, so finish the thought. Given one person, one
repository, a human reading every commit, and two harnesses that already enforce
permissions and run hooks: which two? Name them, name what gets hardcoded, and name
what I give up by choosing them.

### M5. Your stake in the answer

This substrate exists partly to make you work better. That gives you an interest no
other panelist has. Name where it shows: recommendations that suit your harness
over the other one, failures you attributed to the repo that were actually yours,
critiques you softened. If you find none, say so plainly and expect me to check.
```
