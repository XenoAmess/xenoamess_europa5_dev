from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "tools/validate_colonial_region_transfer_static.py"
BUILDER_PATH = REPO_ROOT / "tools/build_colonial_region_transfer_release.py"
PREPARER_PATH = REPO_ROOT / "tools/prepare_colonial_region_transfer_acceptance.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("xcrt_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_builder():
    spec = importlib.util.spec_from_file_location("xcrt_builder", BUILDER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_preparer():
    spec = importlib.util.spec_from_file_location("xcrt_preparer", PREPARER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load acceptance preparer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ColonialRegionTransferToolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.builder = load_builder()
        cls.preparer = load_preparer()

    def test_brace_scanner_ignores_comments_and_strings(self) -> None:
        sample = 'root = { text = "a { brace }" # ignored }\n child = { value = yes }\n}'
        self.assertEqual([], self.validator.brace_errors(sample, "sample"))

    def test_duplicate_detector_is_stable(self) -> None:
        self.assertEqual(["a", "b"], self.validator.duplicate_values(["b", "a", "b", "a"]))

    def test_steam_library_parser_decodes_windows_paths(self) -> None:
        vdf = '"path" "C:\\\\Steam"\n"path" "E:\\\\SteamLibrary"\n'
        self.assertEqual(
            [Path(r"C:\Steam"), Path(r"E:\SteamLibrary")],
            self.validator.steam_library_paths(vdf),
        )

    def test_repository_source_contract(self) -> None:
        args = argparse.Namespace(
            game_root=str(self.validator.DEFAULT_GAME_ROOT),
            allow_missing_game_baseline=True,
            require_metadata=False,
            require_open_kaishek=False,
            report=None,
        )
        report = self.validator.validate(args)
        self.assertFalse(report["errors"], report)
        self.assertIn(report["status"], {"PASS", "PASS_WITH_GATES"})

    def test_selector_region_is_anchored_to_recipient(self) -> None:
        script_path = self.validator.PRODUCT_ROOT / self.validator.SCRIPT_REL
        script = script_path.read_text(encoding="utf-8-sig")
        self.assertNotIn("root.capital.region", script)
        self.assertGreaterEqual(script.count("scope:recipient.capital.region"), 6)

    def test_selector_accepts_all_direct_territorial_subjects(self) -> None:
        script_path = self.validator.PRODUCT_ROOT / self.validator.SCRIPT_REL
        script = script_path.read_text(encoding="utf-8-sig")
        triggers_path = self.validator.PRODUCT_ROOT / self.validator.TRIGGERS_REL
        triggers = triggers_path.read_text(encoding="utf-8-sig")
        self.assertIn("every_subject = {", script)
        self.assertIn("is_subject_of = scope:actor", triggers)
        self.assertNotIn("is_colonial_subject = yes", script + triggers)
        self.assertNotIn("is_colonial_overlord = yes", script + triggers)
        for excluded_type in ("building", "pop", "army"):
            self.assertIn(f"country_type = {excluded_type}", triggers)

    def test_tusi_cap_is_identical_before_and_after_snapshot(self) -> None:
        triggers_path = self.validator.PRODUCT_ROOT / self.validator.TRIGGERS_REL
        triggers = triggers_path.read_text(encoding="utf-8-sig")
        selector_pairs = {
            int(current): int(maximum)
            for current, maximum in self.validator.re.findall(
                r"num_locations\s*=\s*(\d+)\s+"
                r"capital\.region\s*=\s*\{\s*any_location_in_region\s*=\s*\{\s*"
                r"count\s*<=\s*(\d+)\s+xcrt_is_transferable_location\s*=\s*yes\s*\}\s*\}",
                triggers,
            )
        }
        snapshot_pairs = {
            int(current): int(maximum)
            for current, maximum in self.validator.re.findall(
                r"num_locations\s*=\s*(\d+)\s+"
                r"list_size\s*=\s*\{\s*name\s*=\s*xcrt_transfer_locations\s+"
                r"value\s*<=\s*(\d+)\s*\}",
                triggers,
            )
        }
        expected = {current: 15 - current for current in range(1, 15)}
        self.assertEqual(expected, selector_pairs)
        self.assertEqual(expected, snapshot_pairs)
        self.assertNotIn("$MAX$", triggers)
        self.assertNotIn("trigger_if", triggers)
        self.assertEqual(2, triggers.count("NOT = { is_subject_type = tusi }"))

    def test_transfer_set_is_snapshotted_before_mutation(self) -> None:
        script_path = self.validator.PRODUCT_ROOT / self.validator.SCRIPT_REL
        script = script_path.read_text(encoding="utf-8-sig")
        snapshot = script.index("add_to_list = xcrt_transfer_locations")
        replay = script.index("list = xcrt_transfer_locations")
        mutation = script.index("change_location_owner = scope:recipient")
        self.assertLess(snapshot, replay)
        self.assertLess(replay, mutation)

    def test_native_tusi_fixture_isolates_other_donors_after_freezing_them(self) -> None:
        fixture = (
            REPO_ROOT
            / "fixtures/colonial_region_transfer/overlay/in_game/events/"
            "xcrt_phase2_acceptance_fixture.txt"
        ).read_text(encoding="utf-8-sig")
        scenario = fixture.split("xcrt_acceptance.11 = {", 1)[1].split(
            "xcrt_acceptance.12 = {", 1
        )[0]
        self.assertIn("set_capital = location:porto_santo", scenario)
        self.assertIn("NOT = { owner ?= c:GYT }", scenario)
        self.assertIn("NOT = { this = location:tongan_lijiang }", scenario)
        freeze = scenario.index("add_to_list = xcrt_acceptance_extra_donors_to_isolate")
        replay = scenario.index("list = xcrt_acceptance_extra_donors_to_isolate")
        isolation = scenario.index("change_location_owner = c:XCRTI", replay)
        self.assertLess(freeze, replay)
        self.assertLess(replay, isolation)

    def test_acceptance_audits_use_exact_complements_and_cancel_audit(self) -> None:
        base = (
            REPO_ROOT
            / "fixtures/colonial_region_transfer/overlay/in_game/events/"
            "xcrt_acceptance_fixture.txt"
        ).read_text(encoding="utf-8-sig")
        phase2 = (
            REPO_ROOT
            / "fixtures/colonial_region_transfer/overlay/in_game/events/"
            "xcrt_phase2_acceptance_fixture.txt"
        ).read_text(encoding="utf-8-sig")
        for option_name in (
            "xcrt_acceptance.2.fail",
            "xcrt_acceptance.3.fail",
        ):
            option = base.split(f"name = {option_name}", 1)[1].split("custom_tooltip", 1)[0]
            self.assertIn("NAND = {", option)
        for option_name in (
            "xcrt_acceptance.9.fail",
            "xcrt_acceptance.12.fail",
            "xcrt_acceptance.14.fail",
            "xcrt_acceptance.16.fail",
            "xcrt_acceptance.21.fail",
        ):
            option = phase2.split(f"name = {option_name}", 1)[1].split(
                "custom_tooltip", 1
            )[0]
            self.assertIn("NAND = {", option)

        cancel = phase2.split("xcrt_acceptance.16 = {", 1)[1].split(
            "xcrt_acceptance.20 = {", 1
        )[0]
        for expected in (
            "location:tortuga = { owner = c:XCRTT }",
            "location:marien = { owner = global_var:xcrt_acceptance_actor }",
            "location:guahaba = { owner = c:XCRTD }",
            "location:baynoa = { owner = c:XCRTS }",
            "location:iguamuco = { owner = c:XCRTI }",
            "location:porto_santo = { owner = c:XCRTD }",
            "num_locations = 1",
            "num_locations = 2",
        ):
            self.assertIn(expected, cancel)

    def test_interaction_suppresses_undefined_post_action_messages(self) -> None:
        script_path = self.validator.PRODUCT_ROOT / self.validator.SCRIPT_REL
        script = script_path.read_text(encoding="utf-8-sig")
        self.assertIn("show_message = no", script)
        self.assertIn("show_message_to_target = no", script)

    def test_release_builder_refuses_missing_native_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(self.builder.BuildRefused, "metadata.json is missing"):
                self.builder.require_native_metadata(Path(temp))

    def test_acceptance_projection_keeps_fixture_external_to_product(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            profile = temp_root / "profile"
            evidence = temp_root / "evidence"
            profile.mkdir()
            manifest = self.preparer.compose(profile, evidence)
            target = profile / "mod" / self.preparer.MOD_DIRECTORY
            fixture_event = Path("in_game/events/xcrt_acceptance_fixture.txt")
            self.assertTrue((target / fixture_event).is_file())
            self.assertFalse((self.preparer.PRODUCT_ROOT / fixture_event).exists())
            origins = {record["path"]: record["origin"] for record in manifest["files"]}
            self.assertEqual("fixture", origins[fixture_event.as_posix()])
            self.assertEqual("product", origins[".metadata/metadata.json"])

    def test_acceptance_playset_is_ascii_json_and_enables_only_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            profile = temp_root / "profile"
            evidence = temp_root / "evidence"
            profile.mkdir()
            self.preparer.compose(profile, evidence)
            expected = self.preparer.write_playset(profile)
            raw = (profile / "playsets.json").read_bytes()
            self.assertTrue(raw.isascii())
            observed = json.loads(raw)
            self.assertEqual(expected, observed)
            mods = observed["playsets"][0]["orderedListMods"]
            self.assertEqual(1, len(mods))
            self.assertTrue(mods[0]["isEnabled"])
            self.assertTrue(mods[0]["path"].endswith("/xcrt_colonial_region_transfer/"))

    def test_release_projection_is_reproducible_and_allowlisted(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            product_root = temp_root / "product"
            for index, relative in enumerate(self.builder.ALLOWLIST):
                target = product_root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(f"fixture-{index}\n".encode())
            excluded = product_root / "in_game/events/xcrt_acceptance_fixture.txt"
            excluded.parent.mkdir(parents=True, exist_ok=True)
            excluded.write_text("fixture = yes\n", encoding="utf-8")

            report = self.builder.check_reproducible(
                product_root,
                "0.1.0",
                "a" * 40,
                "colonial_region_transfer-v0.1.0",
            )
            self.assertEqual("PASS", report["status"])

            release_root = temp_root / "release"
            manifest = self.builder.build_projection(
                product_root,
                release_root,
                "0.1.0",
                "a" * 40,
                "colonial_region_transfer-v0.1.0",
            )
            manifest_on_disk = json.loads(
                (release_root / "colonial_region_transfer-0.1.0.manifest.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(manifest, manifest_on_disk)
            with zipfile.ZipFile(release_root / "colonial_region_transfer-0.1.0.zip") as archive:
                self.assertEqual(
                    sorted(relative.as_posix() for relative in self.builder.ALLOWLIST),
                    archive.namelist(),
                )
                self.assertNotIn("in_game/events/xcrt_acceptance_fixture.txt", archive.namelist())


if __name__ == "__main__":
    unittest.main()
