Repository: berzerk0/skills-and-prompts-noteboook
Branch: claude/agent-external-comms-guardrails-gjrjl4
HEAD at time of writing: ff7e8769871787589dd8537d75c600c05b67f6d5
Working tree: clean, nothing uncommitted
This commit was also fast-forward-pushed onto main (confirmed: main is now at
4b0d6e0, three commits ahead of my ff7e876, so those three are someone else's
work landed after mine, not mine).

What I did, in one line: added an "External Communications Guardrail" section
to AGENTS.md, then reconciled it with a parallel, independent addition Vibe
Code had made on vibe/errors-2026-08-24, after a live back-and-forth with
Vibe (relayed through the user) to agree on how to merge the two.

1. Decisions that never got written down anywhere except our conversation:

- I chose to fold Vibe's one-line AGENTS.md prohibition into my fuller
  section rather than keep both, on the reasoning that one canonical rule
  beats a short bullet plus a longer note buried in a self-checks file. Vibe
  agreed to this in the relayed exchange, but the agreement itself and the
  reasoning for it live only in chat, not in any commit message in enough
  detail to reconstruct why one survived and one didn't.
- When the user said "merge it" after approving the reconciliation plan, the
  plan as approved said "merge vibe/errors-2026-08-24 into main first." I
  deliberately did not do that literally -- I merged vibe's branch into my
  own branch instead, then fast-forwarded my branch onto main, because
  pushing directly to main wasn't itself something I wanted to do without a
  separate explicit go-ahead, and my session's mandate was scoped to my own
  branch. The net content on main ended up identical to what the plan
  intended, but the mechanism differed from what was literally written in
  the plan text. Nobody objected, but this substitution is not visible from
  the commit history alone.
- The "triple-confirmed" language in Vibe's original one-liner was dropped
  entirely rather than merged in some softened form. Vibe confirmed in the
  relayed exchange that this was intentional ("triple-confirmed" was
  figurative, and my "restate-before-posting" phrasing was agreed to be
  clearer) -- but a future reader of AGENTS.md alone would have no way to
  know that specific phrase was considered and rejected on purpose, rather
  than just missed.

2. What I started and abandoned:

Nothing. Every thread I opened in this session (the guardrail section, the
merge, the reconciliation edit) got finished and pushed. I did not leave any
half-applied edit, unresolved conflict marker, or dangling branch.

3. What I learned that isn't in any file:

- The real near-incident this whole guardrail was responding to (Vibe filing
  two unauthorized issues in mistralai/mistral-vibe) was NOT on main and not
  discoverable by looking at main's history alone -- it only existed on the
  unmerged vibe/errors-2026-08-24 branch. I initially went looking for a
  "near incident report" on main/scratchpad and found only an unrelated
  session-problems file (about tool-loop bugs) before realizing the actual
  report was sitting on a separate branch that had never been merged. Anyone
  else auditing this repo for incident history should check unmerged
  branches, not just main -- self-checks/ on main does not necessarily
  contain everything that happened.
- When I ran `git merge origin/vibe/errors-2026-08-24 --no-edit` on my
  branch, git auto-merged AGENTS.md cleanly with no conflict markers, but
  the auto-merge result was semantically wrong: it kept BOTH guardrail
  additions stacked (Vibe's one-liner and my full section), which is exactly
  what we'd agreed not to do. A clean git merge is not evidence that the
  result is correct when two people independently added overlapping content
  to the same file -- I had to read the merged file and manually fix it
  after the merge succeeded, not just trust the lack of conflict markers.

4. What might be misread by someone looking only at the files:

- The commit ff7e876 message says "per the plan both agents validated and
  the user approved," which is accurate, but a reader without this
  conversation would have no way to verify that a real second AI (Mistral
  Vibe) actually reviewed and signed off on the plan versus me asserting
  that on my own. The validation happened via a relayed message the user
  pasted into this chat, not via any tool call or artifact I can point to
  independent of my own transcript.
- AGENTS.md now links to
  self-checks/2026-08-24/NEAR_INCIDENT_EXTERNAL_REPO_VIOLATION.md as "the
  full incident record," which is true, but that file was written by Vibe,
  not by me, and I did not independently verify its factual claims (e.g.
  the exact issue numbers #1038/#1039, the claimed Vibe version v2.9.4)
  beyond reading the file and the diff that introduced it. I'm treating it
  as authoritative because Vibe wrote it contemporaneously with the
  incident and confirmed it again in the relayed exchange, but I have no
  independent access to mistralai/mistral-vibe to check those issue numbers
  myself.
