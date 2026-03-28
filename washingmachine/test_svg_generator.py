"""Unit tests for svg_generator module."""

import unittest
from svg_generator import generate_washing_machine_svg, refine_svg


class TestGenerateWashingMachineSvg(unittest.TestCase):
    def test_returns_string(self):
        result = generate_washing_machine_svg()
        self.assertIsInstance(result, str)

    def test_valid_svg_structure(self):
        svg = generate_washing_machine_svg()
        self.assertTrue(svg.strip().startswith("<svg"))
        self.assertTrue(svg.strip().endswith("</svg>"))

    def test_contains_viewbox(self):
        svg = generate_washing_machine_svg()
        self.assertIn('viewBox="0 0 800 900"', svg)

    def test_default_dimensions(self):
        svg = generate_washing_machine_svg()
        self.assertIn('width="800"', svg)
        self.assertIn('height="900"', svg)

    def test_custom_dimensions(self):
        svg = generate_washing_machine_svg(600, 700)
        self.assertIn('viewBox="0 0 600 700"', svg)
        self.assertIn('width="600"', svg)
        self.assertIn('height="700"', svg)

    def test_contains_defs_section(self):
        svg = generate_washing_machine_svg()
        self.assertIn("<defs>", svg)
        self.assertIn("</defs>", svg)


class TestRefineSvg(unittest.TestCase):
    def setUp(self):
        self.base_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="800" height="900" viewBox="0 0 800 900"><defs></defs></svg>'

    def test_base_adds_body_shape(self):
        result = refine_svg(self.base_svg, "base")
        self.assertIn("rect", result)

    def test_base_adds_door_circle(self):
        result = refine_svg(self.base_svg, "base")
        self.assertIn("circle", result)

    def test_materials_adds_gradients(self):
        base = refine_svg(self.base_svg, "base")
        result = refine_svg(base, "materials")
        self.assertIn("linearGradient", result)

    def test_materials_adds_radial_gradient(self):
        base = refine_svg(self.base_svg, "base")
        result = refine_svg(base, "materials")
        self.assertIn("radialGradient", result)

    def test_lighting_adds_filter(self):
        base = refine_svg(self.base_svg, "base")
        mats = refine_svg(base, "materials")
        result = refine_svg(mats, "lighting")
        self.assertIn("filter", result)

    def test_details_adds_handle(self):
        base = refine_svg(self.base_svg, "base")
        mats = refine_svg(base, "materials")
        lit = refine_svg(mats, "lighting")
        result = refine_svg(lit, "details")
        self.assertIn("handle", result.lower())

    def test_details_adds_display(self):
        base = refine_svg(self.base_svg, "base")
        mats = refine_svg(base, "materials")
        lit = refine_svg(mats, "lighting")
        result = refine_svg(lit, "details")
        self.assertIn("display", result.lower())

    def test_polish_preserves_existing_elements(self):
        base = refine_svg(self.base_svg, "base")
        mats = refine_svg(base, "materials")
        lit = refine_svg(mats, "lighting")
        det = refine_svg(lit, "details")
        result = refine_svg(det, "polish")
        # Should still have elements from earlier passes
        self.assertIn("rect", result)
        self.assertIn("circle", result)
        self.assertIn("linearGradient", result)

    def test_invalid_pass_raises_value_error(self):
        with self.assertRaises(ValueError):
            refine_svg(self.base_svg, "invalid_pass")

    def test_all_passes_produce_valid_svg(self):
        svg = self.base_svg
        for pass_name in ["base", "materials", "lighting", "details", "polish"]:
            svg = refine_svg(svg, pass_name)
        self.assertTrue(svg.strip().startswith("<svg"))
        self.assertTrue(svg.strip().endswith("</svg>"))


if __name__ == "__main__":
    unittest.main()
