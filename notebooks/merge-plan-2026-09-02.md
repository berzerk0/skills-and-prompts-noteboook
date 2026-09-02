# Merge plan — 2026-09-02

Step 3 output of [`prompt-execute-merge.md`](prompt-execute-merge.md). Phase 2 of
[`integration-plan-2026-08-25.md`](integration-plan-2026-08-25.md).

**Status: awaiting Gate 1 sign-off. Nothing has been pushed to either repository.**

Everything below marked "verified" was produced by running a command in this
session, from full (non-shallow) clones taken 2026-09-02, not by reading a prior
report. Where a prior report and my own run disagree, I say so.

---

## Pre-merge baseline

Recorded now, per Step 4a. This pair of SHAs is what "revert" means.

| Repository | `origin/main` at 2026-09-02 |
|---|---|
| `berzerk0/skills-and-prompts-noteboook` | `2fdbcae78d6e9b91130426bcb8d25094ef23c1d2` |
| `berzerk0/crispy-couscous` | `4d2c23d325c922486097e70d2043e207421b8200` |

`4d2c23d` is also the commit the defect log is stamped valid as of, so its
entries can be re-checked against the exact tree they were written against.

---

## What I verified before deciding (Step 2)

Full clones, no `--depth`. The integration plan's appendix warns that the
shallow-clone numbers in it were wrong; these are from full clones.

**Branch inventory, both repositories:**

