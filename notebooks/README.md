# Notebooks

Informal, exploratory, allowed to be wrong or unfinished. This is the
scratchpad end of the repo -- the opposite of [`docs/`](../docs/), which is
reference material and checked claims.

One file per topic or session is fine; loosely dated if that's useful, but
don't force a rigid structure on something meant to stay low-friction to
add to. If a notebook entry turns out to hold up, promote it into `docs/`
explicitly rather than quietly treating it as authoritative in place.

## Foundation harness exercise (2026-08-24 / 25)

A wants-elicitation exercise: an unedited brain dump, an 8-model committee run over
two rounds, and a verification pass against `berzerk0/crispy-couscous`. **Inert by
design — none of it is a plan, and nothing here is wired into any workflow.** It
lives on the `notebook/foundation-harness-exercise` branch and is deliberately not
merged. (Two things here *were* executed: a draft tool-name validator, and
crispy-couscous's compiler. Both are reported in the defect log with their commands.)

**One file here is not inert:**
[`integration-plan-2026-08-25.md`](integration-plan-2026-08-25.md) is an active
work plan for merging the two repos and is meant to be acted on. Everything else
below is record.

Reading order:

0. [`integration-plan-2026-08-25.md`](integration-plan-2026-08-25.md) — the active
   plan. Three phases: document the ideal (done), merge, assess by running.
1. [`IDEAL.md`](IDEAL.md) — the north star. Ten principles, each with an observable
   and a falsifier so it can be scored by running the harness rather than by listing
   files. **Start here.**
2. [`verified-defects-2026-08-25.md`](verified-defects-2026-08-25.md) — eight
   defects that were actually reproduced, each with the command. Four are in
   crispy-couscous and still open; four were introduced while writing this branch and
   are fixed. Carry the open ones into any merge.
3. [`wants-and-priorities-2026-08-25.md`](wants-and-priorities-2026-08-25.md) — what
   the dump was really asking for, and which parts already exist.
4. [`foundation-harness-vision-2026-08-25.md`](foundation-harness-vision-2026-08-25.md)
   — the original dump. The source.

Lower confidence, kept as a record rather than as guidance:
[`DEBATE-SUMMARY.md`](DEBATE-SUMMARY.md),
[`foundation-harness-behavior-spec-2026-08-25.md`](foundation-harness-behavior-spec-2026-08-25.md),
[`behaviors/`](behaviors/), and
[`VISION-ASSESSMENT.md`](VISION-ASSESSMENT.md) — the last of which is superseded and
retained only to show where the reasoning went wrong.
