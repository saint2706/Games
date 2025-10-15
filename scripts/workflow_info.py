#!/usr/bin/env python3
"""Display information about GitHub Actions workflows.

This script provides detailed information about workflows including:
- Trigger events
- Jobs and dependencies
- Required permissions
- Environment variables
- Actions used
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


def get_workflow_info(workflow_path: Path) -> dict:
    """Extract information from a workflow file."""
    with open(workflow_path) as f:
        workflow = yaml.safe_load(f)

    info = {
        "name": workflow.get("name", "Unnamed"),
        "file": workflow_path.name,
        "triggers": [],
        "jobs": {},
        "permissions": workflow.get("permissions", {}),
        "env": workflow.get("env", {}),
        "actions": set(),
        "concurrency": workflow.get("concurrency", {}),
    }

    # Parse triggers (handle 'on' being parsed as True)
    triggers = workflow.get("on") or workflow.get(True)
    if isinstance(triggers, dict):
        info["triggers"] = list(triggers.keys())
    elif isinstance(triggers, list):
        info["triggers"] = triggers
    elif isinstance(triggers, str):
        info["triggers"] = [triggers]

    # Parse jobs
    jobs = workflow.get("jobs", {})
    for job_name, job_config in jobs.items():
        if isinstance(job_config, dict):
            info["jobs"][job_name] = {
                "runs_on": job_config.get("runs-on", "unknown"),
                "steps": len(job_config.get("steps", [])),
                "needs": job_config.get("needs", []),
                "if": job_config.get("if", ""),
                "timeout": job_config.get("timeout-minutes", "default"),
            }

            # Extract actions used
            for step in job_config.get("steps", []):
                if isinstance(step, dict) and "uses" in step:
                    info["actions"].add(step["uses"])

    return info


def print_workflow_info(info: dict, verbose: bool = False) -> None:
    """Print workflow information in a readable format."""
    print(f"\n📋 {info['name']}")
    print("=" * 60)
    print(f"File: {info['file']}")

    # Triggers
    print(f"\n🎯 Triggers: {', '.join(info['triggers']) or 'None'}")

    # Permissions
    if info["permissions"]:
        print("\n🔒 Permissions:")
        for perm, level in info["permissions"].items():
            print(f"   • {perm}: {level}")

    # Environment variables
    if info["env"]:
        print("\n🌍 Environment Variables:")
        for key, value in info["env"].items():
            print(f"   • {key}: {value}")

    # Jobs
    print(f"\n⚙️  Jobs ({len(info['jobs'])}):")
    for job_name, job_info in info["jobs"].items():
        print(f"\n   {job_name}:")
        print(f"      Runs on: {job_info['runs_on']}")
        print(f"      Steps: {job_info['steps']}")
        if job_info["needs"]:
            needs = job_info["needs"] if isinstance(job_info["needs"], list) else [job_info["needs"]]
            print(f"      Depends on: {', '.join(needs)}")
        if job_info["if"]:
            print(f"      Condition: {job_info['if']}")
        if job_info["timeout"] != "default":
            print(f"      Timeout: {job_info['timeout']} minutes")

    # Concurrency
    if info["concurrency"]:
        group = info["concurrency"].get("group", "<dynamic>")
        cancel = info["concurrency"].get("cancel-in-progress", False)
        print("\n🕒 Concurrency:")
        print(f"   • Group: {group}")
        print(f"   • Cancel in progress: {cancel}")

    # Actions
    if verbose and info["actions"]:
        print(f"\n🔌 Actions Used ({len(info['actions'])}):")
        for action in sorted(info["actions"]):
            print(f"   • {action}")


def list_all_workflows(workflow_dir: Path, verbose: bool = False) -> None:
    """List all workflows with basic information."""
    workflow_files = sorted(workflow_dir.glob("*.yml"))

    print("\n📁 Available Workflows")
    print("=" * 60)

    for workflow_file in workflow_files:
        try:
            info = get_workflow_info(workflow_file)
            print(f"\n{info['name']}")
            print(f"   File: {info['file']}")
            print(f"   Triggers: {', '.join(info['triggers'])}")
            print(f"   Jobs: {len(info['jobs'])}")

            if verbose:
                print(f"   Actions: {len(info['actions'])}")
                print(f"   Permissions: {len(info['permissions'])}")

        except Exception as e:
            print(f"\n{workflow_file.name}")
            print(f"   Error: {e}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Display information about GitHub Actions workflows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all workflows
  python scripts/workflow_info.py

  # Show detailed info for specific workflow
  python scripts/workflow_info.py ci.yml

  # Show verbose information
  python scripts/workflow_info.py ci.yml -v
        """,
    )

    parser.add_argument("workflow", nargs="?", help="Workflow file name (e.g., ci.yml)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed information")
    parser.add_argument("-a", "--all", action="store_true", help="List all workflows")

    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    workflow_dir = repo_root / ".github" / "workflows"

    if not workflow_dir.exists():
        print(f"Error: Workflow directory not found: {workflow_dir}")
        return 1

    if args.all or not args.workflow:
        list_all_workflows(workflow_dir, args.verbose)
        return 0

    # Show specific workflow
    workflow_path = workflow_dir / args.workflow
    if not workflow_path.exists():
        print(f"Error: Workflow file not found: {workflow_path}")
        print("\nAvailable workflows:")
        for wf in workflow_dir.glob("*.yml"):
            print(f"  • {wf.name}")
        return 1

    try:
        info = get_workflow_info(workflow_path)
        print_workflow_info(info, args.verbose)
        return 0
    except Exception as e:
        print(f"Error reading workflow: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
