# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for crispy-couscous. ADRs document important architectural decisions along with their context and consequences.

---

## Active ADRs

| Number | Title | Status | Date |
|--------|-------|--------|------|
| [ADR-001](ADR-001-canonical-skill-format.md) | Canonical Skill Format | PROPOSED | 2026-08-23 |
| [ADR-002](ADR-002-drop-skill-type.md) | Drop skill_type Classification | PROPOSED | 2026-08-23 |

---

## ADR Template

```markdown
# ADR-XXX: Title

**Status:** PROPOSED/ACCEPTED/DEPRECATED/SUPERSEDED  
**Date:** YYYY-MM-DD  
**Author:** Name  
**Supersedes:** ADR-XXX (if applicable)

---

## Context

What is the issue that we're seeing or the background on this?

## Decision

What is the change that we're proposing and/or doing?

### Implementation

How will this be implemented?

## Consequences

### Positive
- What are the benefits?

### Negative
- What are the drawbacks?

## Alternatives Considered

What other options did we consider?

## Related

Links to other ADRs, documentation, or external references.

---

*Last updated: YYYY-MM-DD*
```

---

## Process

1. **Propose:** Create a new ADR file with "PROPOSED" status
2. **Discuss:** Review and discuss the proposal
3. **Accept:** Change status to "ACCEPTED" when decision is made
4. **Implement:** Implement the decision
5. **Deprecate:** Change status to "DEPRECATED" if superseded

---

## References

- [ADR GitHub](https://adr.github.io/)
- [ADR Template](https://github.com/adr/adr-tools/blob/master/templates/adr-template.md)
