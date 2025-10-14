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


def analyze_job_conditions(workflow_path: Path) -> None:
    """Analyze job conditions in a workflow."""
    with open(workflow_path) as f:
        workflow = yaml.safe_load(f)

    print(f"\n🔍 Analyzing: {workflow.get('name', 'Unnamed')}")
    print("=" * 60)

    # Get trigger events
    triggers = workflow.get("on") or workflow.get(True)
    print("\n🎯 Trigger Events:")
    if isinstance(triggers, dict):
        for trigger, config in triggers.items():
            print(f"   • {trigger}")
            if isinstance(config, dict):
                if "branches" in config:
                    print(f"     Branches: {', '.join(config['branches'])}")
                if "tags" in config:
                    print(f"     Tags: {', '.join(config['tags'])}")
    elif isinstance(triggers, list):
        for trigger in triggers:
            print(f"   • {trigger}")
    elif isinstance(triggers, str):
        print(f"   • {triggers}")

    # Analyze jobs
    jobs = workflow.get("jobs", {})
    print(f"\n⚙️  Jobs ({len(jobs)}):")

    skippable_jobs = []
    always_run_jobs = []

    for job_name, job_config in jobs.items():
        if not isinstance(job_config, dict):
            continue

        condition = job_config.get("if", "")
        needs = job_config.get("needs", [])

        print(f"\n   📦 {job_name}:")
        print(f"      Runs on: {job_config.get('runs-on', 'unknown')}")

        if needs:
            needs_list = needs if isinstance(needs, list) else [needs]
            print(f"      Depends on: {', '.join(needs_list)}")

        if condition:
            print(f"      ⚠️  Condition: {condition}")
            skippable_jobs.append((job_name, condition))
        else:
            always_run_jobs.append(job_name)

    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary:")

    if skippable_jobs:
        print(f"\n   ⚠️  Jobs that may be skipped ({len(skippable_jobs)}):")
        for job_name, condition in skippable_jobs:
            print(f"      • {job_name}")
            print(f"        Condition: {condition}")
            analyze_condition(condition)

    if always_run_jobs:
        print(f"\n   ✅ Jobs that always run ({len(always_run_jobs)}):")
        for job_name in always_run_jobs:
            print(f"      • {job_name}")


def analyze_condition(condition: str) -> None:
    """Analyze a job condition and explain when it runs."""
    print("        Explanation:")

    if "startsWith(github.ref, 'refs/tags/v')" in condition:
        print("           • Runs ONLY when a tag starting with 'v' is pushed")
        print("           • Example: git tag v1.0.0 && git push origin v1.0.0")
        print("           • Skipped for: regular commits, PRs, workflow_dispatch")

    elif "github.event_name == 'release'" in condition:
        print("           • Runs ONLY on release events")
        print("           • Skipped for: pushes, PRs, workflow_dispatch")

    elif "github.event_name == 'pull_request'" in condition:
        print("           • Runs ONLY on pull request events")
        print("           • Skipped for: pushes, releases")

    elif "github.ref == 'refs/heads/master'" in condition or "github.ref == 'refs/heads/main'" in condition:
        print("           • Runs ONLY on master/main branch")
        print("           • Skipped for: other branches, PRs")

    else:
        print("           • Custom condition - check workflow logs for details")


def suggest_fixes(workflow_path: Path) -> None:
    """Suggest fixes for common issues."""
    with open(workflow_path) as f:
        workflow = yaml.safe_load(f)

    jobs = workflow.get("jobs", {})
    print("\n💡 Suggestions:")

    for job_name, job_config in jobs.items():
        if not isinstance(job_config, dict):
            continue

        condition = job_config.get("if", "")

        if "startsWith(github.ref, 'refs/tags/v')" in condition:
            print(f"\n   {job_name}:")
            print("      Current: Runs only on version tags (v*)")
            print("      Options:")
            print("         1. To test the job without creating a tag:")
            print("            • Remove or comment out the 'if' condition temporarily")
            print("            • Or add: || github.event_name == 'workflow_dispatch'")
            print("         2. To create a release properly:")
            print("            • git tag v1.0.0")
            print("            • git push origin v1.0.0")
            print("         3. To test with act (local testing):")
            print("            • act -e .github/workflows/events/release.json")


def simulate_execution(workflow_path: Path, event_type: str, ref: str) -> None:
    """Simulate workflow execution for a given event."""
    with open(workflow_path) as f:
        workflow = yaml.safe_load(f)

    print("\n🎬 Simulating Execution:")
    print("=" * 60)
    print(f"Event: {event_type}")
    print(f"Ref: {ref}")

    # Check if event matches triggers
    triggers = workflow.get("on") or workflow.get(True)
    trigger_matches = False

    if isinstance(triggers, dict):
        trigger_matches = event_type in triggers
    elif isinstance(triggers, list):
        trigger_matches = event_type in triggers
    elif isinstance(triggers, str):
        trigger_matches = event_type == triggers

    if not trigger_matches:
        print(f"\n❌ Workflow would NOT run - event '{event_type}' doesn't match triggers")
        return

    print(f"\n✅ Workflow would run - event '{event_type}' matches triggers")

    # Check each job
    jobs = workflow.get("jobs", {})
    print("\n⚙️  Job Execution Status:")

    for job_name, job_config in jobs.items():
        if not isinstance(job_config, dict):
            continue

        condition = job_config.get("if", "")

        if not condition:
            print(f"   ✅ {job_name}: RUNS (no condition)")
        else:
            # Simple evaluation
            would_run = evaluate_condition(condition, event_type, ref)
            status = "✅ RUNS" if would_run else "⏭️  SKIPPED"
            print(f"   {status} {job_name}: {condition}")


def evaluate_condition(condition: str, event_type: str, ref: str) -> bool:
    """Simple evaluation of common conditions."""
    if "startsWith(github.ref, 'refs/tags/v')" in condition:
        return ref.startswith("refs/tags/v")
    elif "github.event_name == 'release'" in condition:
        return event_type == "release"
    elif "github.event_name == 'pull_request'" in condition:
        return event_type == "pull_request"
    elif "github.ref == 'refs/heads/master'" in condition:
        return ref == "refs/heads/master"
    elif "github.ref == 'refs/heads/main'" in condition:
        return ref == "refs/heads/main"
    else:
        # Can't easily evaluate complex conditions
        return False


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Debug GitHub Actions workflow execution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze workflow conditions
  python scripts/debug_workflow.py build-executables.yml

  # Simulate execution
  python scripts/debug_workflow.py build-executables.yml --simulate push --ref refs/heads/master
  python scripts/debug_workflow.py build-executables.yml --simulate push --ref refs/tags/v1.0.0

  # Get fix suggestions
  python scripts/debug_workflow.py build-executables.yml --suggest
        """,
    )

    parser.add_argument("workflow", help="Workflow file name (e.g., build-executables.yml)")
    parser.add_argument("--simulate", help="Simulate execution for event type")
    parser.add_argument("--ref", default="refs/heads/master", help="Git ref for simulation")
    parser.add_argument("--suggest", action="store_true", help="Show fix suggestions")

    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    workflow_dir = repo_root / ".github" / "workflows"
    workflow_path = workflow_dir / args.workflow

    if not workflow_path.exists():
        print(f"Error: Workflow file not found: {workflow_path}")
        return 1

    try:
        analyze_job_conditions(workflow_path)

        if args.simulate:
            simulate_execution(workflow_path, args.simulate, args.ref)

        if args.suggest:
            suggest_fixes(workflow_path)

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
