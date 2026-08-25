#!/usr/bin/env python3
"""
Validate tool names in skill files against the harness tool registry.

This script checks that all declared `allowed-tools` in skill frontmatter
are valid for the target harnesses. It catches silent-drop failures (e.g.,
Vibe silently dropping unrecognized tool names) before the skill is committed.

Usage:
  python notebooks/behaviors/validate-tool-names.py                    # check all skills
  python notebooks/behaviors/validate-tool-names.py skills/*/SKILL.md  # check specific skills
  python notebooks/behaviors/validate-tool-names.py --harness vibe     # check for Vibe only
"""

import sys
import os
import yaml
import argparse
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple

def load_registry(repo_root: Path) -> Dict:
    """Load the tool registry from notebooks/behaviors/tools-registry.yaml"""
    registry_path = repo_root / "notebooks/behaviors/tools-registry.yaml"
    if not registry_path.exists():
        raise FileNotFoundError(f"Tool registry not found at {registry_path}")

    with open(registry_path) as f:
        return yaml.safe_load(f)

def extract_frontmatter(skill_file: Path) -> Tuple[Dict, str]:
    """Extract YAML frontmatter from a skill file."""
    with open(skill_file) as f:
        content = f.read()

    # Find frontmatter between --- markers
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return {}, content

    frontmatter_text = match.group(1)
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        return frontmatter or {}, content
    except yaml.YAMLError as e:
        print(f"Error parsing frontmatter in {skill_file}: {e}", file=sys.stderr)
        return {}, content

def find_skill_files(repo_root: Path, pattern: List[str] = None) -> List[Path]:
    """Find all SKILL.md files in the repository."""
    if pattern:
        # If specific files given, use those
        files = []
        for p in pattern:
            path = Path(p)
            if path.is_absolute():
                files.append(path)
            else:
                files.append(repo_root / p)
        return [f for f in files if f.exists()]
    else:
        # Find all SKILL.md files
        skills_dir = repo_root / "skills"
        if not skills_dir.exists():
            return []
        return sorted(skills_dir.glob("*/SKILL.md"))

def tool_matches_pattern(tool: str, pattern: str) -> bool:
    """Check if a tool name matches a pattern (supports wildcards)."""
    if '*' not in pattern:
        return tool == pattern
    # Simple wildcard matching: pattern can end with *
    if pattern.endswith('*'):
        prefix = pattern[:-1]
        return tool.startswith(prefix)
    return False

def validate_skill(
    skill_file: Path,
    registry: Dict,
    harnesses: List[str] = None
) -> Tuple[bool, List[str]]:
    """
    Validate a single skill file.

    Returns (is_valid, [list of error messages])
    """
    if harnesses is None:
        harnesses = list(registry["harnesses"].keys())

    errors = []
    frontmatter, _ = extract_frontmatter(skill_file)

    # Check if skill has allowed-tools
    allowed_tools = frontmatter.get("allowed-tools", [])
    if not allowed_tools:
        # No tools declared, nothing to validate
        return True, []

    # For each harness, check if all declared tools are valid
    for harness in harnesses:
        if harness not in registry["harnesses"]:
            errors.append(f"Unknown harness: {harness}")
            continue

        valid_tools = registry["harnesses"][harness]["tools"]

        for tool in allowed_tools:
            # Check if tool matches any valid pattern (including wildcards)
            is_valid = any(tool_matches_pattern(tool, vt) for vt in valid_tools)

            if not is_valid:
                # Check if this is a silent-drop situation
                if harness in registry.get("silent-drop-harnesses", []):
                    errors.append(
                        f"Tool '{tool}' not available in {harness} "
                        f"(will be silently dropped!) "
                        f"Valid tools: {', '.join(sorted(valid_tools))}"
                    )
                else:
                    errors.append(
                        f"Tool '{tool}' not available in {harness}. "
                        f"Valid tools: {', '.join(sorted(valid_tools))}"
                    )

    return len(errors) == 0, errors

def main():
    parser = argparse.ArgumentParser(
        description="Validate tool names in skill files"
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Skill files to check (default: all in skills/ directory)"
    )
    parser.add_argument(
        "--harness",
        action="append",
        dest="harnesses",
        help="Check only for specific harness(es) (can be used multiple times)"
    )
    parser.add_argument(
        "--fail-on-error",
        action="store_true",
        help="Exit with code 1 if any errors found"
    )
    parser.add_argument(
        "--show-valid",
        action="store_true",
        help="Show valid skills in output"
    )

    args = parser.parse_args()

    # Determine repo root
    repo_root = Path.cwd()
    while repo_root.parent != repo_root:
        if (repo_root / "notebooks/behaviors/tools-registry.yaml").exists():
            break
        repo_root = repo_root.parent

    if not (repo_root / "notebooks/behaviors/tools-registry.yaml").exists():
        print("Error: notebooks/behaviors/tools-registry.yaml not found. Are you in the repo root?")
        sys.exit(1)

    # Load registry
    try:
        registry = load_registry(repo_root)
    except Exception as e:
        print(f"Error loading registry: {e}", file=sys.stderr)
        sys.exit(1)

    # Find skills to check
    skill_files = find_skill_files(repo_root, args.files if args.files else None)

    if not skill_files:
        print("No skill files found to check")
        return 0

    # Validate each skill
    all_valid = True
    error_count = 0
    valid_count = 0

    for skill_file in skill_files:
        is_valid, errors = validate_skill(
            skill_file,
            registry,
            args.harnesses or None
        )

        if is_valid:
            valid_count += 1
            if args.show_valid:
                print(f"✓ {skill_file.relative_to(repo_root)}")
        else:
            all_valid = False
            error_count += len(errors)
            skill_name = skill_file.parent.name
            print(f"✗ {skill_file.relative_to(repo_root)}")
            for error in errors:
                print(f"  {error}")

    # Summary
    print(f"\nValidation complete: {valid_count} valid, {error_count} errors")

    if not all_valid and args.fail_on_error:
        sys.exit(1)

    return 0 if all_valid else 2

if __name__ == "__main__":
    sys.exit(main())
