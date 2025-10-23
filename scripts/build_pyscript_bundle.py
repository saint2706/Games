"""Build the PyScript bundle containing the browser launcher."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """Return the parsed command-line arguments."""

    parser = argparse.ArgumentParser(description="Build the PyScript web bundle")
    parser.add_argument(
        "--output",
        default="dist/web",
        help="Destination directory for the generated bundle (default: dist/web)",
    )
    parser.add_argument(
        "--wheel-dir",
        default="dist/web/packages",
        help="Directory relative to the output root where the wheel will be stored.",
    )
    parser.add_argument(
        "--skip-wheel",
        action="store_true",
        help="Skip building a wheel (expects an existing wheel in dist/).",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point for the PyScript bundle builder."""

    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    output_dir = (root / args.output).resolve()
    wheel_dir = (root / args.wheel_dir).resolve()
    staging_dir = output_dir / "_staging"

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    wheel_dir.mkdir(parents=True, exist_ok=True)

    _copy_static_assets(root, output_dir)

    if args.skip_wheel:
        wheel_path = _find_existing_wheel(root / "dist")
    else:
        wheel_path = _build_wheel(root, staging_dir)

    shutil.copy2(wheel_path, wheel_dir / wheel_path.name)
    _rewrite_index(output_dir / "index.html", wheel_path.name)

    if staging_dir.exists():
        shutil.rmtree(staging_dir)

    manifest = {
        "wheel": wheel_path.name,
        "output": str(output_dir.relative_to(root)),
        "packages": str(wheel_dir.relative_to(root)),
    }
    (output_dir / "bundle.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def _copy_static_assets(root: Path, output: Path) -> None:
    """Copy web assets and launcher icons into ``output``."""

    web_source = root / "web" / "pyscript"
    if not web_source.exists():
        raise FileNotFoundError(f"Missing web assets directory: {web_source}")
    shutil.copytree(web_source, output, dirs_exist_ok=True)

    icon_source = root / "src" / "games_collection" / "assets" / "launcher"
    icon_target = output / "assets" / "launcher"
    if icon_target.exists():
        shutil.rmtree(icon_target)
    shutil.copytree(icon_source, icon_target)


def _build_wheel(project_root: Path, staging_dir: Path) -> Path:
    """Build the project wheel using ``python -m build``."""

    staging_dir.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, "-m", "build", "--wheel", f"--outdir={staging_dir}"]
    try:
        subprocess.run(command, check=True, cwd=project_root)
    except FileNotFoundError as exc:  # pragma: no cover - subprocess failures are environment specific
        raise RuntimeError("Python executable not found while invoking build") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("Wheel build failed; see logs above for details") from exc

    wheels = sorted(staging_dir.glob("*.whl"))
    if not wheels:
        raise RuntimeError(f"No wheel produced in {staging_dir}")
    return wheels[-1]


def _find_existing_wheel(dist_dir: Path) -> Path:
    """Return the most recent wheel from ``dist_dir``."""

    wheels = sorted(dist_dir.glob("*.whl"))
    if not wheels:
        raise FileNotFoundError("No wheel available; run without --skip-wheel")
    return wheels[-1]


def _rewrite_index(index_path: Path, wheel_name: str) -> None:
    """Replace the ``{{WHEEL_FILENAME}}`` placeholder in ``index_path``."""

    if not index_path.exists():
        raise FileNotFoundError(f"Missing index file at {index_path}")
    contents = index_path.read_text(encoding="utf-8")
    if "{{WHEEL_FILENAME}}" not in contents:
        raise ValueError("index.html does not contain the {{WHEEL_FILENAME}} placeholder")
    updated = contents.replace("{{WHEEL_FILENAME}}", wheel_name)
    index_path.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
