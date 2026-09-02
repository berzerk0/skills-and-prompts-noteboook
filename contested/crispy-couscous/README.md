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
| **[challenge-my-thinking](skills/challenge-my-thinking/SKILL.md)** | Actively challenges assumptions, plays devil's advocate | Thinking Framework | \u2705 Claude, Pi, Vibe |
| **[clarify](skills/clarify/SKILL.md)** | Ask clarifying questions when task is underspecified | Thinking Framework | \u2705 Claude, Pi, Vibe |
| **[escalate](skills/escalate/SKILL.md)** | Create escalation brief when stuck | Workflow | \u2705 Claude, Pi, Vibe |
| **[modern-python](skills/modern-python/SKILL.md)** | Configures Python projects with modern tooling (uv, ruff, ty) | Configuration | \u2705 Claude, Pi, Vibe |
| **[napkin](skills/napkin/SKILL.md)** | Maintain a per-repo napkin as a continuously curated runbook | Documentation | \u2705 Claude, Pi, Vibe |
| **[planning-with-files](skills/planning-with-files/SKILL.md)** | Implements file-based planning for complex multi-step tasks | Planning | \u2705 Claude, Pi, Vibe |
| **[repo-auditor](skills/repo-auditor/SKILL.md)** | Audit repository structure, skills, and cross-agent compatibility | Repository Management | \u2705 Claude, Pi, Vibe |
| **[script-it](skills/script-it/SKILL.md)** | Write throwaway scripts for repetitive operations across 5+ items | Automation | \u2705 Claude, Pi, Vibe |
| **[skill-extractor](skills/skill-extractor/SKILL.md)** | Extracts reusable skills from work sessions | Quality Assurance | \u2705 Claude, Pi, Vibe |
| **[skill-validator](skills/skill-validator/SKILL.md)** | Validate SKILL.md files against Agent Skills specification | Quality Assurance | \u2705 Claude, Pi, Vibe |
| **[timestamp](skills/timestamp/SKILL.md)** | Get current UTC timestamp in YYYY-MM-DD-HHMM format | Utility | \u2705 Claude, Pi, Vibe |
| **[vibe-reference](skills/vibe-reference/SKILL.md)** | Access verified Mistral Vibe Code reference documentation | Reference | \u2705 Claude, Pi, Vibe |
| **[writing-for-agents](skills/writing-for-agents/SKILL.md)** | Writing documents for agents | Documentation | \u2705 Claude, Pi, Vibe |

---

## 🚀 Quick Start

### For Agents Working in This Repo

Skills are **automatically discoverable**. Just ask:

- **"What time is it?"** → Triggers `timestamp` skill
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

## :rotating_light: Symlink Safety Invariant

**NEVER write through symlinks in `.claude/skills/`, `.pi/skills/`, or `.vibe/skills/`.**

These directories are **symlink farms** pointing to the canonical `skills/` directory. Writing through a symlink silently overwrites the canonical SKILL.md file. This caused the 2026-08-24 incident where all 14 SKILL.md files were flattened to 13-line stubs.

**Safe pattern:**
- **READ through symlinks**: Agents discover skills via `.claude/skills/`, `.pi/skills/`, `.vibe/skills/`
- **WRITE only to agent wrapper files**: `.claude/agents/`, `.pi/agents/`, `.vibe/agents/`
- **Canonical source**: `skills/<name>/SKILL.md` - single source of truth


## 📁 Repository Structure
```
.
├── README.md                    # This file - human quick start
├── AGENTS.md                    # Agent instructions for this repo
├── 
├── skills/                      # Portable skill definitions (Agent Skills spec)
│   ├── timestamp/SKILL.md
│   ├── challenge-my-thinking/SKILL.md
│   ├── repo-auditor/SKILL.md
│   ├── skill-validator/SKILL.md
│   └── ... (13 skills total, see table above)
├── 
├── *.py                         # Shared Python implementations
│   └── timestamp_skill.py
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
│   ├── agents/                  # Subagent definitions (one .md per skill)
│   │   ├── timestamp.md
│   │   ├── challenge-my-thinking.md
│   │   ├── repo-auditor.md
│   │   └── ... (13 total, one per skill)
│   └── skills/                  # → symlinks to ../skills/<name>
├── 
├── .pi/                         # Pi Agent configurations
│   ├── agents/                  # Subagent definitions (one .md per skill)
│   │   ├── timestamp.md
│   │   ├── challenge-my-thinking.md
│   │   ├── repo-auditor.md
│   │   └── ... (13 total, one per skill)
│   └── skills/                  # → symlinks to ../skills/<name>
└── 
└── .vibe/                       # Vibe Code configurations
    ├── agents/                  # Subagent definitions
    │   ├── timestamp.toml
    │   ├── challenge-my-thinking.toml
    │   ├── repo-auditor.toml
    │   ├── ... (13 total, one per skill)
    │   └── architect.toml, escalation-fixer.toml, implementer.toml,
    │       reviewer.toml, router.toml, transcription.toml
    │       (6 orchestration subagents -- Vibe-only, no portable skill;
    │       see Subagent Orchestration below)
    └── skills/                  # → symlinks to ../skills/<name>
```

### Subagent Orchestration (Vibe-only)

`.vibe/agents/` also has six subagents with no corresponding `skills/` entry --
they're pure delegation targets, not portable skills, so Claude Code and Pi
Agent don't have equivalents:

| Subagent | Purpose |
|----------|---------|
| `router` | Primary entry point. Routes tasks to the right specialized subagent based on intent, domain, and complexity. |
| `architect` | Architecture and design tasks: broad codebase understanding, final review, design judgment. |
| `implementer` | Implements prose-spec tasks. |
| `reviewer` | Reviews prose-spec implementations: mid-tier floor tasks, multi-file coordination, debugging. |
| `escalation-fixer` | Fix-loop escalation for tasks that failed on a cheaper model -- one tier up. |
| `transcription` | Isolated, mechanical single-file tasks with a clear spec (1-2 files). |

See `docs/MODEL_SELECTION_STRATEGY.md` and `docs/SUBAGENT_RETURN_CONVENTION.md`
for how these fit together.

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
| **[AGENTS.md](AGENTS.md)** | Instructions for agents working in this repo (the live one -- loaded at session start) |
| **[docs/AGENTS.md](docs/AGENTS.md)** | Older, shorter "Agent Manifest" -- predates the root `AGENTS.md` above and has not been reconciled with it. Read the root one; this one needs a keep-or-remove decision. |
| **[SKILL_DESIGN.md](docs/SKILL_DESIGN.md)** | How to design portable skills |
| **[cross-agent-primitives.md](docs/cross-agent-primitives.md)** | Tool name standardization research |
| **[STANDARDS.md](docs/multi-agent/STANDARDS.md)** | Official standards reference |
| **[COMPATIBILITY.md](docs/multi-agent/COMPATIBILITY.md)** | Cross-agent compatibility guide |
| **[GAPS.md](docs/multi-agent/GAPS.md)** | Undocumented gaps in multi-agent standards |
| **[MAINTENANCE.md](docs/multi-agent/MAINTENANCE.md)** | How to keep the standards docs current |
| **[MODEL_SELECTION_STRATEGY.md](docs/MODEL_SELECTION_STRATEGY.md)** | Model tier strategy behind the Vibe orchestration subagents |
| **[SUBAGENT_RETURN_CONVENTION.md](docs/SUBAGENT_RETURN_CONVENTION.md)** | JSON return convention for subagents |

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
