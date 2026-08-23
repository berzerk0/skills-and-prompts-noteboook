# NotebookLM Deep Research Prompt Improvement Guide

---

## Structural / Environmental

**1. Match language to agent type**
Corpus mode = "documents." Web agent mode = "URLs." Wrong vocabulary breaks instruction translation.
*E.g. "list all notebook documents used" -> "list URLs already imported"*

**2. Convert negative constraints to positive assertions**
Gemini processes what to do more reliably than what not to do.
*E.g. "Reject all data predating 2024" -> "Extract data exclusively from January 1, 2024 onward"*

**3. Add recency bias within a hard temporal window**
Broad date ranges let old sources dominate. Explicit recency steers toward fresher results without narrowing the cutoff.
*E.g. Add "Prioritize sources from the most recent 12 months within the window"*

**4. Anchor dimension count at both intro and dimensions header**
Stating the count once decays over long prompts — model loses the constraint before reaching the dimensions block. Restate at both locations.
*E.g. Intro: "across exactly 5 thematic areas" + Header: "Research Dimensions (5 total — do not add, combine, or omit)"*

**4b. State the current date explicitly in the temporal window**
Agents don't reliably self-determine today's date. Without it, recency weighting is undefined.
*E.g. "Extract data from January 1, 2024 onward. Current date: June 4, 2026. Prioritize sources from December 2025–June 2026."*

**5. Add citation metadata capture explicitly**
Deep Research won't preserve URL, publication month, or verbatim anchor unless instructed. Downstream citation formats fail without this.
*E.g. Add "For every source, record full URL, publication date including month, and exact 10–15 word verbatim sentence anchor"*

**6. Reframe state tracking for deduplication**
Track and exclude already-imported sources between sequential queries. Use URLs for web mode, document titles for corpus mode.
*E.g. "Before each query, list URLs already imported and exclude them from this search"*

**7. Hard-cap sub-query branching depth**
Complex dimensions spawn recursive sub-queries, exhausting execution budget on one topic before covering others.
*E.g. Add "Limit sub-query branching to max 3 layers per search angle"*

**8. Enforce inter-document equity (corpus mode)**
Large documents create token-gravity that suppresses shorter sources. Mandate at least one insight per document.
*E.g. Add "Include at least one distinct insight from every uploaded document, regardless of length"*

---

## Dimension / Search Angle Design

**9. Write dimensions as descriptive noun phrases, not commands**
Deep Research decomposes into sub-queries. Noun phrases = search angles. Commands belong in report prompts.
*E.g. "Map exploit chaining vs planning failures" -> "AI autonomous execution limits: exploit chaining, context exhaustion, planning failures"*

**10. Avoid academic phrasing — it pulls academic sources**
Dimensions written as research abstracts attract papers *about* the topic, not real-world evidence *of* it. Anchor to where the evidence lives.
*E.g. "Token attention scoring anomalies" -> "Token attention scoring anomalies: transformer evaluation logs, model-attention visualization studies, ablation test results"*

**11. Use exhaustive noun phrases to imply a collection**
Agents stop once a dimension feels "satisfied." Phrasing that implies multiple instances forces continued searching.
*E.g. "AI context exhaustion limits" -> "Multiple documented instances of AI context exhaustion across diverse model architectures"*

**12. Lead each dimension with its saturation count**
Burying "locate at least 3" mid-sentence downgrades it from hard floor to descriptor. Lead with the count.
*E.g. "Locate at least 3 independent instances of [topic] across [artifacts]" — not "[topic]: locate at least 3..."*

**13. Place saturation and null-result rules globally, not inline per dimension**
Inline repetition per dimension causes duplicate outputs. One global rule covers all dimensions cleanly.
*E.g. Move "If zero results, state: 'No empirical data present'" to Execution Rules, remove from each dimension*

**14. Mandate cross-verification**
Force a second source to confirm, refine, or challenge every primary claim.
*E.g. Add "For every primary claim, find a secondary unrelated source that confirms, refines, or challenges it"*

**15. Audit dimensions against downstream output requirements**
Sections with no matching dimension will be source-starved. Use thematic coverage, not 1:1 structural mirroring.
*E.g. Two report sections with no matching dimension -> absorbed into one broader landscape dimension*

**16. Include both positive and negative evidence angles**
Failure-only dimensions miss positive data; success-only dimensions miss flaws. Both needed for balanced output.
*E.g. "Human cleanup costs" + "AI speed and efficiency gains vs. manual baseline" in same dimension*

**17. Restore specific vocabulary after compression**
High-level phrases won't surface granular detail. Verify sub-terms survive compression.
*E.g. "Limits of independent execution" -> add "context exhaustion, planning failures, tool-level bugs"*

**18. Consolidate overlapping dimensions**
Multiple dimensions targeting the same output section over-concentrate search effort. Merge and use freed slot for underserved angle.
*E.g. Three barrier dimensions -> one, freeing a slot for a contradiction dimension*

**19. Anchor dimensions with artifact-specific nouns**
Conceptual phrases return soft summaries. Append the specific data containers where raw evidence lives.
*E.g. "Implementation flaws" -> "Implementation flaws: commit logs, post-mortems, changelogs, issue trackers, release notes"*

**20. Apply skepticism globally, not per dimension**
Inline skepticism on one dimension causes uneven enforcement — agent applies it most aggressively there, treats global rule as background elsewhere.
*E.g. Remove inline skepticism from individual dimensions; add to Execution Rules: "Treat all vendor claims as idealized baselines across all dimensions"*

**21. Add a contradiction-targeting dimension**
Deep Research defaults toward consensus. Explicitly target independent benchmarks vs. vendor claims.
*E.g. "Conflicting vendor claims vs. independent benchmarks: third-party evaluations, stress test failures, edge-case results"*

**22. Add a negative space / gap analysis dimension**
Agents won't report what's missing unless instructed. Treat silence as data.
*E.g. "Features with zero independent benchmarks: list as 'undocumented by third parties'. Queries attempted: [list]. State: 'No empirical data present in current corpus/web window'"*
