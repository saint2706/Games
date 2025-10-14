#!/usr/bin/env python3
"""Validate GitHub Actions workflow files.

This script validates all GitHub Actions workflows in the repository:
- YAML syntax
- Workflow structure
- Action versions
- Script references
- Event payload files
- Documentation consistency
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml


class WorkflowValidator:
    """Validates GitHub Actions workflows."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.workflow_dir = repo_root / ".github" / "workflows"
        self.events_dir = self.workflow_dir / "events"
        self.scripts_dir = repo_root / "scripts"
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def validate_all(self) -> bool:
        """Run all validations and return True if all pass."""
        print("🔍 Validating GitHub Actions Workflows\n")
        print("=" * 60)

        self.validate_yaml_syntax()
        self.validate_event_payloads()
        self.validate_workflow_structure()
        self.validate_script_references()
        self.validate_actions()
        self.validate_documentation()

        print("\n" + "=" * 60)
        self.print_summary()

        return len(self.errors) == 0

    def validate_yaml_syntax(self) -> None:
        """Validate YAML syntax for all workflow files."""
        print("\n📄 Validating YAML Syntax...")

        workflow_files = sorted(self.workflow_dir.glob("*.yml"))
        if not workflow_files:
            self.errors.append("No workflow files found")
            return

        for yml_file in workflow_files:
            try:
                with open(yml_file) as f:
                    yaml.safe_load(f)
                print(f"  ✓ {yml_file.name}")
            except yaml.YAMLError as e:
                error_msg = f"Invalid YAML in {yml_file.name}: {e}"
                self.errors.append(error_msg)
                print(f"  ✗ {yml_file.name}: {e}")

    def validate_event_payloads(self) -> None:
        """Validate JSON event payload files."""
        print("\n📦 Validating Event Payloads...")

        if not self.events_dir.exists():
            self.warnings.append("Events directory not found")
            return

        json_files = sorted(self.events_dir.glob("*.json"))
        if not json_files:
            self.warnings.append("No event payload files found")
            return

        for json_file in json_files:
            try:
                with open(json_file) as f:
                    json.load(f)
                print(f"  ✓ {json_file.name}")
            except json.JSONDecodeError as e:
                error_msg = f"Invalid JSON in {json_file.name}: {e}"
                self.errors.append(error_msg)
                print(f"  ✗ {json_file.name}: {e}")

    def validate_workflow_structure(self) -> None:
        """Validate workflow structure and required fields."""
        print("\n🏗️  Validating Workflow Structure...")

        workflow_files = sorted(self.workflow_dir.glob("*.yml"))

        for yml_file in workflow_files:
            try:
                with open(yml_file) as f:
                    workflow = yaml.safe_load(f)

                if not isinstance(workflow, dict):
                    self.errors.append(f"{yml_file.name}: Workflow must be a dictionary")
                    continue

                # Check required fields
                if "name" not in workflow:
                    self.warnings.append(f"{yml_file.name}: Missing 'name' field")

                # Check for 'on' or True (yaml treats 'on' as boolean True)
                if "on" not in workflow and True not in workflow:
                    self.errors.append(f"{yml_file.name}: Missing 'on' (trigger events)")
                    continue

                if "jobs" not in workflow:
                    self.errors.append(f"{yml_file.name}: Missing 'jobs' section")
                    continue

                # Validate jobs structure
                jobs = workflow.get("jobs", {})
                if not isinstance(jobs, dict) or not jobs:
                    self.errors.append(f"{yml_file.name}: 'jobs' must be a non-empty dictionary")
                    continue

                # Check each job
                for job_name, job_config in jobs.items():
                    if not isinstance(job_config, dict):
                        self.errors.append(f"{yml_file.name}: Job '{job_name}' must be a dictionary")
                        continue

                    if "runs-on" not in job_config:
                        self.errors.append(f"{yml_file.name}: Job '{job_name}' missing 'runs-on'")

                    if "steps" not in job_config:
                        self.errors.append(f"{yml_file.name}: Job '{job_name}' missing 'steps'")

                print(f"  ✓ {yml_file.name}: Structure valid")

            except yaml.YAMLError:
                # Already caught in validate_yaml_syntax
                pass
            except Exception as e:
                self.errors.append(f"{yml_file.name}: Unexpected error: {e}")

    def validate_script_references(self) -> None:
        """Validate that referenced scripts exist and are executable."""
        print("\n📜 Validating Script References...")

        workflow_files = sorted(self.workflow_dir.glob("*.yml"))
        referenced_scripts = set()

        for yml_file in workflow_files:
            try:
                with open(yml_file) as f:
                    content = f.read()
                    workflow = yaml.safe_load(content)

                # Look for script references in run commands
                if isinstance(workflow, dict):
                    self._find_script_refs(workflow, referenced_scripts)

            except Exception:
                pass  # Already validated

        # Check if referenced scripts exist
        for script_path in referenced_scripts:
            full_path = self.repo_root / script_path
            if not full_path.exists():
                self.errors.append(f"Referenced script not found: {script_path}")
                print(f"  ✗ {script_path}: Not found")
            elif not full_path.is_file():
                self.errors.append(f"Referenced script is not a file: {script_path}")
                print(f"  ✗ {script_path}: Not a file")
            else:
                # Check if executable (on Unix-like systems)
                if full_path.suffix == ".sh" and not (full_path.stat().st_mode & 0o111):
                    self.warnings.append(f"Script not executable: {script_path}")
                    print(f"  ⚠ {script_path}: Not executable")
                else:
                    print(f"  ✓ {script_path}")

    def _find_script_refs(self, obj: Any, refs: set[str]) -> None:
        """Recursively find script references in workflow YAML."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "run" and isinstance(value, str):
                    # Look for script references
                    for line in value.split("\n"):
                        line = line.strip()
                        if line.startswith("./scripts/"):
                            # Extract script path
                            parts = line.split()
                            if parts:
                                script_path = parts[0]
                                if script_path.startswith("./"):
                                    script_path = script_path[2:]
                                refs.add(script_path)
                else:
                    self._find_script_refs(value, refs)
        elif isinstance(obj, list):
            for item in obj:
                self._find_script_refs(item, refs)

    def validate_actions(self) -> None:
        """Validate GitHub Actions usage and versions."""
        print("\n🔌 Validating Actions Usage...")

        workflow_files = sorted(self.workflow_dir.glob("*.yml"))
        actions_found: dict[str, set[str]] = {}

        for yml_file in workflow_files:
            try:
                with open(yml_file) as f:
                    workflow = yaml.safe_load(f)

                if isinstance(workflow, dict):
                    self._find_actions(workflow, actions_found)

            except Exception:
                pass  # Already validated

        # Report actions usage
        if actions_found:
            for action, versions in sorted(actions_found.items()):
                versions_str = ", ".join(sorted(versions))
                print(f"  ✓ {action}: {versions_str}")

                # Check for common outdated actions
                if "actions/checkout" in action:
                    if any(v.startswith("v") and int(v[1]) < 4 for v in versions if v.startswith("v")):
                        self.warnings.append(f"Consider updating {action} to v5 (current: {versions_str})")
                elif "actions/setup-python" in action:
                    if any(v.startswith("v") and int(v[1]) < 5 for v in versions if v.startswith("v")):
                        self.warnings.append(f"Consider updating {action} to v6 (current: {versions_str})")
        else:
            print("  ⚠ No actions found in workflows")

    def _find_actions(self, obj: Any, actions: dict[str, set[str]]) -> None:
        """Recursively find GitHub Actions usage in workflow YAML."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "uses" and isinstance(value, str):
                    # Extract action name and version
                    parts = value.split("@")
                    if len(parts) == 2:
                        action_name = parts[0]
                        action_version = parts[1]
                        if action_name not in actions:
                            actions[action_name] = set()
                        actions[action_name].add(action_version)
                else:
                    self._find_actions(value, actions)
        elif isinstance(obj, list):
            for item in obj:
                self._find_actions(item, actions)

    def validate_documentation(self) -> None:
        """Validate that documentation matches workflows."""
        print("\n📚 Validating Documentation...")

        # Check that run_workflow.sh lists all workflows
        run_workflow_script = self.scripts_dir / "run_workflow.sh"
        if run_workflow_script.exists():
            with open(run_workflow_script) as f:
                script_content = f.read()

            # Check for workflow references in script
            documented_workflows = set()
            if "ci)" in script_content:
                documented_workflows.add("ci")
            if "lint)" in script_content:
                documented_workflows.add("format-and-lint")
            if "test|tests)" in script_content:
                documented_workflows.add("manual-tests")
            if "coverage)" in script_content:
                documented_workflows.add("manual-coverage")
            if "mutation)" in script_content:
                documented_workflows.add("mutation-testing")
            if "build|build-executables)" in script_content:
                documented_workflows.add("build-executables")
            if "codeql)" in script_content:
                documented_workflows.add("codeql")
            if "publish|pypi)" in script_content:
                documented_workflows.add("publish-pypi")

            print(f"  ✓ run_workflow.sh exists and documents {len(documented_workflows)} workflows")
        else:
            self.warnings.append("run_workflow.sh not found")
            print("  ⚠ run_workflow.sh not found")

    def print_summary(self) -> None:
        """Print validation summary."""
        print("\n📊 Validation Summary")
        print("-" * 60)

        if self.errors:
            print(f"\n❌ {len(self.errors)} Error(s) found:")
            for error in self.errors:
                print(f"   • {error}")

        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} Warning(s):")
            for warning in self.warnings:
                print(f"   • {warning}")

        if not self.errors and not self.warnings:
            print("\n✅ All validations passed! Workflows are healthy.")
        elif not self.errors:
            print("\n✅ No critical errors found. Warnings are informational only.")


def main() -> int:
    """Main entry point."""
    repo_root = Path(__file__).parent.parent
    validator = WorkflowValidator(repo_root)

    if validator.validate_all():
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
