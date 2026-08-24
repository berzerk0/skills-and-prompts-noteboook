---
name: security-audit
description: Security audit skill that scans codebases for vulnerabilities, hardcoded secrets, dangerous patterns, and security misconfigurations.
license: MIT
compatibility: [claude, pi, vibe]
metadata:
  author: "berzerk0"
  repository: "https://github.com/berzerk0/skills-and-prompts-notebook"
  tags: ["security", "audit", "vulnerabilities", "secrets"]
user-invocable: true
---

# Security Audit Skill

> **Purpose:** Perform comprehensive security audits on codebases. Scans for vulnerabilities, hardcoded secrets, dangerous patterns, and security misconfigurations. Generates actionable reports with severity levels and remediation guidance.

---

## ⚠️ Security First

**This skill is designed for security analysis only.**
- ⚠️ **Do not run on production systems without isolation**
- ⚠️ **Use in containers or sandboxed environments**
- ⚠️ **Review findings before applying fixes**
- ⚠️ **Never commit secrets or sensitive data to reports**

---

## 🎯 Quick Start

### Basic Audit
```
/security-audit
```

### Audit Specific Paths
```
/security-audit src/,config/
```

### Audit with Severity Filter
```
/security-audit --min-severity high
```

### Audit with Output Format
```
/security-audit --format json
```

---

## 🔍 Audit Workflow

### Phase 1: Discovery
1. Identify all files in scope
2. Determine file types and languages
3. Check for ignore patterns (node_modules/, .git/, etc.)
4. Set up temporary directory for findings

### Phase 2: Pattern Scanning
Run multiple scanners in parallel:

```bash
# Scanner 1: Hardcoded secrets
task: "Scan for hardcoded secrets. Search for: API keys, passwords, tokens, private keys, credentials, access keys, secret keys. Use grep with regex patterns. Check common files: .env, config/*.py, *.json, *.yaml, *.yml. Write findings to /tmp/audit/secrets.json with format: [{\"file\": \"path\", \"line\": 1, \"match\": \"API_KEY=...\", \"severity\": \"critical\", \"category\": \"hardcoded-secret\"}]"

# Scanner 2: Dangerous functions
task: "Scan for dangerous function calls. Search for: eval, exec, system, popen, spawn, os.popen, subprocess.run with shell=True, pickle.loads, yaml.load without safe mode, __import__, compile. Write findings to /tmp/audit/dangerous-functions.json"

# Scanner 3: Injection vulnerabilities
task: "Scan for injection vulnerabilities. Search for: SQL queries with string concatenation, HTML output without escaping, shell commands with user input. Write findings to /tmp/audit/injections.json"

# Scanner 4: Security misconfigurations
task: "Scan for security misconfigurations. Search for: debug=True in production, ALLOWED_HOSTS=['*'], CORS_ALLOW_ALL=True, SESSION_COOKIE_SECURE=False, hardcoded JWT secrets. Write findings to /tmp/audit/misconfigurations.json"
```

### Phase 3: Combine and Deduplicate
1. Read all scanner outputs
2. Deduplicate findings (same issue in multiple files)
3. Merge related findings
4. Assign severity levels
5. Generate unified report

---

## 🔥 Critical Findings (Auto-Escalate)

### 1. Hardcoded Secrets

**Patterns:**
```bash
grep -r "(api[_-]?key|secret|password|token|credential|access[_-]?key|private[_-]?key)" \
  --include="*.py" --include="*.js" --include="*.env" --include="*.json"
```

**Example:**
```python
# ❌ CRITICAL
API_KEY = "sk-1234567890abcdef"
PASSWORD = "admin123"
```

**Fix:** Move to environment variables or secret management system

### 2. Remote Code Execution

**Patterns:**
```bash
grep -r "(eval|exec|system|popen|spawn)\(" --include="*.py"
grep -r "pickle.loads\|yaml.load" --include="*.py" | grep -v "safe_load"
```

**Example:**
```python
# ❌ CRITICAL
os.system(f"echo {user_input}")  # Shell injection
pickle.loads(untrusted_data)    # Deserialization attack
```

**Fix:** Use subprocess without shell=True, use yaml.safe_load()

### 3. SQL Injection

**Patterns:**
```bash
grep -r "execute\s*\(" --include="*.py" -A 1 | grep -B 1 "f\"\\|f'\\|\\+"
```

**Example:**
```python
# ❌ CRITICAL
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")

# ✅ SAFE
cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
```

---

## 🟠 High Severity Findings

### 1. Insecure Deserialization
```python
# ❌ HIGH
pickle.loads(data)
yaml.load(data)  # Without safe mode

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

### 3. XSS (Cross-Site Scripting)
```python
# ❌ HIGH
return f"<html>Hello {user_input}</html>"

# ✅ SAFE
from markupsafe import escape
return f"<html>Hello {escape(user_input)}</html>"
```

---

## 🟡 Medium Severity Findings

### 1. Information Disclosure
```python
# ❌ MEDIUM
app.run(debug=True)
DEBUG = True

# ✅ SAFE
app.run(debug=False)
DEBUG = False
```

### 2. Weak Cryptography
```python
# ❌ MEDIUM
hashlib.md5(password.encode()).hexdigest()

# ✅ SAFE
hashlib.sha256(password.encode()).hexdigest()
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

## 📝 Report Templates

### JSON Format
```json
{
  "audit_id": "{uuid}",
  "timestamp": "{iso_timestamp}",
  "summary": {
    "files_scanned": {count},
    "critical": {count},
    "high": {count},
    "medium": {count},
    "low": {count}
  },
  "findings": [
    {
      "id": "CR-001",
      "severity": "critical",
      "category": "hardcoded-secret",
      "title": "AWS Access Key in config.py",
      "file": "config/prod.py",
      "line": 42,
      "code_snippet": "AWS_ACCESS_KEY_ID = 'AKIA...'",
      "impact": "Attacker can gain access to AWS resources",
      "recommendation": "Move to environment variables"
    }
  ]
}
```

---

## 🎛️ Configuration Options

```
--files <path>        Specific files/directories
--exclude <pattern>  Exclude patterns
--min-severity <level>  critical, high, medium, low
--format <format>    json, markdown, sarif
--output <file>      Output to file
```

---

## 🔗 Integration with Other Tools

### Semgrep
```bash
semgrep --config=p/ciandcd --config=p/security-audit --json -o /tmp/semgrep-results.json
```

### Bandit (Python)
```bash
bandit -r . -f json -o /tmp/bandit-results.json
```

### Trivy
```bash
trivy fs --security-checks vuln,config --format json -o /tmp/trivy-results.json
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

This skill provides **best-effort** security analysis. It cannot guarantee:
- Complete coverage of all vulnerabilities
- Zero false positives or false negatives
- Protection against all attacks

**Always:**
- Review findings manually
- Test fixes thoroughly
- Consider professional security audit for critical systems

---

*Skill version: 1.0.0*
*Last updated: 2026-08-23*
*Compatibility: Mistral Vibe >=2.24.0*
