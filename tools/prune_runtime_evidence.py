#!/usr/bin/env python3
"""Delete explicitly named closed-scenario evidence below _runtime safely."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil


def resolve_target(runtime_root: Path, raw_target: str) -> Path:
    if any(character in raw_target for character in "*?[]"):
        raise ValueError("globs are forbidden; name every evidence target explicitly")
    root = runtime_root.resolve()
    target = (root / raw_target).resolve()
    if target == root or not target.is_relative_to(root):
        raise ValueError(f"target escapes or equals runtime root: {raw_target}")
    return target


def remove_target(target: Path) -> str:
    if target.is_symlink() or target.is_file():
        target.unlink()
        return "file"
    if target.is_dir():
        shutil.rmtree(target)
        return "directory"
    raise FileNotFoundError(f"evidence target does not exist: {target}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-root", type=Path, default=Path("_runtime"))
    parser.add_argument("--target", action="append", required=True)
    args = parser.parse_args(argv)
    root = args.runtime_root.resolve()
    targets = [resolve_target(root, raw_target) for raw_target in args.target]
    if len(set(targets)) != len(targets):
        raise ValueError("duplicate evidence targets are forbidden")
    removed = [
        {"path": str(target), "kind": remove_target(target)}
        for target in targets
    ]
    print(json.dumps({"runtime_root": str(root), "removed": removed}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
