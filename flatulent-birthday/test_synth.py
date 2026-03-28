"""Tests for the flatulence synthesis engine."""

import unittest
import numpy as np
from synth import synthesize, SAMPLE_RATE


class TestSynthesize(unittest.TestCase):
    def test_returns_numpy_array(self):
        result = synthesize(100.0, 0.5, seed=42)
        self.assertIsInstance(result, np.ndarray)

    def test_correct_length(self):
        duration = 0.5
        result = synthesize(100.0, duration, seed=42)
        expected_len = int(SAMPLE_RATE * duration)
        # Allow small tolerance for rounding
        self.assertAlmostEqual(len(result), expected_len, delta=10)

    def test_normalized_range(self):
        result = synthesize(150.0, 1.0, seed=42)
        self.assertLessEqual(np.max(np.abs(result)), 1.0)

    def test_not_silent(self):
        result = synthesize(100.0, 0.5, seed=42)
        rms = np.sqrt(np.mean(result ** 2))
        self.assertGreater(rms, 0.01)

    def test_different_seeds_produce_different_output(self):
        a = synthesize(100.0, 0.5, seed=1)
        b = synthesize(100.0, 0.5, seed=2)
        self.assertFalse(np.array_equal(a, b))

    def test_no_seed_produces_different_output(self):
        a = synthesize(100.0, 0.3)
        b = synthesize(100.0, 0.3)
        # Extremely unlikely to be identical with no seed
        self.assertFalse(np.array_equal(a, b))

    def test_same_seed_reproducible(self):
        a = synthesize(100.0, 0.5, seed=99)
        b = synthesize(100.0, 0.5, seed=99)
        np.testing.assert_array_equal(a, b)

    def test_frequency_affects_spectrum(self):
        low = synthesize(80.0, 1.0, seed=10)
        high = synthesize(400.0, 1.0, seed=10)
        # Check that dominant frequency region differs
        fft_low = np.abs(np.fft.rfft(low))
        fft_high = np.abs(np.fft.rfft(high))
        freqs = np.fft.rfftfreq(len(low), 1.0 / SAMPLE_RATE)
        # Spectral centroid should be higher for high-freq sound
        centroid_low = np.sum(freqs * fft_low) / np.sum(fft_low)
        centroid_high = np.sum(freqs * fft_high) / np.sum(fft_high)
        self.assertGreater(centroid_high, centroid_low)

    def test_various_durations(self):
        for dur in [0.1, 0.5, 2.0]:
            result = synthesize(120.0, dur, seed=42)
            expected = int(SAMPLE_RATE * dur)
            self.assertAlmostEqual(len(result), expected, delta=10)

    def test_no_nan_or_inf(self):
        result = synthesize(200.0, 1.0, seed=7)
        self.assertFalse(np.any(np.isnan(result)))
        self.assertFalse(np.any(np.isinf(result)))


if __name__ == "__main__":
    unittest.main()
