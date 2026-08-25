# Second opinion on a design brain dump

**Target surface:** any external model/session (paste into a fresh chat --
the whole point is getting a read from outside your own context).

**Re-run when:** you've got a raw, unedited brain dump about harness/system
design -- not a finished spec -- and want it stress-tested before folding
it into actual decisions. Use this instead of asking the other model to
tidy the dump up for you; that would just give you a cleaned-up mirror of
your own thinking instead of an independent read.

## Template

Fill in the two bracketed lines, then paste your brain dump verbatim below
the `<brain dump>` tag. Don't edit, organize, or prioritize the dump before
sending it -- that's the point of the exercise.

```
<ask and task>
I'm designing [ONE-SENTENCE DESCRIPTION OF THE SYSTEM/PROJECT]. Below is an
unedited brain dump of [WHAT PART OF THE VISION THIS COVERS]. This is not a
finished spec -- treat it as raw material to stress-test, not a plan to
implement.

Do three things: (1) Tell me which pieces are realistic to build today vs.
which are aspirational/unsolved problems in this domain generally (cite
sources where you can -- I want to know what's already been figured out
elsewhere vs. what I'd be inventing from scratch). (2) Challenge my
thinking directly -- where am I fooling myself, missing a failure mode, or
asking for something that sounds coherent but doesn't actually cash out
into a buildable behavior? (3) Don't try to organize or prioritize the
dump for me -- I want your independent read on it, not a cleaned-up
restatement.
</ask and task>

<brain dump>
[PASTE VERBATIM]
</brain dump>
```

## Worked example

This is the exact prompt used against the "foundation harness" brain dump
from the `repo-vision-clarify` session (2026-08-25), preserved as-is:

```
<ask and task> I'm designing a 'foundation harness' — a reusable substrate of always-on behaviors and a classification framework (prompt vs. script vs. skill vs. subagent vs. MCP connection) meant to underlie any AI coding harness I build, not a specific project. Below is an unedited brain dump of one part of that vision: the harness recognizing when it needs to expand itself and behave responsibly while doing so. This is not a finished spec — treat it as raw material to stress-test, not a plan to implement.
Do three things: (1) Tell me which pieces are realistic to build today vs. which are aspirational/unsolved problems in agent design generally (cite sources where you can — I want to know what's already been figured out elsewhere vs. what I'd be inventing from scratch). (2) Challenge my thinking directly — where am I fooling myself, missing a failure mode, or asking for something that sounds coherent but doesn't actually cash out into a buildable behavior? (3) Don't try to organize or prioritize the dump for me — I want your independent read on it, not a cleaned-up restatement. </ask and task>

<brain dump>
Scalability: the harness knows how to safely expand the harness

When i give it an instruction, it should be able to tell if it needs to expand in its own workspace. Is the pilot's ask going to require a logfile? Is it going to require a multi-step plan? Is it going to require a new skill? A new agent? A new prompt template? A new script? An mcp? RAG?

It should have agents ready and know when to use them. If it doesn't, it should ask the user if it should make them

It should know how those subagents best communicate with each other and if the subagents themselves need to make a logfile or what. Where does that logfile go?

It recognizes when to make a script. It knows how to do that well. it knows where that script's output should go.

All of these decisions are based on either good research or the user's previous written down instructions. 

It knows the principles of being efficient. It knows what tool calls to make and in what order. It knows when to be verbose and when to be direct.

It leaves logs for itself on how it did, and can improve itself as a result. X failed due to an interpretation of Y, next time i'll try z. 

it can tell when the user needs assistance clarifying their ask, and what strategies it takes to extract that information.

it can attempt critical thinking and isn't a gutless sycophant - without being obstinate or dishonest. It knows that sometimes the user has blind spots - but also it can have blind spots.  It knows when to use paragraphs and when to use bullet points. 
If it decides its time to make a skill, it knows how to make a skill. If it it's time to make a prompt, maybe one for a subagent or maybe one for another session, it knows how to make a prompt. If its time to make an agent, it has solid fundamentals of all of these artifacts

it knows basic principles for the models it uses and that they don't behave the same.

It uses well-researched industry best practices or standards. It knows how to act when there is a conflict between what it reads about what is "supposed to be" vs what it actually has evidence for

It knows when to sound the alarm if something breaks or has more trouble than it should

It knows how to talk to other models. It know how to pass messages back and forth.

It knows how to use tools. It knows when to use git, and how. It knows when to call scripts within its workspace and how to write them efficiently. It knows syntax. It knows not to "rm -rf" or "drop tables"

It knows syntax for different shells, and can detect when to use them.

It has access to a wealth of knowledge, but doesn't try to load it all at once. It knows when/if it can connect to another source of information or another tool (mcp server?)

It knows how to act in a self-recoverable way. If a session is interrupted or somehow hard fails, there is enough breadcrumbs for a session with 0 context to pick it back up.

It knows when contradictions between principles exist and how to balance them.

It is flexible between agents because it is based on principles more than specifics.

It knows that sometimes you can't have it all. It is possible to ask a single prompt or session to do too much.

It is solid enough in its design to expect reasonable performance even from weak models.

All of these are best efforts, because models aren't magic. They just predict tokens. </brain dump>
```
