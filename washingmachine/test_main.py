"""Unit tests for main module."""

import os
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image

from main import main


class TestMain(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.orig_dir = os.getcwd()
        os.chdir(self.tmpdir)

    def tearDown(self):
        os.chdir(self.orig_dir)

    def test_produces_jpeg(self):
        main()
        self.assertTrue(os.path.exists("washing_machine.jpeg"))
        self.assertGreater(os.path.getsize("washing_machine.jpeg"), 0)

    def test_produces_svg(self):
        main()
        self.assertTrue(os.path.exists("washing_machine.svg"))

    def test_jpeg_dimensions(self):
        main()
        img = Image.open("washing_machine.jpeg")
        self.assertGreaterEqual(img.width, 800)
        self.assertGreaterEqual(img.height, 900)

    def test_jpeg_is_valid(self):
        main()
        img = Image.open("washing_machine.jpeg")
        self.assertEqual(img.format, "JPEG")
        self.assertEqual(img.mode, "RGB")


if __name__ == "__main__":
    unittest.main()
