# NotebookLM Audit Prompt Improvement Guide

---

## Overview

This guide covers the audit phase of a two-pass NotebookLM report pipeline. The audit prompt runs after a first-pass report is generated, reads the report from chat history, and outputs a fully corrected report in one pass as raw plaintext markdown.

Workflow context:
1. Research phase: research prompt extracts and synthesizes sources per topic into research notes uploaded to the notebook.
2. Report phase: report prompt loads into Configure Chat. Short trigger submitted in chat box. First-pass report generated.
3. Audit phase (this guide): Configure Chat cleared, audit prompt loaded. Chat history preserved. Short audit trigger submitted. Fully corrected report output.
4. Session reset: chat history deleted before running the next topic.

For delivery architecture, prompt structure basics, and output quality principles that apply equally to report and audit prompts, see the NotebookLM Report Prompt Improvement Guide.

---

## Delivery & Architecture

**1. Load the audit prompt into Configure Chat, not the chat box**
The audit prompt carries the same instruction complexity as the report prompt and will experience instruction drift and rule dilution if submitted via the chat box. Configure Chat is the correct surface.
*E.g. After report generation: open Configure Notebook -> clear System Instructions -> paste audit prompt -> Save. Submit short trigger: "Audit and output the fully corrected report from the draft generated directly above using my active custom instructions."*

**2. Preserve chat history through the audit pass**
The audit reads the first-pass report from chat history. Deleting history before the audit destroys the source text the audit needs. Do not delete chat history until after the corrected report is saved.
*E.g. Session order: generate report -> clear Configure Chat -> load audit prompt -> run audit -> save output -> delete chat history -> reset for next topic.*

**3. Treat chat history as the sole text baseline -- use session context only for URL lookup**
Chat history and the source corpus serve two distinct jobs. Chat history is the exclusive source for all text modification. The session context corpus is a read-only reference used only to locate and replace placeholder URLs using Author and Date as the lookup key. The bibliography source list derives from finalized inline citations in the corrected draft.
*E.g. Add: "Treat the chat history draft as the absolute exclusive baseline for all text modification. Use the source corpus strictly as a read-only metadata reference for locating placeholder URLs via Author and Date. Generate the bibliography from unique sources in the finalized inline citations."*

> **Disputed:** Multiple independent Gemini sessions rate the URL resolution approach as architecturally fragile -- NotebookLM's RAG retrieval is semantic, not relational, and cannot reliably surface exact URL metadata on demand. Known failure conditions: URL hallucination when chunk retrieval misses the target, hook mismatching on similar author/date combinations, collision with NotebookLM's native [1] citation markers. The author's testing produced reliable output with a cleanly structured corpus. Treat as a working approach with documented risk.

**4. Account for context saturation**
The audit runs with the first-pass report in chat history, the full source corpus loaded, and the audit instruction set in Configure Chat simultaneously. This increases token payload and risks instruction dropout or structural anchoring -- the model repeats the first-pass report rather than correcting it.
*E.g. Keep the audit prompt as concise as possible without sacrificing coverage. Instruction densification (dropping articles, collapsing verbose phrases, short synonyms) reduces token overhead without removing rules.*

**5. Reset source checkbox selections between sessions**
Deleting chat history does not clear source checkbox selections. Sources checked for a previous topic remain active unless manually reset.
*E.g. During session reset: verify source panel checkboxes are correct for the next topic before deleting chat history and reloading the report prompt.*

---

## Prompt Structure & Rules

**6. Single-pass regeneration changes the failure mode**
The audit must simultaneously evaluate the draft, identify failures, and regenerate corrected prose -- higher compliance load than review-only. Rules that hold in review-only contexts may fail here. Competing mandates must be explicitly resolved.
*E.g. "Retain 100% of original data" vs "remove redundant sentences" is unresolvable without a priority rule. Fix: "retain all source-grounded findings; remove padding and restatements only."*

**7. Delegate sparse corpus evaluation to the audit**
The audit is better positioned than the report prompt for sparse corpus detection -- it evaluates a completed report rather than generating one mid-synthesis. However, the audit does not hold a master source index; detection remains approximate.
*E.g. Add: "If the report contains fewer than 3 distinct cited sources, downgrade all claims to tentative and append: 'Corpus contains [N] sources. Claims are tentative pending broader evidence.'" Treat the threshold as a signal, not a hard count.*

