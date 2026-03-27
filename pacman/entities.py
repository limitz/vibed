"""Entities module - Pac-Man and Ghost game objects with movement and AI."""

from enum import Enum, auto
from typing import Tuple, Optional, List
import random
import math

from maze import Maze


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    NONE = (0, 0)

    @property
    def opposite(self) -> 'Direction':
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
            Direction.NONE: Direction.NONE,
        }
        return opposites[self]


class GhostMode(Enum):
    CHASE = auto()
    SCATTER = auto()
    FRIGHTENED = auto()
    EATEN = auto()
    IN_HOUSE = auto()
    LEAVING_HOUSE = auto()


class GhostPersonality(Enum):
    BLINKY = auto()
    PINKY = auto()
    INKY = auto()
    CLYDE = auto()


def _distance(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


class PacMan:
    """The player-controlled Pac-Man character."""

    def __init__(self, start_row: int, start_col: int):
        self._row = start_row
        self._col = start_col
        self._direction = Direction.NONE
        self._next_direction = Direction.NONE

    @property
    def position(self) -> Tuple[int, int]:
        return (self._row, self._col)

    @property
    def direction(self) -> Direction:
        return self._direction

    def set_direction(self, direction: Direction) -> None:
        self._next_direction = direction

    def move(self, maze: Maze) -> bool:
        # Try queued direction first
        if self._next_direction != Direction.NONE:
            dr, dc = self._next_direction.value
            nr, nc = maze.wrap_position(self._row + dr, self._col + dc)
            if maze.is_walkable(nr, nc):
                self._direction = self._next_direction
                self._next_direction = Direction.NONE
                self._row, self._col = nr, nc
                return True

        # Otherwise continue in current direction
        if self._direction != Direction.NONE:
            dr, dc = self._direction.value
            nr, nc = maze.wrap_position(self._row + dr, self._col + dc)
            if maze.is_walkable(nr, nc):
                self._row, self._col = nr, nc
                return True

        return False

    def reset(self, start_row: int, start_col: int) -> None:
        self._row = start_row
        self._col = start_col
        self._direction = Direction.NONE
        self._next_direction = Direction.NONE


class Ghost:
    """A ghost enemy with AI behavior."""

    def __init__(self, personality: GhostPersonality, start_row: int, start_col: int,
                 scatter_target: Tuple[int, int]):
        self._personality = personality
        self._row = start_row
        self._col = start_col
        self._start_row = start_row
        self._start_col = start_col
        self._scatter_target = scatter_target
        self._mode = GhostMode.IN_HOUSE
        self._direction = Direction.NONE

    @property
    def position(self) -> Tuple[int, int]:
        return (self._row, self._col)

    @property
    def mode(self) -> GhostMode:
        return self._mode

    @property
    def personality(self) -> GhostPersonality:
        return self._personality

    def set_mode(self, mode: GhostMode) -> None:
        old_mode = self._mode
        self._mode = mode
        # Reverse direction on mode change (chase <-> scatter)
        if (old_mode in (GhostMode.CHASE, GhostMode.SCATTER) and
                mode in (GhostMode.CHASE, GhostMode.SCATTER) and old_mode != mode):
            self._direction = self._direction.opposite

    def get_chase_target(self, pacman: PacMan, blinky_pos: Optional[Tuple[int, int]] = None) -> Tuple[int, int]:
        pr, pc = pacman.position

        if self._personality == GhostPersonality.BLINKY:
            return (pr, pc)

        elif self._personality == GhostPersonality.PINKY:
            dr, dc = pacman.direction.value
            return (pr + dr * 4, pc + dc * 4)

        elif self._personality == GhostPersonality.INKY:
            dr, dc = pacman.direction.value
            ahead_r, ahead_c = pr + dr * 2, pc + dc * 2
            if blinky_pos:
                br, bc = blinky_pos
                return (ahead_r + (ahead_r - br), ahead_c + (ahead_c - bc))
            return (pr, pc)

        elif self._personality == GhostPersonality.CLYDE:
            dist = _distance((self._row, self._col), (pr, pc))
            if dist > 8:
                return (pr, pc)
            else:
                return self._scatter_target

        return (pr, pc)

    def _get_target(self, pacman: PacMan, blinky_pos: Optional[Tuple[int, int]] = None) -> Tuple[int, int]:
        if self._mode == GhostMode.CHASE:
            return self.get_chase_target(pacman, blinky_pos)
        elif self._mode == GhostMode.SCATTER:
            return self._scatter_target
        elif self._mode == GhostMode.EATEN:
            # Target ghost house door area
            return (11, 13)  # approximate door position for classic layout
        else:
            # Frightened - random, handled in move
            return (0, 0)

    def move(self, maze: Maze, pacman: PacMan, blinky_pos: Optional[Tuple[int, int]] = None) -> None:
        if self._mode == GhostMode.IN_HOUSE:
            return

        if self._mode == GhostMode.LEAVING_HOUSE:
            door = maze.get_ghost_door_position()
            if door:
                # First align to door column
                if self._col < door[1]:
                    self._col += 1
                elif self._col > door[1]:
                    self._col -= 1
                # Then move up through door
                elif self._row > door[0] - 1:
                    self._row -= 1
                else:
                    # Above the door, now in the maze
                    self._mode = GhostMode.SCATTER
                    self._direction = Direction.LEFT
            return

        # Get valid moves (excluding current position and reverse for non-frightened)
        valid_moves = maze.get_valid_moves(self._row, self._col, is_ghost=(self._mode == GhostMode.EATEN))

        if not valid_moves:
            return

        # Filter out reverse direction (ghosts can't reverse unless mode just changed)
        if self._direction != Direction.NONE and len(valid_moves) > 1:
            dr, dc = self._direction.opposite.value
            reverse_pos = maze.wrap_position(self._row + dr, self._col + dc)
            valid_moves = [m for m in valid_moves if m != reverse_pos] or valid_moves

        if self._mode == GhostMode.FRIGHTENED:
            # Random movement when frightened
            chosen = random.choice(valid_moves)
        else:
            # Move toward target
            target = self._get_target(pacman, blinky_pos)
            chosen = min(valid_moves, key=lambda pos: _distance(pos, target))

        # Update direction based on movement
        dr = chosen[0] - self._row
        dc = chosen[1] - self._col
        # Handle wrapping
        if abs(dc) > 1:
            dc = 1 if dc < 0 else -1
        if abs(dr) > 1:
            dr = 1 if dr < 0 else -1
        for d in Direction:
            if d.value == (dr, dc):
                self._direction = d
                break

        self._row, self._col = chosen

        # If eaten ghost reached house, respawn
        if self._mode == GhostMode.EATEN:
            house_positions = maze.get_ghost_house_positions()
            if (self._row, self._col) in house_positions or _distance(
                    (self._row, self._col), (13, 13)) < 2:
                self._mode = GhostMode.LEAVING_HOUSE

    def reset(self, start_row: int, start_col: int) -> None:
        self._row = start_row
        self._col = start_col
        self._mode = GhostMode.IN_HOUSE
        self._direction = Direction.NONE

    def frighten(self) -> None:
        if self._mode in (GhostMode.CHASE, GhostMode.SCATTER):
            self._mode = GhostMode.FRIGHTENED
            self._direction = self._direction.opposite

    def eat(self) -> None:
        self._mode = GhostMode.EATEN
