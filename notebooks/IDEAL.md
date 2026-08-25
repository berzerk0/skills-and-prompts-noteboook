# The ideal

The north star for the foundation harness. Not a plan, not a spec, not a commitment —
the thing to measure against and come back to.

**Source:** [`foundation-harness-vision-2026-08-25.md`](foundation-harness-vision-2026-08-25.md)
(the unedited dump), filtered through the committee exercise and the 2026-08-25
verification pass recorded in
[`wants-and-priorities-2026-08-25.md`](wants-and-priorities-2026-08-25.md).

**Each principle below has an observable and a falsifier.** That is deliberate. The
ideal has to be scoreable by *running* the harness, because a file listing cannot
distinguish a working skill from a trigger-phrase stub — a mistake made twice while
writing these documents.

---

## 0. The harness is exercised, not just assembled

Every component has been run at least once and its output looked at.

- **Observable:** for each skill, agent, and script, a record that it was invoked and
  what came back.
- **Falsifier:** a component that has never been run, or has been run only by the
  person who wrote it, in the session that wrote it.

*This is principle zero because it is the one currently least satisfied, and because
every other principle below is unscoreable without it.*

---

## 1. Decide the shape of the work before doing the work

Given an ask, the harness determines what it will produce — nothing, a direct answer,
a script, a new skill, a subagent, an external connection — before it starts
producing.

- **Observable:** the shape is stated up front and the work matches it.
- **Falsifier:** the shape emerges implicitly from what got built, or is decided
  after the work is underway.

*This is the first line of the brain dump. Nothing in either repo does the general
version: the router dispatches among capabilities that already exist, and `script-it`
decides one narrow case (script vs. no script) well.*

---

## 2. "Nothing" is a first-class answer

The most frequent correct response to "what does this task need" is *nothing — answer
and stop*.

- **Observable:** some non-trivial share of asks resolve with no artifact created and
  no delegation. Countable as a rate.
- **Falsifier:** every routed ask produces an artifact or a subagent call.

*A decision procedure whose output space contains only expansions will always expand.
The taxonomy generates the debt. This came from one model with a support count of
one — weigh it on merit, not backing.*

---

## 3. Artifacts have declared homes

For every artifact type there is one documented destination, decided once.

- **Observable:** a new logfile, script output, plan, or brief lands in the documented
  place without anyone deciding where.
- **Falsifier:** the destination is chosen per artifact, or two artifacts of the same
  kind live in different places.

*"Where does that logfile go?" appears twice in the dump, both times as a question.*

---

## 4. Evidence beats documentation — including your own documentation

Where a document and the system disagree, the system wins and the discrepancy gets
surfaced rather than silently followed.

- **Observable:** stale or wrong claims in AGENTS.md, README tables, and system
  prompts are caught and corrected.
- **Falsifier:** an agent acts on a documented claim that is not true of the system.

*Already violated, verifiably: `crispy-couscous/prompts/router.md` tells the router
"All skills have Python implementations. Use `bash` to execute them" — there are zero
`.py` files across all 13 skills. This is the highest-severity known defect, because
it is a false premise handed to an agent by the repo rather than invented by the
model.*

---

## 5. Triggers are countable, not felt

Every always-on behavior fires on a number or an event.

- **Observable:** each behavior names a count, a threshold, or a named event.
- **Falsifier:** a trigger that reads "when it seems like" or "when appropriate."

*`script-it` (5+ items) and the 3-strike protocol in `planning-with-files` meet this
bar. "Knows when to sound the alarm," as written in the dump, does not.*

---

## 6. Retrieval is separate from judgment

Steps that gather and format do not also decide.

- **Observable:** reporting and escalation steps produce evidence without
  editorializing, and say what they deliberately do not do.
- **Falsifier:** the gathering step also renders a verdict, summarizes an attempted
  solution, or tidies up to look competent.

*`escalate` is the existing model for this and the best-designed thing in either
repo: "Deliberately does NOT: count attempts, decide if escalation is warranted,
attempt solution summary, clean up to look competent."*

---

## 7. Portability is a compilation problem

One canonical source per artifact; harness-specific files are generated from it.

- **Observable:** every `.claude/`, `.vibe/`, `.pi/` file has a canonical parent, and
  regenerating produces no diff.
- **Falsifier:** a harness-specific file with no parent, or one that has been
  hand-edited since generation.

*Committee voted 7-1 for this and the working compiler agrees. Currently violated by
six orchestration agents — `router`, `architect`, `implementer`, `reviewer`,
`escalation-fixer`, `transcription` — which exist only under `.vibe/`. The component
implementing principle 1 is the least portable thing in the repo.*

---

## 8. Dead artifacts are found and removed

Two-stage loading means every description is resident every turn. Unused skills are a
standing tax and a standing source of misrouting.

- **Observable:** something reports artifacts with zero invocations over a window.
- **Falsifier:** nothing in the system knows what has been used.

---

## 9. Best effort, because models predict tokens

The dump's closing line and the right frame for all of the above. Not scoreable; kept
because it sets the expectation the other nine are held to.

---

## Deliberately not in the ideal

Kept here so they don't creep back in. Each was either withdrawn by the models that
proposed it once n=1 was stated, or rejected on a mechanism the verification
confirmed.

- **Automatic self-improvement from logs.** The event record is ground truth; a lesson
  drawn from it automatically has no verifier. `escalate`'s return leg — a dated
  lesson appended to `napkin.md` by hand — is the version that survives.
- **Governance apparatus.** Quarantine periods, artifact owners, provenance chains,
  two-level supervisors. Git log is the audit trail and you are the verifier.
- **Multiple write-capable agents on one work product.** Parallel read-only fan-out
  returning condensed context to a single writer is fine. The other thing is where
  the interdependency failures live.
- **Principle-level prose as the portability mechanism.** Lost 7-1; the compiler is
  the answer. Principles keep the semantic layer only.
- **Self-authored skill prose.** Scripts are fine — they execute and fail loudly.
  Prose has no verifier until principle 8 produces invocation counts.

---

## How to use this in phase 3

Phase 3 asks "where is the merged repo against this ideal." Two ways to answer it,
and only one of them is worth anything:

- **By inventory** — does something exist for each principle? Fast, and misleading.
  Two of the four crispy-couscous skills read closely on 2026-08-25 were
  trigger-phrase shims that a directory listing and a README table both presented as
  complete.
- **By exercise** — run it and look at what comes back. Slower, and the only thing
  that distinguishes a working component from a named one.

Principle 0 exists because phase 3 needs the second kind. Suggested minimum: invoke
every skill once, on a real ask, and record what came back. A skill that cannot be
invoked, or that returns only its own description, is a stub regardless of what the
table says.

**Before adding the third-party skills on deck:** they will be indistinguishable from
your own by inventory, they add description residency from the moment they land, and
you will have no way to tell whether they work. Principle 0 first, then import.
