# The pile

Everything left unresolved by the 2026-09-02 merge. Built during phase 2, to be
**sorted during phase 3** against `IDEAL.md`. Per
[`integration-plan-2026-08-25.md`](integration-plan-2026-08-25.md): nothing here
is a task yet, and **drop is a valid outcome for any entry**.

Each entry records three things, the third being what makes it sortable later:

- **What** is unresolved
- **From** which repo, branch, or session
- **Why not settled now**

Merge base `2fdbcae` (noteboook) + `4d2c23d` (crispy-couscous). Plan:
[`merge-plan-2026-09-02.md`](merge-plan-2026-09-02.md).

---

## A. Contradictions between the two repos

### A1. `challenge-my-thinking` exists in both, with different content
- **What:** 52 lines (noteboook) vs 26 (crispy). noteboook's copy occupies
  `skills/challenge-my-thinking/`; crispy's is at
  `contested/crispy-couscous/skills/challenge-my-thinking/SKILL.md`.
- **From:** both repos' default branches.
- **Why not settled:** neither version has ever been invoked, so there is no
  evidence either is correct. Line count is not a quality measure — the shorter
  copy may be a deliberate condensation. The crispy copy is the one wired into
  the build step, which makes it the one currently in use but says nothing about
  whether it is better. Phase 2's rule is explicitly to record, not resolve.

### A2. `skill-extractor` exists in both, with different content — in four files
- **What:** `SKILL.md` 210 vs 54 lines, **plus** `references/quality-guide.md`,
  `references/skill-lifecycle.md` and `references/skill-template.md`, all
  differing. The integration plan mentions only the SKILL.md line counts; the
  three reference files are a finding of this merge.
- **From:** both repos' default branches.
- **Why not settled:** same as A1. Additionally, the four files may not agree
  about which version they belong to, and nobody has checked.

### A3. `planning-with-files` is a duplicate, not a contradiction
- **What:** present in both repos, **byte-identical across the entire
  directory** (confirmed by `diff -r`; it produced no merge conflict).
- **From:** both repos' default branches.
- **Why not settled:** nothing to settle — recorded so a later reader does not
  re-investigate it as a third conflict. Safe to drop from the pile.

### A4. `clarify` and `ask-questions-if-underspecified` compete for one trigger
- **What:** `clarify` (45 L, crispy) and `ask-questions-if-underspecified`
  (85 L, noteboook) both describe asking the user to clarify an underspecified
  request. Now co-resident, so their descriptions compete for selection on every
  turn.
- **From:** both repos; flagged in the integration plan and independently in
  `loose-ends/claude-github-repo-access-5p6zbx.md`.
- **Why not settled:** deciding whether they are one skill or two requires
  observing which one actually fires, which is a phase-3 measurement.

### A5. `vibe-internals` and `vibe-reference` may be the same skill twice
- **What:** `vibe-internals` (633 L, noteboook, plus `docs/vibe/internals.md`)
  vs `vibe-reference` (161 L, crispy, plus `docs/vibe/VERIFIED_REFERENCE.md`).
- **From:** both repos. Mapping recorded only in
  `loose-ends/claude-github-repo-access-5p6zbx.md`, never in any repo file.
- **Why not settled:** same as A4, and neither has been invoked.

### A6. Four-way `AGENTS.md` duplication
- **What:** crispy carried three differing agent-instruction files — `AGENTS.md`
  (276 L), `docs/AGENTS.md` (71 L), `.vibe/AGENTS.md` (49 L). noteboook adds a
  fourth (220 L). Post-merge the live `AGENTS.md` is noteboook's; crispy's is at
  `contested/crispy-couscous/AGENTS.md`.
- **From:** both repos. `loose-ends/fix-readme-remove-codeberg-and-stale-refs.md`
  reported this as a possible **three**-way problem inside crispy alone and
  noted its author never compared `.vibe/AGENTS.md` against the other two.
- **Why not settled:** reconciling four instruction files is authoring, not
  merging, and getting it wrong changes agent behavior in every future session.

