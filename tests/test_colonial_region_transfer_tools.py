from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "tools/validate_colonial_region_transfer_static.py"
BUILDER_PATH = REPO_ROOT / "tools/build_colonial_region_transfer_release.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("xcrt_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ColonialRegionTransferToolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()

    def test_brace_scanner_ignores_comments_and_strings(self) -> None:
        sample = 'root = { text = "a { brace }" # ignored }\n child = { value = yes }\n}'
        self.assertEqual([], self.validator.brace_errors(sample, "sample"))

    def test_duplicate_detector_is_stable(self) -> None:
        self.assertEqual(["a", "b"], self.validator.duplicate_values(["b", "a", "b", "a"]))

    def test_repository_source_contract(self) -> None:
        args = argparse.Namespace(
            game_root=str(self.validator.DEFAULT_GAME_ROOT),
            allow_missing_game_baseline=True,
            require_metadata=False,
            report=None,
        )
        report = self.validator.validate(args)
        self.assertFalse(report["errors"], report)
        self.assertEqual("PASS_WITH_GATES", report["status"])

    def test_release_builder_refuses_missing_native_metadata(self) -> None:
        result = subprocess.run(
            [sys.executable, str(BUILDER_PATH)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(2, result.returncode)
        self.assertIn("metadata.json is missing", result.stderr)


if __name__ == "__main__":
    unittest.main()
