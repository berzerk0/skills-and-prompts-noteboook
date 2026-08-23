# Claude Code: Code Review Commands

> **Purpose:** Provide Claude Code with structured code review capabilities that mirror the Vibe code-review skill.

---

## 🎯 Quick Start

### Basic Code Review
```
/code-review
```

### Review Specific Files
```
/code-review src/utils.py src/api/
```

### Review with Options
```
/code-review --focus security,quality --format json --output report.json
```

---

## 📋 Tool Translation for Code Review

| Action | Vibe | Claude |
|--------|------|--------|
| Read file | `read_file: path` | `Read: path` |
| Write file | `write_file: path, content` | `Write: path, content` |
| Search | `grep: pattern, path` | `Grep: pattern, path` |
| Shell | `bash: "command"` | `Bash: "command" |
| Task | `task: "description"` | `Task: "description"` |

---

## 🔍 Code Review Workflow

### Phase 1: Discovery
```
Bash: "find . -type f \( -name '*.py' -o -name '*.js' -o -name '*.ts' \) -not -path './node_modules/*' > /tmp/review/files.txt"
```

### Phase 2: Parallel Analysis

```
# Security review
Task: "Perform security audit. Focus on: hardcoded secrets, dangerous functions (eval, exec, system, pickle.loads), SQL injection, XSS, path traversal. Write findings to /tmp/review/security.md"

# Code quality review
Task: "Analyze code quality. Focus on: style violations, code duplication, function length, complexity, naming conventions. Write findings to /tmp/review/quality.md"

# Testing review
Task: "Review testing coverage. Focus on: test presence, edge cases, mock usage, assertion quality. Write findings to /tmp/review/testing.md"

# Performance review
Task: "Analyze performance. Focus on: algorithm complexity, database query efficiency, caching, I/O in loops. Write findings to /tmp/review/performance.md"
```

### Phase 3: Combine Findings
```
Read: /tmp/review/security.md
Read: /tmp/review/quality.md
Read: /tmp/review/testing.md
Read: /tmp/review/performance.md

Task: "Combine all findings. Deduplicate, group by category and severity. Write to /tmp/review/findings.json"
```

### Phase 4: Generate Report
```
Read: /tmp/review/findings.json
Write: /tmp/review/report.md, "[Formatted report content]"
```

---

## 🔗 Integration with Other Tools

### Semgrep
```bash
semgrep --config=p/ciandcd --config=p/security-audit --json -o /tmp/semgrep-results.json .
```

### Bandit (Python)
```bash
bandit -r . -f json -o /tmp/bandit-results.json
```

### ESLint (JavaScript)
```bash
eslint --format json -o /tmp/eslint-results.json .
```

---

## 📊 Performance Tips

- **Narrow scope:** Review specific files instead of entire codebase
- **Selective focus:** Only enable needed focus areas
- **Use grep first:** Filter files before deep analysis
- **Batch processing:** Process multiple files in one task

---

## 🔗 Related Files

- [cross-agent.md](cross-agent.md) - Cross-agent compatibility
- [security-audit.md](security-audit.md) - Security audit commands
- [../../AGENTS.md](../../AGENTS.md) - Repository compatibility layer
- [../../.vibe/skills/code-review/SKILL.md](../../.vibe/skills/code-review/SKILL.md) - Vibe code review skill

---

*Command version: 1.0.0*
*Last updated: 2026-08-23*
*Compatibility: Claude Code >= 1.0*
