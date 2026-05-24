import io
from dataclasses import dataclass
from enum import Enum

import numpy as np
from PIL import Image


class ChangeDecision(str, Enum):
    IGNORE = "ignore"
    SAVE_ONLY = "save_only"
    PROCESS_WITH_AI = "process_with_ai"


@dataclass
class DiffResult:
    score: float
    decision: ChangeDecision


def _to_grayscale_array(image_bytes: bytes, size: int = 32) -> np.ndarray:
    image = Image.open(io.BytesIO(image_bytes)).convert("L")
    image = image.resize((size, size))
    return np.asarray(image, dtype=np.float32)


def compute_difference_score(previous_bytes: bytes | None, current_bytes: bytes) -> float:
    if previous_bytes is None:
        return 100.0

    previous = _to_grayscale_array(previous_bytes)
    current = _to_grayscale_array(current_bytes)
    diff = np.abs(previous - current)
    return float((diff.mean() / 255.0) * 100.0)


def classify_change(score: float, ignore_threshold: float, save_only_threshold: float) -> ChangeDecision:
    if score < ignore_threshold:
        return ChangeDecision.IGNORE
    if score < save_only_threshold:
        return ChangeDecision.SAVE_ONLY
    return ChangeDecision.PROCESS_WITH_AI
