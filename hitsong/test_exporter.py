"""Tests for exporter module."""

import unittest
import os
import tempfile
import numpy as np
from exporter import export_wav, export_mp3


class TestExportWav(unittest.TestCase):
    def test_creates_file(self):
        audio = np.sin(np.linspace(0, 440 * 2 * np.pi, 44100)).astype(np.float64)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            fname = f.name
        try:
            result = export_wav(audio, fname, 44100)
            self.assertTrue(os.path.exists(result))
            self.assertGreater(os.path.getsize(result), 0)
        finally:
            if os.path.exists(fname):
                os.unlink(fname)

    def test_returns_filename(self):
        audio = np.sin(np.linspace(0, 440 * 2 * np.pi, 44100)).astype(np.float64)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            fname = f.name
        try:
            result = export_wav(audio, fname, 44100)
            self.assertEqual(result, fname)
        finally:
            if os.path.exists(fname):
                os.unlink(fname)


class TestExportMp3(unittest.TestCase):
    def test_creates_file(self):
        audio = np.sin(np.linspace(0, 440 * 2 * np.pi, 44100)).astype(np.float64)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            fname = f.name
        try:
            result = export_mp3(audio, fname, 44100)
            self.assertTrue(os.path.exists(result))
            self.assertGreater(os.path.getsize(result), 0)
        finally:
            if os.path.exists(fname):
                os.unlink(fname)
            # Clean up intermediate wav
            wav_name = fname.replace(".mp3", ".wav")
            if os.path.exists(wav_name):
                os.unlink(wav_name)


if __name__ == "__main__":
    unittest.main()