| Repo | Branch | vs `main` | `loose-ends/` |
|---|---|---|---|
| notebook | `claude/agent-external-comms-guardrails-gjrjl4` | 1 ahead | yes |
| notebook | `claude/github-repo-access-5p6zbx` | 1 ahead | yes |
| notebook | `claude/log-attribution-todo` | 1 ahead | yes |
| notebook | `claude/repo-vision-clarify-u3pays` | 1 ahead | yes |
| notebook | `claude/skills-notebook-evaluation-6gkh2f` | 1 ahead | yes |
| notebook | `claude/validate-mistral-patches-ipuxh1` | 4 ahead | yes |
| notebook | `claude/vibe-symlink-skill-test-ubed41` | 1 ahead | yes |
| notebook | `notebook/foundation-harness-exercise` | 4 ahead | no |
| notebook | `claude/pi-agent-creation-skill-kts9a8` | 2 ahead | **no — see below** |
| notebook | `vibe/errors-2026-08-24` | 3 ahead | no (correctly; the prompt's correction holds) |
| notebook | `claude/merge-plan-rollback-gate`, `claude/outside-perspective-skills-9f2k1`, `claude/repo-vision-debate-r1-ya1c00`, `claude/version-reconciliation-review-jvzxfw` | merged | — |
| crispy | `vibe/implementation-roadmap-4105aff` | 1 ahead, 13 behind | no |
| crispy | `fix/readme-remove-codeberg-and-stale-refs` | 1 ahead (report only) | yes |
| crispy | `local-archaeology-2026-08-25` | 1 ahead (report only) | yes |
| crispy | `vibe/skill-invocation-analysis-3f722e` | 1 ahead | **no — see below** |
| crispy | `fix/generator-symlink-bug` | merged | — |

Nine `loose-ends/` reports found and read in full — seven on notebook, two on
crispy. That matches the prompt's enumeration exactly; the sweep
(`git ls-tree -r <branch> | grep loose-ends` over every branch) found no tenth.

**The appendix's crispy table still matches reality**, with one addition it does
not mention: `vibe/skill-invocation-analysis-3f722e`, one unmerged commit
rewriting three `scratchpad/` files (+444/−379).

**Two unmerged branches carrying real work that no `loose-ends/` report and no
prior document mentions.** Both would be lost silently:

- `claude/pi-agent-creation-skill-kts9a8` — adds `skills/agents-md-init/`
  (SKILL.md + `references/template.md`, 260 lines) and a `skills/README.md`
  index row. A complete, indexed skill.
- `vibe/skill-invocation-analysis-3f722e` — as above.

---

## The verified facts that drive the decisions

### F1. The build step still works — re-confirmed today, not inherited

The integration plan's strongest verified result was recorded 2026-08-25. Step 3
told me to re-run it rather than trust it. On a pristine clone of crispy
`main` @ `4d2c23d`:

```
$ python3 meta/generate_all.py --all   → exit 0
$ git status --porcelain               → (empty)
```

Still holds. Idempotent, nothing generated has been hand-edited.

### F2. A naive union of the two trees breaks it — verified by running

Both repositories have `.claude/skills/` symlink farms. Crispy's
`update_symlinks()` owns that directory and refuses to proceed if it finds a
real directory there (a guardrail added by PR #10). Notebook's farm contains
**three real skill directories and a README**, not just symlinks:

```
.claude/skills/outside-perspective          (real dir)
.claude/skills/outside-perspective-session  (real dir)
.claude/skills/subagent-skill-patterns      (real dir)
.claude/skills/README.md                    (real file)
.vibe/skills/README.md                      (real file)
```

Overlaying notebook onto crispy and running the generator:

```
RuntimeError: Refusing to delete real directory …/.claude/skills/outside-perspective
in symlink farm …/.claude/skills.   exit 1
```

**These three skills exist only in `.claude/skills/` and have no copy in
`skills/`.** They are Claude-only, outside the canonical library — which is the
same structural defect as D3, on the other repo, and nothing in either repo's
documentation says so.

**Remediation, verified to work:** promote the three to `skills/`, move the two
farm READMEs out of the farms (the generator deletes regular files it finds
there, with only a warning). After that, on the same union tree:

```
$ python3 meta/generate_all.py --all   → exit 0, "✓ All symlinks updated"
$ (run again) farm listing identical   → idempotent
33 canonical skills, 32 farm entries per agent
```

### F3. The roadmap branch destroys canonical content if regenerated as-is

Step 3 item 4 says to look at the branch's real commits, not the summary. I did,
and then ran it. From a **pristine clone of `vibe/implementation-roadmap-4105aff`**:

```
skills/vibe-reference/SKILL.md   before: 161 lines
$ python3 meta/generate_all.py --all
skills/vibe-reference/SKILL.md   after:   28 lines   ← canonical source destroyed
```

The branch is 13 commits behind `main` and predates PR #10's symlink guardrail,
so the generator writes straight through `.vibe/skills/vibe-reference` into the
canonical file. This is the 2026-08-24 incident, still live on that branch. On
pristine `main` the identical run leaves the file at 161 lines (F1).

**This does not mean the branch should be dropped — it means it must not be
merged in the other direction.** Verified fix: the branch does not touch `meta/`,
so merging it *into* a `main`-based branch keeps `main`'s guarded generator. Test
merge plus regeneration on the result:

```
skills/vibe-reference/SKILL.md   before: 161   after: 161   ✓ survives
```

The branch does **not** merge cleanly. 13 conflicts, verified:

- 12 × `.vibe/agents/*.toml`
- 1 × `prompts/router.md` (add/add)

### F4. The roadmap branch's tool-profile work is hand-edits to generated output

Running the generator **on the branch itself** reverts four of its own
`.vibe/agents/*.toml` changes. Those files are compiled from `agents/*.yaml`;
the branch edited the output, not the source. So merging the branch preserves
its commit and its two new docs, but **regeneration silently discards the
tool-profile standardization**. That is a contradiction between the branch and
the repo's own single-source-of-truth rule. Per the phase-2 rule I am recording
it, not resolving it — I am not porting the edits into `agents/*.yaml`, because
doing so would be me deciding the branch was right.

### F5. Skill collisions — my own sweep, not the plan's list

The plan named two known cases and told me to check for others with the same
method. Full recursive diff of `skills/` across both repos:

| Skill | notebook | crispy | verdict |
|---|---|---|---|
| `challenge-my-thinking` | 52 L | 26 L | **DIFFERENT** — contradiction |
| `skill-extractor` | 210 L | 54 L | **DIFFERENT** — and *four* files differ, not just SKILL.md (`references/quality-guide.md`, `skill-lifecycle.md`, `skill-template.md` too; the plan only mentions SKILL.md line counts) |
| `planning-with-files` | 63 L | 63 L | **byte-identical, whole directory** — a third collision the plan does not list, and *not* a contradiction |

Cross-name near-duplicates (a plain directory diff misses these):

- `ask-questions-if-underspecified` (85 L, notebook) vs `clarify` (45 L, crispy)
  — descriptions compete for the same trigger, as the plan predicted.
- `vibe-internals` (633 L, notebook) vs `vibe-reference` (161 L, crispy).

**A fourth contradiction, inside notebook itself:** `main` and
`notebook/foundation-harness-exercise` hold divergent versions of both
`outside-perspective` (80 L vs 133 L) and `outside-perspective-session`
(91 L vs 146 L).

### F6. One loose-ends finding is now stale; one is worse than reported

- **Stale.** `claude-github-repo-access-5p6zbx.md` reports a live
  `shutil.rmtree()` hazard in `update_symlinks()`, "present, unpatched, on both
  `main` and `fix/generator-symlink-bug`." `grep -n rmtree meta/generate_all.py`
  on current `main` returns nothing — PR #10 replaced it with the RuntimeError
  guardrail in F2. The report predates the fix. Recording it as *resolved*, with
  the evidence, rather than carrying a false open item onto the pile.
- **Worse than reported.** The same report flags a possible three-way `AGENTS.md`
  duplication in crispy. Verified: crispy has three, all different (276 / 71 / 49
  lines). Notebook has a fourth (220 lines). After the merge it is a **four-way**
  problem.
- **Still true.** `docs/SKILL_DESIGN.md:212` still says "**Planned** (not yet
  implemented)" about generators that exist and run. Confirmed at `4d2c23d`.
- **Still true.** D2/D3 counts re-checked exactly: 19 `.vibe/agents/*.toml`,
  13 `.claude/agents/*.md`, 13 `agents/*.yaml`, 13 `skills/`.

---

## The six decisions

### 1. Base repository — `skills-and-prompts-noteboook`, not a new repo

**Decision:** merge crispy-couscous *into* `skills-and-prompts-noteboook`.

Reasoning:

- The documents that govern this merge and score its result — the integration
  plan, `IDEAL.md`, the defect log, this prompt — already live in notebook, and
  phase 3 runs against them. Moving them makes every cross-reference in them
  wrong.
- Notebook is the larger library (19 canonical skills + 3 orphans, vs 13) and
  carries the governance surface (`AGENTS.md`, `CLAUDE.md`, read-only
  `mailroom/` and `archive/`) that is awkward to relocate.
- Crispy's build tooling is the thing worth protecting, and it is **portable** —
  F2 proves it runs correctly on the union tree. Choosing crispy as base to
  protect the tooling is not necessary, because the tooling survives the other
  direction.
- Against a **new repository**: it has the worst rollback story in this whole
  document. A bad merge into an existing base is one `git revert -m 1`. A bad
  new canonical repo can only be abandoned or archived, and the prompt itself
  flags deletion as the one step with no undo. No offsetting benefit.

**Direction of travel matters and is not symmetric** — see F3. Crispy content
comes to notebook; the roadmap branch merges into the merge branch, never the
reverse.

### 2. Skills in both repos with different content — rule applied, not chosen

No decision here; the integration plan already sets the rule and I am following
it: **keep both, record the conflict, resolve nothing.** Confirmation that I did:

- I ran my own detection rather than trusting the plan's list, and found a third
  collision it does not mention (`planning-with-files`, identical — so it is a
  duplicate, not a contradiction) and three extra differing files under
  `skill-extractor`. See F5.
- **I picked no winner** for `challenge-my-thinking` or `skill-extractor`.

Mechanically, one copy has to sit at `skills/<name>/` for the generator and for
skill discovery to work at all. That placement is a **mechanical default, not a
verdict**: the base repo's copy occupies the live path, and crispy's copy is
preserved verbatim at `contested/crispy-couscous/skills/<name>/`, with a
`contested/README.md` stating in plain terms that occupying the live path is not
evidence of being correct. Both entries go on the pile with that reasoning in
the "why not settled" field.

### 3. crispy-couscous's build tooling — kept, whole, at its existing paths

**Decision:** `meta/`, `agents/`, `.claude/`, `.vibe/`, `.pi/`, `.gitattributes`
all come across unchanged, at the same paths.

The soft constraint from Step 3 — generator still runs clean afterwards — **is
preserved, and I verified it rather than asserting it** (F2). Two structural
changes are required to preserve it, and both are content-preserving:

1. Promote notebook's three orphan skills (`outside-perspective`,
   `outside-perspective-session`, `subagent-skill-patterns`) from
   `.claude/skills/` into canonical `skills/`. Nothing is deleted; the farm entry
   becomes a generated symlink to the promoted copy.
