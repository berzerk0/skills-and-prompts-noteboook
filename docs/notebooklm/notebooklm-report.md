# NotebookLM Report Prompt Improvement Guide

---

## Delivery & Architecture

**1. Use Configure Chat for complex prompts, chat box for triggers only**
Configure Chat ("Configure Notebook / Configure Chat") receives higher system-level priority than the chat input box and persists across all turns in the session. Long or complex prompts submitted directly in the chat box cause instruction drift and unreliable execution. Reserve the chat box for short trigger messages only.
*E.g. Report prompt (5,000+ chars) -> Configure Chat. Chat box trigger -> "Generate the report using my active custom instructions for TARGET TOPIC: [Name]"*

**2. Identify the delivery mechanism before optimizing prompt length**
NotebookLM has two distinct instruction surfaces with different behaviors. Optimizing prompt length for the wrong surface wastes effort.
*E.g. Test Configure Chat and the chat input box ("Ask questions or create something") separately early in development. Failures in the chat box are typically instruction drift, not a hard length limit.*

**3. Clear Configure Chat between report and audit steps -- do not delete chat history**
Two separate actions with opposite effects. Clearing Configure Chat removes the active instruction set. Deleting chat history removes the report the audit needs to read. Do not confuse them.
*E.g. After report generation: open "Configure Notebook" -> clear the System Instructions field -> paste audit prompt -> Save. Leave the Chat History timeline intact. Submit the audit trigger.*

**4. Reset source checkbox selections between sessions**
Deleting chat history does not clear manual source checkbox selections in the source panel. Failing to reset checkboxes causes cross-topic contamination in the next session.
*E.g. After saving corrected output: verify source panel checkboxes are reset for the next topic before deleting chat history and reloading the report prompt.*

**5. One topic per session**
Multiple topics in one session accumulate context that bleeds between reports. Each topic gets a clean session.
*E.g. After saving corrected output: Delete Chat History -> reload report prompt into Configure Chat -> run next topic.*

**6. Do not rely on session memory for complex rule sets**
NotebookLM maintains chat history across turns but complex rules drift under corpus injection pressure. All rules must be present in Configure Chat at generation time.
*E.g. Two-turn approach (rules in turn 1, template in turn 2) tested and abandoned -- rules dropped before generation completed.*

**7. Manually deselect irrelevant sources before generation**
Prompt constraints alone are unreliable for preventing the model from drawing on sources unrelated to the current topic. Manually unchecking sources in the UI sidebar is the most reliable method -- but requires manual effort per session.
*E.g. Before generating a report on Topic A, uncheck sources uploaded for Topics B and C in the source panel. Re-check after the session.*

**8. Be aware of context saturation in the audit pass**
The audit runs with the first-pass report in chat history, the source corpus loaded, and the audit instruction set in Configure Chat simultaneously. This increases token payload and can cause instruction dropout or structural anchoring (the model repeats the first-pass report rather than correcting it). The two-pass design mitigates this by separating synthesis from correction -- but does not eliminate the risk entirely.
*Note: Gemini rates this risk as High. The two-pass architecture is still recommended as the best available mitigation.*

---

## Prompt Structure & Rules

**9. Consolidate each behavioral rule to one authoritative location -- scope repeated output elements to one section**
Repeating the same rule or structural element across multiple sections creates competing instruction pressure. The model defaults to the most recent or most salient instance. Define once, reference downstream.
*E.g. A formatting rule defined in four locations -> inconsistent application. Fix: define once at the top, reference downstream with "apply as defined in Rule N." A status label defined in the summary should not be restated verbatim in the analysis paragraphs or recap.*

> **Special case -- taxonomy-driven reports:** If the report classifies topics into named categories (e.g. risk tiers, maturity levels, displacement labels), the category name will appear wherever classification is referenced. Mitigate by restricting the formal label to the summary and assessment fields, and requiring all other sections to express the same meaning in plain causal language.

**10. Replace negative constraints with positive behavioral direction**
Negative constraints ("do not restate here", "never use X") fail reliably under dense corpus load. The model prioritizes affirmative structural instructions.
*E.g. "Do not open the first paragraph with a summary statement" -> "Open the first paragraph with market adoption metrics, deployment rates, or historical baselines."*

**11. Use exact literal matches for banned source rules**
Semantic category language triggers over-generalization -- the model flags legitimate sources that pattern-match to the category description.
*E.g. "Banned sources: [list exact source names or types]." Explicitly authorize known legitimate sources by name if they risk being caught by the category.*

