#!/usr/bin/env python3
"""Build a deterministic For Vivhite: Colonial Border Cleanup release ZIP."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PRODUCT_ROOT = REPO_ROOT / "mod_colonial_region_transfer"
VALIDATOR = REPO_ROOT / "tools/validate_colonial_region_transfer_static.py"
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-root", help="Europa Universalis V installation root")
    parser.add_argument("--output-root", type=Path, default=REPO_ROOT / "dist")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    metadata_path = PRODUCT_ROOT / METADATA
    if not metadata_path.is_file():
        sys.stderr.write(
            "REFUSED: .metadata/metadata.json is missing. Generate it with the current EU5 Mod Tools; "
            "do not hand-write or copy another game's schema.\n"
        )
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

    missing = [str(relative) for relative in ALLOWLIST if not (PRODUCT_ROOT / relative).is_file()]
    if missing:
        sys.stderr.write(f"REFUSED: allowlisted runtime files are missing: {', '.join(missing)}\n")
        return 3

    version = (PRODUCT_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    output_root = args.output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    zip_path = output_root / f"colonial_region_transfer-{version}.zip"
    manifest_path = output_root / f"colonial_region_transfer-{version}.manifest.json"

    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in sorted(ALLOWLIST, key=lambda item: item.as_posix()):
            source = PRODUCT_ROOT / relative
            info = zipfile.ZipInfo(relative.as_posix(), ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    manifest = {
        "schema": "xcrt.release-manifest.v1",
        "product": "colonial_region_transfer",
        "version": version,
        "steam_app_id": 3450310,
        "steam_build_id": 24187685,
        "allowlist": [relative.as_posix() for relative in ALLOWLIST],
        "inputs": {
            relative.as_posix(): sha256(PRODUCT_ROOT / relative) for relative in ALLOWLIST
        },
        "zip": {"path": zip_path.name, "sha256": sha256(zip_path)},
        "source_date_epoch": int(os.environ.get("SOURCE_DATE_EPOCH", "0")),
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