2. Move `.claude/skills/README.md` → `docs/skills-farm-claude.md` and
   `.vibe/skills/README.md` → `docs/skills-farm-vibe.md`. The generator deletes
   regular files in the farms; leaving them there loses them.

**Acceptance test for Step 4a, run before the PR opens:**
`python3 meta/generate_all.py --all && git status --porcelain` must be empty.
If it is not, the PR does not open and I report why instead.

**Flagged as a judgment I made, not a discovery:** promoting the three orphans
is a change to notebook's structure that no document asked for. I judged it
required — without it the merged repo's only verified-working infrastructure
crashes on first run. It is content-preserving and reversible, but it is my call.
It also goes on the pile, because whether those three skills *should* be canonical
(rather than Claude-only by intent) is a real open question I have no evidence on.

**Known gap → pile:** `agents/*.yaml` covers only crispy's 13 skills. Notebook's
22 get farm symlinks but no per-agent wrappers, so they remain Claude/Vibe-only
in practice while the README-level story implies cross-agent parity. Recorded,
not fixed — writing 22 YAMLs is authoring content, not merging.

### 4. `vibe/implementation-roadmap-4105aff` — merged in, with its losses recorded

**Decision:** carry it across as a real `git merge` into the merge branch, so
commit `1a31cfc` and its authorship stay in history. Not cherry-picked, not
re-typed.

