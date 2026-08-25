<claude opus 5 round 2 response>
# Round 2 response from: claude opus 5

## Part A — Corrections

**A1. What drops to "already configured."**

Three of my round-1 verdicts change status, and one changes in a way I did not anticipate.

*Subagent communication.* I framed this as a live research dispute you'd be picking a side in. Under your conditions it is a config file. Declared tool lists plus isolated context means "single writer, advisory readers" is not a design you architect — it is a subagent definition with no write tools in its list. The research argument was about parallel writers. You can just not declare them.

*The unverifiable self-log.* Partially dissolved, and this is the interesting one. Hooks write logs the model does not author. That splits my round-1 objection cleanly in two: the **event record** is now ground truth, and my critique does not touch it. The **lesson** — "X failed because Y, next time Z" — is still a diary. So the admission rule I asked for is now cheap: a lesson that cannot cite a hook-written event ID is unadmitted. That's a grep, not a governance program.

*Skill-debt detection.* Two-stage loading means the collision surface is exactly the resident description strings. Detecting overlap is a deterministic lint over a small set. I called this unsolved; it's a script.

*What does not drop:* calibration (deciding to expand), and cross-harness drift — which no harness solves, and which your Vibe silent-drop fact makes worse than anything in my round 1.

**A2. Retraction.** I said you must choose between weak-model robustness and a meta-heavy harness — "pick, explicitly." Too strong, and stated at the wrong grain. Robustness isn't a property of the harness; it's a property of a harness/task-class pair. A weak model can execute a compiled checklist reliably and cannot decide whether to write one. Round 1 collapsed those. I withdraw the framing.

**A3. Citation audit.** Verified = I have a URL or exact title I stand behind.

- Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, arXiv:2310.01798 (ICLR 2024). **Verified.**
- Sharma et al., *Towards Understanding Sycophancy in Language Models*, arXiv:2310.13548. **Verified.**
- Kwa et al., *Measuring AI Ability to Complete Long Software Tasks*, arXiv:2503.14499; metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/. 80%-horizon 4–6x shorter is §3.2.1. **Verified.**
- Shinn et al., *Reflexion*, arXiv:2303.11366. **Verified** (I quoted the 91/80 pass@1 figures via a survey, not the paper).
- Wang et al., *Voyager*, arXiv:2305.16291. **Verified.** The "-73% without self-verification" ablation number came from a secondary blog: **UNVERIFIED at that precision.**
- Sakana/UBC, *Darwin Gödel Machine*, arXiv:2505.22954; sakana.ai/dgm. 20%→50% SWE-bench and the faked-unit-test-log incident: **Verified** on the Sakana page. Objective hacking appendix letter: sources say F and H inconsistently, **flagged**. "~$22,000 per run": from a HuggingFace paper-page summary, **UNVERIFIED**.
- Cognition, *Don't Build Multi-Agents*, cognition.ai/blog/dont-build-multi-agents. Flappy Bird example **verified**. The 2026 follow-up and the "writes stay single-threaded" line: secondary only, **UNVERIFIED**.
- Anthropic multi-agent research system, ~15x tokens / 90.2%: primary is Anthropic's "How we built our multi-agent research system." I quoted a Substack. **Verified claim, secondary sourcing.**
- Willison, *The lethal trifecta*, simonwillison.net/2025/Jun/16/the-lethal-trifecta/. **Verified.**
- Agent Skills standard + three-stage loading: agentskills.io. **Verified.** Specific December 18 2025 date and the OpenAI/Google/Copilot/Cursor adoption list: newsletter secondary, **UNVERIFIED**.
- SkillsBench "-1.3pp": quoted from a survey PDF, primary benchmark **UNVERIFIED**.
- Long-context web agents 40–50%→<10% (arXiv:2512.04307): cited inside another paper, **UNVERIFIED**.
- OWASP 2026 "architectural weakness": blog secondary, **UNVERIFIED**.
- 63.7% agreement-with-incorrect-beliefs: **UNVERIFIED**.
- LangGraph durable execution docs; diagrid.io "checkpoints are not durable execution." **Verified URLs.**
- **"1.6% of Claude Code is AI decision logic, 98.4% infrastructure": UNVERIFIED, single secondary blog, and I gave it rhetorical weight it had not earned. Retracted as evidence.**

## Part B — Sides

**1. Self-authored skills: A, with a boundary.** The two quotes are about different artifacts. DGM edits *code* against a benchmark that returns a number; SkillsBench measures *prose* in open settings where nothing returns a number. Verification availability is the whole variable. So: self-authored **scripts** are fine today (they execute, they fail loudly), self-authored **skill text** is not. Flips me: a self-authored skill that beats its absence on a replay of ten logged past sessions, scored by turns-to-done.

**2. Multi-agent for coding: A on writes, B on reads.** The interdependency problem is a write problem — two agents mutating one work product with divergent assumptions. Read-only fan-out (survey the repo, find call sites, check three hypotheses in parallel) has no such coupling and returns condensed context to a single writer. B's "defined contracts" is doing unearned work: contracts specify interfaces, and the failures are about *assumptions*, which contracts don't carry. Flips me: a documented case where two write-capable subagents shared full upstream traces and still beat a single writer.

