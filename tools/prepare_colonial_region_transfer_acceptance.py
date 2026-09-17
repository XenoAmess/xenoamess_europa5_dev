#!/usr/bin/env python3
"""Compose the product and external fixture into one isolated EU5 local Mod tree."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PRODUCT_ROOT = REPO_ROOT / "mod_colonial_region_transfer"
FIXTURE_ROOT = REPO_ROOT / "fixtures/colonial_region_transfer/overlay"
MOD_DIRECTORY = "xcrt_colonial_region_transfer"
PLAYSET_NAME = "XCRT Acceptance"
ACCEPTANCE_LANGUAGE = "l_simp_chinese"
EXACT_BUILD_DLC = (
    ("d000_shared", True),
    ("d017_sacred_sites_pack", False),
    ("d008_fate_of_the_phoenix", False),
    ("d015_ancient_monuments_pack", True),
)
PRODUCT_FILES = (
    Path(".metadata/metadata.json"),
    Path("in_game/common/country_interactions/xcrt_colonial_region_transfer.txt"),
    Path("in_game/common/scripted_triggers/xcrt_subject_territory_consolidation_triggers.txt"),
    *tuple(
        Path(f"main_menu/localization/{language}/xcrt_colonial_region_transfer_l_{language}.yml")
        for language in (
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
    ),
)


class PreparationRefused(RuntimeError):
    """Raised before an unsafe or incomplete acceptance projection is written."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checked_sources(
    product_root: Path = PRODUCT_ROOT,
    fixture_root: Path = FIXTURE_ROOT,
) -> list[tuple[str, Path, Path]]:
    sources: list[tuple[str, Path, Path]] = []
    for relative in PRODUCT_FILES:
        source = product_root / relative
        if not source.is_file():
            raise PreparationRefused(f"missing product runtime file: {relative.as_posix()}")
        if source.is_symlink() or not source.resolve().is_relative_to(product_root.resolve()):
            raise PreparationRefused(f"product source escapes its tree: {relative.as_posix()}")
        sources.append(("product", relative, source))

    if not fixture_root.is_dir():
        raise PreparationRefused(f"fixture overlay is missing: {fixture_root}")
    for source in sorted(fixture_root.rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(fixture_root)
        if source.is_symlink() or not source.resolve().is_relative_to(fixture_root.resolve()):
            raise PreparationRefused(f"fixture source escapes its tree: {relative.as_posix()}")
        if relative in PRODUCT_FILES:
            raise PreparationRefused(f"fixture shadows a product runtime file: {relative.as_posix()}")
        sources.append(("fixture", relative, source))
    return sources


def compose(
    profile: Path,
    evidence_root: Path,
    product_root: Path = PRODUCT_ROOT,
    fixture_root: Path = FIXTURE_ROOT,
) -> dict[str, object]:
    profile = profile.resolve()
    if not profile.is_dir():
        raise PreparationRefused(f"isolated profile does not exist: {profile}")
    mod_root = (profile / "mod").resolve()
    target = (mod_root / MOD_DIRECTORY).resolve()
    if target.parent != mod_root:
        raise PreparationRefused(f"computed Mod target escaped isolated profile: {target}")
    if target.exists():
        raise PreparationRefused(f"refusing to overwrite existing Mod target: {target}")

    evidence_root = evidence_root.resolve()
    if evidence_root.exists() and any(evidence_root.iterdir()):
        raise PreparationRefused(f"evidence directory is not empty: {evidence_root}")
    evidence_root.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, object]] = []
    for origin, relative, source in checked_sources(product_root, fixture_root):
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        records.append(
            {
                "origin": origin,
                "path": relative.as_posix(),
                "size": destination.stat().st_size,
                "sha256": sha256(destination),
            }
        )

    tree_digest = hashlib.sha256()
    for record in sorted(records, key=lambda item: str(item["path"])):
        tree_digest.update(
            f"{record['path']}\0{record['size']}\0{record['sha256']}\n".encode("utf-8")
        )
    manifest: dict[str, object] = {
        "schema": "xcrt.acceptance-projection.v1",
        "profile": str(profile),
        "mod_root": str(target),
        "tree_sha256": tree_digest.hexdigest(),
        "files": sorted(records, key=lambda item: str(item["path"])),
    }
    (evidence_root / "prepared-mod-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return manifest


def write_playset(profile: Path) -> dict[str, object]:
    """Write the build-24187685 playset without locale-sensitive round trips."""
    profile = profile.resolve()
    if not profile.is_dir():
        raise PreparationRefused(f"isolated profile does not exist: {profile}")
    mod_path = (profile / "mod" / MOD_DIRECTORY).resolve()
    if not mod_path.is_dir():
        raise PreparationRefused(f"acceptance Mod projection does not exist: {mod_path}")

    destination = profile / "playsets.json"
    if destination.exists():
        raise PreparationRefused(f"refusing to overwrite existing playset: {destination}")
    playset: dict[str, object] = {
        "file_version": "1.0.0",
        "playsets": [
            {
                "name": PLAYSET_NAME,
                "isActive": True,
                "isAutomaticallySorted": True,
                "orderedListMods": [
                    {
                        "path": mod_path.as_posix() + "/",
                        "isEnabled": True,
                    }
                ],
                "DLC": [
                    {"paradoxAppId": app_id, "isEnabled": enabled}
                    for app_id, enabled in EXACT_BUILD_DLC
                ],
            }
        ],
    }
    destination.write_text(
        json.dumps(playset, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return playset


def write_language_settings(profile: Path) -> dict[str, object]:
    """Seed the exact-build language before EU5 performs its first localization load."""
    profile = profile.resolve()
    if not profile.is_dir():
        raise PreparationRefused(f"isolated profile does not exist: {profile}")

    destination = profile / "pdx_settings.json"
    if destination.exists():
        raise PreparationRefused(
            f"refusing to overwrite existing language settings: {destination}"
        )
    settings: dict[str, object] = {
        "System": {
            "language": ACCEPTANCE_LANGUAGE,
        }
    }
    destination.write_text(
        json.dumps(settings, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return settings


def require_launch_destinations_absent(profile: Path) -> Path:
    """Refuse an already-initialized profile before writing any launch artifact."""
    profile = profile.resolve()
    if not profile.is_dir():
        raise PreparationRefused(f"isolated profile does not exist: {profile}")
    for destination, label in (
        (profile / "playsets.json", "playset"),
        (profile / "pdx_settings.json", "language settings"),
    ):
        if destination.exists():
            raise PreparationRefused(f"refusing to overwrite existing {label}: {destination}")
    return profile


def write_launch_configuration(profile: Path) -> dict[str, object]:
    """Preflight both destinations, then write playset and Simplified Chinese setting."""
    profile = require_launch_destinations_absent(profile)
    mod_path = (profile / "mod" / MOD_DIRECTORY).resolve()
    if not mod_path.is_dir():
        raise PreparationRefused(f"acceptance Mod projection does not exist: {mod_path}")

    settings = write_language_settings(profile)
    playset = write_playset(profile)
    return {"playset": playset, "settings": settings}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument(
        "--write-playset",
        action="store_true",
        help=(
            "also create exact-build playsets.json and pre-launch Simplified Chinese "
            "pdx_settings.json"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.write_playset:
            require_launch_destinations_absent(args.profile)
        manifest = compose(args.profile, args.evidence_root)
        if args.write_playset:
            write_launch_configuration(args.profile)
    except PreparationRefused as exc:
        sys.stderr.write(f"REFUSED: {exc}\n")
        return 2
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
