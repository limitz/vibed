"""Tests for the speech renderer."""

import unittest
import numpy as np
from speakup.speech import render_phoneme, interpolate_phonemes, render_utterance, apply_intonation
from speakup.phonemes import PHONEMES


SAMPLE_RATE = 44100


class TestRenderPhoneme(unittest.TestCase):
    def test_output_length(self):
        spec = PHONEMES["AH"]
        duration = 0.15
        result = render_phoneme(spec, duration, 120.0, SAMPLE_RATE)
        expected = int(duration * SAMPLE_RATE)
        self.assertEqual(len(result), expected)

    def test_vowel_not_silent(self):
        spec = PHONEMES["AH"]
        result = render_phoneme(spec, 0.15, 120.0, SAMPLE_RATE)
        self.assertGreater(np.max(np.abs(result)), 0.01)

    def test_silence_is_silent(self):
        spec = PHONEMES["SIL"]
        result = render_phoneme(spec, 0.05, 0.0, SAMPLE_RATE)
        self.assertAlmostEqual(np.max(np.abs(result)), 0.0, places=5)

    def test_fricative_not_silent(self):
        spec = PHONEMES["S"]
        result = render_phoneme(spec, 0.1, 0.0, SAMPLE_RATE)
        self.assertGreater(np.max(np.abs(result)), 0.01)

    def test_plosive_not_silent(self):
        spec = PHONEMES["T"]
        result = render_phoneme(spec, 0.06, 0.0, SAMPLE_RATE)
        self.assertGreater(np.max(np.abs(result)), 0.01)


class TestInterpolatePhonemes(unittest.TestCase):
    def test_output_length(self):
        a = PHONEMES["AH"]
        b = PHONEMES["EE"]
        duration = 0.03
        result = interpolate_phonemes(a, b, duration, 120.0, SAMPLE_RATE)
        expected = int(duration * SAMPLE_RATE)
        self.assertEqual(len(result), expected)

    def test_not_silent(self):
        a = PHONEMES["AH"]
        b = PHONEMES["EE"]
        result = interpolate_phonemes(a, b, 0.03, 120.0, SAMPLE_RATE)
        self.assertGreater(np.max(np.abs(result)), 0.01)


class TestRenderUtterance(unittest.TestCase):
    def test_produces_audio(self):
        result = render_utterance(["AH", "EE", "OH"], SAMPLE_RATE)
        self.assertGreater(len(result), 0)
        self.assertGreater(np.max(np.abs(result)), 0.01)

    def test_single_phoneme(self):
        result = render_utterance(["AH"], SAMPLE_RATE)
        self.assertGreater(len(result), 0)

    def test_with_silence(self):
        result = render_utterance(["AH", "SIL", "EE"], SAMPLE_RATE)
        self.assertGreater(len(result), 0)

    def test_speed_affects_length(self):
        slow = render_utterance(["AH", "EE"], SAMPLE_RATE, speed=0.5)
        fast = render_utterance(["AH", "EE"], SAMPLE_RATE, speed=2.0)
        self.assertGreater(len(slow), len(fast))


class TestApplyIntonation(unittest.TestCase):
    def test_length_matches(self):
        phonemes = ["AH", "EE", "OH"]
        result = apply_intonation(phonemes, 120.0)
        self.assertEqual(len(result), len(phonemes))

    def test_values_near_base(self):
        phonemes = ["AH", "EE", "OH", "OO"]
        result = apply_intonation(phonemes, 120.0)
        for f0 in result:
            self.assertGreater(f0, 80.0)
            self.assertLess(f0, 180.0)

    def test_not_all_same(self):
        phonemes = ["AH", "EE", "OH", "OO", "UH"]
        result = apply_intonation(phonemes, 120.0)
        self.assertFalse(all(f == result[0] for f in result))


if __name__ == "__main__":
    unittest.main()
