from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from typing import Any


RUN_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{5,127}$")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: Any, *, refuse_overwrite: bool = True) -> None:
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    if refuse_overwrite and path.exists():
        raise FileExistsError(f"refusing to overwrite evidence: {path}")
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def create_run(root: Path, run_id: str) -> tuple[Path, dict[str, object]]:
    if not RUN_ID_PATTERN.fullmatch(run_id):
        raise ValueError("run ID must be 6-128 ASCII letters, digits, dots, underscores, or hyphens")
    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    run = root / run_id
    run.mkdir(exist_ok=False)
    for name in ("evidence", "ocr", "screenshots"):
        (run / name).mkdir()
    manifest: dict[str, object] = {
        "schema": 1,
        "run_id": run_id,
        "created_at_utc": utc_now(),
        "python": sys.version,
        "run_root": str(run),
    }
    write_json(run / "evidence" / "run.json", manifest)
    return run, manifest
