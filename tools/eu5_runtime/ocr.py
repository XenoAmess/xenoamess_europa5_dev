from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .evidence import sha256_file, utc_now
from .model import OcrSpan


CUDA_PROVIDER = "CUDAExecutionProvider"
CPU_PROVIDER = "CPUExecutionProvider"
COMPONENT_NAMES = ("text_det", "text_cls", "text_rec")
COMPONENT_ALIASES = {
    "text_det": ("text_detector", "text_det"),
    "text_cls": ("text_cls",),
    "text_rec": ("text_recognizer", "text_rec"),
}


class OcrBackendError(RuntimeError):
    pass


@dataclass(slots=True)
class OcrRuntime:
    engine: Any
    requested_provider: str
    device_id: int
    available_providers: tuple[str, ...]
    session_providers: dict[str, tuple[str, ...]]
    character_count: int = 0

    def to_dict(self) -> dict[str, object]:
        return {
            "api": "rapidocr-onnxruntime",
            "requested_provider": self.requested_provider,
            "device_id": self.device_id,
            "cuda_dll_preload": self.requested_provider == "cuda",
            "available_providers": list(self.available_providers),
            "session_providers": {
                name: list(providers) for name, providers in self.session_providers.items()
            },
            "character_count": self.character_count,
        }


def available_ort_providers() -> tuple[str, ...]:
    try:
        import onnxruntime as ort
    except ImportError as exc:
        raise OcrBackendError("onnxruntime is not installed") from exc
    return tuple(ort.get_available_providers())


def _preload_cuda_runtime() -> None:
    try:
        import onnxruntime as ort
    except ImportError as exc:
        raise OcrBackendError("onnxruntime is not installed") from exc
    preload = getattr(ort, "preload_dlls", None)
    if not callable(preload):
        raise OcrBackendError("installed onnxruntime does not expose CUDA DLL preloading")
    try:
        preload(directory="")
    except Exception as exc:
        raise OcrBackendError(f"cannot preload isolated CUDA/cuDNN runtime: {exc}") from exc


def _find_session(value: Any, *, depth: int = 5, seen: set[int] | None = None) -> Any | None:
    if value is None or depth < 0:
        return None
    if seen is None:
        seen = set()
    identity = id(value)
    if identity in seen:
        return None
    seen.add(identity)
    getter = getattr(value, "get_providers", None)
    if callable(getter):
        return value
    nested_session = getattr(value, "session", None)
    if nested_session is not None:
        found = _find_session(nested_session, depth=depth - 1, seen=seen)
        if found is not None:
            return found
    for attribute in ("infer", "sess", "ort_session", "predictor", "model", "engine"):
        if hasattr(value, attribute):
            found = _find_session(getattr(value, attribute), depth=depth - 1, seen=seen)
            if found is not None:
                return found
    return None


def _session_map(engine: Any) -> dict[str, Any]:
    sessions: dict[str, Any] = {}
    for name in COMPONENT_NAMES:
        session = None
        for alias in COMPONENT_ALIASES[name]:
            session = _find_session(getattr(engine, alias, None))
            if session is not None:
                break
        if session is None:
            visible = sorted(key for key in vars(engine) if not key.startswith("_"))
            chains: dict[str, list[str]] = {}
            for alias in COMPONENT_ALIASES[name]:
                current = getattr(engine, alias, None)
                chain: list[str] = []
                for _ in range(5):
                    if current is None:
                        break
                    chain.append(
                        f"{type(current).__module__}.{type(current).__name__}:"
                        f"get_providers={callable(getattr(current, 'get_providers', None))}:"
                        f"fields={sorted(vars(current)) if hasattr(current, '__dict__') else []}"
                    )
                    current = getattr(current, "session", None)
                chains[alias] = chain
            raise OcrBackendError(
                f"cannot locate ONNX Runtime session for {name}; engine fields: {visible}; "
                f"chains: {chains}"
            )
        sessions[name] = session
    return sessions


def session_provider_map(engine: Any) -> dict[str, tuple[str, ...]]:
    return {
        name: tuple(session.get_providers())
        for name, session in _session_map(engine).items()
    }


def validate_session_providers(
    requested_provider: str,
    providers: dict[str, tuple[str, ...]],
) -> None:
    expected = CUDA_PROVIDER if requested_provider == "cuda" else CPU_PROVIDER
    for component in COMPONENT_NAMES:
        actual = providers.get(component, ())
        if not actual or actual[0] != expected:
            raise OcrBackendError(
                f"{component} provider mismatch: requested {expected}, actual {list(actual)}"
            )