Conflict handling, per F3/F4 and the record-don't-resolve rule:

- **12 × `.vibe/agents/*.toml`** — take `main`'s side and regenerate. These are
  compiled output; the generator is authoritative for them. **This discards the
  branch's tool-profile standardization**, which is exactly why it goes on the
  pile as a contradiction (F4) rather than being quietly ported into
  `agents/*.yaml`. Porting it would be me deciding the branch was right about 18
  agents' tool profiles, with no evidence.
- **`prompts/router.md` (add/add)** — both versions kept. `main`'s stays at
  `prompts/router.md`; the branch's 214-line version is preserved alongside as
  `prompts/router.roadmap-branch.md`, with provenance. Pile entry: two router
  prompts, neither ever run, no basis for choosing. Note D1 and D2 are recorded
  against `main`'s version specifically.
- Kept outright: `docs/MODEL_SELECTION_STRATEGY.md` (230 L) and
  `docs/SUBAGENT_RETURN_CONVENTION.md` (357 L), both new, no conflict.

The other unmerged branches carrying content — `claude/pi-agent-creation-skill-kts9a8`,
`vibe/skill-invocation-analysis-3f722e`, `notebook/foundation-harness-exercise`,
`vibe/errors-2026-08-24`, `claude/validate-mistral-patches-ipuxh1`, and the seven
`loose-ends/` branches — are handled the same way where they carry content, and
otherwise recorded. **No source branch is deleted**, per the prompt's rollback
requirements.

