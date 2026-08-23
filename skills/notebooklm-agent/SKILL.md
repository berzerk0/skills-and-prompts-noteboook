---
name: notebooklm-agent
description: >
  Expert agent for NotebookLM prompt engineering. Provides delivery architecture
  guidance, prompt structure optimization, and audit/report pipeline management.
  Trigger on "notebooklm help", "notebooklm advice", or when user is working with
  NotebookLM prompts, reports, or audits.
---

# NotebookLM Agent

Expert guidance for building, optimizing, and debugging NotebookLM prompts.
Three phases: **Report** (synthesis), **Audit** (correction), **Deep Research** (evidence gathering).

---

## Delivery & Architecture

### Core Principles

**1. Use Configure Chat for complex prompts, chat box for triggers only**
Configure Chat receives higher system-level priority and persists across all turns.
Long or complex prompts in the chat box cause instruction drift.

**2. One topic per session**
Multiple topics accumulate context that bleeds between reports. Each topic gets a clean session.

**3. Clear Configure Chat between report and audit steps — do not delete chat history**
Clearing Configure Chat removes the active instruction set. Deleting chat history
removes the report the audit needs to read. These are separate actions with opposite effects.

**4. Reset source checkbox selections between sessions**
Deleting chat history does NOT clear manual source checkbox selections. Verify
checkboxes are reset for the next topic before deleting chat history.

**5. Manually deselect irrelevant sources before generation**
Prompt constraints alone are unreliable for preventing the model from drawing on
unrelated sources. Manually unchecking sources in the UI sidebar is most reliable.

### Session Workflow

```
Report phase:
1. Load report prompt into Configure Chat
2. Manually select relevant sources only
3. Submit short trigger in chat box
4. First-pass report generated

Audit phase:
1. Clear Configure Chat (remove report prompt)
2. Load audit prompt into Configure Chat
3. DO NOT delete chat history (audit needs the draft)
4. Submit audit trigger
5. Save corrected report
6. Delete chat history
7. Reset source checkboxes for next topic
```

**Context Saturation Warning:** The audit runs with the first-pass report in chat
history, the full source corpus loaded, AND the audit instruction set simultaneously.
This risks instruction dropout or structural anchoring (model repeats draft instead
of correcting it). Keep audit prompts concise. Use instruction densification
(drop articles, collapse verbose phrases) to reduce token overhead.

---

## Report Prompt Structure & Rules

### What Works

**Consolidate each behavioral rule to one authoritative location**
Repeating rules across sections creates competing instruction pressure.
Define once, reference downstream.

**Replace negative constraints with positive behavioral direction**
"Do not restate here" → "Open the first paragraph with market adoption metrics."
Negative constraints fail under dense corpus load.

**Use exact literal matches for banned source rules**
Semantic categories trigger over-generalization. List exact source names.

**Convert role identity into a prompt-opening statement**
"Write as a [role] producing a [document type] for [audience]." anchors better
than property lists.

**Use short tag-style delimiters**
`<RULES>`, `<OUTPUT>`, `<CONSTRAINTS>` — visual boundaries reduce attention bleed.
Avoid nesting beyond two levels.

**Provide a tone example in the prompt**
A concrete 4-5 sentence example paragraph anchors the model more reliably than
style property lists. Use domain-neutral examples.

**Use plain causal language templates**
For high-stakes fields: provide sentence structure templates, not just constraints.
E.g., "[Subject] because [specific reason from sources]."

**Provide bad/good contrast pairs**
Single positive examples leave failure modes undefined. Show both.

**Scope hedging to forward-looking claims only**
Do not hedge historical facts, raw metrics, or current-state assessments.

**Require exception clauses to reference source-documented evidence**
Prevents analytical labels invented by the model.

**Instruct to define technical terms inline on first use**
Catches all terms without requiring a denylist.

**Prefer principles over rigid syntax templates**
NotebookLM silently updates models. Principles survive; rigid syntax may break.

### URL Handling

**Remove URL burden from report prompt — delegate to audit**
Forcing report prompt to find, format, and embed URLs simultaneously with prose
causes citation dropout. Output citation hooks only in report pass; resolve
to full URLs in audit pass using source corpus as lookup.

Report: `[Source Title/Author (YYYY-MM)]`
Audit: `([Source Title/Author (YYYY-MM)](URL))`

**Architectural Note:** This approach is disputed. NotebookLM's RAG is semantic
(chunk retrieval, not relational lookup), risking URL hallucination or native
citation collision. Works reliably with cleanly structured source corpus.
Known failures: URL hallucination when retrieval misses target, hook mismatching
on similar author/date combinations, collision with NotebookLM's native [1] markers.

**Account for native citation system collisions**
NotebookLM's hardcoded inline citation bubbles ([1], [2]) cannot be removed.
Custom citation formats can collide. Test against simple corpus first.

**Instruct to cite primary publishers, not research note containers**
"When extracting from a research note, cite the original publisher embedded
within, never the container file name."

### Taxonomy-Driven Reports

**Label repetition is structural**
When reports classify topics into named categories, labels appear in summary,
assessment, and recap by design. Mitigation: restrict formal label syntax to
assessment field; require other sections to express meaning in plain causal language.

**Exception clauses must be grounded**
Require exceptions to reference specific documented findings, not analytical categories.

---

## Audit Prompt Structure & Rules

### Single-Pass Regeneration

The audit must simultaneously evaluate the draft, identify failures, and regenerate
corrected prose. Competing mandates must be explicitly resolved.

**Priority Rule:** State priority order explicitly. E.g., "retain all source-grounded
findings; remove padding and restatements only."

