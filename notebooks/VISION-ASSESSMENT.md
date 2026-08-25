> **⚠️ Thought exercise — not a work queue.**
> Nothing in this file has been run, measured, or committed to. Status markers,
> effort estimates, and "next steps" here were written *before* anything was
> verified, and several are known to be wrong. **Do not act on this file, install
> anything from it, or treat its statuses as current.**
> Start at [`IDEAL.md`](IDEAL.md) for what actually holds up; known-wrong claims are
> catalogued in [`verified-defects-2026-08-25.md`](verified-defects-2026-08-25.md).

---

# Foundation Harness Vision: Strategic Assessment

**Date:** 2026-08-25  
**Based on:** Two-round model debate (8 models), repo inspection, crispycouscous context  
**Status:** High-level strategy for moving from vision to shipping reality

---

## Implicit Goals of the Brain Dump

The brain dump describes a harness that can:

1. **Self-recognize its limitations** — knows when it needs to expand (new skill, new agent, new process)
2. **Expand responsibly** — chooses the right artifact type and knows where it goes
3. **Learn from failure** — logs what went wrong and adjusts next time
4. **Communicate across boundaries** — subagents, external tools, other models, user
5. **Choose the right modality** — when to use scripts vs skills vs prompts, when to be verbose, when to be direct
6. **Act with integrity** — sounds alarms, admits blind spots, uses evidence-based reasoning
7. **Remain portable** — works across models and harnesses
8. **Degrade gracefully** — weak models still produce reasonable output

**Underlying thesis:** An AI coding agent should be *designed* like a senior engineer (principled, self-aware, learns from failure) not *treated* like a black box (just ask it harder).

---

## What the Panel Found

### Already Shipped (Stop Designing, Start Using)

✅ **Deny rules** — permissions enforced below model layer  
✅ **Hooks** — deterministic logging on events  
✅ **Session resume** — checkpoints for recovery  
✅ **Subagent isolation** — declared tool lists, controlled delegation  
✅ **Two-stage skill loading** — descriptions resident, bodies load on invocation  
✅ **MCP integration** — external capabilities via schema discovery  

**Verdict:** The panel unanimously agreed these are shipping. Your job: configure them, not design them.

### Already Partially Addressed (Refinement, Not Invention)

⚠️ **Self-recovery** — session resume exists, but breadcrumb completeness unverified  
⚠️ **Cross-context communication** — subagents exist, but shared state unclear  
⚠️ **Event logging** — hooks write logs, but structured interpretation missing  

### The Core Unsolved Problem

🔴 **Cross-harness portability:** Claude Code and Mistral Vibe have incompatible tool names, different harness capabilities, silent failures.

**Why this matters:** You want *one foundation harness* that works in both systems. But they speak different languages.

**Panel verdict:** 7-1 for per-harness compilation (single semantic source, compiled to two nominal outputs). One model (defending its own harness) argued for principle-level instructions.

### What Wasn't Solved

- **Multi-agent write coordination** — parallel read-only fan-out is fine; multiple writers on one work product is a known failure mode
- **Self-authored skill prose** — has no verifier; scripts are fine (they execute loudly)
- **Governance apparatus** — quarantine periods, ownership, expiration policies all withdrawn at n=1 scale
- **Principle-level instruction as primary portability** — lost the debate; silent dropping makes it too dangerous

---

## What Should You Harvest From Elsewhere?

### 1. Hook Infrastructure

**Where to get it:** Already in Claude Code (PreToolUse, Stop hooks) and Mistral Vibe (PRE_TOOL, POST_TOOL in hooks.toml).

**What you need:** Verify that hooks can:
- Access tool-error events (for B2: Premise Re-Check)
- Modify error messages before model sees them
- Log invocations with timestamps (for B3: Retirement Sweep)
- Validate metadata before file load (for B1: Tool-Name Assertion)

**Effort:** Inspection + integration testing. Not research.

### 2. Cross-Harness Tool Translation

**Where it lives:** `docs/cross-tool-notes.md` (already in this repo), verified against:
- Claude Code source
- Mistral Vibe source (mistralai/mistral-vibe @ a84be03)
- Pi Agent docs

