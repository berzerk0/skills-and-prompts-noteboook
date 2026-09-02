#!/usr/bin/env python3
"""
Generate Vibe Code agent wrappers from canonical YAML definitions.

Usage:
    python meta/generate_vibe.py [--all | --skill SKILL_NAME]
    
Examples:
    # Generate all skills
    python meta/generate_vibe.py --all
    
    # Generate a specific skill
    python meta/generate_vibe.py --skill timestamp
"""

import argparse
from pathlib import Path

import yaml

# Repository root
REPO_ROOT = Path(__file__).parent.parent

# Directories
AGENTS_DIR = REPO_ROOT / "agents"
VIBE_AGENTS_DIR = REPO_ROOT / ".vibe" / "agents"

# Default model for Vibe
DEFAULT_MODEL = "mistral-small"


def load_yaml(skill_name: str) -> dict:
    """Load canonical YAML definition for a skill."""
    yaml_path = AGENTS_DIR / f"{skill_name}.yaml"
    if not yaml_path.exists():
        raise FileNotFoundError(f"Canonical YAML not found: {yaml_path}")
    
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)


def generate_agent_toml(skill_name: str, data: dict) -> str:
    """Generate Vibe Code agent TOML file."""
    name = data.get('name', skill_name)
    description = data.get('description', '')
    model = data.get('model', DEFAULT_MODEL)
    
    # Map skill type to enabled tools
    skill_type = data.get('skill_type', '')
    
    # For Vibe Code, we need to determine which tools to enable
    # Vibe uses different tool names than Claude and Pi
    tools_to_enable = []
    
    if skill_type in ['type_b', 'type_c']:
        # API client and file operations
        tools_to_enable = ['python', 'bash', 'read_file', 'write_file', 'edit', 'grep']
    elif skill_type == 'type_a':
        # Pure function - minimal tools
        tools_to_enable = ['python', 'bash']
    else:
        tools_to_enable = ['python', 'bash', 'read_file', 'write_file', 'edit', 'grep']
    
    # Add tools based on operations
    operations = data.get('operations', [])
    for op in operations:
        if op.get('requires_file_access', False):
            if 'read_file' not in tools_to_enable:
                tools_to_enable.append('read_file')
            if 'write_file' not in tools_to_enable:
                tools_to_enable.append('write_file')
            if 'edit' not in tools_to_enable:
                tools_to_enable.append('edit')
    
    # Build TOML content
    toml_content = f"""agent_type = "subagent"
display_name = "{name}"
description = "{description}"
active_model = "{model}"
"""
    
    # Add enabled tools
    for tool in tools_to_enable:
        toml_content += f"\n[{tool}]\n"
        toml_content += f"enabled = true\n"
    
    return toml_content


def write_file(path: Path, content: str) -> None:
    """Write content to a file. Refuses to write through a symlink.
    
    Never write through a symlink: .claude/skills, .pi/skills, .vibe/skills
    are symlink farms pointing at the canonical skills/ library. Writing
    through one silently overwrites the canonical file (see: the 2026-08-24
    incident that flattened all 14 SKILL.md files to stubs).
    Generators must only write per-agent wrapper files, never skill bodies.
    """
    # Never write through a symlink: .claude/skills, .pi/skills, .vibe/skills
    # are symlink farms pointing at the canonical skills/ library. Writing
    # through one silently overwrites the canonical file (see: the 2026-08-24
    # incident that flattened all 14 SKILL.md files to stubs).
    resolved = path.resolve()
    canonical_skills = (REPO_ROOT / "skills").resolve()
    
    # Check if resolved path is inside canonical skills directory
    try:
        resolved.relative_to(canonical_skills)
        raise RuntimeError(
            f"Refusing to write {path} -- it resolves to {resolved}, "
            f"inside the canonical skills/ library. Generators must only "
            f"write per-agent wrapper files, never skill bodies."
        )
    except ValueError:
        # Not inside canonical skills, check parent symlinks
        pass
    
    # Check if any parent is a symlink
    for parent in path.parents:
        if parent.is_symlink():
            raise RuntimeError(
                f"Refusing to write {path} -- parent {parent} is a symlink."
            )
    
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"  \u2713 Written: {path}")


def generate_skill(skill_name: str) -> None:
    """Generate all Vibe Code files for a skill."""
    print(f"\nGenerating Vibe Code files for: {skill_name}")
    
    try:
        data = load_yaml(skill_name)
    except FileNotFoundError as e:
        print(f"  \u26a0 Skipping: {e}")
        return
    
    # Generate agent TOML
    agent_content = generate_agent_toml(skill_name, data)
    agent_path = VIBE_AGENTS_DIR / f"{skill_name}.toml"
    write_file(agent_path, agent_content)
    
    print(f"  \u2713 Generated agent: {agent_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate Vibe Code agent wrappers from canonical YAML'
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
    VIBE_AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    
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
        
        print("\n\u2713 All Vibe Code files generated")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
