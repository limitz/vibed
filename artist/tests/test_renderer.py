"""Tests for renderer module."""

import os
import sys
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from PIL import Image
from stylus_format import StylusEvent, Stroke, Drawing
from renderer import render_drawing, render_stroke, interpolate_events
from tool_profiles import get_profile


class TestRenderDrawing:
    def test_blank_drawing_is_white(self):
        d = Drawing(width=100, height=80, strokes=[])
        img = render_drawing(d, apply_paper=False)
        assert img.size == (100, 80)
        arr = np.array(img)
        # Should be white (255, 255, 255, 255) everywhere
        assert arr[:, :, 0].mean() == 255
        assert arr[:, :, 1].mean() == 255
        assert arr[:, :, 2].mean() == 255

    def test_pen_stroke_creates_pixels(self):
        events = [
            StylusEvent(x=20, y=40, pressure=0.8, tool="pen"),
            StylusEvent(x=80, y=40, pressure=0.8, tool="pen"),
        ]
        stroke = Stroke(events=events)
        d = Drawing(width=100, height=80, strokes=[stroke])
        img = render_drawing(d, apply_paper=False)
        arr = np.array(img)
        # Should have some non-white pixels
        non_white = (arr[:, :, 0] < 250) | (arr[:, :, 1] < 250) | (arr[:, :, 2] < 250)
        assert non_white.sum() > 10

    def test_different_tools_look_different(self):
        results = {}
        for tool in ["pen", "pencil", "brush"]:
            events = [
                StylusEvent(x=20, y=40, pressure=0.7, tool=tool),
                StylusEvent(x=80, y=40, pressure=0.7, tool=tool),
            ]
            stroke = Stroke(events=events)
            d = Drawing(width=100, height=80, strokes=[stroke])
            img = render_drawing(d, apply_paper=False)
            arr = np.array(img)[:, :, :3].astype(float)
            results[tool] = arr.mean()

        # Each tool should produce a different mean brightness
        vals = list(results.values())
        assert len(set(round(v, 1) for v in vals)) >= 2

    def test_pressure_affects_width(self):
        def stroke_width(pressure):
            events = [
                StylusEvent(x=20, y=40, pressure=pressure, tool="brush"),
                StylusEvent(x=80, y=40, pressure=pressure, tool="brush"),
            ]
            stroke = Stroke(events=events)
            d = Drawing(width=100, height=80, strokes=[stroke])
            img = render_drawing(d, apply_paper=False)
            arr = np.array(img)[:, :, :3]
            # Count non-white pixels
            non_white = np.any(arr < 250, axis=2)
            return non_white.sum()

        low = stroke_width(0.1)
        high = stroke_width(1.0)
        # Higher pressure should produce more ink pixels
        assert high > low

    def test_eraser_removes_marks(self):
        # Draw a line
        draw_events = [
            StylusEvent(x=20, y=40, pressure=0.9, tool="pen", color="black"),
            StylusEvent(x=80, y=40, pressure=0.9, tool="pen", color="black"),
        ]
        # Erase over it
        erase_events = [
            StylusEvent(x=20, y=40, pressure=1.0, tool="eraser"),
            StylusEvent(x=80, y=40, pressure=1.0, tool="eraser"),
        ]
        d_no_erase = Drawing(width=100, height=80, strokes=[Stroke(events=draw_events)])
        d_with_erase = Drawing(width=100, height=80, strokes=[
            Stroke(events=draw_events, layer=0),
            Stroke(events=erase_events, layer=1),
        ])
        img_no = render_drawing(d_no_erase, apply_paper=False)
        img_yes = render_drawing(d_with_erase, apply_paper=False)
        # After erasing, the mean should be closer to white
        arr_no = np.array(img_no)[:, :, :3].mean()
        arr_yes = np.array(img_yes)[:, :, :3].mean()
        assert arr_yes > arr_no

    def test_color_rendering(self):
        events = [
            StylusEvent(x=20, y=40, pressure=0.9, tool="pen", color="red"),
            StylusEvent(x=80, y=40, pressure=0.9, tool="pen", color="red"),
        ]
        d = Drawing(width=100, height=80, strokes=[Stroke(events=events)])
        img = render_drawing(d, apply_paper=False)
        arr = np.array(img)
        # Find non-white pixels
        mask = arr[:, :, 0] < 250
        if mask.sum() > 0:
            # Red channel should dominate in colored pixels
            r_mean = arr[mask, 0].mean()
            g_mean = arr[mask, 1].mean()
            b_mean = arr[mask, 2].mean()
            assert r_mean > g_mean
            assert r_mean > b_mean


class TestInterpolateEvents:
    def test_single_step_returns_first(self):
        e1 = StylusEvent(x=0, y=0)
        e2 = StylusEvent(x=10, y=10)
        result = interpolate_events(e1, e2, 1)
        assert len(result) == 1
        assert result[0].x == 0

    def test_correct_count(self):
        e1 = StylusEvent(x=0, y=0)
        e2 = StylusEvent(x=100, y=0)
        result = interpolate_events(e1, e2, 10)
        assert len(result) == 10

    def test_endpoints_match(self):
        e1 = StylusEvent(x=0, y=0, pressure=0.2)
        e2 = StylusEvent(x=100, y=50, pressure=0.8)
        result = interpolate_events(e1, e2, 5)
        assert abs(result[0].x - 0) < 0.01
        assert abs(result[0].y - 0) < 0.01
        assert abs(result[-1].x - 100) < 0.01
        assert abs(result[-1].y - 50) < 0.01

    def test_pressure_interpolated(self):
        e1 = StylusEvent(x=0, y=0, pressure=0.0)
        e2 = StylusEvent(x=10, y=0, pressure=1.0)
        result = interpolate_events(e1, e2, 5)
        pressures = [e.pressure for e in result]
        # Should be monotonically increasing
        for i in range(len(pressures) - 1):
            assert pressures[i + 1] >= pressures[i]

    def test_preserves_tool_and_color(self):
        e1 = StylusEvent(x=0, y=0, tool="brush", color="blue")
        e2 = StylusEvent(x=10, y=10, tool="brush", color="blue")
        result = interpolate_events(e1, e2, 3)
        for e in result:
            assert e.tool == "brush"
            assert e.color == "blue"
