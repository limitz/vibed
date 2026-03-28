"""Tests for song_structure module."""

import unittest
from song_structure import SongStructure, Section, create_hit_song


class TestSection(unittest.TestCase):
    def test_section_creation(self):
        s = Section(name="Verse", bars=8, chords=["C", "Am", "F", "G"] * 2,
                    melody_style="verse")
        self.assertEqual(s.name, "Verse")
        self.assertEqual(s.bars, 8)
        self.assertEqual(len(s.chords), 8)


class TestSongStructure(unittest.TestCase):
    def test_basic_properties(self):
        song = SongStructure(
            title="Test", key="C", tempo=120,
            time_signature=(4, 4),
            sections=[
                Section("V", 4, ["C"] * 4, "verse"),
                Section("C", 4, ["F"] * 4, "chorus"),
            ]
        )
        self.assertEqual(song.beats_per_bar, 4)
        self.assertAlmostEqual(song.seconds_per_beat, 0.5)
        self.assertAlmostEqual(song.seconds_per_bar, 2.0)
        self.assertEqual(song.total_bars, 8)
        self.assertAlmostEqual(song.total_duration, 16.0)


class TestCreateHitSong(unittest.TestCase):
    def test_returns_song_structure(self):
        song = create_hit_song()
        self.assertIsInstance(song, SongStructure)

    def test_has_sections(self):
        song = create_hit_song()
        self.assertGreater(len(song.sections), 0)

    def test_has_reasonable_tempo(self):
        song = create_hit_song()
        self.assertGreaterEqual(song.tempo, 80)
        self.assertLessEqual(song.tempo, 180)

    def test_has_chorus(self):
        song = create_hit_song()
        section_names = [s.name.lower() for s in song.sections]
        self.assertTrue(any("chorus" in n for n in section_names))

    def test_chords_match_bars(self):
        song = create_hit_song()
        for section in song.sections:
            self.assertEqual(len(section.chords), section.bars,
                             f"Section {section.name}: chords count should match bars")

    def test_duration_reasonable(self):
        song = create_hit_song()
        # A hit song should be 2-5 minutes
        self.assertGreater(song.total_duration, 60)
        self.assertLess(song.total_duration, 360)


if __name__ == "__main__":
    unittest.main()
