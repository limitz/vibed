"""Tests for melody module."""

import unittest
from song_structure import SongStructure, Section
from melody import (Note, DrumHit, note_to_freq, generate_lead_melody,
                    generate_bass_line, generate_chord_pads, generate_drum_pattern)


def _make_simple_song():
    return SongStructure(
        title="Test", key="C", tempo=120,
        time_signature=(4, 4),
        sections=[
            Section("Verse", 4, ["C", "Am", "F", "G"], "verse"),
            Section("Chorus", 4, ["F", "G", "Am", "C"], "chorus"),
        ]
    )


class TestNoteToFreq(unittest.TestCase):
    def test_a4(self):
        freq = note_to_freq("A", 4)
        self.assertAlmostEqual(freq, 440.0, places=1)

    def test_c4(self):
        freq = note_to_freq("C", 4)
        self.assertAlmostEqual(freq, 261.63, places=0)

    def test_octave_doubles(self):
        f4 = note_to_freq("A", 4)
        f5 = note_to_freq("A", 5)
        self.assertAlmostEqual(f5 / f4, 2.0, places=2)


class TestGenerateLeadMelody(unittest.TestCase):
    def test_returns_notes(self):
        song = _make_simple_song()
        notes = generate_lead_melody(song)
        self.assertIsInstance(notes, list)
        self.assertGreater(len(notes), 0)
        self.assertIsInstance(notes[0], Note)

    def test_notes_within_song_duration(self):
        song = _make_simple_song()
        notes = generate_lead_melody(song)
        for note in notes:
            self.assertGreaterEqual(note.start, 0)
            self.assertLessEqual(note.start + note.duration, song.total_duration + 0.1)

    def test_velocities_valid(self):
        song = _make_simple_song()
        notes = generate_lead_melody(song)
        for note in notes:
            self.assertGreaterEqual(note.velocity, 0.0)
            self.assertLessEqual(note.velocity, 1.0)


class TestGenerateBassLine(unittest.TestCase):
    def test_returns_notes(self):
        song = _make_simple_song()
        notes = generate_bass_line(song)
        self.assertIsInstance(notes, list)
        self.assertGreater(len(notes), 0)

    def test_bass_frequencies_low(self):
        song = _make_simple_song()
        notes = generate_bass_line(song)
        for note in notes:
            if note.pitch > 0:
                self.assertLess(note.pitch, 300, "Bass notes should be below 300 Hz")


class TestGenerateChordPads(unittest.TestCase):
    def test_returns_chords(self):
        song = _make_simple_song()
        chords = generate_chord_pads(song)
        self.assertIsInstance(chords, list)
        self.assertGreater(len(chords), 0)

    def test_each_chord_has_notes(self):
        song = _make_simple_song()
        chords = generate_chord_pads(song)
        for chord in chords:
            self.assertIsInstance(chord, list)
            self.assertGreater(len(chord), 0)


class TestGenerateDrumPattern(unittest.TestCase):
    def test_returns_hits(self):
        song = _make_simple_song()
        hits = generate_drum_pattern(song)
        self.assertIsInstance(hits, list)
        self.assertGreater(len(hits), 0)
        self.assertIsInstance(hits[0], DrumHit)

    def test_has_kick_and_snare(self):
        song = _make_simple_song()
        hits = generate_drum_pattern(song)
        drums = {h.drum for h in hits}
        self.assertIn("kick", drums)
        self.assertIn("snare", drums)


if __name__ == "__main__":
    unittest.main()
