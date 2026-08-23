# crispy-couscous

**A multi-agent skill repository for Claude Code, Pi Agent, and Mistral Vibe Code.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-Spec_Compliant-blue.svg)](https://agentskills.io/specification)

---

## 🏆 What This Is

This repository stores **portable skills** and **subagent configurations** that work across multiple AI agent platforms. It's designed for:

- **Skill development**: Create, test, and maintain cross-agent skills
- **Skill storage**: Central repository for reusable skill definitions
- **Agent orchestration**: Subagent configurations for delegation workflows
- **Cross-tool compatibility**: Skills that work in Claude Code, Pi Agent, and Vibe Code

---

## 📚 Available Skills

| Skill | Description | Type | Compatibility |
|-------|-------------|------|---------------|
| **[challenge-my-thinking](skills/challenge-my-thinking/SKILL.md)** | Actively challenges assumptions, plays devil's advocate | Thinking Framework | ✅ Claude, Pi, Vibe |
| **[clarify](skills/clarify/SKILL.md)** | Ask clarifying questions when task is underspecified | Thinking Framework | ✅ Claude, Pi, Vibe |
| **[escalate](skills/escalate/SKILL.md)** | Create escalation brief when stuck | Workflow | ✅ Claude, Pi, Vibe |
| **[modern-python](skills/modern-python/SKILL.md)** | Configures Python projects with modern tooling (uv, ruff, ty) | Configuration | ✅ Claude, Pi, Vibe |
| **[napkin](skills/napkin/SKILL.md)** | Maintain a per-repo napkin as a continuously curated runbook | Documentation | ✅ Claude, Pi, Vibe |
| **[planning-with-files](skills/planning-with-files/SKILL.md)** | Implements file-based planning for complex multi-step tasks | Planning | ✅ Claude, Pi, Vibe |
| **[repo-auditor](skills/repo-auditor/SKILL.md)** | Audit repository structure, skills, and cross-agent compatibility | Repository Management | ✅ Claude, Pi, Vibe |
| **[skill-extractor](skills/skill-extractor/SKILL.md)** | Extracts reusable skills from work sessions | Quality Assurance | ✅ Claude, Pi, Vibe |
| **[skill-validator](skills/skill-validator/SKILL.md)** | Validate SKILL.md files against Agent Skills specification | Quality Assurance | ✅ Claude, Pi, Vibe |
| **[vibe-reference](skills/vibe-reference/SKILL.md)** | Access verified Mistral Vibe Code reference documentation | Reference | ✅ Claude, Pi, Vibe |
| **[writing-for-agents](skills/writing-for-agents/SKILL.md)** | Writing documents for agents | Documentation | ✅ Claude, Pi, Vibe |

---

## 🚀 Quick Start

### For Agents Working in This Repo

Skills are **automatically discoverable**. Just ask:

- **"What time is it?"** → Triggers `timestamp` skill
- **"List my Codeberg repos"** → Triggers `codeberg` skill
- **"Challenge my thinking on this"** → Triggers `challenge-my-thinking` skill
- **"Audit this repository"** → Triggers `repo-auditor` skill
- **"Validate the skills"** → Triggers `skill-validator` skill

Or explicitly invoke: `task use <skill-name>` (Vibe Code)

### For Humans Setting Up

1. **Clone the repo**:
   ```bash
   git clone https://github.com/berzerk0/crispy-couscous.git
   cd crispy-couscous
   ```

2. **Install dependencies** (for agent config generation):
   ```bash
   pip install pyyaml toml
   ```

3. **Generate agent configs** (if you add/modify skills):
   ```bash
   python meta/generate_all.py --all
   ```

---

## 📁 Repository Structure

```
.
├── README.md                    # This file - human quick start
├── AGENTS.md                    # Agent instructions for this repo
├── 
├── skills/                      # Portable skill definitions (Agent Skills spec)
│   ├── timestamp/SKILL.md
│   ├── codeberg/SKILL.md
│   ├── challenge-my-thinking/SKILL.md
│   ├── repo-auditor/SKILL.md
│   └── skill-validator/SKILL.md
├── 
├── *.py                         # Shared Python implementations
│   ├── timestamp_skill.py
│   └── codeberg_connector.py
├── 
├── meta/                        # Generation scripts for agent configs
│   ├── generate_all.py
│   ├── generate_claude.py
│   ├── generate_pi.py
│   └── generate_vibe.py
├── 
├── docs/                        # Documentation
│   ├── SKILL_DESIGN.md
│   ├── cross-agent-primitives.md
│   ├── AGENTS.md
│   └── multi-agent/
│       ├── STANDARDS.md
│       ├── COMPATIBILITY.md
│       ├── GAPS.md
│       └── MAINTENANCE.md
├── 
├── .claude/                     # Claude Code configurations
│   ├── agents/                  # Subagent definitions
│   │   ├── timestamp.md
│   │   ├── codeberg.md
│   │   ├── challenge-my-thinking.md
│   │   ├── repo-auditor.md
│   │   └── skill-validator.md
│   └── skills/                  # → symlink to ../skills/
├── 
├── .pi/                         # Pi Agent configurations
│   ├── agents/                  # Subagent definitions
│   │   ├── timestamp.md
│   │   ├── codeberg.md
│   │   ├── challenge-my-thinking.md
│   │   ├── repo-auditor.md
│   │   └── skill-validator.md
│   └── skills/                  # → symlink to ../skills/
└── 
└── .vibe/                       # Vibe Code configurations
    ├── agents/                  # Subagent definitions
    │   ├── timestamp.toml
    │   ├── codeberg.toml
    │   ├── challenge-my-thinking.toml
    │   ├── repo-auditor.toml
    │   └── skill-validator.toml
    └── skills/                  # → symlink to ../skills/
```

---

## ✍️ Adding New Skills

### 1. Create Portable SKILL.md

Create `skills/<name>/SKILL.md` with valid YAML frontmatter:

```yaml
---
name: my-skill
description: What this skill does and when to use it.
license: MIT
compatibility: [claude, pi, vibe]
---
```

**Note:** For internal tracking, you can add custom metadata in the frontmatter:

```yaml
---
name: my-skill
description: What this skill does and when to use it.
license: MIT
compatibility: [claude, pi, vibe]
metadata:
  requires_authentication: false
  requires_network: false
---
```

### 2. Create Python Implementation (Optional)

Create `<name>_skill.py` or `<name>_connector.py`:

```python
"""Implementation for my-skill."""

def main_function():
    """Core logic."""
    pass

if __name__ == "__main__":
    # CLI entry point
    main_function()
```

### 3. Generate Agent Configurations

Generate framework-specific agent configurations from your SKILL.md:

```bash
# Generate agent configs for all skills
python meta/generate_all.py --all

# Generate for a specific skill
python meta/generate_all.py --skill my-skill
```

---

## 📊 Agent Compatibility

| Feature | Claude Code | Pi Agent | Vibe Code |
|---------|--------------|----------|-----------|
| Skill Discovery | `.claude/skills/` | `.pi/skills/` | `.vibe/skills/` |
| Subagents | ✅ Native | ⚠️ Extensions | ✅ Native |
| AGENTS.md | ❌ (uses CLAUDE.md) | ✅ Native | ✅ Native |
| Tool Name | `Read`, `Write`, `Edit`, `Bash` | `read`, `write`, `edit`, `bash` | `read`, `write_file`, `edit`, `bash` |
| **Universal Tool** | **`Bash`** | **`bash`** | **`bash`** |

**Key Insight**: `bash`/`Bash` is the **only tool name consistent across all three agents**. All skill implementations should be invocable via bash.

---

## 🛠️ Agent Configuration Generation

The `meta/` directory contains scripts to generate **framework-specific agent configurations** from portable SKILL.md files:

```bash
# Note: Skills use SKILL.md directly (portable)
# Agent configs are framework-specific and generated from skills

python meta/generate_all.py --all
```

**Important:** Skills themselves (in `skills/<name>/SKILL.md`) are portable and follow the Agent Skills specification. Agent configurations (in `.vibe/agents/`, `.claude/agents/`, `.pi/agents/`) are framework-specific and generated from the canonical skills.

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[AGENTS.md](AGENTS.md)** | Instructions for agents working in this repo |
| **[SKILL_DESIGN.md](docs/SKILL_DESIGN.md)** | How to design portable skills |
| **[cross-agent-primitives.md](docs/cross-agent-primitives.md)** | Tool name standardization research |
| **[STANDARDS.md](docs/multi-agent/STANDARDS.md)** | Official standards reference |
| **[COMPATIBILITY.md](docs/multi-agent/COMPATIBILITY.md)** | Cross-agent compatibility guide |
| **[GAPS.md](docs/multi-agent/GAPS.md)** | Undocumented gaps in multi-agent standards |

---

## 🎯 References

- [Agent Skills Specification](https://agentskills.io/specification)
- [GitHub AGENTS.md](https://agents.md/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/my-skill`)
3. Add your skill following the patterns above
4. Test across all three agents if possible
5. Submit a Pull Request

---

## 📜 License

This repository and all skills are licensed under the **MIT License** unless otherwise specified in individual skill frontmatter.

---

## 📝 To-Do List

- [ ] **writing-style skill** - Define and enforce consistent writing style across documentation
