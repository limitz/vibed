"""Tests for the maze module."""

import unittest
from maze import Maze, Tile, CLASSIC_LAYOUT


class TestMazeInit(unittest.TestCase):
    """Test maze initialization and layout parsing."""

    def test_default_layout(self):
        """Maze initializes with classic layout by default."""
        maze = Maze()
        self.assertEqual(maze.width, 28)
        self.assertEqual(maze.height, 28)

    def test_custom_layout(self):
        """Maze can be initialized with a custom layout."""
        layout = [
            "WWWWW",
            "W...W",
            "W.W.W",
            "W...W",
            "WWWWW",
        ]
        maze = Maze(layout)
        self.assertEqual(maze.width, 5)
        self.assertEqual(maze.height, 5)

    def test_walls_parsed(self):
        """Walls are correctly identified."""
        maze = Maze()
        # Corners should be walls
        self.assertTrue(maze.is_wall(0, 0))
        self.assertTrue(maze.is_wall(0, 27))
        self.assertTrue(maze.is_wall(27, 0))
        self.assertTrue(maze.is_wall(27, 27))

    def test_pellets_parsed(self):
        """Pellets are placed in correct positions."""
        maze = Maze()
        # Row 1 should have pellets
        self.assertEqual(maze.get_tile(1, 1), Tile.PELLET)

    def test_power_pellets_parsed(self):
        """Power pellets are placed in correct positions."""
        maze = Maze()
        # Classic layout has power pellets at specific locations
        self.assertEqual(maze.get_tile(3, 1), Tile.POWER_PELLET)

    def test_ghost_house_parsed(self):
        """Ghost house tiles are identified."""
        maze = Maze()
        # Ghost house should be in the center
        positions = maze.get_ghost_house_positions()
        self.assertTrue(len(positions) > 0)

    def test_ghost_door_parsed(self):
        """Ghost door is identified."""
        maze = Maze()
        door = maze.get_ghost_door_position()
        self.assertIsNotNone(door)


class TestMazeNavigation(unittest.TestCase):
    """Test movement and navigation in the maze."""

    def setUp(self):
        self.maze = Maze()

    def test_is_walkable_empty(self):
        """Empty spaces are walkable."""
        # Find a pellet space
        self.assertTrue(self.maze.is_walkable(1, 1))

    def test_is_not_walkable_wall(self):
        """Walls are not walkable."""
        self.assertFalse(self.maze.is_walkable(0, 0))

    def test_ghost_can_pass_door(self):
        """Ghosts can pass through the ghost door."""
        door = self.maze.get_ghost_door_position()
        if door:
            self.assertTrue(self.maze.is_walkable(door[0], door[1], is_ghost=True))

    def test_pacman_cannot_pass_door(self):
        """Pac-Man cannot pass through the ghost door."""
        door = self.maze.get_ghost_door_position()
        if door:
            self.assertFalse(self.maze.is_walkable(door[0], door[1], is_ghost=False))

    def test_valid_moves(self):
        """Get valid moves returns only walkable adjacent tiles."""
        # Position (1,1) should have at least one valid move
        moves = self.maze.get_valid_moves(1, 1)
        self.assertTrue(len(moves) > 0)
        for r, c in moves:
            self.assertTrue(self.maze.is_walkable(r, c))

    def test_wrap_position_left(self):
        """Wrapping left goes to right side."""
        r, c = self.maze.wrap_position(14, -1)
        self.assertEqual(c, self.maze.width - 1)
        self.assertEqual(r, 14)

    def test_wrap_position_right(self):
        """Wrapping right goes to left side."""
        r, c = self.maze.wrap_position(14, self.maze.width)
        self.assertEqual(c, 0)
        self.assertEqual(r, 14)

    def test_wrap_position_normal(self):
        """Non-edge positions are not wrapped."""
        r, c = self.maze.wrap_position(5, 5)
        self.assertEqual((r, c), (5, 5))


class TestMazePellets(unittest.TestCase):
    """Test pellet management."""

    def setUp(self):
        self.maze = Maze()

    def test_initial_pellet_count(self):
        """Maze starts with correct number of pellets."""
        count = self.maze.remaining_pellets()
        self.assertTrue(count > 0)

    def test_eat_pellet(self):
        """Eating a pellet removes it and returns pellet type."""
        initial = self.maze.remaining_pellets()
        result = self.maze.eat_pellet(1, 1)
        self.assertEqual(result, Tile.PELLET)
        self.assertEqual(self.maze.remaining_pellets(), initial - 1)

    def test_eat_power_pellet(self):
        """Eating a power pellet returns POWER_PELLET."""
        result = self.maze.eat_pellet(3, 1)
        self.assertEqual(result, Tile.POWER_PELLET)

    def test_eat_empty(self):
        """Eating from empty space returns None."""
        result = self.maze.eat_pellet(0, 0)
        self.assertIsNone(result)

    def test_eat_pellet_twice(self):
        """Eating same position twice returns None the second time."""
        self.maze.eat_pellet(1, 1)
        result = self.maze.eat_pellet(1, 1)
        self.assertIsNone(result)

    def test_reset_restores_pellets(self):
        """Reset restores all pellets."""
        initial = self.maze.remaining_pellets()
        self.maze.eat_pellet(1, 1)
        self.maze.reset()
        self.assertEqual(self.maze.remaining_pellets(), initial)


if __name__ == "__main__":
    unittest.main()
