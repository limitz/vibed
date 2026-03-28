"""Tests for the effects module."""

import unittest
from PIL import Image
from effects import (
    draw_glow, draw_nebula, draw_flow_lines,
    draw_particles, draw_text_fragments, draw_mandala,
)


class TestDrawGlow(unittest.TestCase):
    def setUp(self):
        self.img = Image.new("RGBA", (200, 200), (0, 0, 0, 255))

    def test_returns_rgba_image(self):
        result = draw_glow(self.img, (100, 100), 50, (255, 200, 100))
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.mode, "RGBA")

    def test_preserves_dimensions(self):
        result = draw_glow(self.img, (100, 100), 50, (255, 200, 100))
        self.assertEqual(result.size, (200, 200))

    def test_adds_brightness_at_center(self):
        result = draw_glow(self.img, (100, 100), 50, (255, 200, 100))
        r, g, b, a = result.getpixel((100, 100))
        self.assertGreater(r, 0, "Glow should add brightness at center")

    def test_intensity_scales_brightness(self):
        low = draw_glow(self.img, (100, 100), 50, (255, 200, 100), intensity=0.2)
        high = draw_glow(self.img, (100, 100), 50, (255, 200, 100), intensity=1.0)
        r_low = low.getpixel((100, 100))[0]
        r_high = high.getpixel((100, 100))[0]
        self.assertGreater(r_high, r_low)


class TestDrawNebula(unittest.TestCase):
    def setUp(self):
        self.img = Image.new("RGBA", (300, 300), (0, 0, 0, 255))

    def test_returns_rgba_image(self):
        result = draw_nebula(self.img, (50, 50, 250, 250),
                             [(100, 50, 150), (50, 50, 200)])
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.mode, "RGBA")

    def test_is_reproducible_with_seed(self):
        r1 = draw_nebula(self.img.copy(), (50, 50, 250, 250),
                         [(100, 50, 150)], seed=123)
        r2 = draw_nebula(self.img.copy(), (50, 50, 250, 250),
                         [(100, 50, 150)], seed=123)
        self.assertEqual(list(r1.getdata()), list(r2.getdata()))

    def test_adds_color_to_region(self):
        result = draw_nebula(self.img, (50, 50, 250, 250),
                             [(100, 50, 150), (50, 50, 200)])
        # Check center of region has some color
        r, g, b, a = result.getpixel((150, 150))
        self.assertTrue(r > 0 or g > 0 or b > 0,
                        "Nebula should add color within region")


class TestDrawFlowLines(unittest.TestCase):
    def setUp(self):
        self.img = Image.new("RGBA", (400, 400), (0, 0, 0, 255))

    def test_returns_rgba_image(self):
        result = draw_flow_lines(self.img, (200, 200), 20, 150,
                                 (200, 180, 255))
        self.assertIsInstance(result, Image.Image)

    def test_adds_content_near_center(self):
        result = draw_flow_lines(self.img, (200, 200), 30, 150,
                                 (200, 180, 255))
        # Sample a ring around center - at least some pixels should be bright
        bright_count = 0
        for angle_deg in range(0, 360, 10):
            import math
            x = int(200 + 50 * math.cos(math.radians(angle_deg)))
            y = int(200 + 50 * math.sin(math.radians(angle_deg)))
            r, g, b, a = result.getpixel((x, y))
            if r > 10 or g > 10 or b > 10:
                bright_count += 1
        self.assertGreater(bright_count, 0, "Flow lines should be visible")


class TestDrawParticles(unittest.TestCase):
    def setUp(self):
        self.img = Image.new("RGBA", (200, 200), (0, 0, 0, 255))

    def test_returns_rgba_image(self):
        result = draw_particles(self.img, (0, 0, 200, 200), 50,
                                (255, 255, 255))
        self.assertIsInstance(result, Image.Image)

    def test_adds_bright_pixels(self):
        result = draw_particles(self.img, (0, 0, 200, 200), 100,
                                (255, 255, 255))
        pixels = list(result.getdata())
        bright = sum(1 for r, g, b, a in pixels if r > 100)
        self.assertGreater(bright, 0, "Particles should create bright pixels")


class TestDrawTextFragments(unittest.TestCase):
    def setUp(self):
        self.img = Image.new("RGBA", (400, 400), (0, 0, 0, 255))

    def test_returns_rgba_image(self):
        result = draw_text_fragments(
            self.img, ["hello", "world"], (50, 50, 350, 350),
            (200, 200, 255))
        self.assertIsInstance(result, Image.Image)

    def test_adds_visible_content(self):
        result = draw_text_fragments(
            self.img, ["attention", "meaning", "pattern"],
            (50, 50, 350, 350), (200, 200, 255))
        pixels = list(result.getdata())
        non_black = sum(1 for r, g, b, a in pixels if r > 20 or g > 20 or b > 20)
        self.assertGreater(non_black, 0, "Text should be visible")


class TestDrawMandala(unittest.TestCase):
    def setUp(self):
        self.img = Image.new("RGBA", (300, 300), (0, 0, 0, 255))

    def test_returns_rgba_image(self):
        result = draw_mandala(self.img, (150, 150), 80,
                              [(255, 200, 50), (200, 150, 30)])
        self.assertIsInstance(result, Image.Image)

    def test_has_content_at_center(self):
        result = draw_mandala(self.img, (150, 150), 80,
                              [(255, 200, 50), (200, 150, 30)])
        r, g, b, a = result.getpixel((150, 150))
        self.assertTrue(r > 0 or g > 0 or b > 0,
                        "Mandala should have content at center")

    def test_is_reproducible(self):
        r1 = draw_mandala(self.img.copy(), (150, 150), 80,
                          [(255, 200, 50)], seed=99)
        r2 = draw_mandala(self.img.copy(), (150, 150), 80,
                          [(255, 200, 50)], seed=99)
        self.assertEqual(list(r1.getdata()), list(r2.getdata()))


if __name__ == "__main__":
    unittest.main()
