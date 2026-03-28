"""Tests for synthesizer module."""

import unittest
import numpy as np
from melody import Note, DrumHit
from synthesizer import (synthesize_lead, synthesize_bass, synthesize_pads,
                         synthesize_drums, apply_envelope)


class TestSynthesizeLead(unittest.TestCase):
    def test_returns_array(self):
        notes = [Note(440.0, 0.0, 0.5, 0.8), Note(523.25, 0.5, 0.5, 0.8)]
        audio = synthesize_lead(notes, 44100)
        self.assertIsInstance(audio, np.ndarray)

    def test_correct_length(self):
        notes = [Note(440.0, 0.0, 1.0, 0.8)]
        audio = synthesize_lead(notes, 44100)
        # Should be at least 1 second
        self.assertGreaterEqual(len(audio), 44100)

    def test_values_in_range(self):
        notes = [Note(440.0, 0.0, 0.5, 0.8)]
        audio = synthesize_lead(notes, 44100)
        self.assertLessEqual(np.max(np.abs(audio)), 1.5)


class TestSynthesizeBass(unittest.TestCase):
    def test_returns_array(self):
        notes = [Note(110.0, 0.0, 1.0, 0.8)]
        audio = synthesize_bass(notes, 44100)
        self.assertIsInstance(audio, np.ndarray)
        self.assertGreater(len(audio), 0)


class TestSynthesizePads(unittest.TestCase):
    def test_returns_array(self):
        chords = [[Note(261.63, 0.0, 2.0, 0.5),
                    Note(329.63, 0.0, 2.0, 0.5),
                    Note(392.00, 0.0, 2.0, 0.5)]]
        audio = synthesize_pads(chords, 44100)
        self.assertIsInstance(audio, np.ndarray)
        self.assertGreater(len(audio), 0)


class TestSynthesizeDrums(unittest.TestCase):
    def test_returns_array(self):
        hits = [DrumHit("kick", 0.0, 0.9), DrumHit("snare", 0.5, 0.8)]
        audio = synthesize_drums(hits, 44100)
        self.assertIsInstance(audio, np.ndarray)
        self.assertGreater(len(audio), 0)


class TestApplyEnvelope(unittest.TestCase):
    def test_returns_same_length(self):
        signal = np.ones(44100)
        result = apply_envelope(signal, 0.01, 0.05, 0.7, 0.1, 44100)
        self.assertEqual(len(result), len(signal))

    def test_attack_starts_quiet(self):
        signal = np.ones(44100)
        result = apply_envelope(signal, 0.1, 0.05, 0.7, 0.1, 44100)
        # First sample should be near zero
        self.assertLess(abs(result[0]), 0.1)


if __name__ == "__main__":
    unittest.main()
