"""Tests for the converter module."""

import os
import tempfile
import unittest
from converter import svg_to_png


SIMPLE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="0" y="0" width="100" height="100" fill="blue"/>
  <circle cx="50" cy="50" r="30" fill="red"/>
</svg>"""


class TestSvgToPng(unittest.TestCase):
    def test_creates_file(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            output_path = f.name
        try:
            result = svg_to_png(SIMPLE_SVG, output_path)
            self.assertTrue(os.path.exists(output_path))
            self.assertEqual(result, output_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_file_is_png(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            output_path = f.name
        try:
            svg_to_png(SIMPLE_SVG, output_path)
            with open(output_path, "rb") as f:
                header = f.read(8)
            # PNG magic bytes
            self.assertEqual(header[:4], b"\x89PNG")
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_file_has_content(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            output_path = f.name
        try:
            svg_to_png(SIMPLE_SVG, output_path)
            size = os.path.getsize(output_path)
            self.assertGreater(size, 100)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)


if __name__ == "__main__":
    unittest.main()
