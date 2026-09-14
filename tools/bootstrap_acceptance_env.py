#!/usr/bin/env python3
"""Create the isolated Python environment used by EU5 desktop acceptance."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys


RAPIDOCR_DISTRIBUTION = "rapidocr-onnxruntime==1.2.3"
FORBIDDEN_SUFFIXES = {".ps1", ".psm1", ".psd1"}


def run_checked(command: list[str], *, cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True, shell=False)


def remove_forbidden_shell_artifacts(environment: Path) -> list[Path]:
    removed: list[Path] = []
    if not environment.exists():
        return removed
    for path in environment.rglob("*"):
        if path.is_file() and path.suffix.casefold() in FORBIDDEN_SUFFIXES:
            path.unlink()
            removed.append(path)
    return removed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--venv", type=Path, default=Path(".venv"))
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args(argv)

    repository = Path(__file__).resolve().parents[1]
    environment = (repository / args.venv).resolve()
    interpreter = environment / "Scripts" / "python.exe"
    if environment.exists() and not args.update:
        raise FileExistsError(
            f"environment already exists: {environment}; use --update or choose another path"
        )
    if not interpreter.exists():
        run_checked([sys.executable, "-m", "venv", str(environment)], cwd=repository)
        remove_forbidden_shell_artifacts(environment)
    run_checked(
        [
            str(interpreter),
            "-m",
            "pip",
            "install",
            "-r",
            str(repository / "tools" / "requirements-acceptance.txt"),
        ],
        cwd=repository,
    )
    probe_stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_checked(
        [
            str(interpreter),
            "-m",
            "pip",
            "install",
            "--no-deps",
            RAPIDOCR_DISTRIBUTION,
        ],
        cwd=repository,
    )
    removed = remove_forbidden_shell_artifacts(environment)
    for path in removed:
        print(f"removed forbidden generated activation script: {path}")
    run_checked(
        [
            str(interpreter),
            str(repository / "tools" / "eu5_acceptance.py"),
            "probe",
            "--provider",
            "cuda",
            "--output",
            str(repository / "_runtime" / f"acceptance-env-cuda-probe-{probe_stamp}.json"),
        ],
        cwd=repository,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
