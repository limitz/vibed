"""Song structure module - defines sections, chord progressions, tempo, and arrangement."""

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Section:
    """A section of the song (verse, chorus, bridge, etc.)."""
    name: str
    bars: int
    chords: List[str]  # Chord names per bar (e.g. ["C", "Am", "F", "G"])
    melody_style: str  # "verse", "chorus", "bridge", "intro", "outro"


@dataclass
class SongStructure:
    """Complete song structure."""
    title: str
    key: str
    tempo: int  # BPM
    time_signature: Tuple[int, int]  # e.g. (4, 4)
    sections: List[Section] = field(default_factory=list)
    sample_rate: int = 44100

    @property
    def beats_per_bar(self) -> int:
        return self.time_signature[0]

    @property
    def seconds_per_beat(self) -> float:
        return 60.0 / self.tempo

    @property
    def seconds_per_bar(self) -> float:
        return self.seconds_per_beat * self.beats_per_bar

    @property
    def total_bars(self) -> int:
        return sum(s.bars for s in self.sections)

    @property
    def total_duration(self) -> float:
        return self.total_bars * self.seconds_per_bar


def create_hit_song() -> SongStructure:
    """Create a catchy pop song structure.

    Structure: Intro - Verse 1 - Chorus - Verse 2 - Chorus - Bridge - Chorus - Outro
    Key: C major, 120 BPM, 4/4 time
    """
    song = SongStructure(
        title="Electric Dreams",
        key="C",
        tempo=120,
        time_signature=(4, 4),
        sections=[
            Section("Intro", 4,
                    ["C", "G", "Am", "F"],
                    "intro"),
            Section("Verse 1", 8,
                    ["Am", "F", "C", "G", "Am", "F", "C", "G"],
                    "verse"),
            Section("Chorus", 8,
                    ["F", "G", "Am", "C", "F", "G", "C", "C"],
                    "chorus"),
            Section("Verse 2", 8,
                    ["Am", "F", "C", "G", "Am", "F", "C", "G"],
                    "verse"),
            Section("Chorus", 8,
                    ["F", "G", "Am", "C", "F", "G", "C", "C"],
                    "chorus"),
            Section("Bridge", 4,
                    ["Dm", "Em", "F", "G"],
                    "bridge"),
            Section("Chorus", 8,
                    ["F", "G", "Am", "C", "F", "G", "C", "C"],
                    "chorus"),
            Section("Outro", 4,
                    ["C", "G", "Am", "F"],
                    "outro"),
        ]
    )
    return song