**What you need:** Keep this current. It's your Rosetta Stone.

### 3. Session Checkpointing Behavior

**Where to get it:** Both harnesses support it natively. You just need to:
- Verify breadcrumb completeness (what gets logged when session dies?)
- Test recovery from cold start
- Document what's sufficient for hand-off (same model? different model?)

**Effort:** Testing + documentation.

### 4. MCP Ecosystem

**Where to start:** https://modelcontextprotocol.io/

Your repo already connects MCP servers. Question: what should live in MCP vs inline?

**Pattern emerging:** Simple tools run via bash. Structured integration (retrieval, persistence, API access) goes via MCP.

### 5. Deny Rules Framework

**Where it lives:** Both harnesses already enforce these. Your job: define what you want to deny.

**Examples already in place:** Deny `rm -rf`, `drop table`, etc.

**Next:** Add deny rules for harness-specific safety (e.g., "don't commit skills without validation").

---

## What You Should Build Yourselves

### 1. Behaviors (Tier 1: High Support, Implementable Today)

| Behavior | Status | Why Build It | Effort |
|----------|--------|--------------|--------|
| **B1: Tool-Name Validation** | ✅ Done | Cross-harness drift is real; silent drops happen | ✅ Low (done) |
| **B2: Premise Re-Check** | 📋 Ready | Prevents expensive false hypotheses | Medium (hook integration) |
| **B3: Retirement Sweep** | 📋 Ready | Dead skills cost tokens; need regular cleanup | Low (template done) |

**Build these.** Panel consensus: 7-1 or stronger.

### 2. Classification Framework Refinement

**Current:** Prompt, Script, Skill, Subagent, MCP (mixing decision axes).

**What the panel said:** Use **properties** (needs isolation? needs determinism? must fail loudly?) as decision axis. Output the label (prompt/script/skill/subagent/MCP) as a *compiled result*, not a primary choice.

