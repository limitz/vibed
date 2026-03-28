"""Tests for scenes module: all 10 scene render functions."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scenes import create_all_scenes
from renderer import ScreenBuffer


class TestAllScenes:
    """Test that each scene renders without errors at various progress values."""

    def _get_scenes(self):
        return create_all_scenes()

    def test_creates_10_scenes(self):
        scenes = self._get_scenes()
        assert len(scenes) == 10

    def test_all_scenes_have_names(self):
        for s in self._get_scenes():
            assert s.name
            assert s.title
            assert s.duration > 0

    def test_all_scenes_render_at_zero(self):
        buf = ScreenBuffer(80, 24)
        for s in self._get_scenes():
            buf.clear()
            s.render_fn(buf, 0.0)

    def test_all_scenes_render_at_quarter(self):
        buf = ScreenBuffer(80, 24)
        for s in self._get_scenes():
            buf.clear()
            s.render_fn(buf, 0.25)

    def test_all_scenes_render_at_half(self):
        buf = ScreenBuffer(80, 24)
        for s in self._get_scenes():
            buf.clear()
            s.render_fn(buf, 0.5)

    def test_all_scenes_render_at_three_quarter(self):
        buf = ScreenBuffer(80, 24)
        for s in self._get_scenes():
            buf.clear()
            s.render_fn(buf, 0.75)

    def test_all_scenes_render_at_end(self):
        buf = ScreenBuffer(80, 24)
        for s in self._get_scenes():
            buf.clear()
            s.render_fn(buf, 1.0)

    def test_all_scenes_produce_content(self):
        """Each scene should draw something at progress 0.5."""
        buf = ScreenBuffer(80, 24)
        for s in self._get_scenes():
            buf.clear()
            s.render_fn(buf, 0.5)
            non_empty = sum(
                1 for y in range(24) for x in range(80)
                if buf.get_cell(x, y).char != ' '
            )
            assert non_empty > 0, f"Scene {s.name} produced no content at progress 0.5"

    def test_scenes_are_deterministic(self):
        """Same progress should produce same output."""
        buf1 = ScreenBuffer(80, 24)
        buf2 = ScreenBuffer(80, 24)
        for s in self._get_scenes():
            buf1.clear()
            buf2.clear()
            s.render_fn(buf1, 0.5)
            s.render_fn(buf2, 0.5)
            for y in range(24):
                for x in range(80):
                    c1 = buf1.get_cell(x, y)
                    c2 = buf2.get_cell(x, y)
                    assert c1.char == c2.char, (
                        f"Scene {s.name} not deterministic at ({x},{y}): "
                        f"'{c1.char}' vs '{c2.char}'"
                    )
