"""Golden ratio pivot detector."""

from __future__ import annotations

from typing import List, Optional

GOLDEN_RATIO = 1.61803398875


def detect(tokens: List[str]) -> Optional[int]:
    """Return index of major φ pivot if applicable."""
    n = len(tokens)
    if n < 5:
        return None
    idx = round(n / GOLDEN_RATIO)
    return idx if 0 <= idx < n else None