### A7. Two `README.md` files
- **What:** noteboook's (410 L) is live; crispy's (298 L) is at
  `contested/crispy-couscous/README.md`. Crispy's contains the compatibility
  table that D4 shows is wrong.
- **From:** both repos.
- **Why not settled:** a merged README asserts a merged story about what works,
  and phase 3 has not run yet.

### A8. Three `scratchpad/` files contested three ways
- **What:** `findings.md`, `progress.md`, `task_plan.md` exist in both repos with
  different content, **and** crispy's
  `vibe/skill-invocation-analysis-3f722e` branch rewrites all three again
  (+444/−379). noteboook's are live; crispy's are at
  `contested/crispy-couscous/scratchpad/`; the branch's at
  `contested/skill-invocation-analysis/`.
- **From:** both repos plus that branch.
- **Why not settled:** I did not read the three versions closely enough to know
  whether the branch supersedes or contradicts crispy `main`. Stated as a
  known gap rather than guessed at.

---

## B. Contradictions surfaced by the roadmap branch

### B1. The roadmap branch's tool-profile standardization is discarded by regeneration
- **What:** `vibe/implementation-roadmap-4105aff` standardized tool profiles
  across 18 agents by editing `.vibe/agents/*.toml`. Those files are **compiled
  output** of `agents/*.yaml`. Verified: running `meta/generate_all.py --all` on
  the branch reverts four of its own edits. The merge took `main`'s side and let
  the generator stay authoritative, so **the branch's intent is not preserved**.
  Its versions are at `contested/roadmap-branch/.vibe/agents/`.
- **From:** crispy `vibe/implementation-roadmap-4105aff` @ `1a31cfc`.
- **Why not settled:** porting the edits into `agents/*.yaml` would be deciding
  the branch was right about 18 agents' tool profiles, with no evidence and no
  invocation to check against. That is a resolution, and phase 2 does not
  resolve. **This is the single most likely thing in this pile to be silently
  lost** — it looks merged, because the commit is in history, but its effect is
  not in the tree.

### B2. Two `prompts/router.md`, neither ever run
- **What:** crispy `main`'s router prompt is live at `prompts/router.md`; the
  roadmap branch's different 214-line version is beside it at
  `prompts/router.roadmap-branch.md`.
- **From:** crispy `main` @ `4d2c23d` and `1a31cfc`.
- **Why not settled:** the integration plan records that the router has never
  been used. D1 and D2 are recorded against `main`'s version specifically; it is
  unknown whether they apply to the branch's version too.

### B3. The roadmap branch still carries the 2026-08-24 clobbering bug
- **What:** on a pristine clone of that branch, `meta/generate_all.py --all`
  reduces `skills/vibe-reference/SKILL.md` from 161 lines to a 28-line stub, by
  writing through the `.vibe/skills/vibe-reference` symlink. The branch is 13
  commits behind `main` and predates PR #10's guardrail.
- **From:** verified by running, 2026-09-02.
- **Why not settled:** the merged tree is not affected (the merge kept `main`'s
  guarded `meta/`, and the acceptance test confirms the canonical file survives
  at 161 lines). Recorded because **the branch itself is still live and still
  dangerous to check out and run**, and because it is evidence for how the
  original incident happened.

---

## C. Known defects, copied across unfixed

From [`verified-defects-2026-08-25.md`](verified-defects-2026-08-25.md), valid as
of crispy `4d2c23d`. **Copied unfixed on purpose**, per the integration plan's
"Decided — do not relitigate" table. Paths have moved in this merge, so several
need re-verifying before being acted on.

