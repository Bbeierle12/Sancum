"""Chiastic detector using windowed mirror matching."""

from __future__ import annotations

from typing import List, Optional


# This algorithm scans for reverse symmetry around a center point.
# It scores by counting symmetric token pairs in mirrored windows.
# Inspired by classic literary chiasm analysis [Bullinger, 1898].


def detect(tokens: List[str], window: int = 5) -> Optional[tuple[int, float]]:
    """Return best pivot index and score if found."""
    n = len(tokens)
    if n < 3:
        return None

    window = min(window, (n - 1) // 2)
    best = (0, 0.0)
    for center in range(window, n - window):
        score = 0
        for offset in range(1, window + 1):
            if center - offset < 0 or center + offset >= n:
                break
            if tokens[center - offset] == tokens[center + offset]:
                score += 1
        norm = score / window
        if norm > best[1]:
            best = (center, round(norm, 2))
    if best[1] == 0:
        return None
    return best
