from __future__ import annotations

from dataclasses import asdict, dataclass
import unicodedata


def normalize_ocr_text(text: str) -> str:
    """Normalize UI text for matching without changing the recorded source text."""
    return "".join(unicodedata.normalize("NFKC", text).split())


@dataclass(frozen=True, slots=True)
class OcrSpan:
    text: str
    normalized: str
    score: float
    center: tuple[int, int]
    bbox: tuple[int, int, int, int]

    @classmethod
    def from_polygon(
        cls,
        text: str,
        score: float,
        polygon: object,
        offset: tuple[int, int] = (0, 0),
    ) -> "OcrSpan":
        points = list(polygon)  # type: ignore[arg-type]
        if not points:
            raise ValueError("OCR polygon must contain at least one point")
        xs = [float(point[0]) for point in points]
        ys = [float(point[1]) for point in points]
        left = round(min(xs)) + offset[0]
        top = round(min(ys)) + offset[1]
        right = round(max(xs)) + offset[0]
        bottom = round(max(ys)) + offset[1]
        return cls(
            text=text,
            normalized=normalize_ocr_text(text),
            score=float(score),
            center=((left + right) // 2, (top + bottom) // 2),
            bbox=(left, top, right, bottom),
        )

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class WindowBinding:
    process_name: str
    executable: str
    pid: int
    hwnd: int
    title: str
    client_origin: tuple[int, int]
    client_size: tuple[int, int]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
