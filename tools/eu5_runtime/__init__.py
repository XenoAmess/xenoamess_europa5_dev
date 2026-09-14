"""Reusable Python primitives for controlled EU5 runtime acceptance."""

from .evidence import create_run, sha256_file, write_json
from .model import OcrSpan, WindowBinding, normalize_ocr_text

__all__ = [
    "OcrSpan",
    "WindowBinding",
    "create_run",
    "normalize_ocr_text",
    "sha256_file",
    "write_json",
]
