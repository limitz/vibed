"""Tests for timeline module: Scene, Dialogue, Timeline."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from timeline import Scene, Dialogue, Timeline


def dummy_render(buffer, progress):
    pass


def make_scenes():
    return [
        Scene("s1", "Scene One", 10.0, dummy_render, [
            Dialogue(0.0, 0.5, "Hello", "DAVE"),
            Dialogue(0.6, 1.0, "Goodbye", "HAL"),
        ]),
        Scene("s2", "Scene Two", 20.0, dummy_render),
        Scene("s3", "Scene Three", 15.0, dummy_render),
    ]


class TestDialogue:
    def test_dialogue_fields(self):
        d = Dialogue(0.1, 0.5, "Hello", "HAL")
        assert d.start == 0.1
        assert d.end == 0.5
        assert d.text == "Hello"
        assert d.speaker == "HAL"

    def test_dialogue_default_speaker(self):
        d = Dialogue(0.0, 1.0, "Narration")
        assert d.speaker == ""


class TestScene:
    def test_scene_fields(self):
        s = Scene("test", "Test Scene", 10.0, dummy_render)
        assert s.name == "test"
        assert s.title == "Test Scene"
        assert s.duration == 10.0
        assert s.render_fn is dummy_render
        assert s.dialogues == []

    def test_scene_with_dialogues(self):
        d = Dialogue(0.0, 0.5, "Hi")
        s = Scene("test", "Test", 5.0, dummy_render, [d])
        assert len(s.dialogues) == 1


class TestTimeline:
    def test_total_duration(self):
        scenes = make_scenes()
        tl = Timeline(scenes)
        assert tl.total_duration == 45.0

    def test_scene_count(self):
        tl = Timeline(make_scenes())
        assert tl.get_scene_count() == 3

    def test_get_scene_at_start(self):
        tl = Timeline(make_scenes())
        scene, progress, idx = tl.get_scene_at(0.0)
        assert scene.name == "s1"
        assert progress == 0.0
        assert idx == 0

    def test_get_scene_at_middle_of_first(self):
        tl = Timeline(make_scenes())
        scene, progress, idx = tl.get_scene_at(5.0)
        assert scene.name == "s1"
        assert abs(progress - 0.5) < 1e-9
        assert idx == 0

    def test_get_scene_at_second_scene(self):
        tl = Timeline(make_scenes())
        # Scene 2 starts at 10.0, 5 seconds in = 15.0
        scene, progress, idx = tl.get_scene_at(15.0)
        assert scene.name == "s2"
        assert abs(progress - 0.25) < 1e-9
        assert idx == 1

    def test_get_scene_at_third_scene(self):
        tl = Timeline(make_scenes())
        # Scene 3 starts at 30.0
        scene, progress, idx = tl.get_scene_at(37.5)
        assert scene.name == "s3"
        assert abs(progress - 0.5) < 1e-9
        assert idx == 2

    def test_get_scene_at_end(self):
        tl = Timeline(make_scenes())
        result = tl.get_scene_at(45.0)
        assert result is None

    def test_get_scene_at_past_end(self):
        tl = Timeline(make_scenes())
        result = tl.get_scene_at(100.0)
        assert result is None

    def test_get_scene_at_negative(self):
        tl = Timeline(make_scenes())
        result = tl.get_scene_at(-1.0)
        assert result is not None
        scene, progress, idx = result
        assert idx == 0
        assert progress == 0.0

    def test_get_scene_index(self):
        tl = Timeline(make_scenes())
        assert tl.get_scene_index(0.0) == 0
        assert tl.get_scene_index(5.0) == 0
        assert tl.get_scene_index(10.0) == 1
        assert tl.get_scene_index(30.0) == 2

    def test_get_scene_start_time(self):
        tl = Timeline(make_scenes())
        assert tl.get_scene_start_time(0) == 0.0
        assert tl.get_scene_start_time(1) == 10.0
        assert tl.get_scene_start_time(2) == 30.0

    def test_get_scene_start_time_out_of_bounds(self):
        tl = Timeline(make_scenes())
        assert tl.get_scene_start_time(3) == tl.total_duration

    def test_empty_timeline(self):
        tl = Timeline([])
        assert tl.total_duration == 0.0
        assert tl.get_scene_count() == 0
        assert tl.get_scene_at(0.0) is None
