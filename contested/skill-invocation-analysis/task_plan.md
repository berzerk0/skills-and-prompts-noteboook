# Task Plan: Vibe Code Skill Invocation Analysis

## Goal
Answer four questions about Vibe Code's skill system:
1. Can Vibe Code on the web identify its own skills?
2. Can models invoke skills automatically?
3. How about agent files?
4. How does Vibe Code on the web know when to invoke skills?

Validate answers using: (1) docs in this repo, (2) official Mistral docs if insufficient, (3) manual source verification.

## Current Phase
Phase 5: Synthesize Answers

## Phases

### Phase 1: Requirements & Discovery
- [x] Understand the four questions
- [x] Identify relevant documentation in repo
- [x] Document findings from repo docs
- **Status:** completed

### Phase 2: Research from Repo Docs
- [x] Search and read VERIFIED_REFERENCE.md
- [x] Search and read vibe-reference skill
- [x] Search and read COMPATIBILITY.md
- [x] Extract answers to all four questions
- **Status:** completed

### Phase 3: Validate with Official Docs
- [x] Search Mistral docs for skill discovery
- [x] Search Mistral docs for automatic invocation
- [x] Search Mistral docs for agent file behavior
- [x] Cross-validate findings
- **Status:** completed

### Phase 4: Manual Source Verification
- [x] Check source code references in VERIFIED_REFERENCE.md
- [x] Verify skill loading behavior
- [x] Verify model invocation behavior
- **Status:** completed

### Phase 5: Synthesize Answers
- [x] Compile final answers with citations
- [x] Document validation process
- [x] Create findings.md and progress.md
- **Status:** completed

## Key Questions
1. What mechanism does Vibe Code use to discover skills?
2. What triggers skill invocation by the model?
3. How are agent files related to skills?
4. What is the decision process for when to invoke skills?

## Answers Compiled
1. **Skill Discovery**: Vibe Code discovers skills via `.vibe/skills/` (project) and `~/.vibe/skills/` (user) directories, plus `skill_paths` in config.toml
2. **Automatic Invocation**: Models CAN invoke skills automatically when they are enabled and have a description field (model-invoked)
3. **Agent Files**: Agent files (.toml in .vibe/agents/) define subagents with their own tool sets; the `skill` tool must be in enabled_tools for the agent to load skills
4. **Invocation Decision**: Models decide based on skill name+description in system prompt; progressive disclosure means full content loads only on first invocation

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Use planning-with-files methodology | User explicitly requested this approach |
| Created isolated branch | Prevents contamination of main branch |
| Start with repo docs | Highest confidence, already verified |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| None yet | | |
