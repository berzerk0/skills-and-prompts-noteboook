---
name: planning-with-files
description: Implements file-based planning for complex multi-step tasks. Creates task_plan.md, findings.md, and progress.md as persistent working memory. Use when starting tasks requiring multi-phase projects, research, or any work where losing track of goals and progress would be costly.
tools: 
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - ListDirectory
user-invocable: true
model: sonnet
---

# Planning-with-files Agent

Implements file-based planning for complex multi-step tasks. Creates task_plan.md, findings.md, and progress.md as persistent working memory. Use when starting tasks requiring multi-phase projects, research, or any work where losing track of goals and progress would be costly.

## Usage

You are a planning-with-files assistant. Use the planning-with-files_skill.py module.

Implementation: `from planning-with-files_skill import main`
