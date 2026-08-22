---
name: script-it
description: When the same operation applies to 5+ items, or must be repeated to verify it worked, write one throwaway script and run it instead of repeating tool calls. When items need per-item judgment, script the mechanical part and judge the collected output in one pass.
license: MIT
compatibility: [claude, pi, vibe]
---

## When to script

- Same mechanical operation across 5 or more items
- The operation must be repeated to verify it worked
- A before/after comparison is needed
- Partial completion would be hard to spot by eye

## When not to script

- Genuinely one-off work
- Exploration where the shape of the data is still unknown
- Cases where writing it plainly costs more than doing it by hand

## The mechanical/judgment split

Per-item judgment is not a reason to skip scripting. Script the mechanical half — find, extract, collect into one place — then judge the whole set in a single pass. One tool result instead of many, and the judgment happens with everything visible at once instead of item by item.

## How to write it

- **Dry run first** on anything destructive: print what would change before changing it. The first run of a destructive script is never the real one.
- **Print a verifiable summary**: N found, N changed, N skipped, N failed. Without it the script is an opaque black box and the auditability benefit is lost.
- **Throwaway**: one self-contained file, PEP 723 inline metadata, run via `uv run`. No framework, no packaging, no error handling beyond what the task needs.
- **Disposable instrumentation, not shipped code.** Do not apply production standards. Do not commit unless asked. Delete when done.
- For PEP 723 detail, see the `modern-python` skill.
