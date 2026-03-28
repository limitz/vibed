"""Tests for the main composition module."""

import unittest
from PIL import Image
from main import compose, refine


class TestCompose(unittest.TestCase):
    def test_returns_rgba_image(self):
        result = compose(400, 600)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.mode, "RGBA")
        self.assertEqual(result.size, (400, 600))

    def test_has_visual_content(self):
        result = compose(400, 600)
        pixels = list(result.getdata())
        non_black = sum(1 for r, g, b, a in pixels if r > 10 or g > 10 or b > 10)
        total = len(pixels)
        self.assertGreater(non_black / total, 0.05,
                           "Composed image should have significant content")


class TestRefine(unittest.TestCase):
    def test_returns_rgba_image(self):
        img = Image.new("RGBA", (200, 200), (50, 30, 80, 255))
        result = refine(img, iteration=0)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.mode, "RGBA")

    def test_modifies_image(self):
        img = Image.new("RGBA", (200, 200), (50, 30, 80, 255))
        result = refine(img, iteration=0)
        original_pixels = list(img.getdata())
        refined_pixels = list(result.getdata())
        changed = sum(1 for p, o in zip(refined_pixels, original_pixels) if p != o)
        self.assertGreater(changed, 0, "Refinement should modify the image")


if __name__ == "__main__":
    unittest.main()
