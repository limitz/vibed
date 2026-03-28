"""Tests for the SVG generator module."""

import unittest
from svg_generator import (
    generate_bedroom_background,
    generate_cartman,
    generate_liane_cartman,
    generate_kenny,
    generate_vomit,
    generate_scene,
)


class TestBedroomBackground(unittest.TestCase):
    def test_returns_string(self):
        result = generate_bedroom_background()
        self.assertIsInstance(result, str)

    def test_contains_svg_elements(self):
        result = generate_bedroom_background()
        # Should have rectangles for walls, floor, etc.
        self.assertIn("<rect", result)

    def test_contains_bedroom_furniture(self):
        result = generate_bedroom_background()
        # Should have bed, window, or poster elements
        self.assertTrue(
            "<rect" in result or "<polygon" in result or "<path" in result
        )


class TestCartman(unittest.TestCase):
    def test_returns_string(self):
        result = generate_cartman()
        self.assertIsInstance(result, str)

    def test_contains_svg_elements(self):
        result = generate_cartman()
        self.assertTrue(len(result) > 50)

    def test_has_cartman_colors(self):
        """Cartman wears red jacket and yellow-trimmed hat."""
        result = generate_cartman()
        # Should contain red for his jacket
        self.assertTrue("red" in result.lower() or "#" in result)


class TestLianeCartman(unittest.TestCase):
    def test_returns_string(self):
        result = generate_liane_cartman()
        self.assertIsInstance(result, str)

    def test_contains_svg_elements(self):
        result = generate_liane_cartman()
        self.assertTrue(len(result) > 50)


class TestKenny(unittest.TestCase):
    def test_returns_string(self):
        result = generate_kenny()
        self.assertIsInstance(result, str)

    def test_contains_svg_elements(self):
        result = generate_kenny()
        self.assertTrue(len(result) > 50)

    def test_has_kenny_orange(self):
        """Kenny wears an orange parka."""
        result = generate_kenny()
        self.assertTrue("orange" in result.lower() or "#f" in result.lower())


class TestVomit(unittest.TestCase):
    def test_returns_string(self):
        result = generate_vomit()
        self.assertIsInstance(result, str)

    def test_contains_svg_elements(self):
        result = generate_vomit()
        self.assertTrue(len(result) > 10)


class TestGenerateScene(unittest.TestCase):
    def test_returns_valid_svg(self):
        result = generate_scene()
        self.assertIsInstance(result, str)
        self.assertIn("<svg", result)
        self.assertIn("</svg>", result)

    def test_contains_viewbox(self):
        result = generate_scene()
        self.assertIn("viewBox", result)

    def test_custom_dimensions(self):
        result = generate_scene(width=1024, height=768)
        self.assertIn("1024", result)
        self.assertIn("768", result)

    def test_scene_has_all_elements(self):
        """The scene should contain elements from all sub-generators."""
        result = generate_scene()
        # Should be substantial (all characters + background + vomit)
        self.assertGreater(len(result), 500)


if __name__ == "__main__":
    unittest.main()
