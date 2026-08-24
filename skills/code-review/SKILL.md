---
name: code-review
description: Code review assistant that performs comprehensive analysis of codebases. Spawns subagents for different review aspects and combines findings.
license: MIT
compatibility: [claude, pi, vibe]
metadata:
  author: "berzerk0"
  repository: "https://github.com/berzerk0/skills-and-prompts-notebook"
  tags: ["code-review", "security", "quality", "audit"]
user-invocable: true
---

# Code Review Skill

> **Purpose:** Perform comprehensive code reviews with a focus on security, quality, and maintainability. Uses subagents to parallelize different review aspects and combines findings into a unified report.

---

## 🎯 Capabilities

This skill can:
- Perform **security audits** (hardcoded secrets, dangerous functions, permissions)
- Analyze **code quality** (style, complexity, duplication)
- Review **testing coverage** (test presence, quality, edge cases)
- Check **performance implications** (algorithm complexity, bottlenecks)
- Assess **documentation** (presence, quality, accuracy)
- Generate **unified reports** combining all findings

---

## 🚀 Quick Start

### Basic Usage
```
/code-review
```

### Review Specific Files
```
/code-review path/to/file.py path/to/other.py
```

### Review with Focus Areas
```
/code-review --focus security,quality
```

### Generate Report Only
```
/code-review --report-only
```

---

## 📋 Review Workflow

### Step 1: Discovery
- Identify all files to review (or use provided paths)
- Determine file types and appropriate review strategies
- Set up scratchpad directories for each subagent

### Step 2: Parallel Analysis
Spawn subagents for different review aspects:

```bash
# Security review
task: "Perform security audit. Focus on: hardcoded secrets (API keys, passwords, tokens), dangerous functions (eval, exec, system, pickle.loads), SQL injection, XSS, path traversal, permission issues, insecure deserialization. Write findings to /tmp/review/security.md. Use grep to search for patterns."

# Code quality review  
task: "Analyze code quality. Focus on: PEP8/ESLint violations, code duplication, function length (>50 lines), cyclomatic complexity, magic numbers, inconsistent naming, unused imports/variables, TODO/FIXME comments. Write findings to /tmp/review/quality.md"

# Testing review
task: "Review testing coverage. Focus on: test file presence, test coverage percentage, edge cases covered, mock usage, assertion quality, test organization, integration vs unit tests. Write findings to /tmp/review/testing.md"

# Performance review
task: "Analyze performance. Focus on: algorithm complexity (O(n^2) or worse), database query efficiency, caching opportunities, I/O operations in loops, memory usage, blocking operations, async/await usage. Write findings to /tmp/review/performance.md"

# Documentation review
task: "Assess documentation. Focus on: README presence and quality, function/class docstrings, type hints, inline comments quality, changelog, examples, API documentation. Write findings to /tmp/review/docs.md"
```

### Step 3: Combine Findings
Read all subagent reports and create unified findings:

```bash
read_file: /tmp/review/security.md
read_file: /tmp/review/quality.md
read_file: /tmp/review/testing.md
read_file: /tmp/review/performance.md
read_file: /tmp/review/docs.md
```

### Step 4: Generate Report
Create a comprehensive markdown report with:
- Executive summary
- Findings by category (Critical, High, Medium, Low)
- Detailed issues with file:line references
- Recommendations and fixes
- Priority ranking

---

## 🔍 Security Review Checklist

### Critical Priority
- [ ] **Hardcoded secrets** - API keys, passwords, tokens, private keys
- [ ] **Dangerous functions** - eval(), exec(), system(), pickle.loads()
- [ ] **Shell injection** - subprocess with shell=True and user input
- [ ] **SQL injection** - Raw SQL queries with string concatenation
- [ ] **Command injection** - OS commands built from user input

### High Priority
- [ ] **Insecure deserialization** - pickle, yaml.load without safe mode
- [ ] **Path traversal** - User input in file paths without sanitization
- [ ] **XSS vulnerabilities** - Unescaped user input in HTML
- [ ] **CSRF tokens** - Missing or improper CSRF protection
- [ ] **Authentication bypass** - Weak or missing auth checks

### Search Patterns

```bash
# API keys and secrets
grep: "(api[_-]?key|secret|password|token|credential|private[_-]?key)" --include="*.py" --include="*.js" --include="*.env"

# Dangerous functions
grep: "(eval|exec|system|popen|spawn)\(" --include="*.py"

# SQL injection patterns
grep: "execute\s*\(\s*['\"]" --include="*.py"
```

---

## 📊 Code Quality Checklist

### Style
- [ ] Consistent indentation (spaces vs tabs)
- [ ] Line length (< 100-120 characters)
- [ ] Consistent naming (snake_case vs camelCase)
- [ ] Proper imports grouping (stdlib, third-party, local)

### Structure
- [ ] Functions < 50 lines
- [ ] Classes < 200 lines
- [ ] Files < 500 lines
- [ ] Cyclomatic complexity < 10
- [ ] No duplicate code (DRY principle)

### Best Practices
- [ ] Type hints (Python) or JSDoc (JavaScript)
- [ ] Docstrings for all public functions/classes
- [ ] Meaningful variable names (not x, y, data)
- [ ] Consistent error handling
- [ ] Proper resource cleanup (files, connections)

---

## 🧪 Testing Review Checklist

### Coverage
- [ ] Unit tests for all functions
- [ ] Integration tests for modules
- [ ] End-to-end tests for features
- [ ] Edge cases covered
- [ ] Error cases covered

### Quality
- [ ] Tests are isolated (no interdependence)
- [ ] Tests use mocks/stubs appropriately
- [ ] Assertions are specific (not just "truthy")
- [ ] Tests cover both success and failure paths

---

## ⚡ Performance Review Checklist

### Algorithm Complexity
- [ ] No O(n^2) or worse algorithms on large datasets
- [ ] Proper data structures used (sets for membership, heaps for priority)
- [ ] Caching for expensive operations
- [ ] Memoization for pure functions

### Database
- [ ] Indexes on query columns
- [ ] No N+1 query problems
- [ ] Proper transaction management
- [ ] Connection pooling configured

---

## 📝 Report Format

### Executive Summary
```markdown
## Executive Summary

**Review Date:** {date}
**Reviewer:** {agent}
**Repository:** {repo}
**Files Reviewed:** {count}

### Overall Assessment
- **Security:** {grade} (Critical: {count}, High: {count}, Medium: {count}, Low: {count})
- **Quality:** {grade} (Issues: {count})
- **Testing:** {grade} (Coverage: {percentage}%)
- **Performance:** {grade} (Issues: {count})
- **Documentation:** {grade} (Gaps: {count})

**Recommendation:** {merge/needs-work/reject}
```

---

## 🎛️ Configuration Options

### Focus Areas
```
--focus <areas>       Comma-separated focus areas: security,quality,testing,perf,docs
--format <format>    Output format: markdown, json, sarif
--output <file>      Output to file instead of stdout
--quiet              Only show findings, suppress progress
--verbose            Show detailed progress
```

---

## 🔗 Integration with Other Skills

This skill can work with other skills for enhanced analysis:

### Security Audit
```
skill: security-audit
```

### Static Analysis
```
skill: static-analysis
```

---

*Skill version: 1.0.0*
*Last updated: 2026-08-23*
*Compatibility: Mistral Vibe >=2.24.0*
