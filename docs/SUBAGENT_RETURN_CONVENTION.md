# Subagent Return Convention

**Repository:** crispy-couscous  
**Standard:** JSON Schema + LangChain Pattern  
**Status:** DRAFT  
**Version:** 1.0.0

---

## Overview

This document defines the **standardized JSON return format** for subagents in crispy-couscous. This convention ensures:

- ✅ **Parseable results** - Parent agents and scripts can reliably extract data
- ✅ **Type safety** - JSON Schema validation catches format errors early
- ✅ **Composability** - Subagents can chain outputs to other subagents
- ✅ **Tool compatibility** - Works with JSON Schema validators, Pydantic, Zod
- ✅ **Framework agnostic** - Compatible with LangChain, Claude Code, and other agent frameworks

---

## JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://github.com/berzerk0/crispy-couscous/schemas/subagent-return-v1.json",
  "title": "Subagent Return",
  "description": "Standard return format for subagents in crispy-couscous",
  "type": "object",
  "required": ["status", "task"],
  "properties": {
    "status": {
      "type": "string",
      "enum": ["success", "error", "partial", "needs_input"],
      "description": "Overall status of the task execution"
    },
    "task": {
      "type": "string",
      "description": "The task that was performed"
    },
    "summary": {
      "type": "string",
      "description": "Human-readable summary of results"
    },
    "results": {
      "type": "object",
      "description": "Task-specific data. Structure varies by task type.",
      "additionalProperties": true
    },
    "artifacts": {
      "type": "array",
      "description": "Files created during task execution",
      "items": {
        "type": "object",
        "required": ["path", "type"],
        "properties": {
          "path": {
            "type": "string",
            "description": "Absolute or relative path to the artifact",
            "examples": ["/scratchpad/audit-report.md", "./findings.json"]
          },
          "type": {
            "type": "string",
            "enum": ["markdown", "json", "text", "csv", "yaml", "html", "other"],
            "description": "File format/type"
          },
          "description": {
            "type": "string",
            "description": "What this artifact contains"
          }
        }
      }
    },
    "warnings": {
      "type": "array",
      "description": "Non-blocking issues found during execution",
      "items": {
        "type": "string"
      }
    },
    "errors": {
      "type": "array",
      "description": "Blocking issues that prevented full completion",
      "items": {
        "type": "string"
      }
    },
    "stats": {
      "type": "object",
      "description": "Execution statistics",
      "properties": {
        "turns_used": {
          "type": "integer",
          "minimum": 0,
          "description": "Number of LLM turns used"
        },
        "tokens_input": {
          "type": "integer",
          "minimum": 0,
          "description": "Input tokens consumed"
        },
        "tokens_output": {
          "type": "integer",
          "minimum": 0,
          "description": "Output tokens generated"
        },
        "duration_ms": {
          "type": "integer",
          "minimum": 0,
          "description": "Execution duration in milliseconds"
        }
      }
    },
    "next_steps": {
      "type": "array",
      "description": "Suggested follow-up actions",
      "items": {
        "type": "string"
      }
    },
    "metadata": {
      "type": "object",
      "description": "Additional context metadata",
      "properties": {
        "subagent": {
          "type": "string",
          "description": "Name of the subagent that produced this result"
        },
        "timestamp": {
          "type": "string",
          "format": "date-time",
          "description": "When the task was completed"
        },
        "version": {
          "type": "string",
          "description": "Schema version used"
        }
      }
    }
  },
  "additionalProperties": false
}
```

---

## Status Values

| Status | Meaning | When to Use |
|--------|---------|-------------|
| `success` | Task completed fully without issues | All objectives met |
| `error` | Task failed to complete | Blocking errors occurred |
| `partial` | Task completed with limitations | Some objectives met, some not |
| `needs_input` | Task cannot proceed without more info | User clarification required |

---

## Example Returns

### Example 1: repo-auditor (success)

```json
{
  "status": "success",
  "task": "repository_audit",
  "summary": "Audit of crispy-couscous completed. 3 findings identified.",
  "results": {
    "skill_count": 11,
    "agent_count": 17,
    "symlink_count": 13,
    "findings": [
      {
        "severity": "info",
        "code": "SYMLINK-001",
        "description": "All skills in .vibe/skills/ are now symlinks",
        "fixed": true
      },
      {
        "severity": "info",
        "code": "AGENT-001",
        "description": "5 agents are now directly callable",
        "fixed": true
      }
    ]
  },
  "artifacts": [
    {
      "path": "/scratchpad/audit-report-2026-08-22.md",
      "type": "markdown",
      "description": "Full audit report with detailed findings"
    },
    {
      "path": "/scratchpad/findings.json",
      "type": "json",
      "description": "Machine-readable findings"
    }
  ],
  "warnings": [],
  "errors": [],
  "stats": {
    "turns_used": 8,
    "tokens_input": 2500,
    "tokens_output": 1200,
    "duration_ms": 15200
  },
  "next_steps": [
    "Review audit findings in /scratchpad/audit-report-2026-08-22.md",
    "Address warnings if any"
  ],
  "metadata": {
    "subagent": "repo-auditor",
    "timestamp": "2026-08-22T22:30:00Z",
    "version": "1.0.0"
  }
}
```

### Example 2: skill-validator (error)

```json
{
  "status": "error",
  "task": "skill_validation",
  "summary": "Validation failed for 2 skills",
  "results": {
    "total_skills": 11,
    "valid_skills": 9,
    "invalid_skills": 2,
    "errors": {
      "skills/bad-skill/SKILL.md": ["Missing required field: description"],
      "skills/another-bad/SKILL.md": ["Invalid YAML frontmatter"]
    }
  },
  "artifacts": [],
  "warnings": [],
  "errors": [
    "skills/bad-skill/SKILL.md: Missing description",
    "skills/another-bad/SKILL.md: Invalid YAML"
  ],
  "stats": {
    "turns_used": 3,
    "tokens_input": 800,
    "tokens_output": 400,
    "duration_ms": 5000
  },
  "next_steps": [
    "Fix SKILL.md frontmatter in bad-skill",
    "Fix YAML syntax in another-bad"
  ],
  "metadata": {
    "subagent": "skill-validator",
    "timestamp": "2026-08-22T22:35:00Z",
    "version": "1.0.0"
  }
}
```

### Example 3: Simple Timestamp (direct execution)

For simple requests like "what time is it?", the router handles directly:

```bash
python -c "from timestamp_skill import get_utc_timestamp; print(get_utc_timestamp())"
```

Output: `2026-08-22-2230` (plain text, no JSON needed)

---

## Implementation Guidelines

### For Subagent Authors

1. **Always return valid JSON** when the task involves data collection or multi-step processing
2. **Use plain text** for simple, single-value responses (like timestamps)
3. **Include `status` and `task`** in every JSON response (required fields)
4. **Use artifacts** to reference files created in scratchpad
5. **Populate warnings/errors** appropriately for partial failures
6. **Include stats** if you have access to usage data

### For Parent Agents (Router)

1. **Parse JSON responses** from subagents when available
2. **Fallback to text** if JSON parsing fails
3. **Present artifacts** to user with descriptions
4. **Handle errors** by presenting error list to user
5. **Suggest next steps** from the response

### For Validation

```python
# Python validation with jsonschema
import json
import jsonschema

