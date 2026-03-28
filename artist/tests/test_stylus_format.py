"""Tests for stylus_format module."""

import os
import sys
import json
import tempfile
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from stylus_format import (
    StylusEvent, Stroke, Drawing,
    save_drawing, load_drawing,
    resolve_color, COLOR_NAMES, VALID_TOOLS,
)


class TestStylusEvent:
    def test_create_defaults(self):
        e = StylusEvent(x=10.0, y=20.0)
        assert e.x == 10.0
        assert e.y == 20.0
        assert e.pressure == 0.5
        assert e.tool == "pen"
        assert e.color == "black"

    def test_pressure_clamped(self):
        e = StylusEvent(x=0, y=0, pressure=1.5)
        assert e.pressure == 1.0
        e2 = StylusEvent(x=0, y=0, pressure=-0.3)
        assert e2.pressure == 0.0

    def test_angle_clamped(self):
        e = StylusEvent(x=0, y=0, angle_x=60.0, angle_y=-60.0)
        assert e.angle_x == 45.0
        assert e.angle_y == -45.0

    def test_invalid_tool(self):
        with pytest.raises(ValueError, match="Invalid tool"):
            StylusEvent(x=0, y=0, tool="crayon")

    def test_resolved_color_name(self):
        e = StylusEvent(x=0, y=0, color="red")
        assert e.resolved_color() == (220, 30, 30)

    def test_resolved_color_tuple(self):
        e = StylusEvent(x=0, y=0, color=(100, 200, 50))
        assert e.resolved_color() == (100, 200, 50)

    def test_to_dict_and_back(self):
        e = StylusEvent(x=1.5, y=2.5, dx=0.7, dy=0.3, pressure=0.8,
                        angle_x=10.0, angle_y=-5.0, color="blue", tool="pencil")
        d = e.to_dict()
        e2 = StylusEvent.from_dict(d)
        assert e2.x == e.x
        assert e2.y == e.y
        assert e2.pressure == e.pressure
        assert e2.tool == e.tool
        assert e2.color == e.color

    def test_to_dict_rgb_color(self):
        e = StylusEvent(x=0, y=0, color=(10, 20, 30))
        d = e.to_dict()
        assert d["color"] == [10, 20, 30]
        e2 = StylusEvent.from_dict(d)
        assert e2.color == (10, 20, 30)


class TestResolveColor:
    def test_all_named_colors(self):
        for name, rgb in COLOR_NAMES.items():
            assert resolve_color(name) == rgb

    def test_case_insensitive(self):
        assert resolve_color("RED") == (220, 30, 30)
        assert resolve_color("  Black  ") == (10, 10, 10)

    def test_unknown_name(self):
        with pytest.raises(ValueError, match="Unknown color"):
            resolve_color("chartreuse")

    def test_rgb_tuple(self):
        assert resolve_color((0, 128, 255)) == (0, 128, 255)

    def test_rgb_list(self):
        assert resolve_color([0, 128, 255]) == (0, 128, 255)

    def test_rgb_wrong_length(self):
        with pytest.raises(ValueError, match="3 components"):
            resolve_color((1, 2))

    def test_rgb_out_of_range(self):
        with pytest.raises(ValueError, match="0-255"):
            resolve_color((256, 0, 0))

    def test_invalid_type(self):
        with pytest.raises(TypeError):
            resolve_color(42)


class TestStroke:
    def test_create_empty(self):
        s = Stroke()
        assert s.events == []
        assert s.layer == 0

    def test_round_trip(self):
        events = [
            StylusEvent(x=0, y=0, pressure=0.3),
            StylusEvent(x=10, y=10, pressure=0.7),
        ]
        s = Stroke(events=events, layer=2)
        d = s.to_dict()
        s2 = Stroke.from_dict(d)
        assert len(s2.events) == 2
        assert s2.layer == 2
        assert s2.events[0].x == 0
        assert s2.events[1].pressure == 0.7


class TestDrawing:
    def test_defaults(self):
        d = Drawing()
        assert d.width == 1920
        assert d.height == 1080
        assert d.background == (255, 255, 255)
        assert d.strokes == []

    def test_round_trip(self):
        events = [StylusEvent(x=5, y=5), StylusEvent(x=50, y=50)]
        stroke = Stroke(events=events, layer=0)
        drawing = Drawing(width=800, height=600, strokes=[stroke])
        d = drawing.to_dict()
        drawing2 = Drawing.from_dict(d)
        assert drawing2.width == 800
        assert drawing2.height == 600
        assert len(drawing2.strokes) == 1
        assert len(drawing2.strokes[0].events) == 2


class TestSaveLoad:
    def test_save_and_load(self):
        events = [
            StylusEvent(x=0, y=0, color="red", tool="brush"),
            StylusEvent(x=100, y=100, pressure=0.9, color="red", tool="brush"),
        ]
        stroke = Stroke(events=events)
        drawing = Drawing(width=640, height=480, strokes=[stroke])

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name

        try:
            save_drawing(drawing, path)
            loaded = load_drawing(path)
            assert loaded.width == 640
            assert loaded.height == 480
            assert len(loaded.strokes) == 1
            assert loaded.strokes[0].events[0].color == "red"
            assert loaded.strokes[0].events[0].tool == "brush"
            assert loaded.strokes[0].events[1].pressure == 0.9
        finally:
            os.unlink(path)

    def test_file_is_valid_json(self):
        drawing = Drawing(strokes=[])
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            save_drawing(drawing, path)
            with open(path) as f:
                data = json.load(f)
            assert "version" in data
            assert "strokes" in data
        finally:
            os.unlink(path)