**12. Convert role identity into a prompt-opening statement**
Style instructions listed as property lists ("active voice, no pronouns") have lower compliance than a role statement at the top of the prompt. The role anchors all subsequent generation.
*E.g. Property list -> "Write as a [role] producing a [document type] for [audience]. Active voice, no first-person pronouns, prose outside structured fields."*

**13. Remove URL burden from the report prompt -- delegate to the audit**
Forcing the report prompt to find, format, and embed URLs simultaneously with analytical prose causes citation dropout. Output citation hooks only in the report pass; resolve to full URLs in the audit pass using the source corpus as a lookup reference.
*E.g. Report prompt outputs: [Source Title/Author (YYYY-MM)]. Audit resolves to: ([Source Title/Author (YYYY-MM)](URL)).*

> **Architectural note -- disputed:** Gemini (two independent sessions) assesses this approach as fragile, citing NotebookLM's RAG architecture (semantic chunk retrieval, not relational lookup) and risk of URL hallucination or native citation system collision. The author's testing produced reliable output. The approach appears to work when the source corpus is cleanly structured with clear author/date attribution. Known failure conditions: URL hallucination when retrieval misses the target chunk, hook mismatching on similar author/date combinations, potential collision with NotebookLM's native [1] citation markers. Treat as a working approach with documented risk rather than a confirmed best practice.

**14. Account for native citation system collisions**
NotebookLM's hardcoded inline citation bubbles ([1], [2]) cannot be removed. Custom citation format instructions can collide with this system, causing duplicate references, broken markdown syntax, or the model attempting to satisfy both the user's format and the system's RAG citation simultaneously.
*E.g. If custom inline citation format produces garbled output, the native citation system may be overriding it. Test custom citation instructions against a simple corpus first to identify collision behavior before applying to a full pipeline.*

**15. Instruct the model to cite primary publishers, not research note containers**
When research notes are uploaded as sources, the model cites the note container ("Research Notes", "Markdown") rather than the original publisher embedded within. Explicit instruction required.
*E.g. "When extracting a finding from a research note, identify the original primary publisher embedded next to that finding and cite only the primary publisher. Never attribute data to container file names."*

**16. Require raw plaintext markdown output explicitly**
Without an explicit instruction, NotebookLM may apply default formatting behaviors that vary by context. Explicitly instructing raw plaintext output ensures consistent stylistic output and downstream handling.
*E.g. Add: "Output: Raw plaintext markdown only. All citations and links must appear as plaintext markdown syntax."*

> **Disputed:** Two independent Gemini sessions assert that the LLM context always receives raw markdown tokens regardless of UI rendering, making this instruction unnecessary for data integrity. The author's testing found the instruction produced more reliable citation output. Included on the basis of observed behavior. The instruction may function as a stylistic anchor rather than a data integrity measure.

**17. Use short tag-style delimiters to separate prompt sections**
Visual boundaries between instruction blocks reduce attention bleed between sections. Formal XML compliance is not required -- the model recognizes simple bracket-style delimiters.
*E.g. Use <RULES>, <OUTPUT>, <CONSTRAINTS> rather than long descriptive headers. Keep identifiers short. Avoid nesting beyond two levels -- flatten into sequential blocks instead.*

---

## Output Quality

**18. Provide a tone example in the prompt**
Style instructions alone produce inconsistent register. A concrete example paragraph anchors the model to the target tone more reliably than any list of style properties. Use a domain-neutral example to avoid pattern-matching to the task content.
*E.g. Include a 4-5 sentence example paragraph in the target register (internal memo, plain language, active voice) before the structural instructions.*

**19. Use plain causal language templates for key output fields**
High-stakes output fields default to robotic or formulaic phrasing without an explicit sentence structure template. Provide the template, not just the constraint.
*E.g. Instead of "state the primary reason," provide: "[Subject] because [specific reason from sources]." The template anchors the model to the correct sentence construction.*

**20. Provide bad/good contrast pairs for high-risk phrasing**
Single positive examples leave the failure mode undefined. Contrast pairs make the boundary explicit and reduce borderline compliance failures.
*E.g. Wrong: "Product X falls into Category A due to the primary categorical driver being Factor Y." Right: "Product X requires manual oversight because automated tools cannot process its proprietary file format without prior human configuration."*

