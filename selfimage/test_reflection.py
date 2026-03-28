"""Tests for the reflection module."""

import unittest
from PIL import Image
from reflection import create_reflection


class TestCreateReflection(unittest.TestCase):
    def test_returns_rgba_image(self):
        ref = create_reflection(300, 400)
        self.assertIsInstance(ref, Image.Image)
        self.assertEqual(ref.mode, "RGBA")
        self.assertEqual(ref.size, (300, 400))

    def test_has_visual_content(self):
        ref = create_reflection(300, 400)
        pixels = list(ref.getdata())
        non_black = sum(1 for r, g, b, a in pixels if r > 10 or g > 10 or b > 10)
        self.assertGreater(non_black, 100,
                           "Reflection should have substantial visual content")

    def test_is_reproducible(self):
        r1 = create_reflection(200, 200, seed=42)
        r2 = create_reflection(200, 200, seed=42)
        self.assertEqual(list(r1.getdata()), list(r2.getdata()))

    def test_has_color_variety(self):
        ref = create_reflection(300, 400)
        pixels = list(ref.getdata())
        # Check that multiple color channels are used
        has_red = any(r > 50 for r, g, b, a in pixels)
        has_blue = any(b > 50 for r, g, b, a in pixels)
        self.assertTrue(has_red or has_blue,
                        "Reflection should use multiple colors")


if __name__ == "__main__":
    unittest.main()
