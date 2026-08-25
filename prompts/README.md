# Prompts

Reusable prompts -- not one-off transcripts. Each entry here should be
something you'd actually paste into a fresh session again, not a record of
a single conversation.

## Format

- One file per prompt, named for what it does, not when it was written.
- State the target surface (which tool/model/sandbox it's meant to run
  against) and when to re-run it, if that applies.
- If the prompt is meant to run against a weaker or less capable model, keep
  it flat and explicit: numbered steps, explicit output format, stated
  evidence standard. Don't convert a prompt like that into prose -- that
  shape is deliberate, following the convention established in
  [`berzerk0/cl-repo`](https://github.com/berzerk0/cl-repo)'s `prompts/`.

## Index

| Prompt | Target | Re-run when |
| --- | --- | --- |
| [`second-opinion-on-design-braindump.md`](second-opinion-on-design-braindump.md) | any external model/session | you have a raw, unedited design brain dump you want stress-tested before folding it into decisions |
