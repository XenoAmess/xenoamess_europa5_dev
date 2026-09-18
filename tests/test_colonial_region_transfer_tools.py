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

    def test_baseline_subject_matrix_has_per_type_failure_diagnostics(self) -> None:
        phase2 = (
            REPO_ROOT
            / "fixtures/colonial_region_transfer/overlay/in_game/events/"
            "xcrt_phase2_acceptance_fixture.txt"
        ).read_text(encoding="utf-8-sig")
        diagnostics = phase2.split("xcrt_acceptance.22 = {", 1)[1]
        expected = {
            "XMCOL": "colonial_nation",
            "XMCON": "conquistador",
            "XMDOM": "dominion",
            "XMFIE": "fiefdom",
            "XMIFC": "imperial_free_city",
            "XMSEC": "secessionists",
            "XMVAS": "vassal",
            "XMPRN": "pronoia",
            "XMUBE": "uc_bey",
            "XMBNK": "state_bank",
            "XMTRD": "trade_company",
        }
        for tag, subject_type in expected.items():
            option = diagnostics.split(
                f"name = xcrt_acceptance.22.{subject_type}", 1
            )[1].split("option =", 1)[0]
            self.assertIn(f"c:{tag}", option)
            self.assertIn(f"is_subject_type = {subject_type}", option)
            self.assertIn("is_subject_of = global_var:xcrt_acceptance_actor", option)
            expected_country_type = (
                "building" if subject_type in {"state_bank", "trade_company"} else "location"
            )
            self.assertIn(f"country_type = {expected_country_type}", option)
            if expected_country_type == "location":
                self.assertIn("exists = capital", option)

    def test_restricted_subject_types_use_exact_build_contexts(self) -> None:
        phase2 = (
            REPO_ROOT
            / "fixtures/colonial_region_transfer/overlay/in_game/events/"
            "xcrt_phase2_acceptance_fixture.txt"
        ).read_text(encoding="utf-8-sig")
        for event_id, actor, target, subject_type in (
            ("30", "FRA", "ALE", "appanage"),
            ("31", "HSA", "LUB", "hanseatic_member"),
            ("32", "TUN", "BTL", "tributary"),
            ("34", None, "XMSPM", "march"),
            ("36", None, "LUB", "direct_imperial_free_city"),
        ):
            event = phase2.split(f"xcrt_acceptance.{event_id} = {{", 1)[1].split(
                "\nxcrt_acceptance.", 1
            )[0]
            if actor:
                self.assertIn(f"tag = {actor}", event)
            self.assertIn(f"c:{target}", event)
            self.assertIn(f"is_subject_type = {subject_type}", event)
            self.assertIn("country_type = location", event)
            self.assertIn("exists = capital", event)

        march_setup = phase2.split("xcrt_acceptance.33 = {", 1)[1].split(
            "\nxcrt_acceptance.34 = {", 1
        )[0]
        self.assertIn("set_country_rank = country_rank:rank_county", march_setup)
        self.assertIn("type = subject_type:march", march_setup)

        march_diagnostics = phase2.split("xcrt_acceptance.39 = {", 1)[1].split(
            "\nxcrt_acceptance.", 1
        )[0]
        self.assertIn("has_global_variable = xcrt_acceptance_special_march_ready", march_diagnostics)
        self.assertIn("country_exists = c:XMSPM", march_diagnostics)
        self.assertIn("has_global_variable = xcrt_acceptance_actor", march_diagnostics)
        self.assertIn("this = global_var:xcrt_acceptance_actor", march_diagnostics)
        self.assertIn("is_subject_of = global_var:xcrt_acceptance_actor", march_diagnostics)
        self.assertIn("is_subject_type = march", march_diagnostics)
        self.assertIn("country_type = location", march_diagnostics)
        self.assertIn("exists = capital", march_diagnostics)
        self.assertIn("country_rank = country_rank:rank_county", march_diagnostics)
        self.assertIn("subject_type_is_not_locked = yes", march_diagnostics)
        self.assertEqual(18, march_diagnostics.count("\toption ="))
        march_localization = (
            REPO_ROOT
            / "fixtures/colonial_region_transfer/overlay/main_menu/localization/"
            "simp_chinese/xcrt_acceptance_fixture_l_simp_chinese.yml"
        ).read_text(encoding="utf-8-sig")
        for suffix in (
            "title",
            "desc",
            "ready_pass",
            "ready_fail",
            "actor_pass",
            "actor_fail",
            "rank_pass",
            "rank_fail",
            "unlocked_pass",
            "unlocked_fail",
        ):
            self.assertIn(f" xcrt_acceptance.39.{suffix}:", march_localization)

        direct_ifc_setup = phase2.split("xcrt_acceptance.35 = {", 1)[1].split(
            "\nxcrt_acceptance.36 = {", 1
        )[0]
        self.assertIn("tag = UBV", direct_ifc_setup)
        self.assertIn("international_organization:hre", direct_ifc_setup)
        self.assertIn("name = hre_direct_free_cities_subject", direct_ifc_setup)
        self.assertIn("type = subject_type:direct_imperial_free_city", direct_ifc_setup)

        samanta_setup = phase2.split("xcrt_acceptance.37 = {", 1)[1].split(
            "\nxcrt_acceptance.38 = {", 1
        )[0]
        for tag in ("GWA", "HAD", "MEW"):
            self.assertIn(f"c:{tag}", samanta_setup)
        self.assertIn("tag = DLH", samanta_setup)
        self.assertIn("type = subject_type:maha_samanta", samanta_setup)
        self.assertIn("type = subject_type:pradhana_maha_samanta", samanta_setup)

        samanta_audit = phase2.split("xcrt_acceptance.38 = {", 1)[1].split(
            "\nxcrt_acceptance.", 1
        )[0]
        for tag, subject_type in (
            ("GWA", "samanta"),
            ("HAD", "maha_samanta"),
            ("MEW", "pradhana_maha_samanta"),
        ):
            self.assertIn(f"c:{tag}", samanta_audit)
            self.assertIn(f"is_subject_type = {subject_type}", samanta_audit)
        self.assertIn("country_type = location", samanta_audit)
        self.assertIn("exists = capital", samanta_audit)

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

    def test_acceptance_language_settings_seed_exact_build_simplified_chinese(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            profile = Path(temp) / "profile"
            profile.mkdir()
            expected = self.preparer.write_language_settings(profile)
            raw = (profile / "pdx_settings.json").read_bytes()
            self.assertTrue(raw.isascii())
            self.assertEqual(
                {"System": {"language": "l_simp_chinese"}},
                expected,
            )
            self.assertEqual(expected, json.loads(raw))

    def test_acceptance_launch_config_refuses_existing_settings_without_partial_write(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            profile = temp_root / "profile"
            evidence = temp_root / "evidence"
            profile.mkdir()
            self.preparer.compose(profile, evidence)
            settings_path = profile / "pdx_settings.json"
            original = b'{"System":{"language":"l_english"}}\n'
            settings_path.write_bytes(original)

            with self.assertRaisesRegex(
                self.preparer.PreparationRefused,
                "refusing to overwrite existing language settings",
            ):
                self.preparer.write_launch_configuration(profile)

            self.assertEqual(original, settings_path.read_bytes())
            self.assertFalse((profile / "playsets.json").exists())

    def test_acceptance_launch_config_writes_playset_and_language_before_launch(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            profile = temp_root / "profile"
            evidence = temp_root / "evidence"
            profile.mkdir()
            self.preparer.compose(profile, evidence)

            observed = self.preparer.write_launch_configuration(profile)

            self.assertEqual(
                "l_simp_chinese",
                observed["settings"]["System"]["language"],
            )
            self.assertTrue((profile / "playsets.json").is_file())
            self.assertTrue((profile / "pdx_settings.json").is_file())

    def test_acceptance_cli_preflight_refuses_before_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            profile = temp_root / "profile"
            evidence = temp_root / "evidence"
            profile.mkdir()
            settings_path = profile / "pdx_settings.json"
            original = b'{"System":{"language":"l_english"}}\n'
            settings_path.write_bytes(original)

            completed = subprocess.run(
                [
                    sys.executable,
                    str(PREPARER_PATH),
                    "--profile",
                    str(profile),
                    "--evidence-root",
                    str(evidence),
                    "--write-playset",
                ],
                cwd=REPO_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(2, completed.returncode)
            self.assertIn("refusing to overwrite existing language settings", completed.stderr)
            self.assertEqual(original, settings_path.read_bytes())
            self.assertFalse((profile / "mod").exists())
            self.assertFalse(evidence.exists())

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
