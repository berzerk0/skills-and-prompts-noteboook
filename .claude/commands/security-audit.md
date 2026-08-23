# Claude Code: Security Audit Commands

> **Purpose:** Provide Claude Code with structured security audit capabilities that mirror the Vibe security-audit skill.

---

## ⚠️ Security Notice

**This document provides security audit capabilities for code analysis.**
- ⚠️ **Do not run on production systems without isolation**
- ⚠️ **Use in containers or sandboxed environments**
- ⚠️ **Review findings before applying fixes**
- ⚠️ **Never commit secrets or sensitive data to reports**

---

## 🎯 Quick Start

### Basic Security Audit
```
/security-audit
```

### Audit Specific Paths
```
/security-audit src/,config/
```

### Audit with Options
```
/security-audit --min-severity high --format json --output audit.json
```

---

## 🔍 Security Audit Workflow

### Phase 1: Discovery
```
Bash: "find . -type f \( -name '*.py' -o -name '*.js' -o -name '*.env' -o -name '*.json' -o -name '*.yaml' \) -not -path './node_modules/*' > /tmp/audit/files.txt"
```

### Phase 2: Parallel Scanning

```
# Scanner 1: Hardcoded Secrets
Task: "Scan for hardcoded secrets. Search for: API keys, passwords, tokens, private keys. Check .env, config/*.py, *.json, *.yaml. Write findings to /tmp/audit/secrets.json"

# Scanner 2: Dangerous Patterns
Task: "Scan for dangerous patterns. Search for: eval, exec, system, pickle.loads, yaml.load without safe mode. Write findings to /tmp/audit/dangerous-patterns.json"

# Scanner 3: Injection Vulnerabilities
Task: "Scan for injection vulnerabilities. Search for: SQL with string concatenation, HTML output without escaping, shell commands with user input. Write findings to /tmp/audit/injections.json"

# Scanner 4: Security Misconfigurations
Task: "Scan for security misconfigurations. Search for: debug=True, ALLOWED_HOSTS=['*'], SESSION_COOKIE_SECURE=False. Write findings to /tmp/audit/misconfigurations.json"
```

### Phase 3: Combine and Deduplicate
```
Read: /tmp/audit/secrets.json
Read: /tmp/audit/dangerous-patterns.json
Read: /tmp/audit/injections.json
Read: /tmp/audit/misconfigurations.json

Task: "Combine all findings. Deduplicate, assign severity levels, group by category. Write to /tmp/audit/findings.json"
```

### Phase 4: Generate Report
```
Read: /tmp/audit/findings.json
Write: /tmp/audit/security-report.md, "[Formatted security report]"
```

---

## 🔥 Critical Findings (Auto-Escalate)

### 1. Hardcoded Secrets

**Patterns:**
```bash
grep -r "(api[_-]?key|secret|password|token|credential)" --include="*.py" --include="*.env" --include="*.json"
```

**Example:**
```python
# ❌ CRITICAL
API_KEY = "sk-1234567890abcdef"
```

**Fix:** Move to environment variables or secret management system

### 2. Remote Code Execution

**Patterns:**
```bash
grep -r "(eval|exec|system|popen)\(" --include="*.py"
grep -r "pickle.loads" --include="*.py"
```

**Fix:** Use subprocess without shell=True, use yaml.safe_load()

### 3. SQL Injection

**Patterns:**
```bash
grep -r "execute\s*\(" --include="*.py" -A 1 | grep -B 1 "f\"\\|f'"
```

**Fix:** Use parameterized queries

---

## 🟠 High Severity Findings

### 1. Insecure Deserialization
```python
# ❌ HIGH
pickle.loads(data)
yaml.load(data)

# ✅ SAFE
yaml.safe_load(data)
```

### 2. Path Traversal
```python
# ❌ HIGH
file_path = "/var/www/" + user_input

# ✅ SAFE
import os
base_dir = "/var/www/uploads"
full_path = os.path.join(base_dir, user_input.lstrip('/'))
if not os.path.realpath(full_path).startswith(os.path.realpath(base_dir)):
    raise ValueError("Invalid path")
```

---

## 📊 Severity Classification

| Severity | Description | Response |
|----------|-------------|----------|
| **Critical** | Immediate exploitation, RCE, data breach | **Block deployment, fix immediately** |
| **High** | Significant risk, potential for exploitation | **Fix before next release** |
| **Medium** | Moderate risk, requires specific conditions | **Fix in next release cycle** |
| **Low** | Low risk, minor impact | **Fix when convenient** |

---

## 🔧 Integration with Security Tools

### Semgrep
```bash
semgrep --config=p/ciandcd --config=p/security-audit --json -o /tmp/semgrep-results.json .
```

### Bandit (Python)
```bash
bandit -r . -f json -o /tmp/bandit-results.json
```

### Safety (Python Dependencies)
```bash
safety check --json --output-file /tmp/safety-results.json
```

### Trivy
```bash
trivy fs --security-checks vuln,config --format json -o /tmp/trivy-results.json .
```

---

## 🎓 Best Practices

1. **Defense in Depth** - Multiple security layers
2. **Principle of Least Privilege** - Minimal permissions
3. **Fail Securely** - Default to deny
4. **Keep Dependencies Updated** - Regular updates
5. **Security by Design** - Consider security from the start

---

## ⚠️ Disclaimer

This skill provides **best-effort** security analysis. Always:
- Review findings manually
- Test fixes thoroughly
- Consider professional security audit for critical systems

---

## 🔗 Related Files

- [cross-agent.md](cross-agent.md) - Cross-agent compatibility
- [code-review.md](code-review.md) - Code review commands
- [../../AGENTS.md](../../AGENTS.md) - Repository compatibility layer
- [../../.vibe/skills/security-audit/SKILL.md](../../.vibe/skills/security-audit/SKILL.md) - Vibe security audit skill

---

*Command version: 1.0.0*
*Last updated: 2026-08-23*
*Compatibility: Claude Code >= 1.0*
