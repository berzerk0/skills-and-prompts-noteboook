#!/usr/bin/env python3
"""
Find skills that haven't been invoked recently (B3: Retirement Sweep).

This script identifies skills that are not being used, so you can decide
whether to keep, archive, or delete them. Dead skills consume tokens
(their descriptions are always resident in the prompt) and can mislead
the model's routing decisions.

Usage:
  python3 scripts/find-unused-skills.py              # Find truly unused skills
  python3 scripts/find-unused-skills.py --days 30    # Find skills unused for 30+ days
  python3 scripts/find-unused-skills.py --verbose    # Show invocation counts
"""

import sys
import os
import re
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional


def find_skill_files(repo_root: Path) -> List[Path]:
    """Find all SKILL.md files in the repository."""
    skills_dir = repo_root / "skills"
    if not skills_dir.exists():
        return []
    return sorted(skills_dir.glob("*/SKILL.md"))


def extract_skill_name(skill_file: Path) -> str:
    """Extract skill name from directory (or frontmatter if needed)."""
    return skill_file.parent.name


def search_invocations_in_git(
    repo_root: Path,
    skill_name: str,
    since_days: Optional[int] = None
) -> Tuple[int, Optional[str]]:
    """
    Search git history for invocations of a skill.

    Returns: (invocation_count, last_invocation_date)
    """
    import subprocess

    # Look for patterns that indicate skill invocation:
    # - /skill-name (slash command)
    # - /[skill-name (in plan/outline)
    # - skill-name in SKILL.md context (skill loading)
    # - Skill(...) with skill_name parameter

    patterns = [
        f"/{skill_name}",  # slash command invocation
        f"/[{skill_name}",  # in plan
        f"{{skill_name}}",  # in SKILL context
        f"skill.*{skill_name}",  # skill loading mention
    ]

    # Use git log to search
    try:
        # Count invocations
        cmd = ["git", "log", "--all", "--oneline", "--"]
        if since_days:
            cmd.insert(2, f"--since={since_days} days ago")

        # This is a simplified search; a more robust version would parse git logs
        # For now, return a placeholder indicating this needs manual verification
        return 0, None
    except subprocess.CalledProcessError:
        return 0, None


def check_skill_invocations(
    repo_root: Path,
    skill_file: Path,
    since_days: Optional[int] = None,
    verbose: bool = False
) -> Tuple[str, int, bool]:
    """
    Check if a skill has been invoked recently.

    Returns: (skill_name, invocation_count, is_active)
    """
    skill_name = extract_skill_name(skill_file)

    # TODO: This requires:
    # 1. Hook-generated invocation logs (which don't yet exist in this repo)
    # 2. Git history analysis (expensive)
    # 3. Session logs (not yet structured)

    # For now, return placeholder
    invocation_count = 0
    is_active = False  # Placeholder

    return skill_name, invocation_count, is_active


def main():
    parser = argparse.ArgumentParser(
        description="Find unused skills (B3: Retirement Sweep)"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Consider skills unused if not invoked in N days (default: 30)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show invocation counts"
    )
    parser.add_argument(
        "--show-all",
        action="store_true",
        help="Show all skills, not just unused ones"
    )

    args = parser.parse_args()

    # Determine repo root
    repo_root = Path.cwd()
    while repo_root.parent != repo_root:
        if (repo_root / ".git").exists():
            break
        repo_root = repo_root.parent

    if not (repo_root / ".git").exists():
        print("Error: Not in a git repository")
        sys.exit(1)

    # Find skills
    skill_files = find_skill_files(repo_root)

    if not skill_files:
        print("No skills found")
        return 0

    print(f"Checking {len(skill_files)} skills for invocation history...\n")
    print("⚠️  Note: This feature requires hook-generated logs (not yet in place).")
    print("   Currently, this script is a template.\n")

    unused_skills = []
    active_skills = []

    for skill_file in skill_files:
        skill_name, count, is_active = check_skill_invocations(
            repo_root,
            skill_file,
            since_days=args.days,
            verbose=args.verbose
        )

        if is_active or args.show_all:
            active_skills.append((skill_name, count))
        else:
            unused_skills.append((skill_name, count))

    # Report
    if unused_skills:
        print(f"🗑️  Unused skills (last invoked >30 days ago or never):\n")
        for skill_name, count in sorted(unused_skills):
            print(f"  - {skill_name}")
            if args.verbose:
                print(f"    (invoked {count} times)")
        print()

    if args.show_all and active_skills:
        print(f"✓ Active skills (invoked in last 30 days):\n")
        for skill_name, count in sorted(active_skills):
            print(f"  - {skill_name}")
            if args.verbose:
                print(f"    ({count} invocations)")
        print()

    print("📋 Recommendation:")
    print("  1. Review unused skills to decide if they should be deleted")
    print("  2. Archive valuable skills you want to keep but aren't using now")
    print("  3. Delete skills that are clearly obsolete")
    print("  4. Move archived skills to ARCHIVE.md as documentation")
    print()
    print("⏳ This script will be fully functional once hook logging is in place.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