schema = json.loads(open('docs/SUBAGENT_RETURN_CONVENTION.md').read())
# (extract the schema from the markdown)

try:
    jsonschema.validate(instance=response_data, schema=schema)
    print("✓ Valid subagent return")
except jsonschema.ValidationError as e:
    print(f"✗ Invalid: {e.message}")
```

---

## Compatibility Notes

### LangChain Compatibility

This schema is compatible with LangChain's structured output pattern:
```python
from langchain_core.outputs import Generation
# Returns JSON-serialized ToolMessage content
```

### Claude Code Compatibility

Claude Code supports structured JSON outputs. This schema can be used with:
```yaml
response_format: json_schema
```

### JSON Agents Standard

This convention aligns with the JSON Agents specification for agent-to-agent communication, using JSON Schema for type safety.

---

## Migration Path

### Version 1.0.0 (Current)
- Initial convention definition
- JSON Schema validation
- Basic field set

### Future Versions
- Add field: `related_tasks` for task chaining
- Add field: `confidence` for result reliability
- Add field: `cost` for token/price tracking

---

## References

- [JSON Schema Specification](https://json-schema.org/)
- [LangChain Structured Outputs](https://python.langchain.com/docs/modules/model_io/output_parsers/)
- [JSON Agents Standard](https://github.com/JSON-AGENTS/Standard)
- [Claude Code Structured Outputs](https://docs.claude.com/en/agent-sdk/structured-outputs)

---

*Document created: 2026-08-22*  
*Version: 1.0.0*  
*Maintainer: crispy-couscous*