| ID | What | From | Why not settled |
|---|---|---|---|
| **D1** | `prompts/router.md` claims "all skills have Python implementations"; `find skills -name '*.py' \| wc -l` returned 0 | crispy `main` | Plan decided defects are fixed **after** the merge: the merge moves paths and changes counts, so fixing now means fixing twice. Also unclear whether it applies to B2's other router. |
| **D2** | Same file claims "17 subagents and 11 skills"; no reading of the repo produces either number, and its own inline table disagrees with its prose | crispy `main` | As D1. Counts re-verified unchanged at merge time (19/13/13/13) but are now wrong in a new way: the merged repo has 33 skills. |
| **D3** | Six `.vibe/` agents (`router`, `architect`, `implementer`, `reviewer`, `escalation-fixer`, `transcription`) exist outside the single source of truth and are not generated | crispy `main` | Structural; fixing it means authoring six canonical YAMLs. Re-verified unchanged. |
| **D4** | `skill-validator` and `repo-auditor` are ~25-line trigger-phrase stubs presenting as complete, listed `✅ Claude, Pi, Vibe` in the README and wired into the router's exact-match table | crispy `main` | Re-verified: 25 L and 26 L. Not fixable by merging — they need writing. This is the finding that makes phase 3 exercise rather than inventory. |
| **D5** | A drafted retirement-sweep script emitted plausible false findings (all 18 skills reported unused) | noteboook — **marked fixed** (deleted 2026-08-25) | Carried across with its resolved status intact, as evidence rather than a task. |
| **D6** | Unrun material placed in `docs/`, where location asserts "checked" | noteboook — **marked fixed** | As D5. Directly relevant to this merge: it is why `vibe/errors-2026-08-24`'s rejected audit went to `contested/` and not `docs/` (see E3). |
| **D7** | Banners added on top of content that still contradicted them | noteboook — **marked fixed** | As D5. |
| **D8** | A blind `sed` across `*.py` silently changed program behavior | noteboook — **marked fixed** | As D5. |

**Also from that file's "Not checked" section, still not checked:** whether the
router has ever been run; crispy's other nine skills at body level; and
**noteboook's own skills against the D4 standard** — "likely to find the same
thing; cheap to measure; not yet done." Now 33 skills, so the measurement is
larger than when that was written.

---

## D. Items from the `loose-ends/` reports

All nine reports are preserved in `loose-ends/`. Only genuinely unresolved items
are listed here; items already handled by a merge decision are not repeated.

### D1p. `docs/SKILL_DESIGN.md` is stale about its own tooling
- **What:** line 212 still reads "**Planned** (not yet implemented)" about the
  `meta/generate_*.py` generators, which exist and run — the one piece of
  infrastructure in this repo that is verified working.
- **From:** crispy, `loose-ends/fix-readme-remove-codeberg-and-stale-refs.md`.
  Re-verified present at `4d2c23d`.
- **Why not settled:** it is a defect of exactly the D1 class (a false claim an
  agent will act on), and the plan defers defect fixes to after the merge. Its
  author judged it out of scope for a codeberg-removal pass and flagged it
  nowhere else, so it has now been dropped twice.

### D2p. The symlink guardrail was never tested by firing it
- **What:** the `write_file()` guardrail that refuses writes through
  `.claude/skills/`, `.pi/skills/`, `.vibe/skills/` was verified by tracing the
  Python by hand, not by attempting a write and watching it raise. PR #10's
  "Verified clean" means the happy path.
- **From:** crispy, `loose-ends/fix-readme-remove-codeberg-and-stale-refs.md`.
- **Why not settled:** writing that test is authoring. Partially mitigated by
  this merge: `update_symlinks()`'s sibling guardrail **was** observed firing —
  it raised `RuntimeError` on the merged tree before the orphan skills were
  promoted (see F1). That is the same guardrail family, not the same code path.

