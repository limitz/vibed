"""Lyrics module - generates song lyrics."""

from typing import List, Dict
from song_structure import SongStructure


_LYRICS = {
    "verse": [
        [
            "Walking through the neon lights tonight",
            "Every shadow comes alive in sight",
            "The city hums a melody so bright",
            "And I can feel the rhythm hold me tight",
        ],
        [
            "Stars are falling through the digital sky",
            "Every heartbeat echoes amplified",
            "The future waits beyond the flashing signs",
            "Together we'll rewrite the end of time",
        ],
    ],
    "chorus": [
        "Electric dreams are running through my veins",
        "We're burning bright, we'll never be the same",
        "Turn it up and let the music reign",
        "Electric dreams, electric dreams again",
    ],
    "bridge": [
        "When the world goes quiet and the screens go dark",
        "I still hear the echo of your spark",
    ],
    "intro": [],
    "outro": [],
}


def generate_lyrics(song: SongStructure) -> Dict[str, List[str]]:
    """Generate lyrics for each section of the song."""
    lyrics = {}
    verse_count = 0

    for section in song.sections:
        style = section.melody_style

        if style == "verse":
            verse_lyrics = _LYRICS["verse"][verse_count % len(_LYRICS["verse"])]
            lyrics[section.name] = verse_lyrics
            verse_count += 1
        elif style == "chorus":
            lyrics[section.name] = _LYRICS["chorus"]
        elif style == "bridge":
            lyrics[section.name] = _LYRICS["bridge"]
        # intro/outro have no lyrics

    return lyrics
