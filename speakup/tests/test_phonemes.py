"""Tests for phoneme definitions."""

import unittest
from speakup.phonemes import PHONEMES, PhonemeSpec, FormantSpec


class TestPhonemeInventory(unittest.TestCase):
    def test_phonemes_not_empty(self):
        self.assertGreater(len(PHONEMES), 0)

    def test_has_basic_vowels(self):
        for vowel in ["AH", "EE", "EH", "OH", "OO"]:
            self.assertIn(vowel, PHONEMES, f"Missing vowel {vowel}")

    def test_has_basic_consonants(self):
        for cons in ["S", "T", "P", "M", "N", "L", "R"]:
            self.assertIn(cons, PHONEMES, f"Missing consonant {cons}")

    def test_has_silence(self):
        self.assertIn("SIL", PHONEMES)

    def test_vowels_have_formants(self):
        vowels = [p for p in PHONEMES.values() if p.voiced and not p.is_plosive
                  and p.noise_level < 0.3 and p.name != "SIL"]
        for v in vowels:
            self.assertGreaterEqual(len(v.formants), 3,
                                   f"Vowel {v.name} needs at least 3 formants")

    def test_voiced_phonemes_have_f0(self):
        for name, spec in PHONEMES.items():
            if spec.voiced and name != "SIL":
                self.assertGreater(spec.f0, 0, f"{name} is voiced but f0=0")

    def test_plosives_have_burst_freq(self):
        plosives = [p for p in PHONEMES.values() if p.is_plosive]
        self.assertGreater(len(plosives), 0, "No plosives defined")
        for p in plosives:
            self.assertGreater(p.plosive_burst_freq, 0,
                               f"Plosive {p.name} missing burst frequency")

    def test_formant_frequencies_positive(self):
        for name, spec in PHONEMES.items():
            for f in spec.formants:
                self.assertGreater(f.frequency, 0,
                                   f"{name} has non-positive formant freq")

    def test_formant_amplitudes_valid(self):
        for name, spec in PHONEMES.items():
            for f in spec.formants:
                self.assertGreaterEqual(f.amplitude, 0.0)
                self.assertLessEqual(f.amplitude, 1.0,
                                     f"{name} formant amplitude > 1")

    def test_durations_positive(self):
        for name, spec in PHONEMES.items():
            self.assertGreater(spec.duration, 0, f"{name} has zero duration")

    def test_noise_level_range(self):
        for name, spec in PHONEMES.items():
            self.assertGreaterEqual(spec.noise_level, 0.0)
            self.assertLessEqual(spec.noise_level, 1.0)

    def test_fricatives_have_noise(self):
        fricatives = ["S", "SH", "F"]
        for name in fricatives:
            if name in PHONEMES:
                self.assertGreater(PHONEMES[name].noise_level, 0.3,
                                   f"Fricative {name} should have noise")


class TestPhonemeSpec(unittest.TestCase):
    def test_create_phoneme(self):
        spec = PhonemeSpec(
            name="TEST",
            formants=[FormantSpec(500, 1.0, 80)],
            f0=120.0,
            voiced=True,
        )
        self.assertEqual(spec.name, "TEST")
        self.assertEqual(len(spec.formants), 1)


if __name__ == "__main__":
    unittest.main()