### 5. Git history — preserved

**Decision:** `git merge --allow-unrelated-histories`. Both histories survive;
crispy's 100+ commits stay attributable.

Reasoning:

- The pile's "where it came from" field is only auditable if the history that
  proves it still exists. A fresh start makes every provenance line an
  unverifiable assertion — which is precisely the defect class D1–D7 catalogue.
- The rollback procedure in this prompt **requires** a real merge commit:
  `git revert -m 1` has nothing to operate on otherwise.
- It is effectively permanent, and preserving costs nothing now. Discarding is
  the irreversible half of the choice.

Provenance is *also* recorded in files (a `PROVENANCE.md` mapping every
top-level path to its source repo and branch), because the plan says post-merge
that information is not recoverable from the file tree — history makes it
recoverable, but only to someone who knows to look.

### 6. Pile location — `notebooks/pile.md`

One markdown file, per the plan. `notebooks/` is the repo's designated
"unresolved / not yet checked" end, which is exactly what the pile is, and the
plan's "one pile, not two" note points at that branch's material joining it
there.

**One unresolved tension, flagged rather than hidden.** The prompt says to keep
the plan and the pile "somewhere a revert doesn't erase," and I cannot fully
satisfy that: my instructions permit pushing to `claude/skills-prompts-merge-uw810o`
only, so both files live inside the merge PR and a Gate 2 revert would take them
with it. Mitigations: this plan is reported in full in chat, and I will report
the pile in full too. **If you want them genuinely revert-proof, give me
permission to push a second, record-only branch and I will put them there
instead** — that is a question for you, not something I will assume.

---

## What Step 4a will do, in order

1. Re-record both baseline SHAs (above) into this file. ✅ already done
2. Branch `claude/skills-prompts-merge-uw810o` in notebook from `origin/main`.
3. `git remote add crispy … && git fetch --no-tags crispy`
4. `git merge --allow-unrelated-histories crispy/main` — resolve tree-level
   collisions by preserving both sides per decisions 2 and 4.
5. Merge `crispy/vibe/implementation-roadmap-4105aff` — conflict handling per
   decision 4.
6. Bring across content from the unmerged branches listed in decision 4,
   including all nine `loose-ends/` files.
7. Structural fixes from decision 3 (promote three orphans, relocate two farm
   READMEs).
8. Regenerate, then **acceptance test**: `generate_all.py --all` + `git status`
   must be clean. Commit the regenerated output.
9. Write `notebooks/pile.md` and `PROVENANCE.md`.
10. Push the branch, open a PR against notebook `main`, **stop**.

Nothing in this list touches either default branch.

## What Step 4a will *not* do

- Fix any defect from `verified-defects-2026-08-25.md`. Copied across unfixed,
  including the ones whose files I read while working. D5/D6/D7/D8 are marked
  *(fixed)* in the source and are copied across with that status intact.
- Fix `docs/SKILL_DESIGN.md:212`, the four-way `AGENTS.md` duplication, the
  `skill-extractor` `~/.vibe/skills/` write instruction, or the missing
  `.gitattributes`-equivalent on notebook. All → pile.
- Choose between any two contested copies.
- Delete any branch, in either repository.

---

## Things I am not confident about

- **Promoting the three orphan skills** (decision 3) is the one change I make
  that no document asked for. I am confident it is *required* — the crash is
  reproducible — and confident it loses no content. I am not confident it
  matches intent, so it is on the pile as a question.
- **`vibe/skill-invocation-analysis-3f722e`** rewrites three `scratchpad/`
  files. Both repos have a `scratchpad/`, so this is a collision I will handle
  under decision 2's rule, but I have not yet read the file contents closely
  enough to know whether the rewrite supersedes or contradicts what is on
  crispy `main`.
- **The pile's revert-exposure** (decision 6). Flagged above; needs your answer.
