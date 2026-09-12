#!/usr/bin/env python3
"""Build a tagged, deterministic For Vivhite: Colonial Border Cleanup release."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PRODUCT_ROOT = REPO_ROOT / "mod_colonial_region_transfer"
VALIDATOR = REPO_ROOT / "tools/validate_colonial_region_transfer_static.py"
PRODUCT_KEY = "colonial_region_transfer"
METADATA = Path(".metadata/metadata.json")
LANGUAGES = (
    "braz_por",
    "english",
    "french",
    "german",
    "japanese",
    "korean",
    "polish",
    "russian",
    "simp_chinese",
    "spanish",
    "turkish",
)
ALLOWLIST = (
    METADATA,
    Path("in_game/common/country_interactions/xcrt_colonial_region_transfer.txt"),
    *(
        Path(f"main_menu/localization/{language}/xcrt_colonial_region_transfer_l_{language}.yml")
        for language in LANGUAGES
    ),
)
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


class BuildRefused(RuntimeError):
    """Raised when a release invariant is not satisfied."""


def require_native_metadata(product_root: Path) -> Path:
    metadata_path = product_root / METADATA
    if not metadata_path.is_file():
        raise BuildRefused(
            ".metadata/metadata.json is missing. Generate it with the current EU5 Mod Tools; "
            "do not hand-write or copy another game's schema."
        )
    return metadata_path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checked_runtime_files(product_root: Path) -> list[tuple[Path, Path]]:
    root = product_root.resolve()
    result: list[tuple[Path, Path]] = []
    missing: list[str] = []
    for relative in ALLOWLIST:
        source = product_root / relative
        if not source.is_file():
            missing.append(relative.as_posix())
            continue
        if source.is_symlink() or not source.resolve().is_relative_to(root):
            raise BuildRefused(f"allowlisted runtime file escapes the product tree: {relative.as_posix()}")
        result.append((relative, source))
    if missing:
        raise BuildRefused(f"allowlisted runtime files are missing: {', '.join(missing)}")
    return result


def git_output(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown git error"
        raise BuildRefused(f"git {' '.join(args)} failed: {detail}")
    return result.stdout.strip()


def tagged_clean_identity(version: str) -> tuple[str, str]:
    dirty = git_output("status", "--porcelain=v1", "--untracked-files=all")
    if dirty:
        raise BuildRefused("formal release builds require a clean working tree")

    commit = git_output("rev-parse", "HEAD")
    tag = f"{PRODUCT_KEY}-v{version}"
    tagged_commit = git_output("rev-parse", "--verify", f"refs/tags/{tag}^{{commit}}")
    if tagged_commit != commit:
        raise BuildRefused(f"tag {tag} does not resolve to clean HEAD {commit}")
    return commit, tag


def build_projection(
    product_root: Path,
    release_root: Path,
    version: str,
    git_commit: str,
    git_tag: str,
) -> dict[str, object]:
    """Create one release projection; callers must provide a fresh release_root."""

    runtime_files = checked_runtime_files(product_root)
    if release_root.exists():
        raise BuildRefused(f"refusing to overwrite existing release output: {release_root}")

    staging_root = release_root / "staging"
    staging_root.mkdir(parents=True)
    file_records: list[dict[str, object]] = []
    for relative, source in sorted(runtime_files, key=lambda item: item[0].as_posix()):
        destination = staging_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        file_records.append(
            {
                "path": relative.as_posix(),
                "size": destination.stat().st_size,
                "sha256": sha256(destination),
            }
        )

    archive_name = f"{PRODUCT_KEY}-{version}.zip"
    archive_path = release_root / archive_name
    with zipfile.ZipFile(
        archive_path,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for record in file_records:
            relative = Path(str(record["path"]))
            info = zipfile.ZipInfo(relative.as_posix(), ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(
                info,
                (staging_root / relative).read_bytes(),
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )

    manifest: dict[str, object] = {
        "schema": "xcrt.release-manifest.v2",
        "product": PRODUCT_KEY,
        "version": version,
        "git": {"commit": git_commit, "tag": git_tag},
        "steam": {"app_id": 3450310, "build_id": 24187685},
        "staging": {"root": "staging", "files": file_records},
        "zip": {
            "path": archive_name,
            "size": archive_path.stat().st_size,
            "sha256": sha256(archive_path),
            "timestamp": "1980-01-01T00:00:00Z",
        },
    }
    manifest_path = release_root / f"{PRODUCT_KEY}-{version}.manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return manifest


def projection_hashes(release_root: Path) -> dict[str, str]:
    return {
        path.relative_to(release_root).as_posix(): sha256(path)
        for path in sorted(release_root.rglob("*"))
        if path.is_file()
    }


def check_reproducible(
    product_root: Path,
    version: str,
    git_commit: str,
    git_tag: str,
) -> dict[str, object]:
    release_name = f"{PRODUCT_KEY}-{version}"
    with tempfile.TemporaryDirectory(prefix="xcrt-release-a-") as temp_a, tempfile.TemporaryDirectory(
        prefix="xcrt-release-b-"
    ) as temp_b:
        root_a = Path(temp_a) / release_name
        root_b = Path(temp_b) / release_name
        build_projection(product_root, root_a, version, git_commit, git_tag)
        build_projection(product_root, root_b, version, git_commit, git_tag)
        hashes_a = projection_hashes(root_a)
        hashes_b = projection_hashes(root_b)
        if hashes_a != hashes_b:
            raise BuildRefused("independent release projections differ byte-for-byte")
        return {
            "status": "PASS",
            "mode": "reproducibility-check",
            "files": hashes_a,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-root", help="Europa Universalis V installation root")
    parser.add_argument("--output-root", type=Path, default=REPO_ROOT / "dist")
    parser.add_argument(
        "--check",
        action="store_true",
        help="build twice in temporary directories and compare every output byte",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        require_native_metadata(PRODUCT_ROOT)
    except BuildRefused as exc:
        sys.stderr.write(f"REFUSED: {exc}\n")
        return 2

    validator_command = [sys.executable, str(VALIDATOR), "--require-metadata"]
    if args.game_root:
        validator_command.extend(["--game-root", args.game_root])
    validation = subprocess.run(validator_command, cwd=REPO_ROOT, text=True, capture_output=True)
    sys.stdout.write(validation.stdout)
    sys.stderr.write(validation.stderr)
    if validation.returncode:
        sys.stderr.write("REFUSED: static validation failed.\n")
        return validation.returncode

    version = (PRODUCT_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    try:
        commit, tag = tagged_clean_identity(version)
        if args.check:
            report = check_reproducible(PRODUCT_ROOT, version, commit, tag)
        else:
            release_root = args.output_root.resolve() / f"{PRODUCT_KEY}-{version}"
            report = build_projection(PRODUCT_ROOT, release_root, version, commit, tag)
    except BuildRefused as exc:
        sys.stderr.write(f"REFUSED: {exc}\n")
        return 4

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
