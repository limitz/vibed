"""Text-to-phoneme conversion — maps English text to phoneme sequences."""

from __future__ import annotations

import re

from .phonemes import PHONEMES

# Dictionary of common words → phoneme sequences
WORD_DICT: dict[str, list[str]] = {
    "a": ["AH"],
    "am": ["AE", "M"],
    "an": ["AE", "N"],
    "and": ["AE", "N", "D"],
    "are": ["AH", "R"],
    "at": ["AE", "T"],
    "be": ["B", "EE"],
    "been": ["B", "IH", "N"],
    "but": ["B", "UH", "T"],
    "by": ["B", "AY"],
    "can": ["K", "AE", "N"],
    "do": ["D", "OO"],
    "for": ["F", "OH", "R"],
    "from": ["F", "R", "UH", "M"],
    "get": ["G", "EH", "T"],
    "go": ["G", "OH"],
    "got": ["G", "AH", "T"],
    "had": ["HH", "AE", "D"],
    "has": ["HH", "AE", "Z"],
    "have": ["HH", "AE", "V"],
    "he": ["HH", "EE"],
    "hello": ["HH", "EH", "L", "OH"],
    "her": ["HH", "ER"],
    "here": ["HH", "IH", "R"],
    "hi": ["HH", "AY"],
    "him": ["HH", "IH", "M"],
    "his": ["HH", "IH", "Z"],
    "how": ["HH", "AW"],
    "i": ["AY"],
    "if": ["IH", "F"],
    "in": ["IH", "N"],
    "is": ["IH", "Z"],
    "it": ["IH", "T"],
    "just": ["D", "UH", "S", "T"],
    "know": ["N", "OH"],
    "learn": ["L", "ER", "N"],
    "learned": ["L", "ER", "N", "D"],
    "learning": ["L", "ER", "N", "IH", "NG"],
    "let": ["L", "EH", "T"],
    "like": ["L", "AY", "K"],
    "look": ["L", "UH", "K"],
    "make": ["M", "AY", "K"],
    "mama": ["M", "AH", "M", "AH"],
    "me": ["M", "EE"],
    "my": ["M", "AY"],
    "no": ["N", "OH"],
    "not": ["N", "AH", "T"],
    "now": ["N", "AW"],
    "of": ["UH", "V"],
    "on": ["AH", "N"],
    "one": ["W", "UH", "N"],
    "only": ["OH", "N", "L", "EE"],
    "or": ["OH", "R"],
    "out": ["AW", "T"],
    "papa": ["P", "AH", "P", "AH"],
    "say": ["S", "AY"],
    "she": ["SH", "EE"],
    "so": ["S", "OH"],
    "some": ["S", "UH", "M"],
    "speak": ["S", "P", "EE", "K"],
    "synthesis": ["S", "IH", "N", "TH", "AH", "S", "IH", "S"],
    "that": ["DH", "AE", "T"],
    "the": ["DH", "AH"],
    "their": ["DH", "EH", "R"],
    "them": ["DH", "EH", "M"],
    "then": ["DH", "EH", "N"],
    "there": ["DH", "EH", "R"],
    "they": ["DH", "AY"],
    "this": ["DH", "IH", "S"],
    "to": ["T", "OO"],
    "up": ["UH", "P"],
    "us": ["UH", "S"],
    "use": ["Y", "OO", "Z"],
    "using": ["Y", "OO", "Z", "IH", "NG"],
    "was": ["W", "AH", "Z"],
    "we": ["W", "EE"],
    "what": ["W", "AH", "T"],
    "when": ["W", "EH", "N"],
    "will": ["W", "IH", "L"],
    "with": ["W", "IH", "TH"],
    "word": ["W", "ER", "D"],
    "words": ["W", "ER", "D", "Z"],
    "world": ["W", "ER", "L", "D"],
    "yes": ["Y", "EH", "S"],
    "you": ["Y", "OO"],
    "fm": ["EH", "F", "EH", "M"],
}

# Fallback letter/digraph-to-phoneme rules (order matters for digraphs)
_DIGRAPH_RULES: list[tuple[str, list[str]]] = [
    ("sh", ["SH"]),
    ("ch", ["T", "SH"]),
    ("th", ["TH"]),
    ("ng", ["NG"]),
    ("ph", ["F"]),
    ("wh", ["W"]),
    ("ck", ["K"]),
    ("ee", ["EE"]),
    ("oo", ["OO"]),
    ("ea", ["EE"]),
    ("ou", ["AW"]),
    ("ai", ["AY"]),
    ("oa", ["OH"]),
    ("igh", ["AY"]),
    ("qu", ["K", "W"]),
]

_LETTER_RULES: dict[str, list[str]] = {
    "a": ["AE"],
    "b": ["B"],
    "c": ["K"],
    "d": ["D"],
    "e": ["EH"],
    "f": ["F"],
    "g": ["G"],
    "h": ["HH"],
    "i": ["IH"],
    "j": ["D", "SH"],
    "k": ["K"],
    "l": ["L"],
    "m": ["M"],
    "n": ["N"],
    "o": ["AH"],
    "p": ["P"],
    "r": ["R"],
    "s": ["S"],
    "t": ["T"],
    "u": ["UH"],
    "v": ["V"],
    "w": ["W"],
    "x": ["K", "S"],
    "y": ["Y"],
    "z": ["Z"],
}


def word_to_phonemes(word: str) -> list[str]:
    """Convert a single word to phonemes using dictionary then rules."""
    word = word.lower().strip()
    if not word:
        return []

    # Dictionary lookup
    if word in WORD_DICT:
        return list(WORD_DICT[word])

    # Fallback: letter rules with digraph matching
    phonemes = []
    i = 0
    while i < len(word):
        matched = False
        # Try digraphs (longest first — trigraph "igh")
        for digraph, phones in _DIGRAPH_RULES:
            dlen = len(digraph)
            if word[i:i + dlen] == digraph:
                phonemes.extend(phones)
                i += dlen
                matched = True
                break
        if not matched:
            ch = word[i]
            if ch in _LETTER_RULES:
                phonemes.extend(_LETTER_RULES[ch])
            # Skip characters not in rules (silent e, punctuation, etc.)
            i += 1

    return phonemes


def text_to_phonemes(text: str) -> list[str]:
    """Convert English text to a flat sequence of phoneme labels."""
    text = text.strip()
    if not text:
        return []

    # Strip punctuation, split into words
    cleaned = re.sub(r"[^\w\s]", "", text)
    words = cleaned.split()
    if not words:
        return []

    phonemes = []
    for i, word in enumerate(words):
        word_phones = word_to_phonemes(word)
        phonemes.extend(word_phones)
        # Add silence between words (not after last word)
        if i < len(words) - 1:
            phonemes.append("SIL")

    return phonemes
