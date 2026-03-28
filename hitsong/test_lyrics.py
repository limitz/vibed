"""Tests for lyrics module."""

import unittest
from song_structure import SongStructure, Section
from lyrics import generate_lyrics


class TestGenerateLyrics(unittest.TestCase):
    def test_returns_dict(self):
        song = SongStructure(
            title="Test", key="C", tempo=120,
            time_signature=(4, 4),
            sections=[
                Section("Verse 1", 4, ["C"] * 4, "verse"),
                Section("Chorus", 4, ["F"] * 4, "chorus"),
            ]
        )
        lyrics = generate_lyrics(song)
        self.assertIsInstance(lyrics, dict)

    def test_has_lyrics_for_sections(self):
        song = SongStructure(
            title="Test", key="C", tempo=120,
            time_signature=(4, 4),
            sections=[
                Section("Verse 1", 4, ["C"] * 4, "verse"),
                Section("Chorus", 4, ["F"] * 4, "chorus"),
            ]
        )
        lyrics = generate_lyrics(song)
        self.assertGreater(len(lyrics), 0)

    def test_lyrics_are_strings(self):
        song = SongStructure(
            title="Test", key="C", tempo=120,
            time_signature=(4, 4),
            sections=[
                Section("Verse 1", 4, ["C"] * 4, "verse"),
                Section("Chorus", 4, ["F"] * 4, "chorus"),
            ]
        )
        lyrics = generate_lyrics(song)
        for section_name, lines in lyrics.items():
            self.assertIsInstance(section_name, str)
            for line in lines:
                self.assertIsInstance(line, str)
                self.assertGreater(len(line), 0)


if __name__ == "__main__":
    unittest.main()
