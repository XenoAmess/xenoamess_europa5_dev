from __future__ import annotations

from pathlib import Path
import time
from typing import Iterable

from .evidence import sha256_file, utc_now
from .model import WindowBinding


class WindowBindingError(RuntimeError):
    pass


def _imports():
    try:
        import psutil
        import win32con
        import win32gui
        import win32process
    except ImportError as exc:
        raise WindowBindingError("psutil and pywin32 are required for Windows automation") from exc
    return psutil, win32con, win32gui, win32process


def desktop_status(process_names: list[str]) -> dict[str, object]:
    psutil, _win32con, win32gui, win32process = _imports()
    expected = {Path(name).stem.casefold() for name in process_names}
    processes: dict[int, dict[str, object]] = {}
    for process in psutil.process_iter(["pid", "name", "exe", "status", "create_time"]):
        try:
            name = process.info.get("name") or ""
            if Path(name).stem.casefold() in expected:
                processes[process.pid] = {
                    "pid": process.pid,
                    "name": name,
                    "executable": process.info.get("exe") or "",
                    "status": process.info.get("status") or "",
                    "create_time": process.info.get("create_time"),
                    "windows": [],
                }
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue

    def inspect(hwnd: int, _extra: object) -> bool:
        if not win32gui.IsWindowVisible(hwnd):
            return True
        _thread, owner_pid = win32process.GetWindowThreadProcessId(hwnd)
        if owner_pid in processes:
            processes[owner_pid]["windows"].append(
                {"hwnd": hwnd, "title": win32gui.GetWindowText(hwnd)}
            )
        return True

    win32gui.EnumWindows(inspect, None)
    foreground = win32gui.GetForegroundWindow()
    foreground_title = win32gui.GetWindowText(foreground) if foreground else ""
    foreground_pid = None
    if foreground:
        _thread, foreground_pid = win32process.GetWindowThreadProcessId(foreground)
    return {
        "observed_at_utc": utc_now(),
        "requested_processes": process_names,
        "processes": sorted(processes.values(), key=lambda item: int(item["pid"])),
        "foreground": {
            "hwnd": foreground,
            "pid": foreground_pid,
            "title": foreground_title,
        },
    }


def select_unique_window(
    candidates: Iterable[WindowBinding],
    *,
    pid: int | None = None,
    title_contains: str | None = None,
) -> WindowBinding:
    selected = list(candidates)
    if pid is not None:
        selected = [candidate for candidate in selected if candidate.pid == pid]
    if title_contains:
        needle = title_contains.casefold()
        selected = [candidate for candidate in selected if needle in candidate.title.casefold()]
    if len(selected) != 1:
        details = [f"pid={item.pid} hwnd={item.hwnd} title={item.title!r}" for item in selected]
        raise WindowBindingError(
            f"expected exactly one target window, found {len(selected)}: {details}"
        )
    return selected[0]


def find_window(
    process_name: str,
    *,
    pid: int | None = None,
    title_contains: str | None = None,
) -> WindowBinding:
    psutil, _win32con, win32gui, win32process = _imports()
    expected = Path(process_name).stem.casefold()
    processes: dict[int, tuple[str, str]] = {}
    for process in psutil.process_iter(["pid", "name", "exe"]):
        try:
            name = process.info.get("name") or ""
            if Path(name).stem.casefold() == expected:
                processes[process.pid] = (name, process.info.get("exe") or "")
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue
    candidates: list[WindowBinding] = []

    def inspect(hwnd: int, _extra: object) -> bool:
        if not win32gui.IsWindowVisible(hwnd):
            return True
        title = win32gui.GetWindowText(hwnd).strip()
        if not title:
            return True
        _thread, owner_pid = win32process.GetWindowThreadProcessId(hwnd)
        if owner_pid not in processes:
            return True
        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        width, height = right - left, bottom - top
        if width <= 0 or height <= 0:
            return True
        origin = win32gui.ClientToScreen(hwnd, (0, 0))
        name, executable = processes[owner_pid]
        candidates.append(
            WindowBinding(name, executable, owner_pid, hwnd, title, origin, (width, height))
        )
        return True

    win32gui.EnumWindows(inspect, None)
    return select_unique_window(candidates, pid=pid, title_contains=title_contains)


def ensure_foreground(binding: WindowBinding, *, timeout_seconds: float = 3.0) -> None:
    _psutil, win32con, win32gui, _win32process = _imports()
    if not win32gui.IsWindow(binding.hwnd):
        raise WindowBindingError(f"target HWND no longer exists: {binding.hwnd}")
    # SW_RESTORE also unmaximizes an already visible maximized window. That changes
    # the client geometry between binding and input, so restore only real minimized
    # windows and always resolve geometry again immediately before an action.
    if win32gui.IsIconic(binding.hwnd):
        win32gui.ShowWindow(binding.hwnd, win32con.SW_RESTORE)
    win32gui.BringWindowToTop(binding.hwnd)
    try:
        win32gui.SetForegroundWindow(binding.hwnd)
    except Exception as exc:
        raise WindowBindingError(f"cannot foreground target HWND {binding.hwnd}: {exc}") from exc
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if win32gui.GetForegroundWindow() == binding.hwnd:
            return
        time.sleep(0.05)
    raise WindowBindingError(f"target HWND {binding.hwnd} did not become foreground")


