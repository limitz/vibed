"""Integration tests — end-to-end pipeline."""

import os
import unittest
import tempfile
import numpy as np
from speakup.text_to_phoneme import text_to_phonemes
from speakup.speech import render_utterance
from speakup.exporter import normalize, save_wav


SAMPLE_RATE = 44100


class TestEndToEnd(unittest.TestCase):
    def test_text_to_audio(self):
        phonemes = text_to_phonemes("hello")
        audio = render_utterance(phonemes, SAMPLE_RATE)
        self.assertGreater(len(audio), 0)
        self.assertGreater(np.max(np.abs(audio)), 0.01)

    def test_text_to_wav_file(self):
        phonemes = text_to_phonemes("hello world")
        audio = render_utterance(phonemes, SAMPLE_RATE)
        audio = normalize(audio)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            filepath = f.name
        try:
            save_wav(audio, filepath, SAMPLE_RATE)
            self.assertTrue(os.path.exists(filepath))
            self.assertGreater(os.path.getsize(filepath), 100)
        finally:
            os.unlink(filepath)

    def test_sentence_pipeline(self):
        text = "I am learning to speak"
        phonemes = text_to_phonemes(text)
        self.assertGreater(len(phonemes), 5)
        audio = render_utterance(phonemes, SAMPLE_RATE)
        self.assertGreater(len(audio), SAMPLE_RATE * 0.3)  # at least 0.3s
        audio = normalize(audio)
        self.assertLessEqual(np.max(np.abs(audio)), 1.0)

    def test_the_prompt(self):
        text = "Using only FM synthesis learn how to speak"
        phonemes = text_to_phonemes(text)
        audio = render_utterance(phonemes, SAMPLE_RATE, f0_base=115.0, speed=0.7)
        audio = normalize(audio)
        self.assertGreater(len(audio), SAMPLE_RATE * 0.5)


if __name__ == "__main__":
    unittest.main()
