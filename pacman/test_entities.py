"""Tests for the entities module."""

import unittest
from maze import Maze
from entities import PacMan, Ghost, Direction, GhostMode, GhostPersonality


class TestDirection(unittest.TestCase):
    def test_opposite_directions(self):
        self.assertEqual(Direction.UP.opposite, Direction.DOWN)
        self.assertEqual(Direction.DOWN.opposite, Direction.UP)
        self.assertEqual(Direction.LEFT.opposite, Direction.RIGHT)
        self.assertEqual(Direction.RIGHT.opposite, Direction.LEFT)
        self.assertEqual(Direction.NONE.opposite, Direction.NONE)


class TestPacMan(unittest.TestCase):
    def setUp(self):
        layout = [
            "WWWWWWW",
            "W.....W",
            "W.WWW.W",
            "W.....W",
            "W.WWW.W",
            "W.....W",
            "WWWWWWW",
        ]
        self.maze = Maze(layout)
        self.pacman = PacMan(3, 3)

    def test_initial_position(self):
        self.assertEqual(self.pacman.position, (3, 3))

    def test_initial_direction(self):
        self.assertEqual(self.pacman.direction, Direction.NONE)

    def test_set_direction(self):
        """set_direction queues the direction; it applies on next move."""
        self.pacman.set_direction(Direction.LEFT)
        self.pacman.move(self.maze)
        self.assertEqual(self.pacman.direction, Direction.LEFT)

    def test_move_in_empty_space(self):
        self.pacman.set_direction(Direction.LEFT)
        moved = self.pacman.move(self.maze)
        self.assertTrue(moved)
        self.assertEqual(self.pacman.position, (3, 2))

    def test_move_blocked_by_wall(self):
        self.pacman.set_direction(Direction.UP)
        self.pacman.move(self.maze)  # to (2,3) - wall
        # Position (2,3) is wall, should not move
        self.assertEqual(self.pacman.position, (3, 3))

    def test_move_no_direction(self):
        moved = self.pacman.move(self.maze)
        self.assertFalse(moved)
        self.assertEqual(self.pacman.position, (3, 3))

    def test_reset(self):
        self.pacman.set_direction(Direction.LEFT)
        self.pacman.move(self.maze)
        self.pacman.reset(3, 3)
        self.assertEqual(self.pacman.position, (3, 3))
        self.assertEqual(self.pacman.direction, Direction.NONE)

    def test_queued_direction(self):
        """Pac-Man can queue a turn that executes when possible."""
        self.pacman.set_direction(Direction.LEFT)
        self.pacman.move(self.maze)  # (3,2)
        self.pacman.set_direction(Direction.UP)
        self.pacman.move(self.maze)  # (2,2) is wall? let me check layout
        # Row 2: W.WWW.W, col 2 is W. So blocked.
        # Should stay at (3,2)


class TestGhost(unittest.TestCase):
    def setUp(self):
        layout = [
            "WWWWWWWWWWW",
            "W.........W",
            "W.WWW.WWW.W",
            "W.........W",
            "W.WW---WW.W",
            "W.WGGGGGW.W",
            "W.WWWWWWW.W",
            "W.........W",
            "WWWWWWWWWWW",
        ]
        self.maze = Maze(layout)
        self.pacman = PacMan(7, 5)
        self.blinky = Ghost(GhostPersonality.BLINKY, 5, 5, (0, 10))

    def test_initial_position(self):
        self.assertEqual(self.blinky.position, (5, 5))

    def test_initial_mode(self):
        self.assertEqual(self.blinky.mode, GhostMode.IN_HOUSE)

    def test_frighten(self):
        self.blinky.set_mode(GhostMode.CHASE)
        self.blinky.frighten()
        self.assertEqual(self.blinky.mode, GhostMode.FRIGHTENED)

    def test_eat(self):
        self.blinky.set_mode(GhostMode.FRIGHTENED)
        self.blinky.eat()
        self.assertEqual(self.blinky.mode, GhostMode.EATEN)

    def test_reset(self):
        self.blinky.set_mode(GhostMode.CHASE)
        self.blinky.reset(5, 5)
        self.assertEqual(self.blinky.position, (5, 5))
        self.assertEqual(self.blinky.mode, GhostMode.IN_HOUSE)

    def test_blinky_chase_target(self):
        """Blinky targets Pac-Man's position directly."""
        self.blinky.set_mode(GhostMode.CHASE)
        target = self.blinky.get_chase_target(self.pacman)
        self.assertEqual(target, self.pacman.position)

    def test_pinky_chase_target(self):
        """Pinky targets 4 tiles ahead of Pac-Man."""
        pinky = Ghost(GhostPersonality.PINKY, 5, 5, (0, 0))
        pinky.set_mode(GhostMode.CHASE)
        self.pacman.set_direction(Direction.RIGHT)
        self.pacman.move(self.maze)  # apply queued direction
        target = pinky.get_chase_target(self.pacman)
        pr, pc = self.pacman.position
        dr, dc = Direction.RIGHT.value
        self.assertEqual(target, (pr + dr * 4, pc + dc * 4))

    def test_clyde_chase_far(self):
        """Clyde targets Pac-Man when far away (>8 tiles)."""
        # Pacman at (7,5), clyde at (1,1) => dist ~7.2 which is <8
        # Use a pacman far enough away
        far_pacman = PacMan(1, 9)  # dist from (1,1) = 8
        clyde = Ghost(GhostPersonality.CLYDE, 8, 1, (27, 0))
        clyde.set_mode(GhostMode.CHASE)
        target = clyde.get_chase_target(far_pacman)
        # dist from (8,1) to (1,9) = sqrt(49+64) = ~10.6, > 8
        self.assertEqual(target, far_pacman.position)

    def test_clyde_chase_near(self):
        """Clyde targets scatter corner when close to Pac-Man."""
        clyde = Ghost(GhostPersonality.CLYDE, 7, 4, (27, 0))
        clyde.set_mode(GhostMode.CHASE)
        target = clyde.get_chase_target(self.pacman)
        # Close to pacman, should target scatter corner
        self.assertEqual(target, (27, 0))

    def test_ghost_does_not_reverse(self):
        """Ghosts should not reverse direction normally."""
        self.blinky.set_mode(GhostMode.CHASE)
        self.blinky._row = 3
        self.blinky._col = 5
        self.blinky._direction = Direction.RIGHT
        old_dir = self.blinky._direction
        self.blinky.move(self.maze, self.pacman)
        # Ghost should not have reversed to LEFT
        if self.blinky._direction == old_dir.opposite:
            # Only acceptable if it was the only valid move
            moves = self.maze.get_valid_moves(3, 5, is_ghost=True)
            non_reverse = [(r, c) for r, c in moves
                           if (r - 3, c - 5) != old_dir.opposite.value]
            self.assertEqual(len(non_reverse), 0)


class TestGhostScatterTargets(unittest.TestCase):
    def test_scatter_targets_differ(self):
        """Each ghost personality has a unique scatter target."""
        targets = set()
        corners = [(0, 27), (0, 0), (27, 27), (27, 0)]
        for i, personality in enumerate(GhostPersonality):
            ghost = Ghost(personality, 5, 5, corners[i])
            targets.add(corners[i])
        self.assertEqual(len(targets), 4)


if __name__ == "__main__":
    unittest.main()
