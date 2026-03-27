"""Tests for the effects module."""

import unittest
from effects import (
    Particle, ParticleSystem, spawn_explosion, spawn_sparks,
    spawn_fireworks, apply_screen_shake, apply_fade, apply_flash,
    draw_fire, draw_lightning, draw_star_field, draw_scrolling_text,
    draw_matrix_rain, draw_shockwave, draw_combo_text, draw_speed_lines,
    draw_dramatic_zoom_text, draw_energy_aura
)
from renderer import ScreenBuffer, Color


class TestParticle(unittest.TestCase):
    def test_particle_creation(self):
        p = Particle(10, 5, 1.0, -0.5, '*', Color.RED, life=2.0)
        self.assertAlmostEqual(p.x, 10)
        self.assertAlmostEqual(p.y, 5)
        self.assertTrue(p.alive)

    def test_particle_update(self):
        p = Particle(10, 5, 2.0, 0.0, '*', life=1.0)
        p.update(0.5)
        self.assertAlmostEqual(p.x, 11.0)
        self.assertAlmostEqual(p.life, 0.5)
        self.assertTrue(p.alive)

    def test_particle_dies(self):
        p = Particle(0, 0, 0, 0, '*', life=0.5)
        p.update(0.6)
        self.assertFalse(p.alive)

    def test_particle_gravity(self):
        p = Particle(0, 0, 0, 0, '*', life=5.0, gravity=10.0)
        p.update(1.0)
        self.assertAlmostEqual(p.vy, 10.0)
        self.assertAlmostEqual(p.y, 0.0)  # After 1s with initial vy=0, y = 0 + 0*1 = 0 (vy updates after)
        # Actually vy is updated during the step, but y uses original vy
        # y += vy * dt = 0 * 1 = 0, then vy += g * dt = 10


class TestParticleSystem(unittest.TestCase):
    def test_empty_system(self):
        ps = ParticleSystem()
        self.assertEqual(ps.active_count, 0)

    def test_add_particle(self):
        ps = ParticleSystem()
        ps.add(Particle(0, 0, 0, 0, '*', life=1.0))
        self.assertEqual(ps.active_count, 1)

    def test_dead_particles_removed(self):
        ps = ParticleSystem()
        ps.add(Particle(0, 0, 0, 0, '*', life=0.1))
        ps.update(0.2)
        self.assertEqual(ps.active_count, 0)

    def test_draw(self):
        ps = ParticleSystem()
        ps.add(Particle(5, 3, 0, 0, '#', Color.RED, life=1.0))
        buf = ScreenBuffer(20, 10)
        ps.draw(buf)
        cell = buf.get_cell(5, 3)
        self.assertEqual(cell.char, '#')
        self.assertEqual(cell.fg, Color.RED)


class TestSpawnFunctions(unittest.TestCase):
    def test_spawn_explosion(self):
        ps = ParticleSystem()
        spawn_explosion(ps, 10, 5, count=15)
        self.assertEqual(ps.active_count, 15)

    def test_spawn_sparks(self):
        ps = ParticleSystem()
        spawn_sparks(ps, 10, 5, count=8)
        self.assertEqual(ps.active_count, 8)

    def test_spawn_fireworks(self):
        ps = ParticleSystem()
        spawn_fireworks(ps, 10, 5, count=20)
        self.assertEqual(ps.active_count, 20)