def _character_count(engine: Any) -> int:
    recognizer = getattr(engine, "text_recognizer", None)
    postprocessor = getattr(recognizer, "postprocess_op", None)
    characters = getattr(postprocessor, "character", None)
    if not characters or len(characters) < 1000:
        raise OcrBackendError("OCR recognition dictionary is missing or unexpectedly small")
    if any("\ufffd" in str(character) for character in characters):
        raise OcrBackendError("OCR recognition dictionary contains invalid Unicode replacements")
    return len(characters)


def build_runtime(provider: str = "cuda", device_id: int = 0) -> OcrRuntime:
    provider = provider.casefold()
    if provider not in {"cuda", "cpu"}:
        raise ValueError("OCR provider must be 'cuda' or 'cpu'")
    if provider == "cuda":
        _preload_cuda_runtime()
    available = available_ort_providers()
    expected = CUDA_PROVIDER if provider == "cuda" else CPU_PROVIDER
    if expected not in available:
        raise OcrBackendError(
            f"requested {expected} is unavailable; installed providers: {list(available)}"
        )
    try:
        from rapidocr_onnxruntime import RapidOCR
    except ImportError as exc:
        raise OcrBackendError("rapidocr-onnxruntime is not installed") from exc
    if provider == "cuda":
        engine = RapidOCR(det_use_cuda=True, det_model_path=None)
        cuda_options = {
            "device_id": device_id,
            "arena_extend_strategy": "kNextPowerOfTwo",
            "cudnn_conv_algo_search": "EXHAUSTIVE",
            "do_copy_in_default_stream": True,
        }
        cpu_options = {"arena_extend_strategy": "kSameAsRequested"}
        for session in _session_map(engine).values():
            session.set_providers(
                [(CUDA_PROVIDER, cuda_options), (CPU_PROVIDER, cpu_options)]
            )
    else:
        engine = RapidOCR()
    actual = session_provider_map(engine)
    validate_session_providers(provider, actual)
    return OcrRuntime(engine, provider, device_id, available, actual, _character_count(engine))


def _unpack_result(result: Any) -> tuple[Iterable[Any], Iterable[str], Iterable[float]]:
    if hasattr(result, "boxes"):
        boxes = result.boxes if result.boxes is not None else ()
        texts = result.txts if result.txts is not None else ()
        scores = result.scores if result.scores is not None else ()
        return boxes, texts, scores
    if isinstance(result, tuple) and result:
        rows = result[0] or ()
        return (
            [row[0] for row in rows],
            [row[1] for row in rows],
            [row[2] for row in rows],
        )
    raise OcrBackendError(f"unsupported RapidOCR result type: {type(result)!r}")


def recognize_image(
    image_path: Path,
    runtime: OcrRuntime,
    *,
    region: tuple[int, int, int, int] | None = None,
    minimum_score: float = 0.0,
) -> dict[str, object]:
    from PIL import Image
    import numpy as np

    image_path = image_path.resolve()
    with Image.open(image_path) as source:
        source.load()
        width, height = source.size
        if region is None:
            crop_box = (0, 0, width, height)
        else:
            left, top, right, bottom = region
            if left < 0 or top < 0 or right <= left or bottom <= top:
                raise ValueError(f"invalid OCR region: {region}")
            if right > width or bottom > height:
                raise ValueError(f"OCR region {region} exceeds image size {(width, height)}")
            crop_box = region
        cropped = source.convert("RGB").crop(crop_box)
        rgb = np.asarray(cropped)
        bgr = np.ascontiguousarray(rgb[:, :, ::-1])
    try:
        raw = runtime.engine(bgr, text_score=minimum_score)
    except TypeError:
        raw = runtime.engine(bgr)
    boxes, texts, scores = _unpack_result(raw)
    spans: list[OcrSpan] = []
    offset = (crop_box[0], crop_box[1])
    for polygon, text, score in zip(boxes, texts, scores, strict=True):
        if float(score) >= minimum_score:
            spans.append(OcrSpan.from_polygon(str(text), float(score), polygon, offset))
    return {
        "schema": 1,
        "captured_at_utc": utc_now(),
        "image": str(image_path),
        "image_sha256": sha256_file(image_path),
        "image_size": [width, height],
        "region": list(crop_box),
        "minimum_score": minimum_score,
        "ocr": runtime.to_dict(),
        "spans": [span.to_dict() for span in spans],
    }
