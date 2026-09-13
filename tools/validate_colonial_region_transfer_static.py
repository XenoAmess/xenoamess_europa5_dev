#!/usr/bin/env python3
"""Source-level checks for For Vivhite: Subject Territory Consolidation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
PRODUCT_ROOT = REPO_ROOT / "mod_colonial_region_transfer"
SCRIPT_REL = Path("in_game/common/country_interactions/xcrt_colonial_region_transfer.txt")
TRIGGERS_REL = Path(
    "in_game/common/scripted_triggers/xcrt_subject_territory_consolidation_triggers.txt"
)
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
OPEN_KAISHEK_ROOT = REPO_ROOT.parent / "open_kaishek"
OPEN_KAISHEK_JAR = OPEN_KAISHEK_ROOT / "kaishek-cli/target/kaishek-cli-0.1.0-SNAPSHOT.jar"
OPEN_KAISHEK_PROFILE = "eu5-1.3.11-build-24187685"
THUMBNAIL_REL = Path(
    "workshop/colonial_region_transfer/media/icon-vivhite-subject-consolidation-v2-512.png"
)
THUMBNAIL_SHA256 = "ebb1c217d594235070e51bf221b89b156c5fb7a2389e337821f022201027189a"
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
    Path("game/in_game/common/country_interactions/move_subject_capital.txt"): "7c103ee37ff67c8fc6118ea44144d3e7c42ba8c6fd1a4e266f043cb67808e6f0",
    Path("game/in_game/common/subject_types/readme.txt"): "06a72f97064d4f88bd1582dd50890a337ddd95b602f275dc57407f33bf842837",
    Path("game/in_game/common/subject_types/colonial_nation.txt"): "f39406149eec6a7dbc84bac977c9831b081d32667daeb56b2c7b92806483af58",
    Path("game/in_game/common/subject_types/state_bank.txt"): "c90271bca606e9f3129e2ee57d169112c50f4d2e066f312f49d621863a302bae",
    Path("game/in_game/common/subject_types/trade_company.txt"): "5bcdc8852af7dd5633d04bb4c2c01113ca85f3b06a2a466b23301109bc641d55",
}

EXPECTED_SUBJECT_TYPES = {
    "appanage",
    "colonial_nation",
    "conquistador",
    "direct_imperial_free_city",
    "dominion",
    "fiefdom",
    "hanseatic_member",
    "imperial_free_city",
    "maha_samanta",
    "march",
    "pradhana_maha_samanta",
    "pronoia",
    "samanta",
    "secessionists",
    "state_bank",
    "trade_company",
    "tributary",
    "tusi",
    "uc_bey",
    "vassal",
}

REQUIRED_SCRIPT_FRAGMENTS = (
    "xcrt_cleanup_colonial_region = {",
    "type = subject",
    "category = CATEGORY_SUBJECT_ACTIONS",
    "ai_tick = never",
    "show_message = no",
    "show_message_to_target = no",
    "any_subject = {",
    "every_subject = {",
    "xcrt_is_eligible_direct_subject_target = yes",
    "target_flag = recipient",
    "scope:recipient.capital.region = {",
    "any_location_in_region = {",
    "every_location_in_region = {",
    "add_to_list = xcrt_transfer_locations",
    "every_in_list = {",
    "list = xcrt_transfer_locations",
    "change_location_owner = scope:recipient",
    "xcrt_frozen_transfer_list_respects_tusi_cap = yes",
    "xcrt_requirements_changed_tt",
)

REQUIRED_TRIGGER_FRAGMENTS = (
    "xcrt_is_eligible_direct_subject_target = {",
    "country_type = building",
    "country_type = pop",
    "country_type = army",
    "exists = capital",
    "is_subject_of = scope:actor",
    "is_subject_or_below_of = scope:actor",
    "xcrt_recipient_respects_tusi_cap = {",
    "is_subject_type = tusi",
    "count <= $MAX$",
    "xcrt_frozen_transfer_list_respects_tusi_cap = {",
    "list_size = { name = xcrt_transfer_locations value <= 1 }",
)

FORBIDDEN_SCRIPT_FRAGMENTS = (
    "root.capital.region",
    "is_colonial_overlord = yes",
    "is_colonial_subject = yes",
)

REQUIRED_LOC_KEYS = {
    "xcrt_mod_name",
    "xcrt_cleanup_colonial_region",
    "xcrt_cleanup_colonial_region_act",
    "xcrt_cleanup_colonial_region_desc",
    "xcrt_cleanup_colonial_region_effect_text",
    "xcrt_cleanup_colonial_region_effect_text_past",
    "PROPOSE_xcrt_cleanup_colonial_region",
    "xcrt_select_subject",
    "xcrt_no_subject",
    "xcrt_target_must_be_at_peace_tt",
    "xcrt_overlord_capital_outside_region_tt",
    "xcrt_affected_subjects_at_peace_tt",
    "xcrt_has_transferable_locations_tt",
    "xcrt_subject_location_limit_tt",
    "xcrt_transfer_effect_tt",
    "xcrt_requirements_changed_tt",
    "xcrt_select_subject_first_tt",
    "xcrt_select_colonial_subject",
    "xcrt_no_colonial_subject",
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


def png_dimensions(path: Path) -> tuple[int, int] | None:
    """Read the PNG IHDR dimensions without introducing an image dependency."""

    if not path.is_file():
        return None
    raw = path.read_bytes()[:24]
    if len(raw) != 24 or raw[:8] != b"\x89PNG\r\n\x1a\n" or raw[12:16] != b"IHDR":
        return None
    return int.from_bytes(raw[16:20], "big"), int.from_bytes(raw[20:24], "big")


def subject_type_inventory(subject_root: Path) -> set[str]:
    """Collect exact-build top-level subject type declarations."""

    result: set[str] = set()
    if not subject_root.is_dir():
        return result
    declaration = re.compile(r"^([A-Za-z0-9_]+)\s*=\s*\{", re.MULTILINE)
    for path in sorted(subject_root.glob("*.txt")):
        if path.name.casefold() == "readme.txt":
            continue
        result.update(declaration.findall(path.read_text(encoding="utf-8-sig")))
    return result


def run_open_kaishek(path: Path) -> dict[str, Any]:
    command = [
        "java",
        "-jar",
        str(OPEN_KAISHEK_JAR),
        "validate",
        "--profile",
        OPEN_KAISHEK_PROFILE,
        "--file",
        str(path),
    ]
    completed = subprocess.run(command, text=True, capture_output=True, encoding="utf-8")
    output = completed.stdout.strip()
    try:
        payload = json.loads(output)
    except json.JSONDecodeError:
        payload = {
            "status": "ERROR",
            "stdout": output,
            "stderr": completed.stderr.strip(),
        }
    payload["exit_code"] = completed.returncode
    return payload


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
    if script.count("scope:recipient.capital.region") < 6:
        errors.append(
            "recipient capital Region must anchor selector checks, snapshot, and effect-side rechecks"
        )
    if script.count("xcrt_cleanup_colonial_region = {") != 1:
        errors.append("interaction root must be declared exactly once")
    checks["script_sha256"] = sha256(script_path) if script_path.is_file() else None

    triggers_path = PRODUCT_ROOT / TRIGGERS_REL
    triggers = read_bom_text(triggers_path, errors)
    errors.extend(brace_errors(triggers, str(TRIGGERS_REL)))
    for fragment in REQUIRED_TRIGGER_FRAGMENTS:
        if fragment not in triggers:
            errors.append(f"scripted trigger fragment missing: {fragment}")
    tusi_pairs = {
        int(location_count): int(maximum)
        for location_count, maximum in re.findall(
            r"num_locations\s*=\s*(\d+)\s+"
            r"xcrt_has_at_most_transferable_locations\s*=\s*\{\s*MAX\s*=\s*(\d+)\s*\}",
            triggers,
        )
    }
    expected_tusi_pairs = {count: 15 - count for count in range(1, 15)}
    if tusi_pairs != expected_tusi_pairs:
        errors.append(
            f"selector Tusi cap matrix mismatch: expected {expected_tusi_pairs}, got {tusi_pairs}"
        )
    frozen_tusi_pairs = {
        int(location_count): int(maximum)
        for location_count, maximum in re.findall(
            r"num_locations\s*=\s*(\d+)\s+"
            r"list_size\s*=\s*\{\s*name\s*=\s*xcrt_transfer_locations\s+"
            r"value\s*<=\s*(\d+)\s*\}",
            triggers,
        )
    }
    if frozen_tusi_pairs != expected_tusi_pairs:
        errors.append(
            "effect-side frozen-list Tusi cap matrix does not match the selector matrix"
        )
    checks["tusi_cap_matrix"] = tusi_pairs
    checks["scripted_triggers_sha256"] = (
        sha256(triggers_path) if triggers_path.is_file() else None
    )

    referenced_loc = set(
        re.findall(
            r"(?:text|none_available_msg_key)\s*=\s*\"?(xcrt_[A-Za-z0-9_.-]+)\"?"
            r"|name\s*=\s*\"(xcrt_[A-Za-z0-9_.-]+)\"",
            script,
        )
    )
    referenced_loc = {key for pair in referenced_loc for key in pair if key}
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
            if localized_name != "献给白绮的附属地整合":
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
            if metadata.get("id") != "xenoamess.colonial_region_transfer":
                errors.append("metadata stable ID changed")
            if metadata.get("name") != "献给白绮的附属地整合":
                errors.append("metadata name does not match the 0.2.0 title")
    checks["metadata"] = "present" if metadata_path.is_file() else "pending-eu5-mod-tools"

    thumbnail_path = REPO_ROOT / THUMBNAIL_REL
    thumbnail_dimensions = png_dimensions(thumbnail_path)
    if thumbnail_dimensions != (512, 512):
        errors.append(
            f"selected Workshop thumbnail must be a 512x512 PNG: {thumbnail_path}"
        )
    thumbnail_hash = sha256(thumbnail_path) if thumbnail_path.is_file() else None
    if thumbnail_hash != THUMBNAIL_SHA256:
        errors.append(
            f"selected Workshop thumbnail hash mismatch: expected {THUMBNAIL_SHA256} got {thumbnail_hash}"
        )
    checks["selected_thumbnail"] = {
        "path": THUMBNAIL_REL.as_posix(),
        "dimensions": thumbnail_dimensions,
        "sha256": thumbnail_hash,
    }

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
        inventory = subject_type_inventory(
            game_root / "game/in_game/common/subject_types"
        )
        checks["subject_type_inventory"] = sorted(inventory)
        if inventory != EXPECTED_SUBJECT_TYPES:
            errors.append(
                "exact-build subject type inventory changed: "
                f"missing={sorted(EXPECTED_SUBJECT_TYPES - inventory)} "
                f"added={sorted(inventory - EXPECTED_SUBJECT_TYPES)}"
            )
    checks["exact_build_hashes"] = baseline_results

    open_kaishek_results: dict[str, Any] = {}
    if not OPEN_KAISHEK_JAR.is_file():
        message = f"Open Kaishek EU5 profile JAR is unavailable: {OPEN_KAISHEK_JAR}"
        if getattr(args, "require_open_kaishek", False):
            errors.append(message)
        else:
            warnings.append(message)
    else:
        for relative, path in ((SCRIPT_REL, script_path), (TRIGGERS_REL, triggers_path)):
            result = run_open_kaishek(path)
            open_kaishek_results[relative.as_posix()] = result
            if result.get("exit_code") != 0 or result.get("status") != "VALIDATED":
                errors.append(
                    f"Open Kaishek {OPEN_KAISHEK_PROFILE} rejected {relative.as_posix()}: {result}"
                )
    checks["open_kaishek"] = open_kaishek_results
    status = "FAIL" if errors else ("PASS_WITH_GATES" if warnings else "PASS")
    return {
        "schema": "xcrt.static-validation.v2",
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
    parser.add_argument(
        "--require-open-kaishek",
        action="store_true",
        help="fail unless the pinned Open Kaishek EU5 profile validates the product scripts",
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
