#!/usr/bin/env python3
"""Source-level checks for For Vivhite: Colonial Border Cleanup.

This validator is intentionally honest about two gates it cannot satisfy by
itself: EU5-generated metadata and an Open Kaishek EU5 semantic profile.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
PRODUCT_ROOT = REPO_ROOT / "mod_colonial_region_transfer"
SCRIPT_REL = Path("in_game/common/country_interactions/xcrt_colonial_region_transfer.txt")
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
LOC_FILES = {
    language: Path(
        f"main_menu/localization/{language}/xcrt_colonial_region_transfer_l_{language}.yml"
    )
    for language in LANGUAGES
}
METADATA_REL = Path(".metadata/metadata.json")
LEGACY_GAME_ROOT = Path(r"D:\Program Files (x86)\Steam\steamapps\common\Europa Universalis V")
UTF8_BOM = b"\xef\xbb\xbf"
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
LOC_KEY_RE = re.compile(r"^\s*([A-Za-z0-9_.-]+):", re.MULTILINE)

VANILLA_HASHES = {
    Path("binaries/eu5.exe"): "c0db888da5e132cd6ab50c2c531c7cae419488bea0054cf8ac348616332683ef",
    Path("game/in_game/common/country_interactions/give_location_to_subject.txt"): "82f5bdf0c0c85637e7e1d81c9722d09083e7672fa08cfc8d9f91c6f9f6a489f3",
    Path("game/in_game/common/country_interactions/give_subject_location_to_other_subject.txt"): "58e84f71ad9219b2d1d81530d1b648d86b310b91fcda3c179d04e13e8022ee6e",
    Path("game/in_game/common/country_interactions/merge_colonies.txt"): "0aa4d7b3704c1f3c26ec2259bcdb08561acd7993aab925c12c1a2f32a1ffac2a",
    Path("game/in_game/common/country_interactions/readme.txt"): "2656714d72427abacd2497fc23bc80940a91df64f8c4f5d24c3839866a6ead23",
    Path("game/in_game/events/debug/qa_debug.txt"): "26664f3b8013c860dcf96690d5bd6e7544a3544198128fb9b56e13bedf30976e",
    Path("game/main_menu/localization/simp_chinese/country_interactions_l_simp_chinese.yml"): "86833fac8166602c67ba03a06e722b91e3c87ffcaa9ff03012a9f28f80511628",
}

REQUIRED_SCRIPT_FRAGMENTS = (
    "xcrt_cleanup_colonial_region = {",
    "type = subject",
    "category = CATEGORY_SUBJECT_ACTIONS",
    "ai_tick = never",
    "show_message = no",
    "show_message_to_target = no",
    "is_colonial_overlord = yes",
    "is_colonial_subject = yes",
    "target_flag = recipient",
    "scope:recipient.capital.region = {",
    "any_location_in_region = {",
    "every_location_in_region = {",
    "add_to_list = xcrt_transfer_locations",
    "every_in_list = {",
    "list = xcrt_transfer_locations",
    "is_subject_or_below_of = scope:actor",
    "change_location_owner = scope:recipient",
)

FORBIDDEN_SCRIPT_FRAGMENTS = (
    "root.capital.region",
)

REQUIRED_LOC_KEYS = {
    "xcrt_mod_name",
    "xcrt_cleanup_colonial_region",
    "xcrt_cleanup_colonial_region_act",
    "xcrt_cleanup_colonial_region_desc",
    "xcrt_cleanup_colonial_region_effect_text",
    "xcrt_cleanup_colonial_region_effect_text_past",
    "PROPOSE_xcrt_cleanup_colonial_region",
    "xcrt_select_colonial_subject",
    "xcrt_no_colonial_subject",
    "xcrt_target_must_be_at_peace_tt",
    "xcrt_overlord_capital_outside_region_tt",
    "xcrt_affected_subjects_at_peace_tt",
    "xcrt_has_transferable_locations_tt",
    "xcrt_transfer_effect_tt",
    "xcrt_select_colonial_subject_first_tt",
}


def steam_library_paths(vdf_text: str) -> list[Path]:
    """Extract Valve library paths without depending on a third-party VDF parser."""

    paths: list[Path] = []
    for encoded in re.findall(r'"path"\s+"([^"]+)"', vdf_text):
        candidate = Path(encoded.replace(r"\\", "\\"))
        if candidate not in paths:
            paths.append(candidate)
    return paths


def steam_roots() -> list[Path]:
    roots: list[Path] = []

    def add(candidate: str | Path | None) -> None:
        if not candidate:
            return
        path = Path(candidate)
        if path not in roots:
            roots.append(path)

    add(os.environ.get("STEAM_PATH"))
    if sys.platform == "win32":
        try:
            import winreg

            registry_locations = (
                (winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", "SteamPath"),
                (
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SOFTWARE\WOW6432Node\Valve\Steam",
                    "InstallPath",
                ),
            )
            for hive, key_name, value_name in registry_locations:
                try:
                    with winreg.OpenKey(hive, key_name) as key:
                        add(winreg.QueryValueEx(key, value_name)[0])
                except OSError:
                    continue
        except ImportError:
            pass
        add(Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Steam")
        add(Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Steam")
    return roots


def discover_default_game_root() -> Path:
    for steam_root in steam_roots():
        libraries = [steam_root]
        library_file = steam_root / "steamapps/libraryfolders.vdf"
        if library_file.is_file():
            try:
                libraries.extend(
                    steam_library_paths(library_file.read_text(encoding="utf-8-sig"))
                )
            except (OSError, UnicodeDecodeError):
                pass
        for library in libraries:
            candidate = library / "steamapps/common/Europa Universalis V"
            if candidate.is_dir():
                return candidate.resolve()
    return LEGACY_GAME_ROOT


DEFAULT_GAME_ROOT = discover_default_game_root()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_bom_text(path: Path, errors: list[str]) -> str:
    if not path.is_file():
        errors.append(f"missing file: {path}")
        return ""
    raw = path.read_bytes()
    if not raw.startswith(UTF8_BOM):
        errors.append(f"UTF-8 BOM missing: {path}")
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        errors.append(f"invalid UTF-8: {path}: {exc}")
        return ""


def brace_errors(text: str, label: str) -> list[str]:
    """Check P-script braces while ignoring comments and quoted strings."""

    issues: list[str] = []
    depth = 0
    line = 1
    in_string = False
    escaped = False
    in_comment = False
    for character in text:
        if character == "\n":
            line += 1
            in_comment = False
            escaped = False if not in_string else escaped
            continue
        if in_comment:
            continue
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == "#":
            in_comment = True
        elif character == '"':
            in_string = True
        elif character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth < 0:
                issues.append(f"{label}: unexpected closing brace at line {line}")
                depth = 0
    if in_string:
        issues.append(f"{label}: unterminated quoted string")
    if depth:
        issues.append(f"{label}: {depth} unclosed brace(s)")
    return issues


def duplicate_values(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def metadata_version_values(value: Any) -> list[str]:
    """Find version-like fields without assuming an unobserved EU5 schema."""

    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key.casefold() in {"version", "mod_version"} and isinstance(child, str):
                found.append(child)
            found.extend(metadata_version_values(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(metadata_version_values(child))
    return found


def validate(args: argparse.Namespace) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    checks: dict[str, Any] = {}

    version_path = PRODUCT_ROOT / "VERSION"
    if not version_path.is_file():
        errors.append(f"missing file: {version_path}")
        version = ""
    else:
        version = version_path.read_text(encoding="utf-8").strip()
        if not SEMVER_RE.fullmatch(version):
            errors.append(f"VERSION is not SemVer: {version!r}")
    checks["version"] = version

    script_path = PRODUCT_ROOT / SCRIPT_REL
    script = read_bom_text(script_path, errors)
    errors.extend(brace_errors(script, str(SCRIPT_REL)))
    for fragment in REQUIRED_SCRIPT_FRAGMENTS:
        if fragment not in script:
            errors.append(f"script fragment missing: {fragment}")
    for fragment in FORBIDDEN_SCRIPT_FRAGMENTS:
        if fragment in script:
            errors.append(f"forbidden selector scope fragment present: {fragment}")
    if script.count("scope:recipient.capital.region") < 4:
        errors.append(
            "recipient capital Region must be the shared source for all three selector checks and the effect"
        )
    if script.count("xcrt_cleanup_colonial_region = {") != 1:
        errors.append("interaction root must be declared exactly once")
    checks["script_sha256"] = sha256(script_path) if script_path.is_file() else None

    referenced_loc = set(
        re.findall(
            r"(?:name|text|none_available_msg_key)\s*=\s*\"?(xcrt_[A-Za-z0-9_.-]+)\"?",
            script,
        )
    )
    localization_hashes: dict[str, str | None] = {}
    for language, relative in LOC_FILES.items():
        loc_path = PRODUCT_ROOT / relative
        localization = read_bom_text(loc_path, errors)
        expected_header = f"l_{language}:"
        if localization and not localization.startswith(expected_header):
            errors.append(f"{language} localization header must be {expected_header}")
        localization_keys = LOC_KEY_RE.findall(localization)
        loc_duplicates = duplicate_values(localization_keys)
        if loc_duplicates:
            errors.append(f"duplicate {language} localization keys: {', '.join(loc_duplicates)}")
        missing_loc = sorted(REQUIRED_LOC_KEYS.difference(localization_keys))
        if missing_loc:
            errors.append(f"missing {language} localization keys: {', '.join(missing_loc)}")
        missing_references = sorted(referenced_loc.difference(localization_keys))
        if missing_references:
            errors.append(
                f"script references missing from {language} localization: {', '.join(missing_references)}"
            )
        name_match = re.search(r'^\s*xcrt_mod_name:\s*"([^"]+)"', localization, re.MULTILINE)
        localized_name = name_match.group(1) if name_match else ""
        if language == "simp_chinese":
            if localized_name != "献给白绮的殖民领版图整理":
                errors.append("Simplified Chinese Mod name does not match the approved title")
        elif "Vivhite" not in localized_name:
            errors.append(f"{language} Mod name must use the international name Vivhite")
        localization_hashes[language] = sha256(loc_path) if loc_path.is_file() else None
    checks["localization_sha256"] = localization_hashes

    metadata_path = PRODUCT_ROOT / METADATA_REL
    metadata: Any = None
    if not metadata_path.is_file():
        message = "EU5-generated .metadata/metadata.json is absent"
        if args.require_metadata:
            errors.append(message)
        else:
            warnings.append(message)
    else:
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"invalid metadata JSON: {exc}")
        if not isinstance(metadata, dict):
            errors.append("metadata root must be a JSON object")
        else:
            discovered_versions = metadata_version_values(metadata)
            checks["metadata_version_candidates"] = discovered_versions
            if version not in discovered_versions:
                errors.append("metadata has no version/mod_version field matching VERSION")
    checks["metadata"] = "present" if metadata_path.is_file() else "pending-eu5-mod-tools"

    game_root = Path(args.game_root).resolve()
    baseline_results: dict[str, str] = {}
    if not game_root.is_dir():
        message = f"EU5 game root unavailable: {game_root}"
        if args.allow_missing_game_baseline:
            warnings.append(message)
        else:
            errors.append(message)
    else:
        for relative, expected in VANILLA_HASHES.items():
            candidate = game_root / relative
            if not candidate.is_file():
                errors.append(f"exact-build evidence missing: {candidate}")
                baseline_results[relative.as_posix()] = "missing"
                continue
            actual = sha256(candidate)
            baseline_results[relative.as_posix()] = actual
            if actual.casefold() != expected.casefold():
                errors.append(
                    f"exact-build hash mismatch: {relative.as_posix()} expected {expected} got {actual}"
                )
    checks["exact_build_hashes"] = baseline_results

    warnings.append(
        "Open Kaishek EU5 Build 24187685 profile is not yet available; semantic tool coverage is RED"
    )
    status = "FAIL" if errors else ("PASS_WITH_GATES" if warnings else "PASS")
    return {
        "schema": "xcrt.static-validation.v1",
        "status": status,
        "product": "colonial_region_transfer",
        "target": {
            "steam_app_id": 3450310,
            "steam_build_id": 24187685,
            "game_root": str(game_root),
        },
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--game-root",
        default=os.environ.get("EU5_GAME_ROOT") or str(DEFAULT_GAME_ROOT),
        help="Europa Universalis V installation root",
    )
    parser.add_argument(
        "--allow-missing-game-baseline",
        action="store_true",
        help="downgrade an unavailable local EU5 installation to a warning",
    )
    parser.add_argument(
        "--require-metadata",
        action="store_true",
        help="fail unless current-build EU5 Mod Tools metadata exists and matches VERSION",
    )
    parser.add_argument("--report", type=Path, help="also write the JSON report to this path")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = validate(args)
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    sys.stdout.write(rendered)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
