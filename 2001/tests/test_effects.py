"""Tests for effects module: procedural visual effects."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from effects import (
    star_field, fade_in, fade_out, dissolve_transition,
    speed_lines, tunnel_effect, draw_circle, draw_filled_circle,
    wave_pattern, hash_float
)
from renderer import ScreenBuffer, Color


class TestHashFloat:
    def test_returns_float_in_range(self):
        v = hash_float(42, 0)
        assert 0.0 <= v < 1.0

    def test_deterministic(self):
        v1 = hash_float(42, 5)
        v2 = hash_float(42, 5)
        assert v1 == v2

    def test_different_seeds(self):
        v1 = hash_float(42, 0)
        v2 = hash_float(43, 0)
        assert v1 != v2


class TestStarField:
    def test_draws_stars(self):
        buf = ScreenBuffer(80, 24)
        star_field(buf, 0.5)
        non_empty = sum(
            1 for y in range(24) for x in range(80)
            if buf.get_cell(x, y).char != ' '
        )
        assert non_empty > 0

    def test_deterministic(self):
        buf1 = ScreenBuffer(80, 24)
        buf2 = ScreenBuffer(80, 24)
        star_field(buf1, 0.5, seed=42)
        star_field(buf2, 0.5, seed=42)
        for y in range(24):
            for x in range(80):
                assert buf1.get_cell(x, y).char == buf2.get_cell(x, y).char


class TestFade:
    def test_fade_in_at_zero(self):
        buf = ScreenBuffer(10, 5)
        alpha = fade_in(buf, 0.0)
        assert alpha == 0.0

    def test_fade_in_past_threshold(self):
        buf = ScreenBuffer(10, 5)
        alpha = fade_in(buf, 0.5)
        assert alpha == 1.0

    def test_fade_in_at_threshold(self):
        buf = ScreenBuffer(10, 5)
        alpha = fade_in(buf, 0.2)
        assert alpha == 1.0

    def test_fade_in_midway(self):
        buf = ScreenBuffer(10, 5)
        alpha = fade_in(buf, 0.1, threshold=0.2)
        assert 0.0 < alpha < 1.0

    def test_fade_out_at_end(self):
        buf = ScreenBuffer(10, 5)
        alpha = fade_out(buf, 1.0)
        assert alpha == 0.0

    def test_fade_out_before_threshold(self):
        buf = ScreenBuffer(10, 5)
        alpha = fade_out(buf, 0.5)
        assert alpha == 1.0

    def test_fade_out_midway(self):
        buf = ScreenBuffer(10, 5)
        alpha = fade_out(buf, 0.9, threshold=0.8)
        assert 0.0 < alpha < 1.0


class TestDissolve:
    def test_dissolve_fills_some_cells(self):
        buf = ScreenBuffer(40, 12)
        dissolve_transition(buf, 0.5)
        non_empty = sum(
            1 for y in range(12) for x in range(40)
            if buf.get_cell(x, y).char != ' '
        )
        assert non_empty > 0


class TestSpeedLines:
    def test_draws_lines(self):
        buf = ScreenBuffer(80, 24)
        speed_lines(buf, 0.5)
        non_empty = sum(
            1 for y in range(24) for x in range(80)
            if buf.get_cell(x, y).char != ' '
        )
        assert non_empty > 0


class TestTunnelEffect:
    def test_draws_rectangles(self):
        buf = ScreenBuffer(80, 24)
        tunnel_effect(buf, 0.5)
        non_empty = sum(
            1 for y in range(24) for x in range(80)
            if buf.get_cell(x, y).char != ' '
        )
        assert non_empty > 0


class TestCircle:
    def test_draw_circle(self):
        buf = ScreenBuffer(40, 20)
        draw_circle(buf, 20, 10, 5, '*', Color.WHITE, Color.BLACK)
        non_empty = sum(
            1 for y in range(20) for x in range(40)
            if buf.get_cell(x, y).char == '*'
        )
        assert non_empty > 0

    def test_draw_filled_circle(self):
        buf = ScreenBuffer(40, 20)
        draw_filled_circle(buf, 20, 10, 5, '#', Color.RED, Color.BLACK)
        non_empty = sum(
            1 for y in range(20) for x in range(40)
            if buf.get_cell(x, y).char == '#'
        )
        assert non_empty > 10  # filled should have more cells


class TestWavePattern:
    def test_draws_pattern(self):
        buf = ScreenBuffer(80, 24)
        wave_pattern(buf, 0.5)
        non_empty = sum(
            1 for y in range(24) for x in range(80)
            if buf.get_cell(x, y).char != ' '
        )
        assert non_empty > 0
