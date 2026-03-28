"""Tests for audio export."""

import os
import unittest
import tempfile
import wave
import numpy as np
from speakup.exporter import normalize, save_wav, save_audio


SAMPLE_RATE = 44100


class TestNormalize(unittest.TestCase):
    def test_peak_level(self):
        samples = np.array([0.0, 0.5, -0.5, 1.0, -1.0])
        result = normalize(samples, peak=0.95)
        self.assertAlmostEqual(np.max(np.abs(result)), 0.95, places=5)

    def test_silent_input(self):
        samples = np.zeros(100)
        result = normalize(samples, peak=0.95)
        np.testing.assert_allclose(result, np.zeros(100))

    def test_preserves_shape(self):
        samples = np.random.randn(1000)
        result = normalize(samples)
        self.assertEqual(len(result), len(samples))

    def test_already_normalized(self):
        samples = np.array([0.95, -0.95, 0.0])
        result = normalize(samples, peak=0.95)
        np.testing.assert_allclose(result, samples, atol=1e-10)


class TestSaveWav(unittest.TestCase):
    def test_creates_file(self):
        samples = np.sin(np.linspace(0, 2 * np.pi * 440, SAMPLE_RATE))
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            filepath = f.name
        try:
            save_wav(samples, filepath, SAMPLE_RATE)
            self.assertTrue(os.path.exists(filepath))
            self.assertGreater(os.path.getsize(filepath), 0)
        finally:
            os.unlink(filepath)

    def test_readable_wav(self):
        samples = np.sin(np.linspace(0, 2 * np.pi * 440, SAMPLE_RATE))
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            filepath = f.name
        try:
            save_wav(samples, filepath, SAMPLE_RATE)
            with wave.open(filepath, "rb") as wf:
                self.assertEqual(wf.getframerate(), SAMPLE_RATE)
                self.assertEqual(wf.getnchannels(), 1)
                self.assertEqual(wf.getsampwidth(), 2)
                self.assertEqual(wf.getnframes(), SAMPLE_RATE)
        finally:
            os.unlink(filepath)


class TestSaveAudio(unittest.TestCase):
    def test_wav_extension(self):
        samples = np.sin(np.linspace(0, 2 * np.pi * 440, SAMPLE_RATE))
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            filepath = f.name
        try:
            save_audio(samples, filepath, SAMPLE_RATE)
            self.assertTrue(os.path.exists(filepath))
        finally:
            os.unlink(filepath)


if __name__ == "__main__":
    unittest.main()