class TestEffects(unittest.TestCase):
    def test_screen_shake_returns_buffer(self):
        buf = ScreenBuffer(20, 10)
        result = apply_screen_shake(buf, 2.0)
        self.assertIsInstance(result, ScreenBuffer)
        self.assertEqual(result.width, 20)
        self.assertEqual(result.height, 10)

    def test_screen_shake_zero_intensity(self):
        buf = ScreenBuffer(20, 10)
        result = apply_screen_shake(buf, 0)
        self.assertIs(result, buf)  # Should return same buffer

    def test_apply_fade_doesnt_crash(self):
        buf = ScreenBuffer(20, 10)
        buf.draw_text(0, 0, "Hello")
        apply_fade(buf, 0.5)
        # Should not raise

    def test_apply_flash_doesnt_crash(self):
        buf = ScreenBuffer(20, 10)
        apply_flash(buf, 0.5)
        # Should not raise

    def test_draw_fire_doesnt_crash(self):
        buf = ScreenBuffer(20, 10)
        draw_fire(buf, 9, 20, 1.0)

    def test_draw_lightning_doesnt_crash(self):
        buf = ScreenBuffer(20, 10)
        draw_lightning(buf, 10, 2, 8)

    def test_draw_star_field(self):
        buf = ScreenBuffer(40, 20)
        draw_star_field(buf, density=0.1, seed=42)
        # Check that some cells are non-space
        non_space = sum(1 for y in range(20) for x in range(40)
                       if buf.get_cell(x, y).char != ' ')
        self.assertGreater(non_space, 0)

    def test_draw_star_field_deterministic(self):
        buf1 = ScreenBuffer(20, 10)
        buf2 = ScreenBuffer(20, 10)
        draw_star_field(buf1, seed=42)
        draw_star_field(buf2, seed=42)
        for y in range(10):
            for x in range(20):
                self.assertEqual(buf1.get_cell(x, y).char, buf2.get_cell(x, y).char)

    def test_draw_scrolling_text(self):
        buf = ScreenBuffer(40, 10)
        lines = ["Line 1", "Line 2", "Line 3"]
        draw_scrolling_text(buf, lines, 3.0)
        # Line 1 should be at y=3
        # Check center of "Line 1"
        found = False
        for x in range(40):
            if buf.get_cell(x, 3).char == 'L':
                found = True
                break
        self.assertTrue(found)


class TestNewEffects(unittest.TestCase):
    def test_matrix_rain(self):
        buf = ScreenBuffer(40, 20)
        draw_matrix_rain(buf, 0.5)
        non_space = sum(1 for y in range(20) for x in range(40)
                       if buf.get_cell(x, y).char != ' ')
        self.assertGreater(non_space, 0)

    def test_shockwave(self):
        buf = ScreenBuffer(40, 20)
        draw_shockwave(buf, 20, 10, 5.0)
        non_space = sum(1 for y in range(20) for x in range(40)
                       if buf.get_cell(x, y).char != ' ')
        self.assertGreater(non_space, 0)

    def test_combo_text_below_threshold(self):
        buf = ScreenBuffer(40, 10)
        draw_combo_text(buf, 1, 10, 5)
        # Should not draw anything for combo < 2
        cell = buf.get_cell(10, 5)
        self.assertEqual(cell.char, ' ')

    def test_combo_text_above_threshold(self):
        buf = ScreenBuffer(40, 10)
        draw_combo_text(buf, 3, 10, 5)
        cell = buf.get_cell(10, 5)
        self.assertEqual(cell.char, '3')

    def test_speed_lines(self):
        buf = ScreenBuffer(40, 20)
        draw_speed_lines(buf, "horizontal", 0.5)
        # Should draw some dashes
        has_dash = any(buf.get_cell(x, y).char == '-'
                      for y in range(20) for x in range(40))
        self.assertTrue(has_dash)

    def test_dramatic_zoom_text(self):
        buf = ScreenBuffer(40, 10)
        draw_dramatic_zoom_text(buf, "TEST", 0.3, Color.RED)
        # Should have drawn the text
        found = False
        for x in range(40):
            if buf.get_cell(x, 5).char == 'T':
                found = True
                break
        self.assertTrue(found)

    def test_energy_aura(self):
        buf = ScreenBuffer(40, 20)
        draw_energy_aura(buf, 20, 10, 5, Color.BRIGHT_CYAN, 0.5)
        non_space = sum(1 for y in range(20) for x in range(40)
                       if buf.get_cell(x, y).char != ' ')
        self.assertGreater(non_space, 0)


if __name__ == '__main__':
    unittest.main()
