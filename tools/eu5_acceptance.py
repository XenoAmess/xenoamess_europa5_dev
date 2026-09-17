#!/usr/bin/env python3
"""Python-only EU5 runtime acceptance and desktop evidence entrypoint."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import threading
import time
from typing import Callable

from eu5_runtime.evidence import create_run, sha256_file, utc_now, write_json
from eu5_runtime.ocr import (
    OcrBackendError,
    available_ort_providers,
    build_runtime,
    recognize_image,
)
from eu5_runtime.windows import (
    WindowBindingError,
    action_receipt,
    capture,
    click,
    desktop_status,
    drag,
    find_window,
    hotkey,
    hover,
    paste_text,
    post_click,
    press_key,
    press_scan_code,
    wheel,
)


for _stream in (sys.stdout, sys.stderr):
    reconfigure = getattr(_stream, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8", errors="backslashreplace")


DEPENDENCIES = (
    "Pillow",
    "numpy",
    "PyAutoGUI",
    "pyperclip",
    "pywin32",
    "psutil",
    "rapidocr-onnxruntime",
    "onnxruntime-gpu",
    "onnxruntime",
)


def _print_json(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _write_result(path: Path, payload: object) -> None:
    write_json(path, payload)
    _print_json(payload)


def _parse_region(value: str) -> tuple[int, int, int, int]:
    try:
        numbers = tuple(int(item.strip()) for item in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("region must be left,top,right,bottom") from exc
    if len(numbers) != 4:
        raise argparse.ArgumentTypeError("region must contain four integers")
    return numbers  # type: ignore[return-value]


def _binding(args: argparse.Namespace):
    return find_window(
        args.process,
        pid=args.pid,
        title_contains=args.title_contains,
    )


def _cmd_init_run(args: argparse.Namespace) -> int:
    _run, manifest = create_run(args.root, args.run_id)
    _print_json(manifest)
    return 0


def _cmd_hash_files(args: argparse.Namespace) -> int:
    payload = {
        "schema": 1,
        "files": [
            {"path": str(path.resolve()), "sha256": sha256_file(path.resolve())}
            for path in args.path
        ],
    }
    _print_json(payload)
    return 0


def _dependency_versions() -> dict[str, str | None]:
    versions: dict[str, str | None] = {}
    for distribution in DEPENDENCIES:
        try:
            versions[distribution] = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            versions[distribution] = None
    return versions


def _cmd_probe(args: argparse.Namespace) -> int:
    payload: dict[str, object] = {
        "schema": 1,
        "observed_at_utc": utc_now(),
        "platform": platform.platform(),
        "python": sys.version,
        "dependencies": _dependency_versions(),
        "requested_provider": args.provider,
        "device_id": args.device_id,
    }
    try:
        payload["available_providers"] = list(available_ort_providers())
        if not args.skip_engine:
            payload["ocr"] = build_runtime(args.provider, args.device_id).to_dict()
        payload["status"] = "PASS"
        status = 0
    except Exception as exc:
        payload["status"] = "RED"
        payload["error"] = f"{type(exc).__name__}: {exc}"
        status = 2
    _write_result(args.output, payload)
    return status


def _cmd_capture(args: argparse.Namespace) -> int:
    binding = _binding(args)
    screenshot = capture(binding, args.output, coordinate_space=args.space)
    receipt = {
        "schema": 1,
        "captured_at_utc": utc_now(),
        "target": binding.to_dict(),
        "screenshot": screenshot,
    }
    _write_result(args.receipt, receipt)
    return 0


def _cmd_status(args: argparse.Namespace) -> int:
    payload = desktop_status(args.process)
    _write_result(args.output, payload)
    return 0


def _cmd_ocr(args: argparse.Namespace) -> int:
    runtime = build_runtime(args.provider, args.device_id)
    result = recognize_image(
        args.image,
        runtime,
        region=args.region,
        minimum_score=args.minimum_score,
    )
    _write_result(args.output, result)
    return 0


def _sample_gpu_process(stop: threading.Event, samples: list[dict[str, object]]) -> None:
    target_pid = os.getpid()
    command = [
        "nvidia-smi",
        "--query-compute-apps=pid,process_name,used_gpu_memory",
        "--format=csv,noheader,nounits",
    ]
    while not stop.wait(0.1):
        observed_at = utc_now()
        try:
            result = subprocess.run(
                command,
                check=False,
                shell=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
        except FileNotFoundError:
            samples.append({"observed_at_utc": observed_at, "error": "nvidia-smi not found"})
            return
        for line in result.stdout.splitlines():
            fields = [field.strip() for field in line.split(",", maxsplit=2)]
            if fields and fields[0].isdigit() and int(fields[0]) == target_pid:
                samples.append(
                    {
                        "observed_at_utc": observed_at,
                        "pid": target_pid,
                        "process_name": fields[1] if len(fields) > 1 else "",
                        "used_gpu_memory_mib": fields[2] if len(fields) > 2 else "",
                    }
                )


def _cmd_gpu_evidence(args: argparse.Namespace) -> int:
    runtime = build_runtime("cuda", args.device_id)
    samples: list[dict[str, object]] = []
    stop = threading.Event()
    sampler = threading.Thread(target=_sample_gpu_process, args=(stop, samples), daemon=True)
    sampler.start()
    span_counts: list[int] = []
    started = time.perf_counter()
    cpu_started = time.process_time()
    try:
        for _ in range(args.iterations):
            result = recognize_image(
                args.image,
                runtime,
                region=args.region,
                minimum_score=args.minimum_score,
            )
            span_counts.append(len(result["spans"]))
    finally:
        stop.set()
        sampler.join(timeout=2.0)
    payload = {
        "schema": 1,
        "observed_at_utc": utc_now(),
        "pid": os.getpid(),
        "image": str(args.image.resolve()),
        "iterations": args.iterations,
        "wall_seconds": time.perf_counter() - started,
        "cpu_seconds": time.process_time() - cpu_started,
        "span_counts": span_counts,
        "ocr": runtime.to_dict(),
        "process_gpu_samples": samples,
        "status": "PASS" if samples else "RED",
    }
    if not samples:
        payload["error"] = "no process-level NVIDIA compute sample was observed"
    _write_result(args.output, payload)
    return 0 if samples else 2


def _finish_action(
    args: argparse.Namespace,
    binding,
    action: str,
    details: dict[str, object],
) -> int:
    time.sleep(args.delay)
    screenshot = capture(binding, args.screenshot, coordinate_space=args.screenshot_space)
    receipt = action_receipt(binding, action, details, screenshot)
    _write_result(args.receipt, receipt)
    return 0


def _cmd_click(args: argparse.Namespace) -> int:
    binding = _binding(args)
    point = click(
        binding,
        args.x,
        args.y,
        button=args.button,
        coordinate_space=args.space,
    )
    return _finish_action(
        args,
        binding,
        "click",
        {
            "requested_point": [args.x, args.y],
            "screen_point": list(point),
            "coordinate_space": args.space,
            "button": args.button,
        },
    )


def _cmd_post_click(args: argparse.Namespace) -> int:
    binding = _binding(args)
    point = post_click(binding, args.x, args.y)
    return _finish_action(
        args,
        binding,
        "post-click",
        {
            "requested_point": [args.x, args.y],
            "screen_point": list(point),
            "coordinate_space": "client",
            "button": "left",
        },
    )


def _cmd_hover(args: argparse.Namespace) -> int:
    binding = _binding(args)
    point = hover(binding, args.x, args.y, coordinate_space=args.space)
    return _finish_action(
        args,
        binding,
        "hover",
        {
            "requested_point": [args.x, args.y],
            "screen_point": list(point),
            "coordinate_space": args.space,
        },
    )


def _cmd_wheel(args: argparse.Namespace) -> int:
    binding = _binding(args)
    point = wheel(
        binding,
        args.amount,
        x=args.x,
        y=args.y,
        coordinate_space=args.space,
    )
    details: dict[str, object] = {"amount": args.amount}
    if point is not None:
        details.update(
            {
                "requested_point": [args.x, args.y],
                "screen_point": list(point),
                "coordinate_space": args.space,
            }
        )
    return _finish_action(args, binding, "wheel", details)


def _cmd_drag(args: argparse.Namespace) -> int:
    binding = _binding(args)
    start, end = drag(
        binding,
        args.from_x,
        args.from_y,
        args.to_x,
        args.to_y,
        button=args.button,
        coordinate_space=args.space,
        duration=args.duration,
    )
    return _finish_action(
        args,
        binding,
        "drag",
        {
            "requested_from": [args.from_x, args.from_y],
            "requested_to": [args.to_x, args.to_y],
            "screen_from": list(start),
            "screen_to": list(end),
            "coordinate_space": args.space,
            "button": args.button,
            "duration": args.duration,
        },
    )


def _cmd_key(args: argparse.Namespace) -> int:
    binding = _binding(args)
    press_key(binding, args.key)
    return _finish_action(args, binding, "key", {"key": args.key})


def _cmd_scan_key(args: argparse.Namespace) -> int:
    binding = _binding(args)
    press_scan_code(binding, args.scan_code)
    return _finish_action(
        args,
        binding,
        "scan-key",
        {"scan_code": f"0x{args.scan_code:02x}"},
    )


def _cmd_hotkey(args: argparse.Namespace) -> int:
    binding = _binding(args)
    hotkey(binding, args.keys)
    return _finish_action(args, binding, "hotkey", {"keys": args.keys})


def _cmd_paste(args: argparse.Namespace) -> int:
    if args.text_file is not None:
        text = args.text_file.resolve().read_text(encoding="utf-8-sig")
        text_source: dict[str, object] = {
            "path": str(args.text_file.resolve()),
            "sha256": sha256_file(args.text_file.resolve()),
        }
    else:
        text = args.text
        text_source = {"inline": True}
    binding = _binding(args)
    details: dict[str, object] = {
        "text_length": len(text),
        "text_source": text_source,
        "select_all": args.select_all,
    }
    if (args.x is None) != (args.y is None):
        raise ValueError("paste requires both --x and --y when either is provided")
    if args.x is not None:
        point = click(binding, args.x, args.y, coordinate_space=args.space)
        details.update(
            {
                "requested_point": [args.x, args.y],
                "screen_point": list(point),
                "coordinate_space": args.space,
            }
        )
    paste_text(binding, text, select_all=args.select_all)
    return _finish_action(args, binding, "paste", details)


def _cmd_console(args: argparse.Namespace) -> int:
    if args.command_file is not None:
        command = args.command_file.resolve().read_text(encoding="utf-8-sig").rstrip("\r\n")
        command_source: dict[str, object] = {
            "path": str(args.command_file.resolve()),
            "sha256": sha256_file(args.command_file.resolve()),
        }
    else:
        command = args.console_command
        command_source = {"inline": True}
    if not command:
        raise ValueError("console command must not be empty")
    binding = _binding(args)
    # The physical key above Tab has scan code 0x29. Sending the scan code
    # avoids active-layout failures from translating the printable '`' glyph.
    press_scan_code(binding, 0x29)
    time.sleep(0.15)
    paste_text(binding, command, select_all=True)
    press_scan_code(binding, 0x1C)
    time.sleep(args.command_delay)
    if not args.keep_open:
        # EU5 keeps the command input focused after submission. While it owns
        # focus, the physical grave key is inserted as text instead of closing
        # the console, so first defocus on the console history pane.
        click(binding, 20, 300, coordinate_space="client")
        time.sleep(0.15)
        press_scan_code(binding, 0x29)
    return _finish_action(
        args,
        binding,
        "console",
        {
            "command": command,
            "command_source": command_source,
            "toggle_scan_code": "0x29",
            "submit_scan_code": "0x1c",
            "input_replaced": True,
            "close_defocus_point": [20, 300] if not args.keep_open else None,
            "command_delay": args.command_delay,
            "keep_open": args.keep_open,
        },
    )


def _cmd_launch(args: argparse.Namespace) -> int:
    executable = args.executable.resolve()
    if not executable.is_file():
        raise FileNotFoundError(f"executable does not exist: {executable}")
    cwd = args.cwd.resolve() if args.cwd else executable.parent
    command = [str(executable), *args.argument]
    process = subprocess.Popen(command, cwd=cwd)
    payload = {
        "schema": 1,
        "launched_at_utc": utc_now(),
        "pid": process.pid,
        "executable": str(executable),
        "arguments": args.argument,
        "cwd": str(cwd),
        "shell": False,
    }
    _write_result(args.receipt, payload)
    return 0


def _add_target(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--process", default="eu5", help="exact process stem (default: eu5)")
    parser.add_argument("--pid", type=int)
    parser.add_argument("--title-contains")


def _add_action_evidence(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--screenshot", required=True, type=Path)
    parser.add_argument("--screenshot-space", choices=("client", "screen"), default="client")
    parser.add_argument("--delay", type=float, default=0.5)


def _add_point(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--x", required=True, type=int)
    parser.add_argument("--y", required=True, type=int)
    parser.add_argument("--space", choices=("client", "screen"), default="client")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    init_run = commands.add_parser("init-run", help="create a unique evidence run")
    init_run.add_argument("--root", type=Path, default=Path("_runtime"))
    init_run.add_argument("--run-id", required=True)
    init_run.set_defaults(handler=_cmd_init_run)

    hashes = commands.add_parser("hash-files", help="print SHA-256 for evidence files")
    hashes.add_argument("--path", action="append", required=True, type=Path)
    hashes.set_defaults(handler=_cmd_hash_files)

    probe = commands.add_parser("probe", help="record Python and OCR provider state")
    probe.add_argument("--provider", choices=("cuda", "cpu"), default="cuda")
    probe.add_argument("--device-id", type=int, default=0)
    probe.add_argument("--skip-engine", action="store_true")
    probe.add_argument("--output", required=True, type=Path)
    probe.set_defaults(handler=_cmd_probe)

    capture_parser = commands.add_parser("capture", help="capture a bound window or desktop")
    _add_target(capture_parser)
    capture_parser.add_argument("--space", choices=("client", "screen"), default="client")
    capture_parser.add_argument("--output", required=True, type=Path)
    capture_parser.add_argument("--receipt", required=True, type=Path)
    capture_parser.set_defaults(handler=_cmd_capture)

    status = commands.add_parser("status", help="record relevant processes and visible windows")
    status.add_argument("--process", action="append", default=["eu5", "steam"])
    status.add_argument("--output", required=True, type=Path)
    status.set_defaults(handler=_cmd_status)

    ocr = commands.add_parser("ocr", help="OCR an original-resolution screenshot")
    ocr.add_argument("--image", required=True, type=Path)
    ocr.add_argument("--output", required=True, type=Path)
    ocr.add_argument("--provider", choices=("cuda", "cpu"), default="cuda")
    ocr.add_argument("--device-id", type=int, default=0)
    ocr.add_argument("--region", type=_parse_region)
    ocr.add_argument("--minimum-score", type=float, default=0.45)
    ocr.set_defaults(handler=_cmd_ocr)

    gpu_evidence = commands.add_parser(
        "gpu-evidence", help="run OCR while sampling this process in NVIDIA compute state"
    )
    gpu_evidence.add_argument("--image", required=True, type=Path)
    gpu_evidence.add_argument("--output", required=True, type=Path)
    gpu_evidence.add_argument("--device-id", type=int, default=0)
    gpu_evidence.add_argument("--region", type=_parse_region)
    gpu_evidence.add_argument("--minimum-score", type=float, default=0.45)
    gpu_evidence.add_argument("--iterations", type=int, default=3)
    gpu_evidence.set_defaults(handler=_cmd_gpu_evidence)

    click_parser = commands.add_parser("click", help="foreground and click the bound target")
    _add_target(click_parser)
    _add_point(click_parser)
    _add_action_evidence(click_parser)
    click_parser.add_argument("--button", choices=("left", "right", "middle"), default="left")
    click_parser.set_defaults(handler=_cmd_click)

    post = commands.add_parser("post-click", help="send a client-relative click message")
    _add_target(post)
    post.add_argument("--x", required=True, type=int)
    post.add_argument("--y", required=True, type=int)
    _add_action_evidence(post)
    post.set_defaults(handler=_cmd_post_click)

    hover_parser = commands.add_parser("hover", help="foreground and move over a point")
    _add_target(hover_parser)
    _add_point(hover_parser)
    _add_action_evidence(hover_parser)
    hover_parser.set_defaults(handler=_cmd_hover)

    wheel_parser = commands.add_parser("wheel", help="scroll the foreground target")
    _add_target(wheel_parser)
    _add_action_evidence(wheel_parser)
    wheel_parser.add_argument("--amount", required=True, type=int)
    wheel_parser.add_argument("--x", type=int)
    wheel_parser.add_argument("--y", type=int)
    wheel_parser.add_argument("--space", choices=("client", "screen"), default="client")
    wheel_parser.set_defaults(handler=_cmd_wheel)

    drag_parser = commands.add_parser("drag", help="drag between two points")
    _add_target(drag_parser)
    _add_action_evidence(drag_parser)
    drag_parser.add_argument("--from-x", required=True, type=int)
    drag_parser.add_argument("--from-y", required=True, type=int)
    drag_parser.add_argument("--to-x", required=True, type=int)
    drag_parser.add_argument("--to-y", required=True, type=int)
    drag_parser.add_argument("--space", choices=("client", "screen"), default="client")
    drag_parser.add_argument("--button", choices=("left", "right", "middle"), default="left")
    drag_parser.add_argument("--duration", type=float, default=0.5)
    drag_parser.set_defaults(handler=_cmd_drag)

    key_parser = commands.add_parser("key", help="press one named key")
    _add_target(key_parser)
    _add_action_evidence(key_parser)
    key_parser.add_argument("--key", required=True)
    key_parser.set_defaults(handler=_cmd_key)

    scan_key_parser = commands.add_parser(
        "scan-key", help="press one physical keyboard scan code"
    )
    _add_target(scan_key_parser)
    _add_action_evidence(scan_key_parser)
    scan_key_parser.add_argument("--scan-code", required=True, type=lambda value: int(value, 0))
    scan_key_parser.set_defaults(handler=_cmd_scan_key)

    hotkey_parser = commands.add_parser("hotkey", help="press a key chord")
    _add_target(hotkey_parser)
    _add_action_evidence(hotkey_parser)
    hotkey_parser.add_argument("--keys", nargs="+", required=True)
    hotkey_parser.set_defaults(handler=_cmd_hotkey)

    paste = commands.add_parser("paste", help="paste text through the clipboard")
    _add_target(paste)
    _add_action_evidence(paste)
    paste.add_argument("--select-all", action="store_true")
    paste.add_argument("--x", type=int)
    paste.add_argument("--y", type=int)
    paste.add_argument("--space", choices=("client", "screen"), default="client")
    paste_text_source = paste.add_mutually_exclusive_group(required=True)
    paste_text_source.add_argument("--text")
    paste_text_source.add_argument("--text-file", type=Path)
    paste.set_defaults(handler=_cmd_paste)

    console = commands.add_parser("console", help="run one EU5 console command")
    _add_target(console)
    _add_action_evidence(console)
    console_command_source = console.add_mutually_exclusive_group(required=True)
    console_command_source.add_argument("--command", dest="console_command")
    console_command_source.add_argument("--command-file", type=Path)
    console.add_argument("--command-delay", type=float, default=0.5)
    console.add_argument("--keep-open", action="store_true")
    console.set_defaults(handler=_cmd_console)

    launch = commands.add_parser("launch", help="launch an executable without a command shell")
    launch.add_argument("--executable", required=True, type=Path)
    launch.add_argument("--argument", action="append", default=[])
    launch.add_argument("--cwd", type=Path)
    launch.add_argument("--receipt", required=True, type=Path)
    launch.set_defaults(handler=_cmd_launch)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    handler: Callable[[argparse.Namespace], int] = args.handler
    try:
        return handler(args)
    except (OcrBackendError, WindowBindingError, FileExistsError, FileNotFoundError, ValueError) as exc:
        print(
            json.dumps(
                {"status": "RED", "error": f"{type(exc).__name__}: {exc}"},
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
