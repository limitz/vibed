"""Tests for text-to-phoneme conversion."""

import unittest
from speakup.text_to_phoneme import text_to_phonemes, word_to_phonemes
from speakup.phonemes import PHONEMES


class TestWordToPhonemes(unittest.TestCase):
    def test_known_word_hello(self):
        result = word_to_phonemes("hello")
        self.assertEqual(result, ["HH", "EH", "L", "OH"])

    def test_known_word_world(self):
        result = word_to_phonemes("world")
        self.assertEqual(result, ["W", "ER", "L", "D"])

    def test_case_insensitive(self):
        self.assertEqual(word_to_phonemes("Hello"), word_to_phonemes("hello"))

    def test_returns_valid_phonemes(self):
        result = word_to_phonemes("speak")
        for phoneme in result:
            self.assertIn(phoneme, PHONEMES, f"Invalid phoneme: {phoneme}")

    def test_unknown_word_fallback(self):
        result = word_to_phonemes("xyz")
        self.assertGreater(len(result), 0, "Should produce phonemes for unknown words")
        for phoneme in result:
            self.assertIn(phoneme, PHONEMES, f"Invalid phoneme: {phoneme}")


class TestTextToPhonemes(unittest.TestCase):
    def test_single_word(self):
        result = text_to_phonemes("hello")
        self.assertGreater(len(result), 0)

    def test_multiple_words_have_silence(self):
        result = text_to_phonemes("hello world")
        self.assertIn("SIL", result, "Words should be separated by silence")

    def test_all_phonemes_valid(self):
        result = text_to_phonemes("I am learning to speak")
        for phoneme in result:
            self.assertIn(phoneme, PHONEMES, f"Invalid phoneme: {phoneme}")

    def test_empty_string(self):
        result = text_to_phonemes("")
        self.assertEqual(result, [])

    def test_punctuation_stripped(self):
        result = text_to_phonemes("hello!")
        for phoneme in result:
            self.assertIn(phoneme, PHONEMES)

    def test_sentence(self):
        result = text_to_phonemes("Hello world.")
        self.assertGreater(len(result), 3)


if __name__ == "__main__":
    unittest.main()
