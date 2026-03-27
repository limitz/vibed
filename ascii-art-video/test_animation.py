"""Tests for the animation module."""

import unittest
from animation import Scene, Timeline, ease_in_out, ease_in, ease_out, lerp, bounce
from renderer import ScreenBuffer


class TestEasing(unittest.TestCase):
    def test_ease_in_out_endpoints(self):
        self.assertAlmostEqual(ease_in_out(0.0), 0.0)
        self.assertAlmostEqual(ease_in_out(1.0), 1.0)

    def test_ease_in_out_midpoint(self):
        self.assertAlmostEqual(ease_in_out(0.5), 0.5)

    def test_ease_in_endpoints(self):
        self.assertAlmostEqual(ease_in(0.0), 0.0)
        self.assertAlmostEqual(ease_in(1.0), 1.0)

    def test_ease_out_endpoints(self):
        self.assertAlmostEqual(ease_out(0.0), 0.0)
        self.assertAlmostEqual(ease_out(1.0), 1.0)

    def test_lerp(self):
        self.assertAlmostEqual(lerp(0, 10, 0.0), 0)
        self.assertAlmostEqual(lerp(0, 10, 0.5), 5)
        self.assertAlmostEqual(lerp(0, 10, 1.0), 10)

    def test_bounce_endpoints(self):
        self.assertAlmostEqual(bounce(0.0), 0.0)
        self.assertAlmostEqual(bounce(1.0), 1.0, places=2)


class TestScene(unittest.TestCase):
    def test_scene_creation(self):
        def dummy(buf, p):
            pass
        scene = Scene("test", 5.0, dummy)
        self.assertEqual(scene.name, "test")
        self.assertEqual(scene.duration, 5.0)

    def test_scene_render(self):
        rendered = []
        def render_fn(buf, p):
            rendered.append(p)
        scene = Scene("test", 1.0, render_fn)
        buf = ScreenBuffer(10, 5)
        scene.render(buf, 0.5)
        self.assertEqual(len(rendered), 1)
        self.assertAlmostEqual(rendered[0], 0.5)

    def test_scene_clamps_progress(self):
        values = []
        def render_fn(buf, p):
            values.append(p)
        scene = Scene("test", 1.0, render_fn)
        buf = ScreenBuffer(10, 5)
        scene.render(buf, -0.5)
        scene.render(buf, 1.5)
        self.assertAlmostEqual(values[0], 0.0)
        self.assertAlmostEqual(values[1], 1.0)


class TestTimeline(unittest.TestCase):
    def setUp(self):
        self.timeline = Timeline()
        self.timeline.add_scene(Scene("s1", 2.0, lambda b, p: None))
        self.timeline.add_scene(Scene("s2", 3.0, lambda b, p: None))
        self.timeline.add_scene(Scene("s3", 1.0, lambda b, p: None))

    def test_total_duration(self):
        self.assertAlmostEqual(self.timeline.total_duration, 6.0)

    def test_get_scene_at_start(self):
        result = self.timeline.get_scene_at(0.0)
        self.assertIsNotNone(result)
        scene, progress = result
        self.assertEqual(scene.name, "s1")
        self.assertAlmostEqual(progress, 0.0)

    def test_get_scene_at_middle(self):
        result = self.timeline.get_scene_at(3.0)
        self.assertIsNotNone(result)
        scene, progress = result
        self.assertEqual(scene.name, "s2")
        self.assertAlmostEqual(progress, 1.0 / 3.0)

    def test_get_scene_at_last(self):
        result = self.timeline.get_scene_at(5.5)
        self.assertIsNotNone(result)
        scene, progress = result
        self.assertEqual(scene.name, "s3")
        self.assertAlmostEqual(progress, 0.5)

    def test_get_scene_past_end(self):
        result = self.timeline.get_scene_at(7.0)
        self.assertIsNone(result)

    def test_is_complete(self):
        self.assertFalse(self.timeline.is_complete(0.0))
        self.assertFalse(self.timeline.is_complete(5.9))
        self.assertTrue(self.timeline.is_complete(6.0))
        self.assertTrue(self.timeline.is_complete(10.0))


if __name__ == '__main__':
    unittest.main()
