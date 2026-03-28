"""Tests for mixer module."""

import unittest
import numpy as np
from mixer import mix_tracks, apply_reverb, apply_compression, normalize, master


class TestMixTracks(unittest.TestCase):
    def test_mixes_two_tracks(self):
        t1 = np.ones(44100) * 0.5
        t2 = np.ones(44100) * 0.3
        mixed = mix_tracks([(t1, 1.0), (t2, 1.0)])
        self.assertEqual(len(mixed), 44100)

    def test_volume_scaling(self):
        t1 = np.ones(1000) * 1.0
        mixed = mix_tracks([(t1, 0.5)])
        self.assertAlmostEqual(mixed[0], 0.5, places=2)

    def test_different_lengths(self):
        t1 = np.ones(44100)
        t2 = np.ones(22050)
        mixed = mix_tracks([(t1, 1.0), (t2, 1.0)])
        self.assertEqual(len(mixed), 44100)


class TestNormalize(unittest.TestCase):
    def test_normalizes_to_target(self):
        audio = np.array([0.1, -0.2, 0.3, -0.1])
        result = normalize(audio, 0.9)
        self.assertAlmostEqual(np.max(np.abs(result)), 0.9, places=2)

    def test_silent_audio(self):
        audio = np.zeros(100)
        result = normalize(audio, 0.9)
        self.assertTrue(np.all(result == 0))


class TestApplyCompression(unittest.TestCase):
    def test_reduces_peaks(self):
        audio = np.array([0.1, 0.5, 1.0, 0.8, 0.3])
        result = apply_compression(audio, threshold=0.5, ratio=4.0)
        self.assertLessEqual(np.max(np.abs(result)), np.max(np.abs(audio)))


class TestApplyReverb(unittest.TestCase):
    def test_returns_array(self):
        audio = np.random.randn(44100) * 0.1
        result = apply_reverb(audio, 0.3, 44100)
        self.assertIsInstance(result, np.ndarray)
        self.assertGreater(len(result), 0)


class TestMaster(unittest.TestCase):
    def test_returns_array(self):
        audio = np.random.randn(44100) * 0.3
        result = master(audio, 44100)
        self.assertIsInstance(result, np.ndarray)
        self.assertGreater(len(result), 0)

    def test_output_normalized(self):
        audio = np.random.randn(44100) * 0.3
        result = master(audio, 44100)
        self.assertLessEqual(np.max(np.abs(result)), 1.0)


if __name__ == "__main__":
    unittest.main()
