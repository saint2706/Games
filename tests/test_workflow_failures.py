"""Tests for workflow failure inspection utilities."""

from __future__ import annotations

from typing import Any

import pytest

from scripts import workflow_failures


def test_parse_repository_from_remote_with_https() -> None:
    """Ensure HTTPS remote URLs are parsed into owner/repo values."""

    remote = "https://github.com/example/project.git"
    assert workflow_failures._parse_repository_from_remote(remote) == "example/project"


def test_parse_repository_from_remote_with_ssh() -> None:
    """Ensure SSH remote URLs are parsed into owner/repo values."""

    remote = "git@github.com:example/project"
    assert workflow_failures._parse_repository_from_remote(remote) == "example/project"


def test_determine_repository_prefers_explicit(monkeypatch: pytest.MonkeyPatch) -> None:
    """Explicit CLI argument should take precedence over environment variables."""

    monkeypatch.setenv("GITHUB_REPOSITORY", "other/repo")
    assert workflow_failures.determine_repository("cli/repo") == "cli/repo"


def test_determine_repository_uses_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Environment variable should be used when CLI argument is absent."""

    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    monkeypatch.setenv("REPO", "env/repo")
    assert workflow_failures.determine_repository() == "env/repo"


def test_get_failed_runs_filters_and_limits(monkeypatch: pytest.MonkeyPatch) -> None:
    """Workflow runs should be filtered to failures and limited to requested amount."""

    pages = {
        1: {
            "workflow_runs": [
                {
                    "id": 1,
                    "run_number": 17,
                    "run_attempt": 1,
                    "name": "CI",
                    "display_title": "CI",
                    "path": ".github/workflows/ci.yml",
                    "conclusion": "failure",
                    "status": "completed",
                    "event": "push",
                    "head_branch": "feature",
                    "actor": {"login": "octocat"},
                    "html_url": "https://example.com/run/1",
                    "created_at": "2024-05-01T12:00:00Z",
                    "updated_at": "2024-05-01T12:05:00Z",
                },
                {
                    "id": 2,
                    "run_number": 18,
                    "name": "CI",
                    "display_title": "CI",
                    "path": ".github/workflows/ci.yml",
                    "conclusion": "success",
                    "status": "completed",
                    "event": "push",
                    "head_branch": "main",
                    "actor": {"login": "octocat"},
                    "html_url": "https://example.com/run/2",
                },
            ]
        }
    }

    jobs = {
        1: {
            "jobs": [
                {
                    "name": "lint",
                    "conclusion": "failure",
                    "html_url": "https://example.com/job/1",
                    "started_at": "2024-05-01T12:00:00Z",
                    "completed_at": "2024-05-01T12:02:30Z",
                },
                {
                    "name": "tests",
                    "conclusion": "success",
                    "html_url": "https://example.com/job/2",
                },
            ]
        }
    }

    def fake_fetch(url: str, token: str | None) -> dict[str, Any]:
        if url.endswith("/jobs?per_page=100"):
            return jobs[1]
        return pages[1]

    monkeypatch.setattr(workflow_failures, "fetch_json", fake_fetch)

    runs = workflow_failures.get_failed_runs("example/project", limit=1, token=None)
    assert len(runs) == 1
    run = runs[0]
    assert run.run_id == 1
    assert run.jobs[0].name == "lint"
    assert run.jobs[0].conclusion == "failure"


def test_print_summary_handles_no_runs(capsys: pytest.CaptureFixture[str]) -> None:
    """Summary printer should indicate when there are no failed runs."""

    workflow_failures.print_summary([], "example/project", 5)
    captured = capsys.readouterr()
    assert "No failed workflow runs" in captured.out


def test_print_summary_includes_debug_hint(capsys: pytest.CaptureFixture[str]) -> None:
    """Summary should include a helpful debug command suggestion."""

    run = workflow_failures.WorkflowRun(
        run_id=1,
        run_number=42,
        attempt=1,
        name="CI",
        workflow_name="CI",
        workflow_path=".github/workflows/ci.yml",
        html_url="https://example.com/run/1",
        status="completed",
        conclusion="failure",
        event="push",
        branch="feature",
        actor="octocat",
        created_at="2024-05-01T12:00:00Z",
        updated_at="2024-05-01T12:05:00Z",
        jobs=(
            workflow_failures.WorkflowJob(
                name="lint",
                conclusion="failure",
                html_url="https://example.com/job/1",
                started_at="2024-05-01T12:00:00Z",
                completed_at="2024-05-01T12:02:30Z",
            ),
        ),
    )

    workflow_failures.print_summary([run], "example/project", 1)
    output = capsys.readouterr().out
    assert "debug_workflow.py" in output
    assert "lint" in output
