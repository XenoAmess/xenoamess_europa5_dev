from __future__ import annotations

import os
import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


REPOSITORY = Path(__file__).resolve().parents[1]
TOOLS = REPOSITORY / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from eu5_acceptance import build_parser  # noqa: E402
from eu5_runtime.evidence import create_run  # noqa: E402
from eu5_runtime.model import OcrSpan, WindowBinding, normalize_ocr_text  # noqa: E402
from eu5_runtime.ocr import (  # noqa: E402
    CPU_PROVIDER,
    CUDA_PROVIDER,
    OcrBackendError,
    OcrRuntime,
    recognize_image,
    validate_session_providers,
)
from eu5_runtime.windows import (  # noqa: E402
    WindowBindingError,
    action_receipt,
    drag,
    ensure_foreground,
    select_unique_window,
    wheel,
)
from prune_runtime_evidence import resolve_target  # noqa: E402


class ModelTests(unittest.TestCase):
    def test_normalization_and_bbox_projection(self) -> None:
        span = OcrSpan.from_polygon(
            " 整合\n附属地 ",
            0.9,
            [(1.2, 2.1), (11.2, 2.0), (11.0, 8.8), (1.0, 9.0)],
            (100, 200),
        )
        self.assertEqual("整合附属地", normalize_ocr_text(span.text))
        self.assertEqual((101, 202, 111, 209), span.bbox)
        self.assertEqual((106, 205), span.center)