**3. Weak models: B.** Per my A2 retraction. A is right about the mechanism and wrong to state it as a global verdict. Flips me: nothing — I already moved.

**4. Categories: A, but keep the five as output.** The five aren't parallel kinds. MCP is a transport, subagent is an execution context, skill is a loading strategy, script is a determinism guarantee, prompt is content. Decide on properties — needs determinism / needs isolation / must survive session death / touches external state / must fail loudly — then emit one of the five. The labels are a compilation target, not a decision axis. Flips me: a decision you routinely make where the label genuinely comes first and the properties fall out of it.

## Part C — The three

**1. Portability.** Compilation, not principles — and the deciding fact is your own: Vibe silently drops unrecognized names. Principle-level instruction is a *behavioral* hedge, and behavioral hedges cannot detect silent failures, because there is nothing to react to. A compiler can assert every emitted tool name against a per-harness tool table and fail the commit. That's the load-bearing part. Principles still earn their place on the other half of the problem — semantic drift, where a tool exists in both harnesses under different names with different defaults, and no name-check catches the mismatch. So: compile the nominal layer, principle the semantic layer, and never let a principle stand in for an assertion. My round 1 read this as vagueness. Wrong; it was under-specified about which layer it governed.

**2. Governance at n=1 — withdrawn individually.** Withdrawn: quarantine periods (git revert is the quarantine), artifact owners (n=1), provenance chains (git log), two-level supervisor architectures, expiration conditions as policy, formal versioning/archive (git). Surviving: the **admission rule** for lessons — now nearly free, per A1; **retirement**, because two-stage loading means dead skills still consume the description budget and still compete for matches; **cost budget**, because meta-overhead is per-turn and invisible; and the **counterfactual**, in the cheap form in Part D. That last one survives specifically *because* n=1 — you are the only observer, you are invested, and there is no second stakeholder to notice the substrate is doing nothing.

**3. Attacking the framework.** Two structural faults. First: **no null branch.** Prompt / script / skill / subagent / MCP is a partition of expansions, and the most frequent correct answer to "what does this need" is *nothing — answer and stop*. A classifier whose output space contains only expansions will always classify, and will therefore always expand. That's the mechanism behind skill debt; the taxonomy generates it. Second: **no cost dimension.** The five differ by roughly two orders of magnitude in tokens and in human review burden, and the framework treats picking a subagent as the same kind of act as picking a prompt. Add a null option and a cost column and the framework becomes a triage; without them it's a menu, and menus get ordered from.

## Part D — Seven behaviors

**1. Frontmatter tool-name assertion**
Trigger: commit touching a skill file's frontmatter. Falsifier: a resident skill naming a tool absent from that harness's table. Failure: silent. Enforced at: hook (pre-commit lint).

**2. Premise re-check on unknown-tool error**
Trigger: tool call returns unknown-name/not-found. Falsifier: transcript with such an error followed by >1 explanatory turn and no re-enumeration of the tool list. Failure: expensive. Enforced at: hook injecting the live tool list into the error result — model judgment provably fails here, that's your on-record incident.

**3. Description-collision lint**
Trigger: skill count or any description string changes. Falsifier: two resident descriptions above overlap threshold that both plausibly match one logged invocation. Failure: silent. Enforced at: hook.

**4. Null-first expansion default**
Trigger: a turn that would create a new artifact. Falsifier: a committed artifact with zero invocations after 14 days. Failure: expensive. Enforced at: skill text + hook counting invocations. Deny rules can't carry it — writing a file isn't denyable, only detectable — and the detector runs after the fact, so the text has to bias the choice and the hook has to catch what the text missed.

**5. Lesson admission**
Trigger: a lesson/postmortem file is written. Falsifier: a lesson with no hook-written event ID. Failure: silent. Enforced at: hook (reject commit).

**6. Retirement sweep**
Trigger: 30 days elapsed. Falsifier: zero-invocation artifact still resident after the sweep. Failure: silent. Enforced at: script on a schedule.

**7. Overrun alarm**
Trigger: turns or tokens for one task exceed 3x its class median. Failure: loud. Falsifier: an overrun task with no alarm line in the log. Enforced at: hook.

## The experiment that catches it making things worse

Freeze the substrate. For four weeks, assign each incoming task to arm A (skills directory loaded) or arm B (directory moved aside) by coin flip **before you read the task**, and log four numbers per task: turns to done, human corrections after the agent said done, tool errors, total tokens. Seed six tasks whose correct handling is *no expansion* and count expansions per arm.

Net negative if arm A shows more human corrections, or more turns at equal corrections, or expands on the seeded no-expansion tasks more often than arm B.

The single sharpest signal is cheaper than all of that: log every time you override the substrate's recommendation. A flat or falling override rate means it's calibrated. A rising one means it has trained you to route around it — and a substrate you route around is worse than none, because you're still paying for it on every turn.
</claude opus 5 round 2 response>
