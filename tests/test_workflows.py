"""Tests for GitHub Actions workflow validation."""

from __future__ import annotations

from pathlib import Path

import pytest

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    yaml = None

# Get the repository root
REPO_ROOT = Path(__file__).parent.parent


def test_workflow_files_exist():
    """Test that expected workflow files exist."""
    workflow_dir = REPO_ROOT / ".github" / "workflows"
    assert workflow_dir.exists(), "Workflow directory should exist"

    expected_workflows = [
        "ci.yml",
        "format-and-lint.yml",
        "manual-tests.yml",
        "manual-coverage.yml",
        "mutation-testing.yml",
        "build-executables.yml",
        "codeql.yml",
        "publish-pypi.yml",
        "test-act-setup.yml",
    ]

    for workflow in expected_workflows:
        workflow_path = workflow_dir / workflow
        assert workflow_path.exists(), f"Workflow {workflow} should exist"


def test_event_payload_files_exist():
    """Test that event payload files exist."""
    events_dir = REPO_ROOT / ".github" / "workflows" / "events"
    assert events_dir.exists(), "Events directory should exist"

    expected_events = [
        "push.json",
        "pull_request.json",
        "release.json",
        "workflow_dispatch.json",
    ]

    for event in expected_events:
        event_path = events_dir / event
        assert event_path.exists(), f"Event payload {event} should exist"


def test_workflow_validation_script_exists():
    """Test that the workflow validation script exists."""
    script_path = REPO_ROOT / "scripts" / "validate_workflows.py"
    assert script_path.exists(), "Workflow validation script should exist"
    assert script_path.is_file(), "Workflow validation script should be a file"


def test_workflow_validation_passes():
    """Test that workflow validation passes."""
    if yaml is None:
        pytest.skip("PyYAML not installed")
    import subprocess

    script_path = REPO_ROOT / "scripts" / "validate_workflows.py"
    result = subprocess.run(
        ["python3", str(script_path)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )

    assert result.returncode == 0, f"Workflow validation should pass\n{result.stdout}\n{result.stderr}"


def test_workflow_syntax_valid():
    """Test that all workflow files have valid YAML syntax."""
    if yaml is None:
        pytest.skip("PyYAML not installed")

    workflow_dir = REPO_ROOT / ".github" / "workflows"
    workflow_files = list(workflow_dir.glob("*.yml"))

    assert len(workflow_files) > 0, "Should have at least one workflow file"

    for workflow_file in workflow_files:
        with open(workflow_file) as f:
            try:
                workflow = yaml.safe_load(f)
                assert workflow is not None, f"{workflow_file.name} should not be empty"
                assert isinstance(workflow, dict), f"{workflow_file.name} should be a dictionary"
            except yaml.YAMLError as e:
                pytest.fail(f"Invalid YAML in {workflow_file.name}: {e}")


def test_event_payload_syntax_valid():
    """Test that all event payload files have valid JSON syntax."""
    import json

    events_dir = REPO_ROOT / ".github" / "workflows" / "events"
    event_files = list(events_dir.glob("*.json"))

    assert len(event_files) > 0, "Should have at least one event payload file"

    for event_file in event_files:
        with open(event_file) as f:
            try:
                event = json.load(f)
                assert event is not None, f"{event_file.name} should not be empty"
                assert isinstance(event, dict), f"{event_file.name} should be a dictionary"
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON in {event_file.name}: {e}")


def test_workflow_structure():
    """Test that all workflows have required structure."""
    if yaml is None:
        pytest.skip("PyYAML not installed")

    workflow_dir = REPO_ROOT / ".github" / "workflows"
    workflow_files = list(workflow_dir.glob("*.yml"))

    for workflow_file in workflow_files:
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        # Check for required fields
        assert "name" in workflow, f"{workflow_file.name} should have a name"

        # Check for 'on' or True (YAML treats 'on' as boolean True)
        assert "on" in workflow or True in workflow, f"{workflow_file.name} should have trigger events"

        assert "jobs" in workflow, f"{workflow_file.name} should have jobs"
        assert isinstance(workflow["jobs"], dict), f"{workflow_file.name} jobs should be a dictionary"
        assert len(workflow["jobs"]) > 0, f"{workflow_file.name} should have at least one job"

        # Check each job has required fields
        for job_name, job_config in workflow["jobs"].items():
            assert isinstance(job_config, dict), f"Job {job_name} in {workflow_file.name} should be a dictionary"
            assert "runs-on" in job_config, f"Job {job_name} in {workflow_file.name} should have runs-on"
            assert "steps" in job_config, f"Job {job_name} in {workflow_file.name} should have steps"


def test_workflow_scripts_exist():
    """Test that scripts referenced in workflows exist."""
    scripts_dir = REPO_ROOT / "scripts"

    expected_scripts = [
        "run_workflow.sh",
        "setup_act.sh",
        "validate_workflows.py",
    ]

    for script in expected_scripts:
        script_path = scripts_dir / script
        assert script_path.exists(), f"Script {script} should exist"
        assert script_path.is_file(), f"Script {script} should be a file"


def test_workflow_documentation_exists():
    """Test that workflow documentation exists."""
    docs_dir = REPO_ROOT / "docs" / "development"

    expected_docs = [
        "LOCAL_WORKFLOWS.md",
        "WORKFLOW_TESTING_QUICKSTART.md",
    ]

    for doc in expected_docs:
        doc_path = docs_dir / doc
        assert doc_path.exists(), f"Documentation {doc} should exist"
        assert doc_path.is_file(), f"Documentation {doc} should be a file"
