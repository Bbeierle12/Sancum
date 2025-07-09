"""Simple Hawkes-process forecaster."""

from __future__ import annotations

from typing import List

import numpy as np


class HawkesForecaster:
    """Very small Hawkes-like process using exponential kernel."""

    def __init__(
        self, baseline: float = 0.1, alpha: float = 0.5, beta: float = 1.0
    ) -> None:
        self.baseline = baseline
        self.alpha = alpha
        self.beta = beta

    def forecast(self, events: List[int], horizon: int) -> List[float]:
        times = np.arange(1, horizon + 1)
        intensity = np.full_like(times, self.baseline, dtype=float)
        past_events = np.array(events)
        for t in times:
            # Filter events that occurred before the current time t
            relevant_events = past_events[past_events < t]
            if relevant_events.size > 0:
                intensity[t - 1] += self.alpha * np.sum(
                    np.exp(-self.beta * (t - relevant_events))
                )
        prob = 1 - np.exp(-intensity)
        return prob.tolist()