**21. Scope hedging to forward-looking claims only**
Global hedging instructions produce over-hedged output where factual cited claims are qualified unnecessarily. Restrict hedging to projections and future-state claims.
*E.g. "Prepend epistemic qualifiers strictly to forward-looking projections and future-state claims. Do not hedge historical facts, raw metrics, or current-state assessments."*

**22. Require exception clauses to reference source-documented evidence**
Open-ended exception instructions produce analytical labels invented by the model rather than grounded observations. Require any exception or qualifier to reference a specific capability or barrier named in the source corpus.
*E.g. "Exception clause must reference a specific finding named in the source corpus -- not an analytical category. If the finding uses technical terminology, define it inline in parentheses."*

**23. Instruct the model to define technical terms inline on first use**
Domain-specific terminology (acronyms, product names, regulatory frameworks) is invisible to non-technical readers. A general inline definition instruction catches all terms without requiring a denylist.
*E.g. "Any technical term, acronym, or domain-specific phrase unrecognizable to a non-technical reader -> define inline in parentheses on first use. Shorthand permitted after definition."*

**24. Do not rely on the model to count sources mid-generation**
LLMs cannot reliably maintain a running source count while simultaneously synthesizing analytical prose. Sparse corpus detection based on counting produces inconsistent results.
*E.g. Remove source-count thresholds from the report prompt. Delegate sparse corpus evaluation to the audit prompt, which can assess the completed report against the source list in session context.*

**25. Prefer principles over rigid syntax templates**
NotebookLM silently updates its underlying models over time. Highly specific structural templates (exact sentence patterns, hard formatting constraints) are fragile and may break across backend model updates.
*E.g. Prefer "open with market data" over "open with exactly one sentence containing a percentage figure." The principle survives model updates; the rigid syntax may not.*

---

## What Didn't Work

**Two-turn instruction loading**
Splitting the prompt across two chat turns (rules in turn 1, output template in turn 2) was tested as a workaround for the chat box length limit. Session memory holds across turns, but complex rules drift under corpus injection pressure -- the model deprioritizes turn 1 instructions before generation completes. Abandoned in favor of Configure Chat.
*Verdict: unreliable for multi-rule prompts. Only viable for very simple rule sets.*

**Verification scaffold**
A pre-report output block was added requiring the model to explicitly verify coverage of key structural elements before generating the corrected report. Intended to catch silent dropout of required sections. Added workflow overhead and was frequently ignored or superficially completed. Removed in favor of stronger inline section instructions.
*Verdict: surface-level compliance check that does not prevent the underlying failure. Fix the instruction, not the verification.*

**Escaped link syntax**
Backslash-escaping URL parentheses (\(URL\)) was tested to prevent NotebookLM's UI from rendering markdown links as clickable hyperlinks. Confirmed to corrupt valid URLs in output. The rendering issue is UI-only and does not affect downstream plaintext use.
*Verdict: breaks more than it fixes. Standard unescaped markdown syntax is correct.*

**Sentence count enforcement**
Hard sentence count constraints per paragraph ("exactly 4-5 sentences") were included across multiple prompt versions. LLMs generate text token-by-token and cannot reliably maintain a running sentence count during complex synthesis. Compliance was inconsistent regardless of instruction strength.
*Verdict: not reliably enforceable at generation time. Use as audit guidance only, not a hard generation constraint.*

---

## Appendix -- Special Cases

### Taxonomy-driven reports
Some report designs classify each topic into a named category (e.g. risk tiers, maturity levels, status labels) based on source evidence. These designs introduce structural challenges that do not arise in open-ended report formats.

**Label repetition is structural, not a prompt failure.** When a report must state a classification in the summary, the assessment, and the recap, the label will appear multiple times by design. The mitigation is not to remove the label but to restrict formal label syntax to the assessment field and require all other sections to express the same meaning in plain causal language.

**Bifurcation or exception syntax amplifies the repetition problem.** If the classification system supports qualified labels ("Category A -- except where [condition] applies"), the exception clause will appear wherever the label appears. Restricting the full bifurcation syntax to one field and requiring downstream sections to paraphrase reduces verbatim repetition without losing analytical nuance.

**Exception clauses must be grounded in source evidence.** When the model generates exception clauses without a grounding constraint, it produces analytical labels ("except where configuration complexity applies") rather than observable conditions. Requiring the exception to reference a specific documented finding or capability closes this gap.
