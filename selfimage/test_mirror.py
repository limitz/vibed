"""Tests for the mirror module."""

import unittest
from PIL import Image
from mirror import create_dream_background, draw_mirror_frame, get_mirror_mask


class TestDreamBackground(unittest.TestCase):
    def test_returns_rgba_image(self):
        bg = create_dream_background(400, 600)
        self.assertIsInstance(bg, Image.Image)
        self.assertEqual(bg.mode, "RGBA")
        self.assertEqual(bg.size, (400, 600))

    def test_is_predominantly_dark(self):
        bg = create_dream_background(200, 200)
        pixels = list(bg.getdata())
        avg_brightness = sum(r + g + b for r, g, b, a in pixels) / (len(pixels) * 3)
        self.assertLess(avg_brightness, 60, "Dream background should be dark")

    def test_is_reproducible(self):
        bg1 = create_dream_background(100, 100, seed=42)
        bg2 = create_dream_background(100, 100, seed=42)
        self.assertEqual(list(bg1.getdata()), list(bg2.getdata()))


class TestMirrorFrame(unittest.TestCase):
    def setUp(self):
        self.img = Image.new("RGBA", (400, 600), (10, 5, 20, 255))

    def test_returns_image_and_mask(self):
        result, mask = draw_mirror_frame(self.img, (200, 300), (300, 400))
        self.assertIsInstance(result, Image.Image)
        self.assertIsInstance(mask, Image.Image)

    def test_frame_has_correct_dimensions(self):
        result, mask = draw_mirror_frame(self.img, (200, 300), (300, 400))
        self.assertEqual(result.size, (400, 600))

    def test_frame_adds_color(self):
        result, mask = draw_mirror_frame(self.img, (200, 300), (300, 400))
        # Frame pixels should have gold/amber tones somewhere
        r, g, b, a = result.getpixel((200, 100))  # top of frame area
        # At least some pixels should differ from input
        pixels = list(result.getdata())
        original = list(self.img.getdata())
        changed = sum(1 for p, o in zip(pixels, original) if p != o)
        self.assertGreater(changed, 0, "Frame should modify some pixels")


class TestMirrorMask(unittest.TestCase):
    def test_returns_l_mode_image(self):
        mask = get_mirror_mask((200, 300), (300, 400), (400, 600))
        self.assertIsInstance(mask, Image.Image)
        self.assertEqual(mask.mode, "L")
        self.assertEqual(mask.size, (400, 600))

    def test_center_is_white(self):
        mask = get_mirror_mask((200, 300), (300, 400), (400, 600))
        self.assertEqual(mask.getpixel((200, 300)), 255,
                         "Center of mirror should be white in mask")

    def test_corner_is_black(self):
        mask = get_mirror_mask((200, 300), (300, 400), (400, 600))
        self.assertEqual(mask.getpixel((0, 0)), 0,
                         "Corner outside mirror should be black")


if __name__ == "__main__":
    unittest.main()
