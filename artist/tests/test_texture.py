"""Tests for texture module."""

import os
import sys
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from texture import pencil_grain, paper_texture, brush_bristle_pattern, charcoal_noise


class TestPencilGrain:
    def test_shape(self):
        result = pencil_grain(100, 80)
        assert result.shape == (80, 100)

    def test_value_range(self):
        result = pencil_grain(50, 50, intensity=0.8)
        assert result.min() >= 0.0
        assert result.max() <= 1.0

    def test_seed_reproducibility(self):
        a = pencil_grain(50, 50, seed=42)
        b = pencil_grain(50, 50, seed=42)
        np.testing.assert_array_equal(a, b)

    def test_different_seeds_differ(self):
        a = pencil_grain(50, 50, seed=1)
        b = pencil_grain(50, 50, seed=2)
        assert not np.array_equal(a, b)

    def test_intensity_effect(self):
        low = pencil_grain(50, 50, intensity=0.1, seed=0)
        high = pencil_grain(50, 50, intensity=0.9, seed=0)
        # Higher intensity = more variation (lower minimum values)
        assert low.min() > high.min()


class TestPaperTexture:
    def test_shape(self):
        result = paper_texture(120, 90)
        assert result.shape == (90, 120)

    def test_value_range(self):
        result = paper_texture(50, 50)
        assert result.min() >= 0.0
        assert result.max() <= 1.0

    def test_mostly_flat(self):
        result = paper_texture(100, 100)
        # Paper should be mostly near 1.0 (white)
        assert result.mean() > 0.95

    def test_seed_reproducibility(self):
        a = paper_texture(50, 50, seed=7)
        b = paper_texture(50, 50, seed=7)
        np.testing.assert_array_equal(a, b)


class TestBrushBristlePattern:
    def test_shape(self):
        result = brush_bristle_pattern(64)
        assert result.shape == (64,)

    def test_value_range(self):
        result = brush_bristle_pattern(64)
        assert result.min() >= 0.0
        assert result.max() <= 1.0

    def test_seed_reproducibility(self):
        a = brush_bristle_pattern(64, seed=10)
        b = brush_bristle_pattern(64, seed=10)
        np.testing.assert_array_equal(a, b)

    def test_has_variation(self):
        result = brush_bristle_pattern(64, seed=5)
        assert result.std() > 0.01


class TestCharcoalNoise:
    def test_shape(self):
        result = charcoal_noise(80, 60)
        assert result.shape == (60, 80)

    def test_value_range(self):
        result = charcoal_noise(50, 50, intensity=0.7)
        assert result.min() >= 0.0
        assert result.max() <= 1.0

    def test_seed_reproducibility(self):
        a = charcoal_noise(50, 50, seed=99)
        b = charcoal_noise(50, 50, seed=99)
        np.testing.assert_array_equal(a, b)

    def test_different_from_pencil(self):
        # Charcoal and pencil should produce visually different textures
        pencil = pencil_grain(100, 100, intensity=0.5, seed=0)
        charcoal = charcoal_noise(100, 100, intensity=0.5, seed=0)
        assert not np.allclose(pencil, charcoal, atol=0.01)
