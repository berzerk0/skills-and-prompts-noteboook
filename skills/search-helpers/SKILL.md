---
name: search-helpers
description: >
  Structured search guidance for evidence gathering. Provides coverage, quality,
  verification, transparency, and gap-handling rules. Trigger on explicit
  search requests or when user invokes a search snippet by name.
---

# Search Helpers

Apply these rules when performing web search, document research, or any
evidence-gathering task. Each rule set can be invoked independently.

## search-coverage

Ensure comprehensive source coverage:
- Minimum 3 independently parsed sources from distinct domains
- Continue searching after question is answered -- don't stop at first satisfying result
- If topic is jurisdiction-dependent, require geographically relevant sources
- If topic is contested, require opposing viewpoints

## search-quality

Enforce source quality standards:
- Prefer primary sources (official docs, RFCs, government sites, peer-reviewed papers)
- Prefer aggregators only when no primary source available
- Exclude forums, SEO farms, and AI-generated content
- Require publication date within 12 months for time-sensitive topics

## search-verification

Verify claims rigorously:
- Cross-check key claims across sources
- Flag any claim supported by only one source
- Flag circular sourcing -- when sources cite each other without independent basis
- Surface disagreements between sources explicitly -- do not silently synthesize

## search-transparency

Maintain transparency in research process:
- Show search queries used
- State which sources were found but rejected and why
- Flag paywalled or inaccessible sources encountered

## search-gaps

Handle evidence gaps properly:
- Do not predict when evidence is insufficient
- Flag partial answers explicitly: "found X but not Y"
- Distinguish "not found" from "does not exist"
- After 3 attempts without sufficient answer, flag the gap -- do not continue speculating

## search-citations

Format citations correctly:
- Cite each source in full: (Source Name, YYYY-MM, URL)
- Note if source has been updated since original publication
- Flag sources with known bias or conflicts of interest

## search-full

Complete search requirements (combines all above):

**Source quality:**
- Prefer primary sources (official docs, RFCs, government sites, peer-reviewed papers)
- Prefer aggregators only when no primary source available
- Exclude forums, SEO farms, and AI-generated content
- Require publication date within 12 months for time-sensitive topics

**Coverage:**
- Minimum 3 independently parsed sources from distinct domains
- Continue searching after question is answered -- don't stop at first satisfying result
- If topic is jurisdiction-dependent, require geographically relevant sources
- If topic is contested, require opposing viewpoints

**Verification:**
- Cross-check key claims across sources
- Flag any claim supported by only one source
- Flag circular sourcing -- when sources cite each other without independent basis
- Surface disagreements between sources explicitly -- do not silently synthesize

**Transparency:**
- Show search queries used
- State which sources were found but rejected and why
- Flag paywalled or inaccessible sources encountered

**Gap handling:**
- Do not predict when evidence is insufficient
- Flag partial answers explicitly: "found X but not Y"
- Distinguish "not found" from "does not exist"
- After 3 attempts without sufficient answer, flag the gap -- do not continue speculating

**Citations:**
- Cite each source in full: (Source Name, YYYY-MM, URL)
- Note if source has been updated since original publication
- Flag sources with known bias or conflicts of interest
