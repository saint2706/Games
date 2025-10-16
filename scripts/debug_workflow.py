#!/usr/bin/env python3
"""Debug GitHub Actions workflow execution.

This script helps debug why certain workflow jobs are being skipped by:
- Analyzing job conditions
- Checking trigger events
- Simulating workflow execution scenarios
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


def _find_workflow_file(workflow_name: str) -> Path:
    """Find a workflow file by name, searching common locations."""
    if ".yml" not in workflow_name and ".yaml" not in workflow_name:
        workflow_name += ".yml"

    # Start search from the script's directory and go up
    current_dir = Path(__file__).parent.resolve()
    for directory in [current_dir, *current_dir.parents]:
        workflow_path = directory / ".github" / "workflows" / workflow_name
        if workflow_path.exists():
            return workflow_path

    raise FileNotFoundError(f"Workflow file '{workflow_name}' not found in any '.github/workflows' directory.")


def analyze_job_conditions(workflow_path: Path, workflow_data: dict) -> None:
    """Analyze job conditions in a workflow."""
    print(f"\n🔍 Analyzing: {workflow_data.get('name', 'Unnamed')}")
    print("=" * 60)

    triggers = workflow_data.get("on", {})
    print("\n🎯 Trigger Events:")
    if isinstance(triggers, dict):
        for trigger, config in triggers.items():
            print(f"   • {trigger}")
            if isinstance(config, dict):
                if "branches" in config:
                    print(f"     Branches: {config['branches']}")
                if "tags" in config:
                    print(f"     Tags: {config['tags']}")
    elif isinstance(triggers, list):
        for trigger in triggers:
            print(f"   • {trigger}")

    jobs = workflow_data.get("jobs", {})
    print(f"\n⚙️  Jobs ({len(jobs)}):")
    for job_name, job_config in jobs.items():
        if not isinstance(job_config, dict):
            continue
        condition = job_config.get("if", "")
        print(f"\n   📦 {job_name}:")
        print(f"      Runs on: {job_config.get('runs-on', 'unknown')}")
        if condition:
            print(f"      ⚠️  Condition: {condition}")
            _analyze_condition(condition)


def _analyze_condition(condition: str) -> None:
    """Analyze a job condition and explain when it runs."""
    print("        Explanation:")
    if "startsWith(github.ref, 'refs/tags/v')" in condition:
        print("           • Runs ONLY when a tag starting with 'v' is pushed.")
    elif "github.event_name == 'release'" in condition:
        print("           • Runs ONLY on release events.")
    elif "github.event_name == 'pull_request'" in condition:
        print("           • Runs ONLY on pull request events.")
    elif "github.ref == 'refs/heads/main'" in condition:
        print("           • Runs ONLY on the main branch.")
    else:
        print("           • Custom condition - check workflow logs for details.")


def suggest_fixes(workflow_data: dict) -> None:
    """Suggest fixes for common issues."""
    print("\n💡 Suggestions:")
    for job_name, job_config in workflow_data.get("jobs", {}).items():
        if not isinstance(job_config, dict):
            continue
        condition = job_config.get("if", "")
        if "startsWith(github.ref, 'refs/tags/v')" in condition:
            print(f"\n   {job_name}:")
            print("      Current: Runs only on version tags (v*)")
            print("      To test without a tag, temporarily remove the 'if' condition.")


def simulate_execution(workflow_data: dict, event_type: str, ref: str) -> None:
    """Simulate workflow execution for a given event."""
    print("\n🎬 Simulating Execution:")
    print(f"Event: {event_type}, Ref: {ref}")
    print("=" * 60)

    triggers = workflow_data.get("on", {})
    if not isinstance(triggers, (dict, list)):
        print("❌ Invalid 'on' trigger configuration.")
        return

    if isinstance(triggers, list) and event_type not in triggers:
        print("❌ Workflow would NOT run - event does not match triggers.")
        return

    print("\n⚙️  Job Execution Status:")
    for job_name, job_config in workflow_data.get("jobs", {}).items():
        if not isinstance(job_config, dict):
            continue
        condition = job_config.get("if", "")
        if not condition:
            print(f"   ✅ {job_name}: RUNS (no condition)")
            continue
        would_run = _evaluate_condition(condition, event_type, ref)
        status = "✅ RUNS" if would_run else "⏭️  SKIPPED"
        print(f"   {status} {job_name}: {condition}")


def _evaluate_condition(condition: str, event_type: str, ref: str) -> bool:
    """Simple evaluation of common conditions."""
    if "startsWith(github.ref, 'refs/tags/v')" in condition:
        return ref.startswith("refs/tags/v")
    if "github.event_name == 'release'" in condition:
        return event_type == "release"
    if "github.event_name == 'pull_request'" in condition:
        return event_type == "pull_request"
    if "github.ref == 'refs/heads/main'" in condition:
        return ref == "refs/heads/main"
    # Default to False for complex conditions
    return False


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Debug GitHub Actions workflow execution.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("workflow", help="Workflow file name (e.g., build-executables.yml).")
    parser.add_argument("--simulate", help="Simulate execution for an event type.")
    parser.add_argument("--ref", default="refs/heads/main", help="Git ref for simulation.")
    parser.add_argument("--suggest", action="store_true", help="Show fix suggestions.")
    args = parser.parse_args()

    try:
        workflow_path = _find_workflow_file(args.workflow)
        workflow_data = yaml.safe_load(workflow_path.read_text())

        analyze_job_conditions(workflow_path, workflow_data)
        if args.simulate:
            simulate_execution(workflow_data, args.simulate, args.ref)
        if args.suggest:
            suggest_fixes(workflow_data)

        return 0
    except (FileNotFoundError, yaml.YAMLError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
