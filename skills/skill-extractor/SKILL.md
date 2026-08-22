---
name: skill-extractor
description: Extracts reusable skills from work sessions. Use when: non-obvious problem solved, pattern discovered, workaround found, debugging technique learned, or project-specific pattern worth preserving.
license: MIT
compatibility: [claude, pi, vibe]
---

Extracts reusable knowledge from work sessions and saves it as a skill.

## When to Use

- Solved a non-obvious problem through investigation
- Discovered a workaround that required trial-and-error
- Found a debugging technique that would help in similar situations
- Learned a project-specific pattern worth preserving
- Fixed an error where the root cause was not immediately apparent

## When NOT to Use

- Simple documentation lookups (bookmark the docs instead)
- Trivial fixes (typos, obvious errors)
- One-off project-specific configurations
- Knowledge already well-documented elsewhere
- Unverified solutions

## Finding Extraction Candidates

Ask yourself:
- What did I just learn that was not obvious before starting?
- If I faced this exact problem again, what would I wish I knew?
- What error message or symptom led me here, and what was the actual cause?
- Is this pattern specific to this project, or would it help in similar projects?
- What would I tell a colleague who hits this same issue?

If you can answer at least two with something non-trivial, it is worth extracting.

## Extraction Process

1. Identify the core insight or solution
2. Generalize it beyond the specific context
3. Write clear instructions for future use
4. Save to appropriate skill location
5. Test the extracted skill works

## Output

Save extracted skills to ~/.vibe/skills/ with proper frontmatter and tool-agnostic instructions.
