"""Tests for the Happy Birthday melody module."""

import unittest
from melody import happy_birthday


class TestHappyBirthday(unittest.TestCase):
    def test_returns_list(self):
        result = happy_birthday()
        self.assertIsInstance(result, list)

    def test_returns_tuples(self):
        result = happy_birthday()
        for item in result:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 2)

    def test_frequencies_are_positive_or_zero(self):
        result = happy_birthday()
        for freq, dur in result:
            self.assertGreaterEqual(freq, 0)

    def test_durations_are_positive(self):
        result = happy_birthday()
        for freq, dur in result:
            self.assertGreater(dur, 0)

    def test_has_enough_notes(self):
        result = happy_birthday()
        # Happy Birthday has 25 notes
        self.assertGreaterEqual(len(result), 20)

    def test_tempo_affects_duration(self):
        slow = happy_birthday(tempo_bpm=60.0)
        fast = happy_birthday(tempo_bpm=120.0)
        total_slow = sum(d for _, d in slow)
        total_fast = sum(d for _, d in fast)
        self.assertGreater(total_slow, total_fast)

    def test_octave_affects_frequency(self):
        low = happy_birthday(base_octave=3)
        high = happy_birthday(base_octave=5)
        # Compare first non-rest note
        freq_low = next(f for f, _ in low if f > 0)
        freq_high = next(f for f, _ in high if f > 0)
        self.assertGreater(freq_high, freq_low)

    def test_contains_expected_frequency_range(self):
        notes = happy_birthday(base_octave=4)
        freqs = [f for f, _ in notes if f > 0]
        # Should be roughly in the C4-C5 range (261-523 Hz)
        self.assertTrue(any(200 < f < 600 for f in freqs))


if __name__ == "__main__":
    unittest.main()
