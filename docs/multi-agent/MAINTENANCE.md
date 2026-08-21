# Maintenance Guide for Multi-Agent Standards

**Last Updated:** August 21, 2026  
**Repository:** [berzerk0/crispy-couscous](https://github.com/berzerk0/crispy-couscous)  
**Purpose:** How to keep the multi-agent standards documentation (`STANDARDS.md`, `COMPATIBILITY.md`, `GAPS.md`) up-to-date with official sources.

---

## 📌 Overview

The multi-agent standards documentation in this repo (`docs/multi-agent/`) is **version-specific** and relies on **official sources** for accuracy. To ensure the docs remain current, follow this guide to:
1. **Track updates** to official specifications and tool documentation.
2. **Validate claims** against primary sources.
3. **Update the docs** when changes are detected.

---

## 🔄 Keeping Documentation Current

### 1. Monitor Official Sources

The docs reference **official sources** for every claim. To stay updated:

#### Cross-Tool Standards
| **Standard** | **Primary Source** | **How to Monitor** |
|-------------|-------------------|--------------------|
| **Agent Skills** | [agentskills.io/specification](https://agentskills.io/specification) | <ul><li>Watch the [agentskills/agentskills GitHub repo](https://github.com/agentskills/agentskills).</li><li>Subscribe to [agentskills.io updates](https://agentskills.io).</li><li>Follow [@agentskills](https://github.com/agentskills) on GitHub.</li></ul> |
| **AGENTS.md** | [agents.md](https://agents.md/) | <ul><li>Watch the [agentsmd/agents.md GitHub repo](https://github.com/agentsmd/agents.md).</li><li>Follow [@agentsmd](https://github.com/agentsmd) on GitHub.</li></ul> |
| **MCP** | [modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2026-07-28) | <ul><li>Watch the [modelcontextprotocol/spec GitHub repo](https://github.com/modelcontextprotocol/modelcontextprotocol).</li><li>Subscribe to the [MCP Blog](https://blog.modelcontextprotocol.io/).</li><li>Follow [@modelcontextprotocol](https://github.com/modelcontextprotocol) on GitHub.</li></ul> |

#### Tool-Specific Sources
| **Tool** | **Primary Source** | **How to Monitor** |
|---------|-------------------|--------------------|
| **Claude Code** | [code.claude.com/docs](https://code.claude.com/docs) | <ul><li>Watch the [anthropics/claude-code GitHub repo](https://github.com/anthropics/claude-code).</li><li>Follow [@anthropics](https://github.com/anthropics) on GitHub.</li><li>Subscribe to the [Claude Code Newsletter](https://code.claude.com) (if available).</li></ul> |
| **Pi Agent** | [pi.dev/docs](https://pi.dev/docs) | <ul><li>Watch the [earendil-works/pi GitHub repo](https://github.com/earendil-works/pi).</li><li>Follow [@earendil-works](https://github.com/earendil-works) on GitHub.</li><li>Monitor the [Pi News page](https://pi.dev/news/releases).</li></ul> |
| **Vibe Code** | [docs.mistral.ai](https://docs.mistral.ai) | <ul><li>Watch the [mistralai/mistral-vibe GitHub repo](https://github.com/mistralai/mistral-vibe).</li><li>Follow [@mistralai](https://github.com/mistralai) on GitHub.</li><li>Monitor the [Mistral AI Blog](https://mistral.ai/news/).</li></ul> |

---

### 2. Automated Validation (CI Check Concept)

While we are **not implementing** a CI check here, the following **approach** can be used to validate the documentation against official sources:

#### CI Check Workflow
1. **Fetch Official Docs**:
   - Use `curl` or `wget` to download the latest versions of:
     - [Agent Skills Spec](https://agentskills.io/specification) (HTML/JSON)
     - [MCP Spec](https://modelcontextprotocol.io/specification/2026-07-28) (JSON)
     - Tool-specific docs (e.g., Claude Code’s `tools-reference` page).
   - Parse the content to extract **key claims** (e.g., tool lists, timeouts, paths).

2. **Compare with Local Docs**:
   - Use `grep` or a custom script to **extract claims** from the local `STANDARDS.md`, `COMPATIBILITY.md`, and `GAPS.md` files.
   - Compare these claims against the **fetched official docs**.

3. **Flag Discrepancies**:
   - If a claim in the local docs **does not match** the official source, the CI check should:
     - **Fail** the build.
     - **Report** the discrepancy (e.g., "Claude Code’s `Bash` timeout is now 3 minutes, but docs say 2 minutes").

4. **Update Docs Automatically (Optional)**:
   - For **version numbers** (e.g., Pi v0.80.6, Vibe v2.24.2), the CI check could:
     - Extract the latest version from the official source (e.g., PyPI for Vibe, GitHub releases for Pi).
     - **Auto-update** the local docs if the version has changed.

#### Example CI Check Pseudocode
```bash
#!/bin/bash
# Example: Validate Claude Code's Bash timeout claim
OFFICIAL_TIMEOUT=$(curl -s https://code.claude.com/docs/en/env-vars | grep -oP 'BASH_DEFAULT_TIMEOUT_MS.*?\[0-9\]+' | head -1)
LOCAL_CLAIM=$(grep -oP 'BASH_DEFAULT_TIMEOUT_MS.*?\[0-9\]+' docs/multi-agent/COMPATIBILITY.md | head -1)

if [ "$OFFICIAL_TIMEOUT" != "$LOCAL_CLAIM" ]; then
  echo "❌ Discrepancy: Official timeout is $OFFICIAL_TIMEOUT, but docs say $LOCAL_CLAIM"
  exit 1
fi

echo "✅ Claims are up-to-date"
```

#### Tools for CI Checks
| **Tool** | **Purpose** | **Example** |
|---------|-------------|-------------|
| `curl` | Fetch official docs | `curl -s https://agentskills.io/specification` |
| `grep` / `ripgrep` | Extract claims | `rg 'BASH_DEFAULT_TIMEOUT_MS' docs/` |
| `jq` | Parse JSON docs (e.g., MCP spec) | `curl -s https://modelcontextprotocol.io/specification/2026-07-28.json | jq '.tools[]'` |
| `yq` | Parse YAML docs | `yq eval '.tools' docs.yaml` |
| `diff` | Compare versions | `diff <(curl -s URL) local_file.md` |

---

### 3. Manual Validation Process

If you prefer **manual validation**, follow this checklist:

#### Quarterly Review (Recommended)
- [ ] **Cross-Tool Standards**:
  - [ ] Check [Agent Skills Spec](https://agentskills.io/specification) for updates.
  - [ ] Check [AGENTS.md Spec](https://agents.md/) for updates.
  - [ ] Check [MCP Spec](https://modelcontextprotocol.io/specification/2026-07-28) for updates.
- [ ] **Claude Code**:
  - [ ] Check [Tools Reference](https://code.claude.com/docs/en/tools-reference) for new/removed tools.
  - [ ] Check [Env Vars Docs](https://code.claude.com/docs/en/env-vars) for timeout/limit changes.
  - [ ] Check [GitHub Releases](https://github.com/anthropics/claude-code/releases) for version updates.
- [ ] **Pi Agent**:
  - [ ] Check [Pi Docs](https://pi.dev/docs/latest) for new/removed tools.
  - [ ] Check [GitHub Releases](https://github.com/earendil-works/pi/releases) for version updates.
  - [ ] Check [Pi News](https://pi.dev/news/releases) for announcements.
- [ ] **Vibe Code**:
  - [ ] Check [Mistral Docs](https://docs.mistral.ai) for new/removed tools.
  - [ ] Check [GitHub Releases](https://github.com/mistralai/mistral-vibe/releases) for version updates.
  - [ ] Check [PyPI](https://pypi.org/project/mistral-vibe/) for version updates.

#### After Major Releases
- [ ] Update **version numbers** in `COMPATIBILITY.md`.
- [ ] Update **new/removed tools** in the comparison tables.
- [ ] Update **new/changed behaviors** (e.g., timeouts, paths).
- [ ] Test **this repo’s skills/subagents** with the new versions.

---

### 4. Updating the Documentation

When updating the docs:

1. **Edit the Source Files**:
   - Update the relevant file (`STANDARDS.md`, `COMPATIBILITY.md`, or `GAPS.md`).
   - **Preserve the structure** (tables, headings, official source links).

2. **Add a Changelog Entry**:
   - Update the **Changelog** table at the bottom of the modified file.
   - Example:
     ```markdown
     | **Date**       | **Change**                          | **Author**   |
     |----------------|------------------------------------|--------------|
     | 2026-09-01     | Updated Pi Agent version to v0.81.0 | @contributor |
     ```

3. **Test the Changes**:
   - Verify that **all links** still work.
   - Verify that **claims are accurate** against the official sources.
   - Test **this repo’s skills/subagents** with the updated agents.

4. **Commit and Push**:
   ```bash
   git add docs/multi-agent/
   git commit -m "docs: update multi-agent standards for <tool> v<version>"
   git push origin HEAD
   ```

---

## 📅 Maintenance Schedule

| **Task** | **Frequency** | **Responsible** | **Notes** |
|----------|---------------|-----------------|-----------|
| Monitor official sources | Weekly | Maintainers | Watch GitHub repos for updates. |
| Validate claims | Quarterly | Maintainers | Manual or automated check. |
| Update docs | As needed | Contributors | After major releases or discrepancies. |
| Test skills/subagents | Quarterly | Maintainers | Ensure compatibility with latest agent versions. |

---

## 🤝 Contributing to Maintenance

### Reporting Issues
If you find a **discrepancy** between the docs and official sources:
1. **Open an issue** in this repo with:
   - The **incorrect claim** in the docs.
   - The **official source** that contradicts it.
   - The **correct claim** (if known).
2. **Label the issue** as `docs` and `multi-agent`.

### Submitting Updates
If you want to **update the docs**:
1. **Fork this repo** and create a branch.
2. **Update the relevant file(s)** with the correct claims.
3. **Add official source links** for every change.
4. **Test the changes** (see above).
5. **Submit a PR** with a clear description of the updates.

---

## 📚 Resources

### Official Sources
- [Agent Skills Specification](https://agentskills.io/specification)
- [AGENTS.md Specification](https://agents.md/)
- [MCP Specification](https://modelcontextprotocol.io/specification/2026-07-28)
- [Claude Code Docs](https://code.claude.com/docs)
- [Pi Agent Docs](https://pi.dev/docs)
- [Vibe Code Docs](https://docs.mistral.ai)

### Unofficial Resources
- [Claude Code System Prompts](https://github.com/Piebald-AI/claude-code-system-prompts) (Tool descriptions)
- [Vibe Code DeepWiki](https://deepwiki.com/mistralai/mistral-vibe/) (Implementation details)
- [Pi Agent DeepWiki](https://deepwiki.com/agentic-dev-io/pi-agent/) (Tool internals)

---

## 📝 Changelog

| **Date** | **Change** | **Author** |
|----------|------------|------------|
| 2026-08-21 | Initial maintenance guide | Vibe Code |
