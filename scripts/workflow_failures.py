"""Utility for inspecting recent failed GitHub Actions workflow runs.

This module provides a small command line interface that fetches the most
recent failed runs for a repository and prints a summary with actionable
follow-up commands. It is designed to complement ``scripts/debug_workflow.py``
by quickly surfacing the runs that need attention together with the jobs that
failed in each run.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Optional, Sequence
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_ROOT = "https://api.github.com"


@dataclass(slots=True)
class WorkflowJob:
    """Representation of a job within a workflow run."""

    name: str
    conclusion: str
    html_url: str
    started_at: Optional[str]
    completed_at: Optional[str]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON serialisable dictionary representation."""

        return asdict(self)


@dataclass(slots=True)
class WorkflowRun:
    """Representation of a workflow run with its failed jobs."""

    run_id: int
    run_number: int
    attempt: int
    name: str
    workflow_name: str
    workflow_path: str
    html_url: str
    status: str
    conclusion: str
    event: str
    branch: Optional[str]
    actor: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    jobs: tuple[WorkflowJob, ...]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON serialisable dictionary representation."""

        data = asdict(self)
        data["jobs"] = [job.to_dict() for job in self.jobs]
        return data


def determine_repository(explicit: Optional[str] = None) -> str:
    """Determine the GitHub repository in ``owner/repo`` format.

    Args:
        explicit: Optional repository value provided by the caller.

    Returns:
        A repository string in ``owner/repo`` format.

    Raises:
        RuntimeError: If the repository cannot be determined automatically.
    """

    if explicit:
        return explicit

    env_repo = os.getenv("GITHUB_REPOSITORY")
    if env_repo:
        return env_repo

    env_repo = os.getenv("REPO")
    if env_repo:
        return env_repo

    repo_from_git = _repository_from_git_remote()
    if repo_from_git:
        return repo_from_git

    raise RuntimeError(
        "Unable to determine repository. Provide --repo or set GITHUB_REPOSITORY."
    )


def _repository_from_git_remote() -> Optional[str]:
    """Infer repository from the ``origin`` git remote."""

    try:
        result = subprocess.run(  # noqa: S603
            ["git", "config", "--get", "remote.origin.url"],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return None

    remote_url = result.stdout.strip()
    if not remote_url:
        return None

    return _parse_repository_from_remote(remote_url)


def _parse_repository_from_remote(remote_url: str) -> Optional[str]:
    """Extract ``owner/repo`` from a git remote URL."""

    if remote_url.endswith(".git"):
        remote_url = remote_url[:-4]

    if remote_url.startswith("git@"):
        # e.g. git@github.com:owner/repo
        _, _, path = remote_url.partition(":")
        return path or None

    if remote_url.startswith("https://") or remote_url.startswith("http://"):
        parts = remote_url.split("//", maxsplit=1)[-1].split("/", maxsplit=1)
        if len(parts) == 2:
            return parts[1]

    if remote_url.count("/") == 1 and "github.com" not in remote_url:
        return remote_url

    return None


def build_request(url: str, token: Optional[str]) -> Request:
    """Build an authenticated request for the GitHub API."""

    request = Request(url)
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("User-Agent", "games-workflow-tools")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    return request


def fetch_json(url: str, token: Optional[str]) -> dict[str, Any]:
    """Fetch JSON data from the GitHub API."""

    try:
        with urlopen(build_request(url, token)) as response:  # noqa: S310
            payload = response.read().decode("utf-8")
    except HTTPError as exc:  # pragma: no cover - network failure path
        raise RuntimeError(
            f"GitHub API request failed ({exc.code}): {exc.reason}. "
            "Provide a token via --token or GITHUB_TOKEN to increase limits."
        ) from exc
    except URLError as exc:  # pragma: no cover - network failure path
        raise RuntimeError(f"Unable to reach GitHub API: {exc.reason}") from exc

    return json.loads(payload)


def get_failed_runs(
    repository: str,
    limit: int,
    token: Optional[str],
    workflow_filter: Optional[str] = None,
) -> list[WorkflowRun]:
    """Return the most recent failed workflow runs for the repository."""

    if limit <= 0:
        raise ValueError("limit must be a positive integer")

    per_page = min(100, limit)
    runs: list[WorkflowRun] = []
    page = 1

    while len(runs) < limit:
        url = (
            f"{API_ROOT}/repos/{repository}/actions/runs"
            f"?status=completed&per_page={per_page}&page={page}"
        )
        data = fetch_json(url, token)
        workflow_runs = data.get("workflow_runs", [])
        if not workflow_runs:
            break

        for run_data in workflow_runs:
            if run_data.get("conclusion") != "failure":
                continue
            if workflow_filter and not _workflow_matches(run_data, workflow_filter):
                continue

            run = _create_workflow_run(repository, run_data, token)
            runs.append(run)
            if len(runs) >= limit:
                break

        if len(workflow_runs) < per_page:
            break
        page += 1

    return runs


def _workflow_matches(run_data: dict[str, Any], workflow_filter: str) -> bool:
    """Return True if the run matches the provided workflow filter."""

    target = workflow_filter.lower()
    candidates = [
        run_data.get("name", ""),
        run_data.get("display_title", ""),
        run_data.get("path", ""),
    ]
    return any(target in candidate.lower() for candidate in candidates if candidate)


def _create_workflow_run(
    repository: str,
    run_data: dict[str, Any],
    token: Optional[str],
) -> WorkflowRun:
    """Create a :class:`WorkflowRun` instance from API data."""

    job_data = fetch_json(
        f"{API_ROOT}/repos/{repository}/actions/runs/{run_data['id']}/jobs?per_page=100",
        token,
    ).get("jobs", [])

    failed_jobs = [
        WorkflowJob(
            name=job.get("name", "Unnamed job"),
            conclusion=job.get("conclusion", "unknown"),
            html_url=job.get("html_url", ""),
            started_at=job.get("started_at"),
            completed_at=job.get("completed_at"),
        )
        for job in job_data
        if job.get("conclusion") in {"failure", "timed_out", "cancelled"}
    ]

    return WorkflowRun(
        run_id=int(run_data["id"]),
        run_number=int(run_data.get("run_number", 0)),
        attempt=int(run_data.get("run_attempt", 1)),
        name=run_data.get("name", "Unnamed run"),
        workflow_name=run_data.get("name", "Unnamed workflow"),
        workflow_path=run_data.get("path", ""),
        html_url=run_data.get("html_url", ""),
        status=run_data.get("status", "unknown"),
        conclusion=run_data.get("conclusion", "unknown"),
        event=run_data.get("event", "unknown"),
        branch=run_data.get("head_branch"),
        actor=(run_data.get("actor") or {}).get("login"),
        created_at=run_data.get("created_at"),
        updated_at=run_data.get("updated_at"),
        jobs=tuple(failed_jobs),
    )


def _format_timestamp(timestamp: Optional[str]) -> str:
    """Return a human friendly timestamp string."""

    if not timestamp:
        return "unknown time"

    try:
        dt_value = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return timestamp

    return dt_value.strftime("%Y-%m-%d %H:%M:%S UTC")


def _format_duration(job: WorkflowJob) -> str:
    """Return a human friendly job duration string."""

    if not job.started_at or not job.completed_at:
        return "duration unknown"

    try:
        start = datetime.fromisoformat(job.started_at.replace("Z", "+00:00"))
        end = datetime.fromisoformat(job.completed_at.replace("Z", "+00:00"))
    except ValueError:
        return "duration unknown"

    duration = end - start
    total_seconds = int(duration.total_seconds())
    if total_seconds < 0:
        return "duration unknown"
    minutes, seconds = divmod(total_seconds, 60)
    if minutes:
        return f"{minutes}m {seconds}s"
    return f"{seconds}s"


def print_summary(runs: Sequence[WorkflowRun], repository: str, limit: int) -> None:
    """Print a user friendly summary of failed workflow runs."""

    if not runs:
        print(f"✅ No failed workflow runs found for {repository} (requested {limit}).")
        return

    print(
        f"🚨 Failed workflow runs for {repository} "
        f"(showing {len(runs)} of requested {limit})"
    )
    print("=" * 80)

    for index, run in enumerate(runs, start=1):
        timestamp = _format_timestamp(run.created_at)
        branch = run.branch or "unknown branch"
        actor = run.actor or "unknown actor"
        print(
            f"{index:2d}. {run.workflow_name} (Run #{run.run_number}, attempt {run.attempt})"
        )
        print(f"    Event: {run.event} on {branch} by {actor} at {timestamp}")
        print(f"    URL: {run.html_url}")
        print(f"    Workflow file: {run.workflow_path}")

        if run.jobs:
            print("    Failed jobs:")
            for job in run.jobs:
                duration = _format_duration(job)
                print(
                    f"      • {job.name} — {job.conclusion} "
                    f"({duration})\n        {job.html_url}"
                )
        else:
            print("    Failed jobs: Not available (check run logs)")

        suggested_ref = f"refs/heads/{branch}" if branch else "refs/heads/main"
        workflow_file = os.path.basename(run.workflow_path) or run.workflow_name
        print(
            "    Debug suggestion: "
            f"python scripts/debug_workflow.py {workflow_file} --simulate {run.event} "
            f"--ref {suggested_ref}"
        )
        print("-" * 80)


def collect_token(explicit: Optional[str]) -> Optional[str]:
    """Collect an authentication token from arguments or environment."""

    if explicit:
        return explicit
    return os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN") or os.getenv("GITHUB_ACCESS_TOKEN")


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Command line entry point for listing failed workflow runs."""

    parser = argparse.ArgumentParser(
        description="List recent failed GitHub Actions workflow runs.",
    )
    parser.add_argument("--repo", help="Repository in owner/name format.")
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Number of failed runs to retrieve (default: 20).",
    )
    parser.add_argument(
        "--workflow",
        help="Optional workflow name or file to filter the results.",
    )
    parser.add_argument(
        "--token",
        help="GitHub token for authenticated requests (defaults to environment).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON instead of a formatted summary.",
    )

    args = parser.parse_args(argv)

    try:
        repository = determine_repository(args.repo)
        token = collect_token(args.token)
        runs = get_failed_runs(repository, args.limit, token, args.workflow)
    except (RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps([run.to_dict() for run in runs], indent=2))
    else:
        print_summary(runs, repository, args.limit)

    return 0


if __name__ == "__main__":
    sys.exit(main())
