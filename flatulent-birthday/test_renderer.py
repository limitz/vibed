"""Tests for the song renderer module."""

import unittest
import os
import tempfile
import numpy as np
from renderer import render_song, save_mp3


class TestRenderSong(unittest.TestCase):
    def test_returns_numpy_array(self):
        notes = [(261.63, 0.3), (293.66, 0.3)]
        result = render_song(notes)
        self.assertIsInstance(result, np.ndarray)

    def test_correct_approximate_length(self):
        notes = [(261.63, 0.5), (293.66, 0.5)]
        result = render_song(notes, sample_rate=44100)
        expected = 44100 * 1.0  # ~1 second total
        self.assertAlmostEqual(len(result), expected, delta=500)

    def test_silence_for_zero_freq(self):
        notes = [(0, 0.5)]
        result = render_song(notes)
        rms = np.sqrt(np.mean(result ** 2))
        self.assertLess(rms, 0.01)

    def test_not_silent_for_real_notes(self):
        notes = [(200.0, 0.5)]
        result = render_song(notes, master_volume=0.5)
        rms = np.sqrt(np.mean(result ** 2))
        self.assertGreater(rms, 0.001)

    def test_master_volume_affects_output(self):
        notes = [(200.0, 0.5)]
        loud = render_song(notes, master_volume=0.8)
        quiet = render_song(notes, master_volume=0.1)
        # Due to randomness, compare RMS roughly
        rms_loud = np.sqrt(np.mean(loud ** 2))
        rms_quiet = np.sqrt(np.mean(quiet ** 2))
        self.assertGreater(rms_loud, rms_quiet)

    def test_normalized_range(self):
        notes = [(200.0, 0.3), (300.0, 0.3), (400.0, 0.3)]
        result = render_song(notes, master_volume=0.3)
        self.assertLessEqual(np.max(np.abs(result)), 1.0)

    def test_no_nan_or_inf(self):
        notes = [(100.0, 0.5), (200.0, 0.5)]
        result = render_song(notes)
        self.assertFalse(np.any(np.isnan(result)))
        self.assertFalse(np.any(np.isinf(result)))


class TestSaveMp3(unittest.TestCase):
    def test_creates_mp3_file(self):
        audio = np.sin(2 * np.pi * 440 * np.linspace(0, 1, 44100))
        audio = (audio * 0.3).astype(np.float64)
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            path = f.name
        try:
            save_mp3(audio, path)
            self.assertTrue(os.path.exists(path))
            self.assertGreater(os.path.getsize(path), 100)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
