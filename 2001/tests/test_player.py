"""Tests for player module: Player state machine."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from player import Player, PlayerState
from timeline import Scene, Timeline
from renderer import ScreenBuffer


def dummy_render(buffer, progress):
    buffer.draw_text(0, 0, f"p={progress:.2f}")


def make_timeline():
    scenes = [
        Scene("s1", "Scene One", 10.0, dummy_render),
        Scene("s2", "Scene Two", 20.0, dummy_render),
        Scene("s3", "Scene Three", 15.0, dummy_render),
    ]
    return Timeline(scenes)


class TestPlayerState:
    def test_initial_state_paused(self):
        p = Player(make_timeline())
        assert p.state == PlayerState.PAUSED
        assert p.position == 0.0
        assert p.speed == 1.0

    def test_play(self):
        p = Player(make_timeline())
        p.play()
        assert p.state == PlayerState.PLAYING

    def test_pause(self):
        p = Player(make_timeline())
        p.play()
        p.pause()
        assert p.state == PlayerState.PAUSED

    def test_toggle_pause(self):
        p = Player(make_timeline())
        p.toggle_pause()
        assert p.state == PlayerState.PLAYING
        p.toggle_pause()
        assert p.state == PlayerState.PAUSED


class TestPlayerUpdate:
    def test_update_advances_position(self):
        p = Player(make_timeline())
        p.play()
        p.update(1.0)
        assert abs(p.position - 1.0) < 1e-9

    def test_update_respects_speed(self):
        p = Player(make_timeline())
        p.play()
        p.set_speed(2.0)
        p.update(1.0)
        assert abs(p.position - 2.0) < 1e-9

    def test_update_paused_no_advance(self):
        p = Player(make_timeline())
        p.update(1.0)
        assert p.position == 0.0

    def test_update_clamps_to_end(self):
        p = Player(make_timeline())
        p.play()
        p.update(100.0)
        assert p.position == 45.0

    def test_update_clamps_to_start_on_rewind(self):
        p = Player(make_timeline())
        p.play()
        p.position = 5.0
        p.set_speed(-1.0)
        p.update(10.0)
        assert p.position == 0.0

    def test_rewind_negative_speed(self):
        p = Player(make_timeline())
        p.play()
        p.position = 10.0
        p.set_speed(-2.0)
        p.update(3.0)
        assert abs(p.position - 4.0) < 1e-9


class TestPlayerSpeed:
    def test_cycle_forward_speed(self):
        p = Player(make_timeline())
        assert p.speed == 1.0
        p.cycle_forward_speed()
        assert p.speed == 2.0
        p.cycle_forward_speed()
        assert p.speed == 4.0
        p.cycle_forward_speed()
        assert p.speed == 1.0

    def test_cycle_rewind_speed(self):
        p = Player(make_timeline())
        p.cycle_rewind_speed()
        assert p.speed == -1.0
        p.cycle_rewind_speed()
        assert p.speed == -2.0
        p.cycle_rewind_speed()
        assert p.speed == -4.0
        p.cycle_rewind_speed()
        assert p.speed == 1.0

    def test_cycle_forward_resets_rewind(self):
        p = Player(make_timeline())
        p.set_speed(-2.0)
        p.cycle_forward_speed()
        assert p.speed == 1.0


class TestPlayerSceneSkip:
    def test_skip_scene_forward(self):
        p = Player(make_timeline())
        p.position = 5.0  # middle of scene 1
        p.skip_scene_forward()
        assert p.position == 10.0  # start of scene 2

    def test_skip_scene_forward_from_last(self):
        p = Player(make_timeline())
        p.position = 35.0  # in scene 3
        p.skip_scene_forward()
        assert p.position == 45.0  # end

    def test_skip_scene_back(self):
        p = Player(make_timeline())
        p.position = 15.0  # middle of scene 2
        p.skip_scene_back()
        assert p.position == 10.0  # start of scene 2

    def test_skip_scene_back_near_start_of_scene(self):
        p = Player(make_timeline())
        p.position = 10.5  # just 0.5s into scene 2 (< 1s threshold)
        p.skip_scene_back()
        assert p.position == 0.0  # goes to previous scene

    def test_skip_scene_back_past_threshold(self):
        p = Player(make_timeline())
        p.position = 12.0  # 2s into scene 2 (> 1s threshold)
        p.skip_scene_back()
        assert p.position == 10.0  # goes to start of current scene

    def test_skip_scene_back_at_scene_start(self):
        p = Player(make_timeline())
        p.position = 10.0  # exactly at start of scene 2
        p.skip_scene_back()
        assert p.position == 0.0  # start of scene 1

    def test_skip_scene_back_from_first(self):
        p = Player(make_timeline())
        p.position = 0.0
        p.skip_scene_back()
        assert p.position == 0.0

    def test_restart(self):
        p = Player(make_timeline())
        p.position = 30.0
        p.restart()
        assert p.position == 0.0

    def test_is_finished(self):
        p = Player(make_timeline())
        assert not p.is_finished()
        p.position = 45.0
        assert p.is_finished()


class TestPlayerGetFrame:
    def test_get_current_frame(self):
        p = Player(make_timeline())
        p.position = 5.0
        buf = ScreenBuffer(20, 5)
        p.get_current_frame(buf)
        assert buf.get_cell(0, 0).char == 'p'