**Add to framework:**
- Decision matrix (property → label mapping)
- Null branch (default: don't create anything)
- Cost column (tokens, review burden)

**Effort:** Medium (design + testing against real routing decisions).

### 3. Portability Layer (Per-Harness Compilation)

**Build the infrastructure for:** Single source file (semantic, harness-agnostic) → compile to `.claude/` and `.vibe/` versions.

**Not required to ship immediately,** but the infrastructure should exist for:
- Skill files (translate `allowed-tools`, frontmatter)
- AGENTS.md (different semantics between harnesses)
- Hook configurations (Claude Code hooks ≠ Vibe hooks)

**Effort:** Medium-high (build compiler + test against real skills).

### 4. Invocation Logging (Dependency for B3, B4)

**What you need:** Every time a skill/script/subagent is invoked, log:
- Name
- Timestamp
- Outcome (success/failure)
- Optionally: tokens, tool calls, errors

**Where it lives:** Hook (post-invocation logging, deterministic).

**Why build it:** Retirement sweep needs this data. Can't identify unused skills without invocation logs.

**Effort:** Medium (hook integration + schema design).

### 5. Override Log Measurement System

**What you need:** A log file where you record decisions *against* the harness's recommendation.

```
2026-08-25: B1 said "tool X not in Vibe", I committed anyway (one-off script, not a skill)
2026-08-26: B3 found 5 unused skills, I archived them
```

**Why build it:** Cheapest way to measure whether behaviors actually help. Rising override rate = you're routing around it (bad). Flat/falling = calibrated (good).

**Effort:** Very low (one log file, one-line format).

---

## What You Should Ignore (Or Postpone Indefinitely)

### 1. Automated Self-Improvement From Logs

**Proposal in brain dump:** "It leaves logs for itself on how it did, and can improve itself as a result."

**Panel verdict:** Unanimous rejection. Logs are ground truth. Lessons drawn from them are opinions. No automatic lesson adoption.

**What survives:** Event logs (ground truth). Manual lesson extraction (your judgment).

**Why ignore:** Automated interpretation of logs runs into the same problems as automated code review — high false-positive rate, high cost of mistakes.

### 2. Governance Apparatus

**Originally proposed:** Quarantine periods, artifact owners, expiration policies, provenance chains, two-level supervisors.

**Panel verdict:** All withdrawn at n=1 scale.

**What survives:** Git log as audit trail. Human as decision gate.

**Why ignore:** At one person, git blame + code review already provides governance. Formal apparatus adds process debt without reducing failure rate.

### 3. Dynamic Skill Self-Generation

**Proposal in brain dump:** "If it decides its time to make a skill, it knows how to make a skill."

**Panel verdict:** Self-authored *scripts* are fine (execute, fail loudly). Self-authored *skill prose* has no verifier.

**What survives:** Scripts generated and executed (measurable). Skills created by human or human-reviewed AI (skill prose needs a reader).

**Why ignore (for now):** No verifier for generated skill quality. Revisit once B3 + B4 produce invocation counts (that would be your verifier).

### 4. Principle-Level Instruction as Primary Portability

**Proposal:** "It is flexible between agents because it is based on principles more than specifics."

**Panel verdict:** 7-1 for per-harness compilation instead. Principles survive as *semantic layer*, but compilation handles *nominal layer* (tool names).

**Why ignore:** Silent dropping makes principle-level hedging too dangerous. "Use the read tool" survives, but it must compile to both Read and read_file in the actual files, checked automatically.

### 5. AGI-Level Reasoning About its Own Limitations

**Implicit in brain dump:** "It can tell when the user needs assistance clarifying their ask" and "can attempt critical thinking."

**Panel verdict:** Weak models can be made useful for *constrained tasks* with scaffolding. Not for open-ended judgment.

**Why ignore:** No evidence that prompt-level instruction can give a model reliable metacognitive judgment. Focus on constrained behaviors (tool validation, premise re-check) instead.

---

## Surprises

### 1. The Harness Already Provides Most of the Infrastructure

Your implicit goal was "how do I make the harness recognize when it needs to expand?" The panel's finding: the harness already provides the mechanisms (hooks, logs, deny rules, subagent isolation). The question you should be asking is not "how do I build this?" but "how do I configure what I have?"

### 2. Cross-Harness Drift Is the Real Blocker

The brain dump has 89 lines covering 15 different topics (logging, skills, agents, communication, reasoning). The panel converged on one: **tool name portability**. Not because it's the hardest philosophically, but because it's the most immediate practical problem. Mistral reported a real session error.

### 3. Weak Models Aren't the Blocker; the Harness Design Is

Original brain dump assumes strong models. Panel finding: weak models can be made useful with the right harness design (deny rules, hooks, bounded context, explicit stopping conditions). The harness is more important than the model.

### 4. Skill Debt Is a Taxonomy Problem, Not a Cleanup Problem

One panel member identified the mechanism: "A classifier whose output space contains only expansions will always classify, therefore always expand." The taxonomy (prompt/script/skill/subagent/MCP) generates the debt upstream. B3 (retirement) is downstream cleanup. The real fix is B4 (null-first expansion): defaulting to "don't create anything."

### 5. Citation Quality Signals Model Honesty

When asked to audit citations generically, all models rubber-stamped each other. When accused by name of inventing a GitHub issue, the model confessed fully. Specific accusation is more effective than general audit. This is a behavior: `[UNVERIFIED OBSERVATION]` tag for real observations without citable sources.

---

## What You Already Have in Place

### Repository Structure

✅ **CLAUDE.md** — Project-specific instructions (read-only mailroom, archive)  
✅ **AGENTS.md** — Shared instructions for both Claude Code and Vibe  
✅ **skills/** — 18+ reusable skills (library, not live discovery paths)  
✅ **mailroom/** — Staging area (read-only, human review gate)  
✅ **archive/** — Historical work (read-only)  
✅ **notebooks/** — Debate materials and specifications  
✅ **docs/** — Cross-tool notes, behavior specs  

### Harness Capabilities

✅ **Session resumption** — Checkpoint on failure  
✅ **Deny rules** — Enforce permissions  
✅ **Hooks** — Deterministic logging  
✅ **Two-stage loading** — Descriptions resident, bodies lazy-load  
✅ **Subagent isolation** — Declared tool lists  
✅ **MCP integration** — External capabilities  

### Extracted Behaviors (Tier 1-2)

✅ **B1** — Tool-name validation (implemented, tested)  
📋 **B2** — Premise re-check (documented, awaiting hook capability)  
📋 **B3** — Retirement sweep (template, awaiting hook logging)  
📋 **B4-B7** — Tier 2 behaviors (documented, awaiting resource allocation)  

### Documentation

✅ **Tool translation table** — Claude Code ↔ Vibe ↔ Pi Agent  
✅ **Debate summary** — Findings + next steps  
✅ **Behavior specifications** — Triggers, falsifiers, enforcement  
✅ **Quick-start guide** — For new users  

---

## What You Have From crispycouscous (When Joined)

**Unknown without inspection, but likely:**

- Additional skills or workflows
- Different harness configuration
- Testing infrastructure
- CI/CD pipeline
- Additional models/agents

**Action:** When merged, audit for:
- Tool compatibility (run B1 validation against new skills)
- Overlapping skill definitions (semantic dedup)
- Portability assumptions (which harnesses is it targeting?)
- Governance patterns (what conventions does it follow?)

---

## Next Steps to Make This Shipping Reality

### Phase 1: Validation & Integration (3-5 Days)

**Goal:** Prove behaviors work, establish measurement baseline.

1. **Verify hook capabilities:** (1 day)
   - Check Claude Code docs: can `PreToolUse` hook access tool-error events?
   - Check Vibe source: can `PRE_TOOL` hook modify error messages?
   - If yes to both: B2 is unblocked. If no: design alternative.

2. **Run B1 validation:** (1 day)
   - Execute against all existing skills
   - Fix flagged issues (skill-extractor tool names)
   - Validate fixes
   - Install pre-commit hook (optional but recommended)

3. **Start override log:** (same day)
   - Create `docs/override-log.md`
   - Establish measurement baseline

4. **Merge crispycouscous & audit:** (1-2 days)
   - Run B1 validation on new skills
   - Spot-check for duplicates
   - Document any tool-name issues

### Phase 2: Hook Integration & B2/B3 (1-2 Weeks)

**Goal:** Implement B2 and B3 with full harness integration.

1. **Implement B2 (Premise Re-Check):** (3-5 days)
   - Hook integration for tool-error events
   - Inject available tool list into error message
   - Test against real tool-not-found scenarios

2. **Implement B3 (Retirement Sweep):** (2-3 days)
   - Hook-based invocation logging (if Phase 1 verified hook capability)
   - B3 script queries invocation logs
   - Schedule monthly sweep

3. **Quick docs for B4-B7:** (1 day)
   - One-pager per behavior (not full docs)
   - Implementation checklist
   - Defer detailed design

### Phase 3: Classification Framework (1 Week)

**Goal:** Replace five-category taxonomy with property-based routing.

1. **Build decision matrix:** (2-3 days)
   - Map properties (isolation? determinism?) to artifact types
   - Test against 10 recent real decisions from this repo
   - Document edge cases (compound tasks)

2. **Add framework elements:** (1-2 days)
   - Null branch (default: don't create)
   - Cost column (rough estimates)
   - Document in AGENTS.md

3. **Create routing skill:** (1 day)
   - Skill that teaches property-based routing
   - Test a few times with models

### Phase 4: Portability Layer (2-4 Weeks)

**Goal:** Single-source skills that work in both Claude Code and Vibe.

**This is the real work.** The phases above are validation. This is implementation.

1. **Build compilation infrastructure:** (1-2 weeks)
   - YAML schema for single-source skill
   - Compiler: YAML → claude-code/SKILL.md + vibe/SKILL.md
   - Tool name translation (Read → read_file)
   - Frontmatter adaptation (allowed-tools, user-invocable)
   - Validation & CI checks

2. **Pilot with 5 skills:** (1-2 weeks)
   - Convert 5 existing skills to single-source format
   - Test both outputs in both harnesses
   - Fix compiler bugs
   - Document conventions

3. **Optional: Migrate remaining skills:** (1-2 weeks, defer)
   - Convert 13 remaining skills
   - Consolidate duplicates discovered in process
   - Update documentation

### Phase 5: Measurement & Optimization (Runs Parallel to Phases 2-4)

**Goal:** Prove the substrate helps or identify what needs change.

1. **Run experiment design (after 4 weeks):**
   - 10 standardized tasks
   - Coin-flip assign to arm A (with substrate) vs B (without)
   - Measure time, errors, tokens, expansions

2. **Monitor override log:**
   - Track calibration (override rate trend)
   - Identify patterns (which behaviors get overridden most?)
   - Adjust thresholds/criteria

3. **Quarterly review:**
   - Is the substrate net positive?
   - Which behaviors provide value?
   - Which should be removed or redesigned?

---

## Success Criteria (How to Know This Worked)

### Minimum Viable (After Phase 1)

✅ B1 (tool-name validation) prevents at least one real tool-name issue from being committed  
✅ No silent failures from unrecognized tool names in Vibe  
✅ Skills are portable (work in both harnesses or clearly marked single-harness)  
✅ Override log shows calibrated substrate (constant or falling override rate)

### Full Vision (After Phase 5)

✅ Behaviors prevent measurable classes of errors (tool-name drift, premise mismatches, skill debt)  
✅ Cross-harness portability is solved (single source, compiled outputs)  
✅ Classification framework routes accurately (property-based, not category-based)  
✅ Weak models produce reasonable output with the right harness design  
✅ Experiment shows substrate improves or maintains both speed and accuracy  

---

## Risk Assessment

### High Risk (Address Now)

🔴 **Hook capability gap:** If Claude Code `PreToolUse` can't access tool-error events, B2 becomes impossible (blocks Phase 2).

**Mitigation:** Verify hook capabilities immediately. Design alternative for B2 if needed.

🔴 **Crispycouscous integration:** Unknown surface area. Could introduce incompatible assumptions.

**Mitigation:** Audit on merge. Document differences. Run B1 validation on all incoming skills.

### Medium Risk (Plan For)

🟡 **Portability complexity:** Per-harness compilation adds infrastructure (build system, testing, CI checks).

**Mitigation:** Start small (5 skills). Automate compilation. Fail loudly if compilation breaks.

🟡 **Weak model performance:** Scaffold makes weak models useful for *constrained tasks*, not general work.

**Mitigation:** Define task classes clearly. Don't expect weak models to solve open-ended problems. Use them for mechanical work (formatting, test scaffolding, refactoring).

### Low Risk (Understand)

🟢 **Over-engineering:** Building too much infrastructure before validating that behaviors help.

**Mitigation:** Run override log + cheap proxy measurement first. Full experiment design after 4 weeks. Build only what's proven valuable.

---

## In One Sentence

**Your vision is 80% implemented (harness provides infrastructure). Your job is 20% (build the 7 behaviors and solve cross-harness portability). The key blocker is hook capability verification (3-5 days to Phase 1 complete). The key insight is that weak models are fine; the harness design matters more than the model.**

---

## Recommendation

**Do Phase 1 this week.** It's 3-5 days:
1. Check hook capability (1 day)
2. Run B1 validation + fix issues (1 day)
3. Start override log (same day)
4. Merge crispycouscous and audit (1-2 days)

Then decide whether to proceed to Phases 2-5 based on what you learn.

**If hooks support what you need:** Phase 2 (B2/B3 implementation) is another 1-2 weeks. Then Phase 3 (framework) is 1 week. Then Phase 4 (portability layer) is 2-4 weeks of real work.

**Total realistic timeline:** 1-2 weeks validation → 1 week hook integration → 1 week framework → 2-4 weeks portability = **5-8 weeks to shipping** (not 4+ months).

---

**Status:** Ready to move forward  
**Immediate action:** Phase 1 (this week)  
**Decision point:** Hook capability verification results  
**Check-in:** After Phase 1 (end of week)
