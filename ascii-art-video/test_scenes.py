"""Tests for the scenes module."""

import unittest
from renderer import ScreenBuffer, Color
from scenes import (
    mirror_sprite, render_title, FightChoreography,
    FunnyMoment, render_fade_out, render_credits,
    STICK_IDLE, STICK_PUNCH_RIGHT
)


class TestMirrorSprite(unittest.TestCase):
    def test_mirror_simple(self):
        sprite = [" /|\\"]
        mirrored = mirror_sprite(sprite)
        self.assertEqual(mirrored, ["/|\\ "])

    def test_mirror_preserves_length(self):
        sprite = ["ABC", "DEF"]
        mirrored = mirror_sprite(sprite)
        self.assertEqual(len(mirrored), 2)
        self.assertEqual(len(mirrored[0]), 3)

    def test_mirror_direction_chars(self):
        sprite = ["> <"]
        mirrored = mirror_sprite(sprite)
        self.assertIn('<', mirrored[0])
        self.assertIn('>', mirrored[0])

    def test_mirror_idle_sprite(self):
        mirrored = mirror_sprite(STICK_IDLE)
        # Should be same shape, just direction chars flipped
        self.assertEqual(len(mirrored), len(STICK_IDLE))


class TestRenderTitle(unittest.TestCase):
    def test_render_title_start(self):
        buf = ScreenBuffer(80, 24)
        render_title(buf, 0.0)
        # Should have drawn something (star field at minimum)
        non_space = sum(1 for y in range(24) for x in range(80)
                       if buf.get_cell(x, y).char != ' ')
        self.assertGreater(non_space, 0)

    def test_render_title_end(self):
        buf = ScreenBuffer(80, 24)
        render_title(buf, 1.0)
        non_space = sum(1 for y in range(24) for x in range(80)
                       if buf.get_cell(x, y).char != ' ')
        self.assertGreater(non_space, 0)

    def test_render_title_small_screen(self):
        buf = ScreenBuffer(60, 20)
        render_title(buf, 0.5)
        # Should not crash on smaller screen


class TestFightChoreography(unittest.TestCase):
    def setUp(self):
        self.fight = FightChoreography()
        self.buf = ScreenBuffer(80, 24)

    def test_render_all_phases(self):
        """Render each phase to verify no crashes."""
        for p in [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0]:
            buf = ScreenBuffer(80, 24)
            self.fight.render(buf, p)

    def test_health_decreases(self):
        # Run through some fight phases
        for p in [0.2, 0.3, 0.4, 0.5, 0.6]:
            self.fight.render(self.buf, p)
        # Health should have decreased
        self.assertTrue(self.fight.p1_health < 100 or self.fight.p2_health < 100)

    def test_initial_health(self):
        self.assertEqual(self.fight.p1_health, 100)
        self.assertEqual(self.fight.p2_health, 100)


class TestFunnyMoment(unittest.TestCase):
    def setUp(self):
        self.funny = FunnyMoment()

    def test_render_all_phases(self):
        for p in [0.0, 0.05, 0.15, 0.25, 0.4, 0.55, 0.7, 0.8, 0.9, 1.0]:
            buf = ScreenBuffer(80, 24)
            self.funny.render(buf, p)

    def test_friendship_ending(self):
        buf = ScreenBuffer(80, 24)
        self.funny.render(buf, 0.95)
        # Should have "FRIENDSHIP WINS!" text
        found = False
        for x in range(80):
            if buf.get_cell(x, 3) and buf.get_cell(x, 3).char == 'F':
                found = True
                break
        self.assertTrue(found)


class TestFadeOut(unittest.TestCase):
    def test_render_all_progress(self):
        for p in [0.0, 0.2, 0.5, 0.8, 1.0]:
            buf = ScreenBuffer(80, 24)
            render_fade_out(buf, p)

    def test_final_message(self):
        buf = ScreenBuffer(80, 24)
        render_fade_out(buf, 0.85)
        # Should have some text visible
        non_space = sum(1 for y in range(24) for x in range(80)
                       if buf.get_cell(x, y).char != ' ')
        self.assertGreater(non_space, 0)


class TestCredits(unittest.TestCase):
    def test_render_all_progress(self):
        for p in [0.0, 0.25, 0.5, 0.75, 1.0]:
            buf = ScreenBuffer(80, 24)
            render_credits(buf, p)

    def test_has_star_field(self):
        buf = ScreenBuffer(80, 24)
        render_credits(buf, 0.0)
        # Star field should have some non-space chars
        non_space = sum(1 for y in range(24) for x in range(80)
                       if buf.get_cell(x, y).char != ' ')
        self.assertGreater(non_space, 0)


if __name__ == '__main__':
    unittest.main()
