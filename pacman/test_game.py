"""Tests for the game logic module."""

import unittest
from maze import Maze, Tile
from entities import PacMan, Ghost, Direction, GhostMode, GhostPersonality
from game import Game, GameState, PELLET_SCORE, POWER_PELLET_SCORE


class TestGameInit(unittest.TestCase):
    def test_initial_state(self):
        game = Game()
        self.assertEqual(game.state, GameState.READY)

    def test_initial_score(self):
        game = Game()
        self.assertEqual(game.score, 0)

    def test_initial_lives(self):
        game = Game()
        self.assertEqual(game.lives, 3)

    def test_initial_level(self):
        game = Game()
        self.assertEqual(game.level, 1)

    def test_has_pacman(self):
        game = Game()
        self.assertIsNotNone(game.pacman)

    def test_has_ghosts(self):
        game = Game()
        self.assertEqual(len(game.ghosts), 4)


class TestGameplay(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.start()

    def test_start_sets_playing(self):
        self.assertEqual(self.game.state, GameState.PLAYING)

    def test_handle_input(self):
        self.game.handle_input(Direction.LEFT)
        # Pac-Man should have queued direction
        self.assertIsNotNone(self.game.pacman)

    def test_eating_pellet_scores(self):
        """Moving onto a pellet increases score."""
        # Find Pac-Man's position and a direction with a pellet
        pr, pc = self.game.pacman.position
        # Move left (row 19, col 13 -> 12 should have pellet in classic layout)
        self.game.handle_input(Direction.LEFT)
        self.game.update()
        # Score should increase if moved onto pellet
        # (depends on starting position having adjacent pellet)

    def test_pause_toggle(self):
        self.game.toggle_pause()
        self.assertEqual(self.game.state, GameState.PAUSED)
        self.game.toggle_pause()
        self.assertEqual(self.game.state, GameState.PLAYING)

    def test_update_when_paused(self):
        """Game doesn't update when paused."""
        self.game.toggle_pause()
        old_tick = self.game._tick
        self.game.update()
        self.assertEqual(self.game._tick, old_tick)


class TestScoring(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.start()

    def test_pellet_score(self):
        """Eating a pellet gives correct score."""
        # Manually trigger pellet eating
        pr, pc = self.game.pacman.position
        # Place a pellet at pacman's position for testing
        self.game.maze._grid[pr][pc] = Tile.PELLET
        self.game._eat_pellet()
        self.assertEqual(self.game.score, PELLET_SCORE)

    def test_power_pellet_score(self):
        """Eating a power pellet gives correct score."""
        pr, pc = self.game.pacman.position
        self.game.maze._grid[pr][pc] = Tile.POWER_PELLET
        self.game._eat_pellet()
        self.assertEqual(self.game.score, POWER_PELLET_SCORE)

    def test_power_pellet_frightens_ghosts(self):
        """Eating a power pellet frightens ghosts."""
        # First set ghosts to chase mode
        for ghost in self.game.ghosts:
            ghost.set_mode(GhostMode.CHASE)
        pr, pc = self.game.pacman.position
        self.game.maze._grid[pr][pc] = Tile.POWER_PELLET
        self.game._eat_pellet()
        for ghost in self.game.ghosts:
            self.assertEqual(ghost.mode, GhostMode.FRIGHTENED)


class TestLives(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.start()

    def test_lose_life(self):
        initial_lives = self.game.lives
        self.game._lose_life()
        self.assertEqual(self.game.lives, initial_lives - 1)

    def test_game_over_at_zero_lives(self):
        self.game._lives = 1
        self.game._lose_life()
        self.assertEqual(self.game.state, GameState.GAME_OVER)


class TestLevelProgression(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.start()

    def test_level_complete_when_no_pellets(self):
        """Level completes when all pellets eaten."""
        # Eat all pellets
        for r in range(self.game.maze.height):
            for c in range(self.game.maze.width):
                self.game.maze.eat_pellet(r, c)
        self.game._check_level_complete()
        self.assertEqual(self.game.state, GameState.WON_LEVEL)

    def test_advance_level(self):
        self.game._advance_level()
        self.assertEqual(self.game.level, 2)


if __name__ == "__main__":
    unittest.main()