def _current_client_geometry(binding: WindowBinding) -> tuple[tuple[int, int], tuple[int, int]]:
    _psutil, _win32con, win32gui, _win32process = _imports()
    if not win32gui.IsWindow(binding.hwnd):
        raise WindowBindingError(f"target HWND no longer exists: {binding.hwnd}")
    left, top, right, bottom = win32gui.GetClientRect(binding.hwnd)
    size = (right - left, bottom - top)
    if size[0] <= 0 or size[1] <= 0:
        raise WindowBindingError(f"target HWND {binding.hwnd} has no usable client area")
    return win32gui.ClientToScreen(binding.hwnd, (0, 0)), size


def _current_binding(binding: WindowBinding) -> WindowBinding:
    origin, size = _current_client_geometry(binding)
    return WindowBinding(
        binding.process_name,
        binding.executable,
        binding.pid,
        binding.hwnd,
        binding.title,
        origin,
        size,
    )


def _screen_point(binding: WindowBinding, x: int, y: int, coordinate_space: str) -> tuple[int, int]:
    if coordinate_space == "screen":
        return x, y
    if coordinate_space != "client":
        raise ValueError("coordinate space must be 'client' or 'screen'")
    origin, (width, height) = _current_client_geometry(binding)
    if not 0 <= x < width or not 0 <= y < height:
        raise ValueError(f"client point {(x, y)} is outside client size {(width, height)}")
    return origin[0] + x, origin[1] + y


def capture(binding: WindowBinding, output: Path, *, coordinate_space: str = "client") -> dict[str, object]:
    from PIL import ImageGrab

    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError(f"refusing to overwrite screenshot: {output}")
    if coordinate_space == "client":
        (left, top), (width, height) = _current_client_geometry(binding)
        bbox = (left, top, left + width, top + height)
        image = ImageGrab.grab(bbox=bbox, all_screens=True)
        origin = [left, top]
    elif coordinate_space == "screen":
        import ctypes

        image = ImageGrab.grab(all_screens=True)
        origin = [
            ctypes.windll.user32.GetSystemMetrics(76),
            ctypes.windll.user32.GetSystemMetrics(77),
        ]
    else:
        raise ValueError("coordinate space must be 'client' or 'screen'")
    image.save(output)
    return {
        "path": str(output),
        "sha256": sha256_file(output),
        "size": list(image.size),
        "coordinate_space": coordinate_space,
        "origin": origin,
    }


def click(
    binding: WindowBinding,
    x: int,
    y: int,
    *,
    button: str = "left",
    coordinate_space: str = "client",
) -> tuple[int, int]:
    import pyautogui

    ensure_foreground(binding)
    point = _screen_point(binding, x, y, coordinate_space)
    pyautogui.click(*point, button=button)
    return point


def post_click(binding: WindowBinding, x: int, y: int) -> tuple[int, int]:
    _psutil, win32con, win32gui, _win32process = _imports()
    origin, (width, height) = _current_client_geometry(binding)
    if not 0 <= x < width or not 0 <= y < height:
        raise ValueError(f"client point {(x, y)} is outside client size {(width, height)}")
    packed = (y << 16) | (x & 0xFFFF)
    win32gui.PostMessage(binding.hwnd, win32con.WM_MOUSEMOVE, 0, packed)
    win32gui.PostMessage(binding.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, packed)
    win32gui.PostMessage(binding.hwnd, win32con.WM_LBUTTONUP, 0, packed)
    return origin[0] + x, origin[1] + y


def hover(
    binding: WindowBinding,
    x: int,
    y: int,
    *,
    coordinate_space: str = "client",
) -> tuple[int, int]:
    import pyautogui

    ensure_foreground(binding)
    point = _screen_point(binding, x, y, coordinate_space)
    pyautogui.moveTo(*point)
    return point


def wheel(binding: WindowBinding, amount: int) -> None:
    import pyautogui

    ensure_foreground(binding)
    pyautogui.scroll(amount)


def press_key(binding: WindowBinding, key: str) -> None:
    import pyautogui

    ensure_foreground(binding)
    pyautogui.press(key)


def hotkey(binding: WindowBinding, keys: list[str]) -> None:
    import pyautogui

    ensure_foreground(binding)
    pyautogui.hotkey(*keys)


def paste_text(binding: WindowBinding, text: str, *, select_all: bool = False) -> None:
    import pyautogui
    import pyperclip

    ensure_foreground(binding)
    try:
        previous = pyperclip.paste()
    except Exception:
        previous = None
    pyperclip.copy(text)
    try:
        if select_all:
            pyautogui.keyDown("ctrl")
            time.sleep(0.1)
            pyautogui.press("a")
            time.sleep(0.1)
            pyautogui.keyUp("ctrl")
            time.sleep(0.1)
        pyautogui.keyDown("ctrl")
        time.sleep(0.1)
        pyautogui.press("v")
        time.sleep(0.1)
        pyautogui.keyUp("ctrl")
        time.sleep(1.0)
    finally:
        if previous is not None:
            pyperclip.copy(previous)


def action_receipt(
    binding: WindowBinding,
    action: str,
    details: dict[str, object],
    screenshot: dict[str, object],
) -> dict[str, object]:
    try:
        target = _current_binding(binding).to_dict()
        target["closed_after_action"] = False
    except WindowBindingError:
        # Native pickers and confirmation dialogs commonly destroy their HWND as
        # the successful result of a click. Preserve the pre-action binding and
        # make that lifecycle explicit instead of losing the receipt.
        target = binding.to_dict()
        target["closed_after_action"] = True
    return {
        "schema": 1,
        "sent_at_utc": utc_now(),
        "action": action,
        "target": target,
        "details": details,
        "post_action_screenshot": screenshot,
        "claim_boundary": "input-sent-only",
    }