**8. Consolidate hedging rules to one block**
Hedging instructions scattered across audit parameters produce uneven enforcement. One authoritative block at the top covers all sections.
*E.g. "Prepend epistemic qualifiers strictly to forward-looking projections and future-state claims. Do not hedge historical facts, raw metrics, or current-state assessments." Remove hedging mentions from individual parameters.*

**9. Use exact literal matches for banned source rules**
Semantic category language triggers over-generalization -- the model flags legitimate sources that pattern-match to the category.
*E.g. "Banned sources (exact matches only): [list]. Valid sources including [named legitimate vendors] are fully permitted -- never flag or downgrade them."*

**10. Add anti-redundancy instructions explicitly**
The audit may re-introduce repeated elements during correction. Explicitly instruct it to preserve the scope boundaries established by the report prompt.
*E.g. "Do not restate the classification label outside the summary and assessment fields. Do not repeat verbatim sentences across sections. Recap must paraphrase, not restate, the Overall Assessment."*

**11. Use short tag-style delimiters to separate audit parameters**
Visual boundaries between parameters reduce attention bleed under high correction load.
*E.g. Use <PERSONA>, <RULES>, <PARAMETERS>. Keep identifiers short. Flatten hierarchy -- avoid nesting beyond two levels.*

---

## Output Quality

**12. Provide a tone example before the audit parameters**
The audit corrects register and phrasing as well as structure. A concrete example anchors the model to the target tone before it reads the correction rules.
*E.g. Include a 4-5 sentence example in the target register using a domain-neutral scenario. Place before the parameter list.*

**13. Provide bad/good contrast pairs for high-risk phrasing patterns**
Single positive examples leave the failure mode undefined. Patterns that appeared repeatedly in live output need explicit contrast pairs.
*E.g. Wrong: "The primary categorical driver is Factor Y." Right: "[Subject] requires [outcome] because [specific reason from sources]."*

**14. Use a hard replacement list for jargon that must never appear**
A general plain language instruction misses specific inherited terms under correction load. Explicit replacement rules are more reliable.
*E.g. List exact terms and replacements: "Term A -> plain equivalent." Apply before any other correction pass.*

**15. Require inline definition of technical terms on first use**
The audit may introduce or preserve technical terminology from source material. A general definition instruction catches all terms without an exhaustive denylist.
*E.g. "Any technical term unrecognizable to a non-technical reader -> define inline in parentheses on first use. Shorthand permitted after definition."*

**16. Require raw plaintext markdown output explicitly**
Explicit plaintext instruction ensures consistent output format and downstream handling.
*E.g. Add at the top: "Output ONLY the fully corrected report as raw plaintext markdown. No commentary, logs, or pre-report blocks."*

> **Disputed:** Multiple independent Gemini sessions assert the LLM context always receives raw markdown tokens regardless of UI rendering, making this unnecessary for data integrity. The author's testing found the instruction produced more reliable output. Included as a stylistic anchor rather than a data integrity measure.

**17. Order audit parameters by correction priority**
The model applies early parameters more reliably than late ones. Place critical corrections first.
*E.g. Order: (1) output format, (2) citation and URL repair, (3) classification label scope, (4) structural completeness, (5) tone and plain language, (6) stylistic details.*

**18. The audit cannot correct what the first-pass report omitted**
If the report prompt silently drops a required section or finding, the audit has no visibility into the omission and cannot insert missing content.
*E.g. If a required section is consistently absent from audited reports, fix the report prompt -- not the audit prompt.*

**19. Correction confidence decreases as departure from the draft increases**
Small corrections (word substitutions, citation fixes) are more reliable than large ones (paragraph rewrites, structural reorganization). Use the report prompt to prevent structural problems rather than relying on the audit to fix them.
*E.g. Prioritize close-to-draft corrections. Accept that structural rewrites will have lower compliance.*

**20. The audit trigger message is part of the instruction set**
The short chat box trigger affects output quality. Vague triggers produce different results than specific ones that reinforce key constraints.
*E.g. "Audit this" -> unreliable. "Audit and output the fully corrected report from the draft generated directly above using my active custom instructions. The entire report should be plaintext markdown, beginning with ``` and ending with ```." -> consistent.*

**21. Hard replacement lists need explicit application order**
If two replacement rules interact -- replacing Term A produces Term B, which also needs replacing -- unordered lists produce inconsistent results.
*E.g. Order the list to prevent collisions, or make each replacement atomic enough that order does not matter.*