### D3p. `skill-extractor` instructs agents to write into a symlink farm
- **What:** `skills/skill-extractor/SKILL.md:47` (crispy's copy) tells agents to
  save newly extracted skills to `~/.vibe/skills/` — the symlink-farm-write
  mistake in prose. A skill saved that way lands for Vibe only and never reaches
  the canonical library.
- **From:** noteboook, `loose-ends/claude-github-repo-access-5p6zbx.md`.
- **Why not settled:** it is in a **contested** file (A2). Fixing it would mean
  first choosing which `skill-extractor` wins.

### D4p. crispy's 41 symlinks have no cross-platform protection
- **What:** on a clone without `core.symlinks=true` (the Windows default), the
  symlinks check out as plain text files containing their target paths. No CI or
  pre-commit guard exists against this class of bug.
- **From:** noteboook, `loose-ends/claude-github-repo-access-5p6zbx.md`.
- **Why not settled:** crispy's `.gitattributes` came across in this merge, but
  whether it actually covers this was not checked, and noteboook previously had
  none. Adding CI is new infrastructure, not a merge action.

### D5p. Three "synced" skills are in neither repository
- **What:** `pilot-preset`, `karpathy-guidelines`, `solus-skill` live only in the
  owner's `~/.claude/skills/synced/`. Merge two sources or three is listed
  **Open** in the plan's own decision table.
- **From:** the integration plan; owner-held.
- **Why not settled:** they are not in either repo, so this merge cannot reach
  them. Requires the owner to decide and to supply them.

### D6p. An unreviewed third-party skill draft sits on a branch
- **What:** `skills/openai-gh-fix-ci/` — Apache-2.0 script and LICENSE copied
  verbatim from upstream, but with the "When to Use"/"When NOT to Use" sections
  written by a session and never reviewed, and **no** row in `skills/README.md`
  or `NOTICE.md` as this repo's third-party convention requires. Its own author
  says it "looks more finished than it is."
- **From:** noteboook, `loose-ends/claude-skills-notebook-evaluation-6gkh2f.md`.
  Left **untracked on disk** in that session, so it is not in git and **this
  merge did not bring it across.**
- **Why not settled:** it is not in any commit on any branch. If it is wanted, it
  has to be re-created from upstream, and the licensing question below settled
  first.

### D7p. CC-BY-SA licensing has no precedent in this repo
- **What:** three other candidate skills (`writing-great-skills`, `goal-prompt`,
  `code-improver`) are CC-BY-SA-4.0 at the repository level — share-alike, with
  no precedent in `skills/README.md`'s license column, which has only
  Apache-2.0/MIT.
- **From:** noteboook, `loose-ends/claude-skills-notebook-evaluation-6gkh2f.md`.
- **Why not settled:** a licensing decision, not a merge decision, and blocking
  on it would have blocked the merge.

### D8p. The foundation-harness classification framework exists only in a transcript
- **What:** a 5-axis framework for deciding whether a recurring need should be a
  prompt, script, skill, MCP connection, or subagent, cross-checked against
  published sources, was worked out in conversation and **never written into any
  file**. What was committed is the raw brain dump and a prompt template, not the
  framework.
- **From:** noteboook, `loose-ends/claude-repo-vision-clarify-u3pays.md`.
- **Why not settled:** it cannot be merged, because it does not exist as an
  artifact. Recovering it means going back to that transcript. Its author notes
  the committed files read as more decided than they are.

### D9p. `self-checks/2026-08-24/MERGER_PLAN.md` reads as in-progress but is not started
- **What:** an ordered four-PR plan (GAPS, STANDARDS, MAINTENANCE, COMPATIBILITY)
  where none of the four has been started; source files untouched in
  `mailroom/multi-agent-drop-823/`. Its confident tone reads as "in progress."
- **From:** noteboook, `loose-ends/claude-log-attribution-todo.md`.
- **Why not settled:** the D7-class problem (a document asserting a status it
  does not have). Fixing it is editing, deferred with the other defects.

### D10p. The skill-attribution TODO is a flagged concern, not a scoped task
- **What:** logged "Open" in `self-checks/2026-08-24/action-items.md` with zero
  scoping — not one skill's real origin was checked. Reads as a defined task.
- **From:** noteboook, `loose-ends/claude-log-attribution-todo.md`.
- **Why not settled:** scoping it means auditing 33 skills' provenance; the
  merge only establishes which **repo** each came from (`PROVENANCE.md`), not
  original authorship.

### D11p. Two branch deletions are pending and neither happened
- **What:** deletions attempted on noteboook's `vibe/errors-2026-08-24` and one
  on crispy; one blocked by a GitHub 403, one by a permission classifier. The
  report also warns these two failure modes look alike but only one is fixed by
  retrying.
- **From:** noteboook, `loose-ends/claude-log-attribution-todo.md`; crispy,
  `loose-ends/fix-readme-remove-codeberg-and-stale-refs.md`.
- **Why not settled:** **must not be settled yet.** The merge prompt's rollback
  section requires that no source branch be deleted until phase 3 has run, and
  `vibe/errors-2026-08-24` is one of the branches this merge drew from.

### D12p. A `git merge` reported clean while producing a semantically wrong result
- **What:** merging `vibe/errors-2026-08-24` auto-merged `AGENTS.md` with no
  conflict markers but stacked **both** guardrail additions — the one outcome the
  two authors had agreed against. Caught only by reading the merged file.
- **From:** noteboook, `loose-ends/claude-agent-external-comms-guardrails-gjrjl4.md`.
- **Why not settled:** not an open task — a **method warning that applies
  directly to this merge**, which performed 23 conflict resolutions. A clean exit
  code is not evidence of a correct merge. Kept as evidence for whoever reviews
  the PR.

### D13p. Reasoning behind two merged decisions exists only in chat
- **What:** (a) why Vibe's one-line `AGENTS.md` prohibition was folded into a
  fuller section rather than kept alongside; (b) why the "triple-confirmed"
  phrasing was deliberately dropped rather than softened. Both agreed in a
  relayed exchange; neither is reconstructible from any commit.
- **From:** noteboook, `loose-ends/claude-agent-external-comms-guardrails-gjrjl4.md`.
- **Why not settled:** the record is gone; only the owner can confirm it.
  Relevant to A6, since `AGENTS.md` is contested four ways.

### D14p. An incident record underpinning a merged guardrail was never independently verified
- **What:** `self-checks/2026-08-24/NEAR_INCIDENT_EXTERNAL_REPO_VIOLATION.md` is
  linked from `AGENTS.md` as "the full incident record." Its specifics (issue
  numbers #1038/#1039, Vibe v2.9.4) were never checked against
  `mistralai/mistral-vibe`. Separately, the 2026-08-24 SKILL.md-flattening
  incident that motivates the symlink guardrail was also taken as given.
- **From:** noteboook, `loose-ends/claude-agent-external-comms-guardrails-gjrjl4.md`;
  crispy, `loose-ends/fix-readme-remove-codeberg-and-stale-refs.md`.
- **Why not settled:** verifying needs access to an external repo that no session
  here has had. Note the guardrail's own code is checkable regardless of whether
  the origin story is exact — and B3 is independent evidence that the clobbering
  mechanism is real.
- **Note:** the second half of this is **partly answered by this merge**. B3
  reproduces the clobbering from a pristine clone, so the mechanism is no longer
  merely asserted.

### D15p. Two `.claude/skills/` and `.vibe/skills/` symlinks are undeclared test artifacts
- **What:** `time-estimate` symlinks in both farms were added to answer a one-off
  discovery question. Nothing in the tree marks them as tests; a later reader
  would read them as intentional structure.
- **From:** noteboook, `loose-ends/claude-vibe-symlink-skill-test-ubed41.md`.
- **Why not settled:** now moot in form — the farms are fully regenerated by
  `meta/generate_all.py`, so every skill including `time-estimate` has symlinks
  in every farm, and there is nothing special about these two. Recorded so the
  original intent is not lost. Likely a **drop**.

### D16p. Vibe's `.vibe/skills/` discovery was never verified from Vibe
- **What:** Claude Code follows a symlinked skill directory identically to a real
  one — tested and confirmed. The equivalent test for Mistral Vibe could not run:
  there is no `vibe` binary in the session container.
- **From:** noteboook, `loose-ends/claude-vibe-symlink-skill-test-ubed41.md`.
- **Why not settled:** needs a real Vibe session. This merge makes it more
  load-bearing, not less: all 33 skills are now reachable for Vibe only through
  that farm.

### D17p. The `search_replace` root-cause hypothesis is still unverified
- **What:** the claim that calling a nonexistent `search_replace` tool caused
  Vibe's "file not found" errors is stated more confidently in
  `scratchpad/VIBE_FOLLOWUP_ACTION_ITEMS.md`'s summary than its own
  "Inferred / uncertain" section supports. What Vibe actually returns for an
  unknown tool was never established — if it returns a clear error, the proposed
  "Bug A" evaporates. All URL citations in that file came from **search snippets,
  not fetched pages**, because the egress proxy blocked docs.mistral.ai and
  github.com.
- **From:** noteboook, `loose-ends/claude-validate-mistral-patches-ipuxh1.md`;
  file brought across by this merge.
- **Why not settled:** needs a Vibe session to run one tool call. Do not file
  anything upstream on this until it is checked.

### D18p. `AGENTS.md` had the right answer resident and the agent still called the wrong tool
- **What:** the tool-translation table (`Edit` → `edit`, no `search_replace`) was
  in `AGENTS.md`, which Vibe loads every turn. The session that produced the
  error commits had it in its system prompt throughout. So the failure mode is
  **not** missing documentation. Candidate causes — an overriding loaded skill, a
  model behavior issue, the v2.7.0 skills-not-loading bug — none investigated.
- **From:** noteboook, `loose-ends/claude-validate-mistral-patches-ipuxh1.md`.
- **Why not settled:** unanswered, and it bears directly on A6: if resident
  instructions were not followed, reconciling four `AGENTS.md` files may not fix
  what anyone expects it to.

### D19p. An open PR predates the merge and may be silently superseded
- **What:** noteboook PR #5, from `claude/repo-vision-clarify-u3pays`, unreviewed
  and unmerged. Its author flagged it "worth someone's attention during the repo
  merge so it doesn't get silently dropped."
- **From:** noteboook, `loose-ends/claude-repo-vision-clarify-u3pays.md`.
- **Why not settled:** its branch's `loose-ends/` report was collected, but
  whether its **content** is superseded by this merge was not assessed. Owner
  call.

---

## E. Items arising from this merge

### E1. Three skills were promoted out of the Claude-only farm — a judgment call
- **What:** `outside-perspective`, `outside-perspective-session` and
  `subagent-skill-patterns` were real directories inside `.claude/skills/` with
  **no copy in `skills/`**. They were promoted to canonical, so they are now
  symlinked into all three agent farms.
- **From:** noteboook `main`; discovered by this merge, documented nowhere.
- **Why not settled:** the promotion was **required** — without it
  `meta/generate_all.py` exits 1 on the merged tree, verified. It is
  content-preserving and reversible. But whether those three were *meant* to be
  Claude-only is a genuine open question, and I had no evidence either way.
  Approved by the owner at Gate 1 as the mechanical default, explicitly to be
  revisited in phase 3. Note this is the same structural defect as D3 (harness
  files without a canonical parent), on the other repo.

### E2. 23 of 33 skills have no canonical `agents/*.yaml`
- **What:** `agents/` holds 13 YAMLs, all from crispy. The 20 skills from
  noteboook, plus the 3 promoted in E1, get farm symlinks but **no per-agent
  wrappers** — so `.claude/agents/` and `.vibe/agents/` cover 13 of 33.
- **From:** this merge, by construction.
- **Why not settled:** writing 20 YAMLs is authoring content, not merging.
  Directly relevant to the "stay cross-agent" decision: the merged repo's
  cross-agent parity is now much thinner than its README-level story implies.

### E3. Content assessed as fabricated was preserved rather than dropped
- **What:** `vibe/errors-2026-08-24`'s
  `TOOL_VERSION_INCONSISTENCY_AUDIT.md` and two companions are at
  `contested/unmerged-branches/notebook-vibe-errors-2026-08-24/`.
  `loose-ends/claude-log-attribution-todo.md` assesses the audit as fabricated —
  increasing specificity with zero citations, and a runtime version that shifted
  three times (v2.7.0 → v2.9.4 → v2.24.3) with rising confidence each time — and
  records that it is rebutted in `self-checks/2026-08-24/`.
- **From:** noteboook `vibe/errors-2026-08-24`.
- **Why not settled:** two rules pulled against each other. Dropping it silently
  is what phase 2 forbids; putting it in `docs/` is D6 exactly, where placement
  asserts "checked." Compromise: preserved under `contested/`, out of `docs/`,
  with the rebuttal named here. **Anyone checking out that branch directly still
  finds the audit with no visible pointer to its rebuttal** — that part is
  unfixed.

### E4. Two unmerged branches carried real work that no document mentioned
- **What:** `claude/pi-agent-creation-skill-kts9a8` (a complete, indexed
  `agents-md-init` skill, 260 lines) and crispy
  `vibe/skill-invocation-analysis-3f722e`. Neither has a `loose-ends/` report;
  neither appears in the integration plan's appendix or the merge prompt's
  enumeration. Both are now in the merge.
- **From:** discovered by sweeping every branch of both repos.
- **Why not settled:** `agents-md-init` came across with its content but **its
  `skills/README.md` index row did not** — adding it means editing a file whose
  merged state is already contested (A7). More importantly: the enumeration in
  the merge prompt was **incomplete**, exactly as it warned it might be. If two
  branches were missed, the collection method — not the list — is what future
  work should trust.

### E5. The plan and this pile live inside the merge commit
- **What:** `notebooks/merge-plan-2026-09-02.md` and this file are part of the
  merge PR, so a Gate 2 revert would delete both.
- **From:** this merge.
- **Why not settled:** **mitigated, not unresolved.** The owner granted a
  record-only branch at Gate 1; both files are also pushed to
  `claude/skills-prompts-merge-uw810o-record`, which is not part of the PR and
  survives a revert of it.

### E6. One loose-ends finding was already stale and is recorded as closed
- **What:** `loose-ends/claude-github-repo-access-5p6zbx.md` reports a live
  `shutil.rmtree()` hazard in `update_symlinks()` "present, unpatched, on both
  `main` and `fix/generator-symlink-bug`." It is **fixed**: `grep -n rmtree
  meta/generate_all.py` on crispy `4d2c23d` returns nothing, and the code now
  raises `RuntimeError` instead. The report predates PR #10.
- **From:** noteboook; re-verified 2026-09-02.
- **Why not settled:** nothing to settle — recorded so a false open item is not
  carried forward, and as a reminder that the reports are dated snapshots.
  **Drop.**

---

## F. Verified during this merge — evidence, not tasks

Recorded because phase 3 needs to know what was actually run, as opposed to read.

- **F1.** The build step still works, re-confirmed 2026-09-02 on a pristine clone
  of crispy `4d2c23d`: `python3 meta/generate_all.py --all` → exit 0, then
  `git status --porcelain` → empty. The integration plan's strongest verified
  result still holds.
- **F2.** It also works on the **merged** tree, after E1's promotion: exit 0,
  idempotent on a second run, and `skills/vibe-reference/SKILL.md` intact at 161
  lines. The soft constraint from the merge prompt is preserved, by running it
  rather than by asserting it.
- **F3.** `update_symlinks()`'s guardrail was **observed firing** — it raised
  `RuntimeError` on the merged tree before E1's promotion. See D2p.
- **F4.** B3's clobbering was reproduced from a pristine clone, twice.
- **F5.** D2/D3's counts re-checked exactly as recorded: 19 `.vibe/agents/*.toml`,
  13 `.claude/agents/*.md`, 13 `agents/*.yaml`, 13 crispy `skills/`.
- **F6.** `skills/planning-with-files` is byte-identical between the repos
  (`diff -r`, no merge conflict). See A3.

**Still true, and it is the reason for phase 3:** nothing in the merged
repository has been invoked. This merge verified *infrastructure*, never a
skill. Every A-, C- and D-entry above remains unjudgeable until skills are run.
