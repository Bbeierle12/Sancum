from datetime import datetime, timedelta


def update_sm2_stats(ease: float, reps: int, interval: int, q: int) -> dict:
    """Update spaced repetition statistics using the SM-2 algorithm.

    Args:
        ease: Current easiness factor.
        reps: Number of successful repetitions so far.
        interval: Current interval in days.
        q: Quality of recall from 0 (complete blackout) to 5 (perfect).

    Returns:
        dict with updated ``easiness_factor``, ``repetitions``, ``interval`` and
        ``next_due`` ``datetime``.
    """
    if not 0 <= q <= 5:
        raise ValueError("q rating must be between 0 and 5")

    # Reset on complete failure
    if q <= 2:
        reps = 0
        interval = 1
    else:
        reps += 1
        if reps == 1:
            interval = 1
        elif reps == 2:
            interval = 6
        else:
            interval = round(interval * ease)

    # Update easiness factor according to SM-2
    ease += 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)
    if ease < 1.3:
        ease = 1.3

    next_due = datetime.utcnow() + timedelta(days=interval)

    return {
        "easiness_factor": ease,
        "repetitions": reps,
        "interval": interval,
        "next_due": next_due,
    }


def update_sm2(verse: dict, quality: int):
    """Backward compatible wrapper around :func:`update_sm2_stats`."""
    stats = update_sm2_stats(
        verse.get("easiness_factor", 2.5),
        verse.get("repetitions", 0),
        verse.get("interval", 0),
        quality,
    )
    verse.update(stats)
    return verse
