"""Tests for assessor module."""

import os
import sys
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from PIL import Image, ImageDraw
from assessor import (
    assess_coverage, assess_value_range, assess_symmetry,
    assess_line_quality, assess_region_count, assess_gradient_smoothness,
    assess_color_diversity, assess_composition, assess_horizontal_zones,
)


def _white_image(w=200, h=150):
    return Image.new("RGB", (w, h), (255, 255, 255))


def _black_image(w=200, h=150):
    return Image.new("RGB", (w, h), (0, 0, 0))


def _line_image(w=200, h=150, y=75, color=(0, 0, 0), width=2):
    img = _white_image(w, h)
    draw = ImageDraw.Draw(img)
    draw.line([(10, y), (190, y)], fill=color, width=width)
    return img


class TestAssessCoverage:
    def test_blank_zero_coverage(self):
        r = assess_coverage(_white_image())
        assert r["score"] < 1.0
        assert r["passed"]  # 0 is within default [0, 100]

    def test_full_coverage(self):
        r = assess_coverage(_black_image())
        assert r["score"] > 99.0

    def test_min_coverage_fail(self):
        r = assess_coverage(_white_image(), min_pct=50.0)
        assert not r["passed"]

    def test_max_coverage_fail(self):
        r = assess_coverage(_black_image(), max_pct=50.0)
        assert not r["passed"]


class TestAssessValueRange:
    def test_blank_no_ink(self):
        r = assess_value_range(_white_image(), min_range=10)
        assert not r["passed"]

    def test_black_image_range(self):
        # Create image with both light and dark areas
        img = _white_image()
        draw = ImageDraw.Draw(img)
        draw.rectangle([(0, 0), (100, 75)], fill=(30, 30, 30))
        draw.rectangle([(0, 75), (100, 150)], fill=(200, 200, 200))
        r = assess_value_range(img, min_range=100)
        assert r["passed"]


class TestAssessSymmetry:
    def test_symmetric_image(self):
        img = _white_image()
        draw = ImageDraw.Draw(img)
        # Draw symmetric shape
        draw.ellipse([(60, 40), (140, 110)], fill=(0, 0, 0))
        r = assess_symmetry(img, threshold=0.8)
        assert r["passed"]
        assert r["score"] > 0.8

    def test_asymmetric_image(self):
        img = _white_image()
        draw = ImageDraw.Draw(img)
        draw.rectangle([(10, 10), (50, 50)], fill=(0, 0, 0))
        r = assess_symmetry(img, threshold=0.8)
        assert not r["passed"]


class TestAssessLineQuality:
    def test_straight_horizontal(self):
        img = _line_image(y=75)
        r = assess_line_quality(img, expected_angle_deg=0, max_deviation_px=3.0)
        assert r["passed"]
        assert r["score"] < 3.0

    def test_no_ink(self):
        r = assess_line_quality(_white_image())
        assert not r["passed"]


class TestAssessRegionCount:
    def test_no_regions(self):
        r = assess_region_count(_white_image(), min_regions=1)
        assert not r["passed"]

    def test_single_region(self):
        img = _white_image()
        draw = ImageDraw.Draw(img)
        draw.ellipse([(50, 50), (100, 100)], fill=(0, 0, 0))
        r = assess_region_count(img, min_regions=1, max_regions=5)
        assert r["passed"]
        assert r["score"] >= 1

    def test_multiple_regions(self):
        img = _white_image()
        draw = ImageDraw.Draw(img)
        draw.ellipse([(10, 10), (40, 40)], fill=(0, 0, 0))
        draw.ellipse([(60, 60), (90, 90)], fill=(0, 0, 0))
        draw.ellipse([(120, 10), (150, 40)], fill=(0, 0, 0))
        r = assess_region_count(img, min_regions=3, max_regions=5)
        assert r["passed"]


class TestAssessGradientSmoothness:
    def test_smooth_gradient(self):
        # Create smooth horizontal gradient
        arr = np.zeros((150, 200, 3), dtype=np.uint8)
        for x in range(200):
            val = int(255 * x / 200)
            arr[:, x] = [val, val, val]
        img = Image.fromarray(arr)
        r = assess_gradient_smoothness(img, max_banding=0.1)
        assert r["passed"]

    def test_sharp_banding(self):
        # Create hard bands
        arr = np.ones((150, 200, 3), dtype=np.uint8) * 255
        for i in range(5):
            y0, y1 = i * 30, i * 30 + 15
            arr[y0:y1, :] = [0, 0, 0]
        img = Image.fromarray(arr)
        r = assess_gradient_smoothness(img, max_banding=0.01)
        assert not r["passed"]


class TestAssessColorDiversity:
    def test_monochrome(self):
        img = _line_image(color=(0, 0, 0))
        r = assess_color_diversity(img, min_colors=1)
        assert r["passed"]
        assert r["score"] >= 1

    def test_multicolor(self):
        img = _white_image()
        draw = ImageDraw.Draw(img)
        draw.rectangle([(10, 10), (60, 60)], fill=(220, 30, 30))  # red
        draw.rectangle([(70, 10), (120, 60)], fill=(30, 30, 200))  # blue
        draw.rectangle([(130, 10), (180, 60)], fill=(30, 150, 30))  # green
        r = assess_color_diversity(img, min_colors=3)
        assert r["passed"]
        assert r["score"] >= 3


class TestAssessComposition:
    def test_centered(self):
        img = _white_image()
        draw = ImageDraw.Draw(img)
        draw.ellipse([(70, 45), (130, 105)], fill=(0, 0, 0))
        r = assess_composition(img, centered=True)
        assert r["passed"]

    def test_not_centered(self):
        img = _white_image()
        draw = ImageDraw.Draw(img)
        draw.rectangle([(10, 10), (60, 60)], fill=(0, 0, 0))
        r = assess_composition(img, centered=False)
        assert r["passed"]


class TestAssessHorizontalZones:
    def test_sky_ground(self):
        arr = np.ones((150, 200, 3), dtype=np.uint8) * 200  # light sky
        arr[75:, :] = [50, 80, 30]  # dark ground
        img = Image.fromarray(arr)
        r = assess_horizontal_zones(img, min_zones=2)
        assert r["passed"]

    def test_uniform(self):
        r = assess_horizontal_zones(_white_image(), min_zones=3)
        assert not r["passed"]
