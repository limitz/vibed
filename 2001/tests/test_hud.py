"""Tests for hud module: timeline bar, titles, subtitles."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from hud import (
    format_time, format_speed, get_active_dialogue,
    draw_scene_title, draw_timeline_bar, draw_dialogue, draw_hud
)
from renderer import ScreenBuffer
from timeline import Scene, Dialogue, Timeline
from player import Player


def dummy_render(buf, p):
    pass


class TestFormatTime:
    def test_zero(self):
        assert format_time(0) == "0:00"

    def test_seconds(self):
        assert format_time(45) == "0:45"

    def test_minutes(self):
        assert format_time(125) == "2:05"

    def test_large(self):
        assert format_time(600) == "10:00"


class TestFormatSpeed:
    def test_normal(self):
        assert format_speed(1.0) == ">1x"

    def test_fast_forward(self):
        assert format_speed(2.0) == ">>2x"
        assert format_speed(4.0) == ">>4x"

    def test_rewind(self):
        assert format_speed(-1.0) == "<<1x"
        assert format_speed(-2.0) == "<<2x"


class TestGetActiveDialogue:
    def test_no_dialogues(self):
        s = Scene("t", "T", 10.0, dummy_render)
        assert get_active_dialogue(s, 0.5) is None

    def test_active_dialogue(self):
        d = Dialogue(0.2, 0.6, "Hello", "HAL")
        s = Scene("t", "T", 10.0, dummy_render, [d])
        result = get_active_dialogue(s, 0.3)
        assert result.text == "Hello"

    def test_no_match(self):
        d = Dialogue(0.2, 0.6, "Hello", "HAL")
        s = Scene("t", "T", 10.0, dummy_render, [d])
        assert get_active_dialogue(s, 0.8) is None


class TestDrawHud:
    def test_draw_scene_title(self):
        buf = ScreenBuffer(40, 10)
        draw_scene_title(buf, "Test Title")
        # Title should be on row height - 3 = 7
        found = False
        for x in range(40):
            if buf.get_cell(x, 7).char == 'T':
                found = True
                break
        assert found

    def test_draw_dialogue(self):
        buf = ScreenBuffer(40, 10)
        draw_dialogue(buf, "Hello World", "HAL")
        # Should be on row height - 1 = 9
        found = False
        for x in range(40):
            if buf.get_cell(x, 9).char != ' ':
                found = True
                break
        assert found

    def test_draw_timeline_bar(self):
        tl = Timeline([Scene("t", "T", 10.0, dummy_render)])
        p = Player(tl)
        p.position = 5.0
        buf = ScreenBuffer(60, 10)
        draw_timeline_bar(buf, p)
        # Should be on row height - 2 = 8
        found = False
        for x in range(60):
            if buf.get_cell(x, 8).char != ' ':
                found = True
                break
        assert found

    def test_draw_hud_integrates(self):
        tl = Timeline([
            Scene("t", "Test", 10.0, dummy_render, [
                Dialogue(0.0, 1.0, "Hello", "HAL"),
            ])
        ])
        p = Player(tl)
        p.position = 5.0
        buf = ScreenBuffer(60, 10)
        draw_hud(buf, p)
        # Bottom 3 rows should have content
        has_content = False
        for row in range(7, 10):
            for x in range(60):
                if buf.get_cell(x, row).char != ' ':
                    has_content = True
        assert has_content
