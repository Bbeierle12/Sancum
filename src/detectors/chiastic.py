
import re
from typing import List, Optional, Dict

def detect(words: List[str]) -> Optional[Dict]:
    """
    Detects a chiastic structure in a list of words and provides a basic score.
    A chiasm is a rhetorical device of repetition in reverse order (A-B-C-B-A).
    This detector identifies the center and pairs of corresponding words.
    Reference: Based on general principles of literary analysis, e.g.,
    Bullinger, E. W. (1898). Figures of Speech Used in the Bible.
    """
    word_count = len(words)
    # A meaningful chiasm needs at least 5 elements (A-B-C-B-A)
    if word_count < 5:
        return None

    center_point = ""
    max_depth = word_count // 2
    
    if word_count % 2 != 0:
        # Odd number of words, single word is the center
        center_point = words[max_depth]
    else:
        # Even number of words, center is between two words
        center_point = f"{words[max_depth - 1]} | {words[max_depth]}"

    elements = []
    match_count = 0
    for i in range(max_depth):
        word_a = words[i]
        word_b = words[word_count - 1 - i]
        pair = f"({chr(65+i)}) {word_a} <-> {word_b}"
        elements.append(pair)
        if word_a == word_b:
            match_count += 1

    # Simple scoring: ratio of identical pairs to total possible pairs
    score = round(match_count / max_depth, 2) if max_depth > 0 else 0

    return {
        "type": "Chiastic",
        "center": center_point,
        "elements": elements,
        "score": score,
        "match_count": match_count,
        "depth": max_depth
    }
