from datetime import datetime, timedelta


def update_sm2(verse: dict, quality: int):
    """
    Updates SM-2 parameters based on recall quality.
    A simplified approach for demonstration.

    Args:
        verse (dict): The verse record containing SM-2 fields.
        quality (int): Recall quality: 0-Again, 1-Hard, 2-Good, 3-Easy, 4-Perfect

    Returns:
        dict: The updated verse record.
    """
    if quality < 2:  # If "Again" or "Hard"
        verse["repetitions"] = 0
        verse["interval"] = 1
    else:
        verse["repetitions"] += 1
        if verse["repetitions"] == 1:
            verse["interval"] = 1
        elif verse["repetitions"] == 2:
            verse["interval"] = 6
        else:
            verse["interval"] = round(verse["interval"] * verse["easiness_factor"])

        # Adjust easiness factor
        verse["easiness_factor"] += (0.1 - (4 - quality) * (0.08 + (4 - quality) * 0.02))
        if verse["easiness_factor"] < 1.3:
            verse["easiness_factor"] = 1.3

    verse["next_due"] = datetime.utcnow() + timedelta(days=verse["interval"])
    return verse
