#!/usr/bin/env python3
"""
Generate Pi Agent wrappers from canonical YAML definitions.

Usage:
    python meta/generate_pi.py [--all | --skill SKILL_NAME]
    
Examples:
    # Generate all skills
    python meta/generate_pi.py --all
    
    # Generate a specific skill
    python meta/generate_pi.py --skill timestamp
"""

import argparse
import os
from pathlib import Path

import yaml

# Repository root
REPO_ROOT = Path(__file__).parent.parent

# Directories
AGENTS_DIR = REPO_ROOT / "agents"
PI_AGENTS_DIR = REPO_ROOT / ".pi" / "agents"
PI_SKILLS_DIR = REPO_ROOT / ".pi" / "skills"

# Tool names for Pi Agent
PI_TOOLS = ["read", "write", "edit", "bash", "grep", "find", "ls"]

# Default model for Pi
DEFAULT_MODEL = "gpt-4o-mini"


def load_yaml(skill_name: str) -> dict:
    """Load canonical YAML definition for a skill."""
    yaml_path = AGENTS_DIR / f"{skill_name}.yaml"
    if not yaml_path.exists():
        raise FileNotFoundError(f"Canonical YAML not found: {yaml_path}")
    
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)


def generate_agent_md(skill_name: str, data: dict) -> str:
    """Generate Pi Agent markdown file."""
    name = data.get('name', skill_name)
    description = data.get('description', '')
    
    # Determine tools based on skill type and operations
    tools = []
    skill_type = data.get('skill_type', '')
    
    if skill_type in ['type_b', 'type_c']:
        # API client and file operations need more tools
        tools = PI_TOOLS.copy()
    elif skill_type == 'type_a':
        # Pure function skills need fewer tools
        tools = ["bash"]
    else:
        tools = PI_TOOLS.copy()
    
    # Add any explicitly required tools from operations
    operations = data.get('operations', [])
    for op in operations:
        if op.get('requires_file_access', False):
            if "read" not in tools:
                tools.append("read")
            if "write" not in tools:
                tools.append("write")
            if "edit" not in tools:
                tools.append("edit")
    
    # Deduplicate while preserving order
    seen = set()
    unique_tools = []
    for tool in tools:
        if tool not in seen:
            seen.add(tool)
            unique_tools.append(tool)
    
    # Format tools as YAML array
    tools_str = "\n  - " + "\n  - ".join(unique_tools) if unique_tools else "[]"
    
    # Get model preference
    model = data.get('model', DEFAULT_MODEL)
    
    # Build the markdown content
    md_content = f"""---
name: {name}
description: {description}
tools: {tools_str}
model: {model}
---

# {name.capitalize()} Agent

{description}

## Usage

You are a {name} assistant. Use the {data.get('implementation_module', f'{name}_skill.py')} module.
"""
    
    # Add implementation reference
    impl_module = data.get('implementation_module', f'{name}_skill.py')
    if impl_module:
        md_content += f"\nImplementation: `from {impl_module.replace('.py', '')} import {data.get('implementation_function', 'main')}`\n"
    
    # Add triggers
    triggers = data.get('triggers', [])
    if triggers:
        md_content += "\n## Trigger Conditions\n\n"
        for trigger in triggers:
            md_content += f"- {trigger}\n"
    
    # Add operations
    if operations:
        md_content += "\n## Available Operations\n\n"
        for op in operations:
            op_name = op.get('name', '')
            op_desc = op.get('description', '')
            if op_name and op_desc:
                md_content += f"- **{op_name}**: {op_desc}\n"
    
    # Add authentication info
    auth = data.get('authentication', {})
    if auth.get('required', False):
        env_var = auth.get('env_var', '')
        if env_var:
            md_content += f"\n## Authentication\n\n"
            md_content += f"Set the {env_var} environment variable for authentication.\n"
    
    return md_content


def generate_skill_md(skill_name: str, data: dict) -> str:
    """Generate portable SKILL.md file for Pi Agent."""
    name = data.get('name', skill_name)
    description = data.get('description', '')
    license = data.get('license', 'MIT')
    compatibility = data.get('compatibility', ['claude', 'pi', 'vibe'])
    
    # Format compatibility as YAML array
    compat_str = "\n  - " + "\n  - ".join(compatibility) if compatibility else "[]"
    
    # Build the markdown content
    md_content = f"""---
name: {name}
description: {description}
license: {license}
compatibility: {compat_str}
---

{description}

"""
    
    # Add implementation reference
    impl_module = data.get('implementation_module', f'{name}_skill.py')
    impl_func = data.get('implementation_function', 'main')
    if impl_module:
        md_content += f"Implementation: `from {impl_module.replace('.py', '')} import {impl_func}`\n"
    
    # Add usage section
    triggers = data.get('triggers', [])
    if triggers:
        md_content += "\n## When to Use\n\n"
        for trigger in triggers:
            md_content += f"- {trigger}\n"
    
    # Add output format if specified
    output_format = data.get('output_format', '')
    if output_format:
        md_content += f"\n## Output Format\n\n{output_format}\n"
    
    return md_content


def write_file(path: Path, content: str) -> None:
    """Write content to a file, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"  ✓ Written: {path}")


def generate_skill(skill_name: str) -> None:
    """Generate all Pi Agent files for a skill."""
    print(f"\nGenerating Pi Agent files for: {skill_name}")
    
    try:
        data = load_yaml(skill_name)
    except FileNotFoundError as e:
        print(f"  ⚠ Skipping: {e}")
        return
    
    # Generate agent markdown
    agent_content = generate_agent_md(skill_name, data)
    agent_path = PI_AGENTS_DIR / f"{skill_name}.md"
    write_file(agent_path, agent_content)
    
    # Generate skill markdown
    skill_content = generate_skill_md(skill_name, data)
    skill_dir = PI_SKILLS_DIR / skill_name
    skill_path = skill_dir / "SKILL.md"
    write_file(skill_path, skill_content)
    
    print(f"  ✓ Generated agent: {agent_path}")
    print(f"  ✓ Generated skill: {skill_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate Pi Agent wrappers from canonical YAML'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Generate all skills'
    )
    parser.add_argument(
        '--skill',
        type=str,
        help='Generate a specific skill'
    )
    args = parser.parse_args()
    
    # Ensure output directories exist
    PI_AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    PI_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    
    if args.skill:
        # Generate specific skill
        generate_skill(args.skill)
    elif args.all:
        # Generate all skills
        yaml_files = list(AGENTS_DIR.glob("*.yaml"))
        if not yaml_files:
            print("No YAML files found in agents/ directory")
            return
        
        print(f"Found {len(yaml_files)} canonical YAML definitions")
        for yaml_file in yaml_files:
            skill_name = yaml_file.stem
            generate_skill(skill_name)
        
        print("\n✓ All Pi Agent files generated")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