**22. Both prompts need their own tone example**
If the tone example lives only in the report prompt, the audit generates without a register anchor. Include a separate example in the audit prompt before the parameter list.
*E.g. Use the same example as the report prompt if the target register is identical. Domain-neutral examples avoid content pattern-matching.*

**23. The audit is prone to accepting first-pass hallucinations**
The audit's attention weights prioritize text strings present in chat history. Convincing hallucinations from the first-pass report are likely to be preserved rather than corrected against the source corpus.
*E.g. Add: "Cross-check all quantitative claims and named sources against the uploaded corpus. If a claim cannot be verified, flag it as unverified rather than preserving it." Accept partial compliance.*

**24. Prefer principles over rigid syntax templates**
NotebookLM silently updates its underlying models. Highly specific structural templates are fragile across backend updates.
*E.g. Prefer "open with market data" over "open with exactly one sentence containing a percentage figure."*

---

## What Didn't Work

**Two-turn instruction loading**
Rules in turn 1, output template in turn 2 tested as a workaround for the chat box length limit. Session memory holds across turns but complex rules drift under corpus injection pressure. Abandoned in favor of Configure Chat.
*Verdict: unreliable for multi-rule prompts. Only viable for very simple rule sets.*

**Verification scaffold**
A pre-report block required explicit verification of key structural elements before generation. Added workflow overhead, frequently ignored or superficially completed. Removed in favor of stronger inline instructions.
*Verdict: surface-level check that does not prevent the underlying failure. Fix the instruction, not the verification.*

**Escaped link syntax**
Backslash-escaping URL parentheses (\(URL\)) tested to prevent hyperlink rendering. Confirmed to corrupt valid URLs. Rendering is UI-only and does not affect downstream plaintext.
*Verdict: breaks more than it fixes. Standard unescaped markdown syntax is correct.*

**Bibliography extraction from inline citations only (without URL lookup)**
Earlier version extracted bibliography from finalized inline citations without accessing session context for URLs. Placeholder URLs ("URL", "Markdown", "PDF") propagated unchanged. Resolution: bibliography source list from inline citations; actual URLs from session context via Author/Date lookup. These are two separate jobs.
*Verdict: draft-only extraction insufficient when report prompt outputs citation hooks. URL lookup requires session context access.*

**Sentence count enforcement**
Hard sentence count constraints produced inconsistent compliance. The audit cannot reliably count sentences while simultaneously correcting prose, citations, structure, and tone in one pass.
*Verdict: not reliably enforceable in single-pass regeneration. Use as soft guidance only.*

---

## Appendix -- Special Cases

### Single-pass regeneration constraints
The audit outputs a fully corrected report in one pass rather than a review checklist. This changes which instructions are enforceable and which create compliance conflicts.

**Competing correction mandates create resolution ambiguity.** Rules like "retain 100% of original data" and "remove redundant sentences" conflict when a finding is stated redundantly. State the priority order explicitly.

**Structural rewrites fail under single-pass load.** Correcting tone, citations, structure, and prose simultaneously exceeds reliable single-pass compliance. Prioritize critical corrections. Accept that minor stylistic failures may persist.

**The model anchors to the draft structure.** Under high correction load, the model defaults to preserving the first-pass structure rather than applying rewrites. If structural correction is critical, place it first -- not buried in a parameter list.

### Sparse corpus handling
The audit is better positioned than the report prompt to evaluate source coverage because it reads a completed report rather than generating one.

**Threshold detection is more reliable in the audit.** The audit evaluates the report holistically rather than mid-synthesis -- but does not hold a master source index. Treat counts as approximate.

**Qualitative source assessment belongs in the audit.** Judgments about speculative, vendor-only, or evidentiary sources require reading the report in context. Add qualitative sparse corpus handling to the audit prompt, not the report prompt.

### Taxonomy-driven reports
When the report classifies topics into named categories, the audit inherits the label repetition problem and adds a correction-specific risk.

**The audit may over-enforce label suppression.** If the report prompt restricted classification labels to specific fields, the audit must not re-introduce them elsewhere during correction. Instruct the audit to preserve the label scope established by the report prompt.

**Bifurcation exception clauses require source verification.** The audit can verify that exception clauses reference source-documented capabilities -- a check the report prompt cannot reliably perform at generation time. Add an explicit verification step.
