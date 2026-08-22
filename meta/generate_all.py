#!/usr/bin/env python3
"""
Master generation script to create all per-agent wrappers from canonical YAML.

Usage:
    python meta/generate_all.py [--all | --skill SKILL_NAME]
    
Examples:
    # Generate all skills for all agents
    python meta/generate_all.py --all
    
    # Generate a specific skill for all agents
    python meta/generate_all.py --skill timestamp
    
    # Validate all YAML files without generating
    python meta/generate_all.py --validate
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Repository root
REPO_ROOT = Path(__file__).parent.parent
AGENTS_DIR = REPO_ROOT / "agents"

# Generation scripts
GENERATION_SCRIPTS = {
    'claude': REPO_ROOT / "meta" / "generate_claude.py",
    'pi': REPO_ROOT / "meta" / "generate_pi.py",
    'vibe': REPO_ROOT / "meta" / "generate_vibe.py",
}


def run_script(script_path: Path, args: list) -> bool:
    """Run a generation script and return success status."""
    cmd = [sys.executable, str(script_path)] + args
    print(f"\n{'='*60}")
    print(f"Running: {' '.join(cmd)}")
    print('='*60)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"STDERR: {result.stderr}", file=sys.stderr)
    
    return result.returncode == 0


def validate_yaml_files() -> bool:
    """Validate all YAML files in the agents directory."""
    import yaml
    
    yaml_files = list(AGENTS_DIR.glob("*.yaml"))
    if not yaml_files:
        print("❌ No YAML files found in agents/ directory")
        return False
    
    print(f"Validating {len(yaml_files)} YAML files...")
    
    all_valid = True
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r') as f:
                data = yaml.safe_load(f)
            
            # Check required fields
            if 'name' not in data:
                print(f"  ❌ {yaml_file.name}: Missing 'name' field")
                all_valid = False
            if 'description' not in data:
                print(f"  ❌ {yaml_file.name}: Missing 'description' field")
                all_valid = False
            
            print(f"  ✓ {yaml_file.name}: Valid")
            
        except yaml.YAMLError as e:
            print(f"  ❌ {yaml_file.name}: Invalid YAML - {e}")
            all_valid = False
        except Exception as e:
            print(f"  ❌ {yaml_file.name}: Error - {e}")
            all_valid = False
    
    return all_valid


def generate_for_skill(skill_name: str) -> bool:
    """Generate wrappers for a specific skill across all agents."""
    all_success = True
    
    for agent_name, script_path in GENERATION_SCRIPTS.items():
        if not script_path.exists():
            print(f"⚠ Script not found: {script_path}")
            continue
        
        success = run_script(script_path, ['--skill', skill_name])
        if not success:
            all_success = False
    
    return all_success


def generate_all() -> bool:
    """Generate wrappers for all skills across all agents."""
    yaml_files = list(AGENTS_DIR.glob("*.yaml"))
    if not yaml_files:
        print("❌ No YAML files found in agents/ directory")
        return False
    
    print(f"Found {len(yaml_files)} skills to generate")
    
    all_success = True
    for yaml_file in yaml_files:
        skill_name = yaml_file.stem
        success = generate_for_skill(skill_name)
        if not success:
            all_success = False
    
    return all_success


def update_symlinks() -> bool:
    """Update symlinks for all skills directories."""
    from pathlib import Path
    
    print("\n" + "="*60)
    print("Updating symlinks for skill discoverability")
    print("="*60)
    
    # Agent-specific skill directories
    agent_skill_dirs = {
        'claude': REPO_ROOT / ".claude" / "skills",
        'pi': REPO_ROOT / ".pi" / "skills",
        'vibe': REPO_ROOT / ".vibe" / "skills",
    }
    
    # Get all skill directories
    skill_dirs = [d for d in (REPO_ROOT / "skills").iterdir() if d.is_dir()]
    
    if not skill_dirs:
        print("❌ No skill directories found in skills/")
        return False
    
    # Remove old symlinks and create new ones
    for agent_name, agent_skills_dir in agent_skill_dirs.items():
        # Remove existing symlinks
        if agent_skills_dir.exists():
            for item in agent_skills_dir.iterdir():
                if item.is_symlink():
                    item.unlink()
                elif item.is_dir():
                    # Remove directory if it's a copied skill
                    import shutil
                    shutil.rmtree(item)
        else:
            agent_skills_dir.mkdir(parents=True, exist_ok=True)
        
        # Create new symlinks
        for skill_dir in skill_dirs:
            skill_name = skill_dir.name
            target = agent_skills_dir / skill_name
            if not target.exists():
                target.symlink_to(f"../../skills/{skill_name}")
                print(f"  ✓ Created symlink: {target} -> ../../skills/{skill_name}")
    
    print("\n✓ All symlinks updated")
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Master generation script for all agent wrappers'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Generate all skills for all agents'
    )
    parser.add_argument(
        '--skill',
        type=str,
        help='Generate a specific skill for all agents'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate YAML files without generating'
    )
    parser.add_argument(
        '--symlinks',
        action='store_true',
        help='Update symlinks for skill discoverability'
    )
    args = parser.parse_args()
    
    if args.validate:
        # Just validate YAML files
        if validate_yaml_files():
            print("\n✓ All YAML files are valid")
            sys.exit(0)
        else:
            print("\n❌ Some YAML files have issues")
            sys.exit(1)
    
    elif args.symlinks:
        # Just update symlinks
        if update_symlinks():
            sys.exit(0)
        else:
            sys.exit(1)
    
    elif args.skill:
        # Generate specific skill
        if generate_for_skill(args.skill):
            print(f"\n✓ Successfully generated '{args.skill}' for all agents")
            sys.exit(0)
        else:
            print(f"\n❌ Failed to generate '{args.skill}'")
            sys.exit(1)
    
    elif args.all:
        # Generate all skills
        if generate_all():
            print("\n✓ Successfully generated all skills for all agents")
            # Also update symlinks
            update_symlinks()
            sys.exit(0)
        else:
            print("\n❌ Failed to generate some skills")
            sys.exit(1)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
