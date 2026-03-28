"""Unit tests for converter module."""

import os
import tempfile
import unittest
from PIL import Image
from converter import svg_to_jpeg, svg_to_png


SIMPLE_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
  <rect width="100" height="100" fill="white"/>
  <circle cx="50" cy="50" r="40" fill="blue"/>
</svg>'''


class TestSvgToJpeg(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def test_creates_file(self):
        path = os.path.join(self.tmpdir, "test.jpeg")
        svg_to_jpeg(SIMPLE_SVG, path)
        self.assertTrue(os.path.exists(path))
        self.assertGreater(os.path.getsize(path), 0)

    def test_returns_path(self):
        path = os.path.join(self.tmpdir, "test.jpeg")
        result = svg_to_jpeg(SIMPLE_SVG, path)
        self.assertEqual(result, path)

    def test_output_is_valid_jpeg(self):
        path = os.path.join(self.tmpdir, "test.jpeg")
        svg_to_jpeg(SIMPLE_SVG, path)
        img = Image.open(path)
        self.assertEqual(img.format, "JPEG")

    def test_rgb_no_alpha(self):
        path = os.path.join(self.tmpdir, "test.jpeg")
        svg_to_jpeg(SIMPLE_SVG, path)
        img = Image.open(path)
        self.assertEqual(img.mode, "RGB")

    def test_quality_affects_size(self):
        path_high = os.path.join(self.tmpdir, "high.jpeg")
        path_low = os.path.join(self.tmpdir, "low.jpeg")
        svg_to_jpeg(SIMPLE_SVG, path_high, quality=95)
        svg_to_jpeg(SIMPLE_SVG, path_low, quality=10)
        self.assertGreater(os.path.getsize(path_high), os.path.getsize(path_low))


class TestSvgToPng(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def test_creates_file(self):
        path = os.path.join(self.tmpdir, "test.png")
        svg_to_png(SIMPLE_SVG, path)
        self.assertTrue(os.path.exists(path))
        self.assertGreater(os.path.getsize(path), 0)

    def test_returns_path(self):
        path = os.path.join(self.tmpdir, "test.png")
        result = svg_to_png(SIMPLE_SVG, path)
        self.assertEqual(result, path)

    def test_scale_factor(self):
        path = os.path.join(self.tmpdir, "test.png")
        svg_to_png(SIMPLE_SVG, path, scale=2.0)
        img = Image.open(path)
        self.assertEqual(img.width, 200)
        self.assertEqual(img.height, 200)


if __name__ == "__main__":
    unittest.main()
