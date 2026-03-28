"""Tests for student module."""

import os
import sys
import math
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from student import (
    draw_line, draw_curve, draw_circle, draw_rectangle,
    draw_hatching, draw_crosshatching, draw_pressure_ramp,
    draw_ellipse, draw_arc, draw_s_curve, draw_triangle,
    draw_filled_circle, draw_gradient_fill, take_lesson,
)
from stylus_format import Stroke


class TestDrawLine:
    def test_returns_stroke(self):
        s = draw_line(0, 0, 100, 0)
        assert isinstance(s, Stroke)
        assert len(s.events) > 0

    def test_correct_event_count(self):
        s = draw_line(0, 0, 100, 0, num_events=10)
        assert len(s.events) == 10

    def test_endpoints_near_targets(self):
        s = draw_line(10, 20, 200, 300, num_events=20)
        assert abs(s.events[0].x - 10) < 2
        assert abs(s.events[0].y - 20) < 2
        assert abs(s.events[-1].x - 200) < 2
        assert abs(s.events[-1].y - 300) < 2

    def test_pressure_curve(self):
        pressures = [0.1, 0.5, 0.9, 0.5, 0.1]
        s = draw_line(0, 0, 100, 0, num_events=5, pressure_curve=pressures)
        assert abs(s.events[0].pressure - 0.1) < 0.01
        assert abs(s.events[2].pressure - 0.9) < 0.01

    def test_tool_preserved(self):
        s = draw_line(0, 0, 100, 0, tool="brush")
        for e in s.events:
            assert e.tool == "brush"


class TestDrawCircle:
    def test_returns_stroke(self):
        s = draw_circle(100, 100, 50)
        assert isinstance(s, Stroke)

    def test_closed(self):
        s = draw_circle(100, 100, 50, num_events=30)
        # First and last points should be near each other
        d = math.sqrt((s.events[0].x - s.events[-1].x) ** 2 +
                      (s.events[0].y - s.events[-1].y) ** 2)
        assert d < 5  # Within 5 pixels

    def test_radius_approximate(self):
        cx, cy, r = 200, 150, 60
        s = draw_circle(cx, cy, r, num_events=40)
        for e in s.events:
            dist = math.sqrt((e.x - cx) ** 2 + (e.y - cy) ** 2)
            assert abs(dist - r) < 3  # Within 3 pixels of expected radius


class TestDrawRectangle:
    def test_returns_stroke(self):
        s = draw_rectangle(10, 20, 100, 80)
        assert isinstance(s, Stroke)
        assert len(s.events) > 0

    def test_has_corners(self):
        s = draw_rectangle(0, 0, 100, 50, num_events_per_side=10)
        xs = [e.x for e in s.events]
        ys = [e.y for e in s.events]
        # Should span the rectangle area approximately
        assert max(xs) > 95
        assert max(ys) > 45


class TestDrawHatching:
    def test_returns_list_of_strokes(self):
        result = draw_hatching(0, 0, 200, 200, spacing=10)
        assert isinstance(result, list)
        assert len(result) > 0
        for s in result:
            assert isinstance(s, Stroke)

    def test_more_lines_with_smaller_spacing(self):
        wide = draw_hatching(0, 0, 200, 200, spacing=20)
        narrow = draw_hatching(0, 0, 200, 200, spacing=5)
        assert len(narrow) > len(wide)


class TestDrawCrosshatching:
    def test_more_strokes_than_single_hatching(self):
        single = draw_hatching(0, 0, 200, 200, angle_deg=45, spacing=10)
        cross = draw_crosshatching(0, 0, 200, 200, spacing=10)
        assert len(cross) > len(single)


class TestPressureRamp:
    def test_pressure_varies(self):
        s = draw_pressure_ramp(0, 0, 200, 0, num_events=20)
        pressures = [e.pressure for e in s.events]
        assert max(pressures) > 0.5
        assert min(pressures) < 0.3
        # Should peak in the middle
        mid = len(pressures) // 2
        assert pressures[mid] > pressures[0]
        assert pressures[mid] > pressures[-1]


class TestTakeLesson:
    def test_all_lessons_produce_drawings(self):
        for i in range(1, 21):
            d = take_lesson(i, 400, 300)
            assert d.width == 400
            assert d.height == 300
            assert len(d.strokes) > 0

    def test_invalid_lesson_raises(self):
        with pytest.raises(ValueError):
            take_lesson(99, 400, 300)

    def test_portrait_lessons_use_custom_canvas(self):
        # Lessons 16-18 should work with portrait dimensions
        for i in [16, 17, 18]:
            d = take_lesson(i, 600, 800)
            assert d.width == 600
            assert len(d.strokes) > 0
