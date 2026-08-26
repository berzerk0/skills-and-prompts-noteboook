# [Role Name] Agent

[One-sentence mission -- what this subagent exists to produce.]

## Role

[One paragraph: the mission, and which judgment calls belong to this role
specifically -- what it decides on its own vs what it must not decide.]

## Inputs

You receive these parameters in your prompt:

- **[param_name]**: [what it is, and its type -- string, path, list]
- **[param_name]**: [...]

## Process

### Step 1: [Action]

[What to do, in enough detail that a subagent with no other context can
follow it without guessing.]

### Step 2: [Action]

[...]

## Output Format

[If a later step consumes this mechanically, give the exact JSON shape with
a field-descriptions section below it -- see
skills/skill-creator/agents/grader.md for a worked example. If this is the
final human-facing answer instead, say so explicitly and give the required
prose structure instead of JSON.]

```json
{
  "field": "...",
}
```

### Field Descriptions

- **field**: [what it means, valid values/range]

## Guidelines

- [Do: the specific behavior this role must get right]
- [Don't: the specific trap this role tends to fall into]
