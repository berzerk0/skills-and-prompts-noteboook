# Loose ends -- claude/repo-vision-clarify-u3pays

Repository: skills-and-prompts-noteboook
Branch: claude/repo-vision-clarify-u3pays
HEAD at time of writing: 404a37b5a0a74ad37100c278d98d2f89de6156b2
Working tree: clean, nothing uncommitted
Recent commits (mine, this session): 404a37b (move brain dump to notebooks/),
b8182eb (add second-opinion-on-design-braindump prompt)

This branch has an open, unmerged PR: #5
(https://github.com/berzerk0/skills-and-prompts-noteboook/pull/5). It has not
been reviewed or merged as of this writing. Worth someone's attention during
the repo merge so it doesn't get silently dropped.

## What did I decide that never got written down?

The session was a long Socratic back-and-forth with the user (not code work)
about what this repo's purpose should be -- a "foundation harness": a
reusable substrate of always-on behaviors plus a classification framework
for deciding whether a recurring need should become a prompt, a script, a
skill, an MCP connection, or a subagent. Over the conversation I synthesized
a concrete 5-axis version of that classification framework (roughly: would
you type this more than once? is it fully deterministic? does it need live
external access? does it need an isolated context/parallel execution? else
it's a skill) and cross-checked it against published sources (Anthropic's
"Building Effective Agents," "Skills explained," and HumanLayer's
12-Factor Agents). That framework, and the specific reasoning for it, only
exists in the chat transcript -- it was never written into the repo. What
got committed is the raw brain dump and a reusable prompt template for
getting outside opinions on future brain dumps, not the framework itself.
If the framework matters going forward, it needs to be pulled out of this
conversation and written down deliberately; it isn't sitting in any file
right now.

## What did I start and abandon?

Nothing was abandoned mid-work, but the underlying vision this branch
serves is explicitly unfinished by design -- the user was still actively
working out and writing down their own version of the vision outside this
session when we stopped. Don't read the two committed files
(`prompts/second-opinion-on-design-braindump.md`,
`notebooks/foundation-harness-vision-2026-08-25.md`) as a settled decision
about what the repo's foundation-harness content should be. They're a
snapshot of one brain dump and a tool for processing future ones, not the
harness design itself.

## What did I learn that is not in any file?

WebFetch to anthropic.com, claude.com, and github.com is blocked by this
environment's network egress proxy (`EGRESS_BLOCKED`). WebSearch still
works and returns usable snippets, but full-page fetches from those three
domains fail outright. Anyone doing source-grounded research in this kind
of session should expect to work from search snippets, not fetched pages,
for those domains specifically.

## What did I do that a later reader would misread?

The classification framework and the "always-present" artifact list
(timestamp -> script, skill-creator -> skill, planning-with-files -> skill,
challenge-thinking -> gated skill, a claim-verifying subagent, etc.) that I
worked out in conversation with the user was explicitly provisional --
offered as a draft for the user to react to and correct, not a conclusion
either of us had actually validated end-to-end against their real
experience. The committed notebook file preserves the raw brain dump
faithfully, but doesn't carry that "this was draft, not settled" framing
forward. A later reader skimming just the committed files could mistake
the direction as more decided than it actually was at the point this
session ended.
