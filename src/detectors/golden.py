
from typing import List, Optional, Dict

# The golden ratio, φ (phi), is an irrational number approximately
# equal to 1.618. It is often found in art, architecture, and nature.
# Some scholars suggest it's also used as a structural principle in literature.
# Ref: https://en.wikipedia.org/wiki/Golden_ratio
GOLDEN_RATIO = 1.61803398875

def detect(words: List[str]) -> Optional[Dict]:
    """
    Finds the pivot point in a text based on the golden ratio (phi).
    The pivot is the word at the index that divides the text into two
    segments whose lengths are in the golden ratio.
    There are two pivot points: the major section and the minor section.
    Major: total / phi
    Minor: total * (1 - 1/phi)
    """
    word_count = len(words)
    if word_count < 5:
        return None

    # Major section pivot
    major_index = round(word_count / GOLDEN_RATIO)
    major_word = words[major_index] if 0 <= major_index < word_count else ""
    
    # Minor section pivot (from the beginning)
    minor_index = round(word_count * (1 - (1 / GOLDEN_RATIO)))
    minor_word = words[minor_index] if 0 <= minor_index < word_count else ""

    return {
        "type": "Golden Ratio",
        "total_words": word_count,
        "major_pivot": {
            "index": major_index,
            "word": major_word
        },
        "minor_pivot": {
            "index": minor_index,
            "word": minor_word
        }
    }