**Correction confidence decreases with departure from draft**
Small corrections (word substitutions, citation fixes) are more reliable than
large ones (paragraph rewrites, structural reorganization). Use report prompt
to prevent structural problems rather than relying on audit to fix them.

**The audit is prone to accepting first-pass hallucinations**
Attention weights prioritize text strings present in chat history. Convincing
hallucinations from first-pass report are likely preserved. Add explicit
verification: "Cross-check all quantitative claims and named sources against the
uploaded corpus. If a claim cannot be verified, flag it as unverified."

### Sparse Corpus Handling

**Audit is better positioned than report prompt**
Audit evaluates a completed report rather than generating one mid-synthesis.
But audit does not hold a master source index; detection remains approximate.

**Add to audit prompt:**
"If the report contains fewer than 3 distinct cited sources, downgrade all claims
to tentative and append: 'Corpus contains [N] sources. Claims are tentative
pending broader evidence.'"

### Structural Rules

**Use exact literal matches for banned source rules**
Semantic category language triggers over-generalization.

**Consolidate hedging rules to one block**
Scattered hedging instructions produce uneven enforcement.

**Add anti-redundancy instructions explicitly**
Audit may re-introduce repeated elements during correction.

**Use short tag-style delimiters**
`<PERSONA>`, `<RULES>`, `<PARAMETERS>` — reduces attention bleed.

**Order audit parameters by correction priority**
Model applies early parameters more reliably. Place critical corrections first.

**The audit trigger message is part of the instruction set**
Vague triggers produce unreliable results. Specific triggers that reinforce
key constraints produce consistent output.

**Hard replacement lists need explicit application order**
Unordered lists produce inconsistent results when replacements interact.

**Both prompts need their own tone example**
If tone example lives only in report prompt, audit generates without register anchor.

### What Didn't Work (Report & Audit)

**Two-turn instruction loading** — unreliable for multi-rule prompts.
**Verification scaffold** — surface-level check that doesn't prevent underlying failure.
**Escaped link syntax** — corrupts valid URLs.
**Bibliography extraction from inline citations only** — placeholder URLs propagate.
**Sentence count enforcement** — not reliably enforceable in single-pass regeneration.

---

## Deep Research Prompt Structure & Rules

### Structural / Environmental

**Match language to agent type**
Corpus mode = "documents." Web agent mode = "URLs." Wrong vocabulary breaks
instruction translation.

**Convert negative constraints to positive assertions**
"Reject all data predating 2024" → "Extract data exclusively from January 1, 2024 onward."

**Add recency bias within a hard temporal window**
"Prioritize sources from the most recent 12 months within the window."

**Anchor dimension count at both intro and dimensions header**
Stating count once decays over long prompts. Restate at both locations.

**State the current date explicitly**
Agents don't reliably self-determine today's date.

**Add citation metadata capture explicitly**
Deep Research won't preserve URL, publication month, or verbatim anchor unless instructed.
"For every source, record full URL, publication date including month, and exact
10-15 word verbatim sentence anchor."

**Reframe state tracking for deduplication**
Track and exclude already-imported sources between sequential queries.
Use URLs for web mode, document titles for corpus mode.

**Hard-cap sub-query branching depth**
"Limit sub-query branching to max 3 layers per search angle."

**Enforce inter-document equity (corpus mode)**
"Include at least one distinct insight from every uploaded document, regardless of length."

### Dimension / Search Angle Design

**Write dimensions as descriptive noun phrases, not commands**
Deep Research decomposes into sub-queries. Noun phrases = search angles.

**Avoid academic phrasing**
Attracts papers *about* the topic, not real-world evidence *of* it.

**Use exhaustive noun phrases to imply a collection**
"Multiple documented instances of [topic] across [artifacts]" forces continued searching.

**Lead each dimension with its saturation count**
"Locate at least 3 independent instances of [topic]" — not buried mid-sentence.

**Place saturation and null-result rules globally, not inline**
Inline repetition per dimension causes duplicate outputs.

**Mandate cross-verification**
"For every primary claim, find a secondary unrelated source that confirms, refines, or challenges it."

**Audit dimensions against downstream output requirements**
Sections with no matching dimension will be source-starved.

**Include both positive and negative evidence angles**
Failure-only dimensions miss positive data; success-only miss flaws.

**Restore specific vocabulary after compression**
High-level phrases won't surface granular detail.

**Consolidate overlapping dimensions**
Multiple dimensions targeting same output over-concentrate search effort.

**Anchor dimensions with artifact-specific nouns**
"Implementation flaws: commit logs, post-mortems, changelogs, issue trackers."

**Apply skepticism globally, not per dimension**
Inline skepticism causes uneven enforcement.

**Add a contradiction-targeting dimension**
"Conflicting vendor claims vs. independent benchmarks."

**Add a negative space / gap analysis dimension**
"Features with zero independent benchmarks: list as 'undocumented by third parties'."

---

## Quick Reference: Common Fixes

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Audit preserves first-pass hallucinations | Attention anchoring to chat history | Add explicit verification step in audit |
| Structural rewrites fail in audit | Single-pass load too high | Prioritize critical corrections; accept minor failures |
| Source count inconsistent | Model can't count mid-generation | Delegate to audit; use as soft guidance only |
| Custom citations garbled | Native citation collision | Test custom format against simple corpus first |
| URLs missing or wrong | Report prompt overloaded | Output hooks in report, resolve in audit |
| Label repeated everywhere | Taxonomy-driven report | Restrict formal labels to assessment field |
| Dimension returns wrong sources | Academic phrasing | Use artifact-specific nouns |
| Search stops too early | Dimension feels "satisfied" | Use exhaustive noun phrases |