class EvidenceTests(unittest.TestCase):
    def test_create_run_is_unique_and_non_overwriting(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run, manifest = create_run(root, "xcrt-test-run")
            self.assertEqual("xcrt-test-run", manifest["run_id"])
            self.assertTrue((run / "evidence" / "run.json").is_file())
            with self.assertRaises(FileExistsError):
                create_run(root, "xcrt-test-run")

    def test_prune_target_cannot_escape_runtime_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaises(ValueError):
                resolve_target(root, "../outside")
            with self.assertRaises(ValueError):
                resolve_target(root, "*.json")


class OcrTests(unittest.TestCase):
    def test_cuda_provider_must_be_first_for_every_session(self) -> None:
        valid = {
            name: (CUDA_PROVIDER, CPU_PROVIDER)
            for name in ("text_det", "text_cls", "text_rec")
        }
        validate_session_providers("cuda", valid)
        valid["text_rec"] = (CPU_PROVIDER,)
        with self.assertRaises(OcrBackendError):
            validate_session_providers("cuda", valid)

    def test_recognize_projects_crop_coordinates(self) -> None:
        from PIL import Image

        class Output:
            boxes = [[(1, 2), (11, 2), (11, 8), (1, 8)]]
            txts = ["白绮"]
            scores = [0.95]

        class Engine:
            def __call__(self, _image):
                return Output()

        runtime = OcrRuntime(
            Engine(),
            "cpu",
            0,
            (CPU_PROVIDER,),
            {name: (CPU_PROVIDER,) for name in ("text_det", "text_cls", "text_rec")},
        )
        with tempfile.TemporaryDirectory() as temporary:
            image_path = Path(temporary) / "screen.png"
            Image.new("RGB", (100, 80), "white").save(image_path)
            result = recognize_image(image_path, runtime, region=(20, 10, 70, 60))
        span = result["spans"][0]
        self.assertEqual([21, 12, 31, 18], list(span["bbox"]))
        self.assertEqual([26, 15], list(span["center"]))


class WindowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.first = WindowBinding("eu5.exe", "C:/eu5.exe", 10, 100, "EU5", (0, 0), (100, 80))
        self.second = WindowBinding("eu5.exe", "C:/eu5.exe", 20, 200, "EU5 Debug", (0, 0), (100, 80))

    def test_select_unique_window_can_pin_pid(self) -> None:
        self.assertEqual(self.second, select_unique_window([self.first, self.second], pid=20))

    def test_select_unique_window_refuses_ambiguity(self) -> None:
        with self.assertRaises(WindowBindingError):
            select_unique_window([self.first, self.second])

    def test_foreground_does_not_restore_visible_maximized_window(self) -> None:
        gui = mock.Mock()
        gui.IsWindow.return_value = True
        gui.IsIconic.return_value = False
        gui.GetForegroundWindow.return_value = self.first.hwnd
        constants = mock.Mock(SW_RESTORE=9)
        with mock.patch(
            "eu5_runtime.windows._imports",
            return_value=(mock.Mock(), constants, gui, mock.Mock()),
        ):
            ensure_foreground(self.first)
        gui.ShowWindow.assert_not_called()
        gui.BringWindowToTop.assert_called_once_with(self.first.hwnd)

    def test_foreground_restores_minimized_window(self) -> None:
        gui = mock.Mock()
        gui.IsWindow.return_value = True
        gui.IsIconic.return_value = True
        gui.GetForegroundWindow.return_value = self.first.hwnd
        constants = mock.Mock(SW_RESTORE=9)
        with mock.patch(
            "eu5_runtime.windows._imports",
            return_value=(mock.Mock(), constants, gui, mock.Mock()),
        ):
            ensure_foreground(self.first)
        gui.ShowWindow.assert_called_once_with(self.first.hwnd, constants.SW_RESTORE)

    def test_receipt_preserves_target_when_dialog_closes(self) -> None:
        with mock.patch(
            "eu5_runtime.windows._current_binding",
            side_effect=WindowBindingError("dialog closed"),
        ):
            receipt = action_receipt(self.first, "click", {}, {"path": "screen.png"})
        self.assertTrue(receipt["target"]["closed_after_action"])
        self.assertEqual(self.first.hwnd, receipt["target"]["hwnd"])

    def test_wheel_can_target_a_client_point(self) -> None:
        automation = mock.Mock()
        with (
            mock.patch.dict(sys.modules, {"pyautogui": automation}),
            mock.patch("eu5_runtime.windows.ensure_foreground"),
            mock.patch(
                "eu5_runtime.windows._screen_point",
                return_value=(310, 420),
            ) as resolve,
        ):
            point = wheel(self.first, -4, x=10, y=20, coordinate_space="client")
        self.assertEqual((310, 420), point)
        resolve.assert_called_once_with(self.first, 10, 20, "client")
        automation.scroll.assert_called_once_with(-4, x=310, y=420)

    def test_wheel_without_coordinates_keeps_legacy_behavior(self) -> None:
        automation = mock.Mock()
        with (
            mock.patch.dict(sys.modules, {"pyautogui": automation}),
            mock.patch("eu5_runtime.windows.ensure_foreground"),
        ):
            point = wheel(self.first, 3)
        self.assertIsNone(point)
        automation.scroll.assert_called_once_with(3)

    def test_wheel_rejects_an_incomplete_point_before_input(self) -> None:
        automation = mock.Mock()
        with (
            mock.patch.dict(sys.modules, {"pyautogui": automation}),
            mock.patch("eu5_runtime.windows.ensure_foreground") as foreground,
        ):
            with self.assertRaises(ValueError):
                wheel(self.first, -1, x=10)
        foreground.assert_not_called()
        automation.scroll.assert_not_called()

    def test_drag_releases_button_when_movement_fails(self) -> None:
        automation = mock.Mock()
        automation.moveTo.side_effect = [None, RuntimeError("movement failed")]
        with (
            mock.patch.dict(sys.modules, {"pyautogui": automation}),
            mock.patch("eu5_runtime.windows.ensure_foreground"),
            mock.patch(
                "eu5_runtime.windows._screen_point",
                side_effect=[(10, 20), (30, 40)],
            ),
        ):
            with self.assertRaisesRegex(RuntimeError, "movement failed"):
                drag(self.first, 1, 2, 3, 4, duration=0.75)
        self.assertEqual(
            [mock.call(10, 20), mock.call(30, 40, duration=0.75)],
            automation.moveTo.call_args_list,
        )
        automation.mouseDown.assert_called_once_with(button="left")
        automation.mouseUp.assert_called_once_with(button="left")

    def test_drag_rejects_invalid_duration_before_input(self) -> None:
        automation = mock.Mock()
        with (
            mock.patch.dict(sys.modules, {"pyautogui": automation}),
            mock.patch("eu5_runtime.windows.ensure_foreground") as foreground,
        ):
            with self.assertRaises(ValueError):
                drag(self.first, 1, 2, 3, 4, duration=float("nan"))
        foreground.assert_not_called()
        automation.moveTo.assert_not_called()


class CliTests(unittest.TestCase):
    def test_ocr_defaults_to_cuda(self) -> None:
        args = build_parser().parse_args(
            ["ocr", "--image", "screen.png", "--output", "ocr.json"]
        )
        self.assertEqual("cuda", args.provider)
        self.assertEqual(0.45, args.minimum_score)

    def test_gpu_evidence_has_multiple_iterations_by_default(self) -> None:
        args = build_parser().parse_args(
            ["gpu-evidence", "--image", "screen.png", "--output", "gpu.json"]
        )
        self.assertEqual(3, args.iterations)

    def test_mutating_action_requires_receipt_and_screenshot(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            build_parser().parse_args(["click", "--x", "1", "--y", "2"])

    def test_wheel_accepts_explicit_screen_coordinates(self) -> None:
        args = build_parser().parse_args(
            [
                "wheel",
                "--amount",
                "-5",
                "--x",
                "2100",
                "--y",
                "700",
                "--space",
                "screen",
                "--receipt",
                "receipt.json",
                "--screenshot",
                "screen.png",
            ]
        )
        self.assertEqual((2100, 700, "screen"), (args.x, args.y, args.space))

    def test_wheel_omitted_coordinates_remain_supported(self) -> None:
        args = build_parser().parse_args(
            [
                "wheel",
                "--amount",
                "2",
                "--receipt",
                "receipt.json",
                "--screenshot",
                "screen.png",
            ]
        )
        self.assertIsNone(args.x)
        self.assertIsNone(args.y)
        self.assertEqual("client", args.space)

    def test_drag_parser_captures_endpoints_and_motion(self) -> None:
        args = build_parser().parse_args(
            [
                "drag",
                "--from-x",
                "10",
                "--from-y",
                "20",
                "--to-x",
                "30",
                "--to-y",
                "40",
                "--space",
                "screen",
                "--button",
                "middle",
                "--duration",
                "0.75",
                "--receipt",
                "receipt.json",
                "--screenshot",
                "screen.png",
            ]
        )
        self.assertEqual((10, 20, 30, 40), (args.from_x, args.from_y, args.to_x, args.to_y))
        self.assertEqual("screen", args.space)
        self.assertEqual("middle", args.button)
        self.assertEqual(0.75, args.duration)

    def test_paste_accepts_a_text_file_as_single_source(self) -> None:
        args = build_parser().parse_args(
            [
                "paste",
                "--text-file",
                "description.bbcode",
                "--receipt",
                "receipt.json",
                "--screenshot",
                "screen.png",
            ]
        )
        self.assertEqual(Path("description.bbcode"), args.text_file)
        self.assertIsNone(args.text)

    def test_console_accepts_a_command_file_as_single_source(self) -> None:
        args = build_parser().parse_args(
            [
                "console",
                "--command-file",
                "command.txt",
                "--receipt",
                "receipt.json",
                "--screenshot",
                "screen.png",
            ]
        )
        self.assertEqual(Path("command.txt"), args.command_file)
        self.assertIsNone(args.console_command)

    def test_scan_key_accepts_hexadecimal_scan_code(self) -> None:
        args = build_parser().parse_args(
            [
                "scan-key",
                "--scan-code",
                "0x29",
                "--receipt",
                "receipt.json",
                "--screenshot",
                "screen.png",
            ]
        )
        self.assertEqual(0x29, args.scan_code)


class RepositoryPolicyTests(unittest.TestCase):
    def test_no_powershell_files_exist(self) -> None:
        forbidden_suffixes = {"." + "ps1", "." + "psm1", "." + "psd1"}
        offenders: list[str] = []
        for root, directories, files in os.walk(REPOSITORY):
            directories[:] = [
                name for name in directories if name not in {".git", "__pycache__"}
            ]
            for filename in files:
                if Path(filename).suffix.casefold() in forbidden_suffixes:
                    offenders.append(str(Path(root, filename).relative_to(REPOSITORY)))
        self.assertEqual([], offenders)

    def test_python_never_invokes_powershell(self) -> None:
        forbidden = (("power" + "shell").casefold(), ("pw" + "sh").casefold())
        offenders: list[str] = []
        for path in REPOSITORY.rglob("*.py"):
            if path == Path(__file__).resolve() or any(
                part in {".git", ".venv", "__pycache__", "_runtime"} for part in path.parts
            ):
                continue
            source = path.read_text(encoding="utf-8", errors="replace").casefold()
            if any(token in source for token in forbidden):
                offenders.append(str(path.relative_to(REPOSITORY)))
        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
