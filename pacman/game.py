"""Game logic module - manages game state, scoring, lives, and level progression."""

from typing import List, Optional, Tuple
from enum import Enum, auto

from maze import Maze, Tile
from entities import PacMan, Ghost, GhostPersonality, GhostMode, Direction


class GameState(Enum):
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    WON_LEVEL = auto()
    READY = auto()


PELLET_SCORE = 10
POWER_PELLET_SCORE = 50
GHOST_SCORES = [200, 400, 800, 1600]

FRIGHTENED_DURATION = 40
GHOST_RELEASE_TIMES = [0, 30, 60, 90]

# Pac-Man start position (below ghost house)
PACMAN_START_ROW = 21
PACMAN_START_COL = 14

# Ghost start positions (inside ghost house)
GHOST_STARTS = {
    GhostPersonality.BLINKY: (10, 14, (0, 27)),   # Red - starts above house
    GhostPersonality.PINKY: (13, 13, (0, 0)),      # Pink - top left
    GhostPersonality.INKY: (13, 14, (27, 27)),     # Cyan - bottom right
    GhostPersonality.CLYDE: (13, 15, (27, 0)),     # Orange - bottom left
}


class Game:
    """Main game controller managing all game state and logic."""

    def __init__(self):
        self.maze = Maze()
        self._state = GameState.READY
        self._score = 0
        self._lives = 3
        self._level = 1
        self._tick = 0
        self._frightened_timer = 0
        self._ghost_eat_count = 0
        self._ready_timer = 0
        self._won_timer = 0
        self.pacman: Optional[PacMan] = None
        self.ghosts: List[Ghost] = []
        self._init_entities()

    def _init_entities(self) -> None:
        self.pacman = PacMan(PACMAN_START_ROW, PACMAN_START_COL)
        self.ghosts = []
        for personality, (row, col, scatter) in GHOST_STARTS.items():
            ghost = Ghost(personality, row, col, scatter)
            # Blinky starts outside the house, already active
            if personality == GhostPersonality.BLINKY:
                ghost.set_mode(GhostMode.SCATTER)
                ghost._direction = Direction.LEFT
            self.ghosts.append(ghost)

    @property
    def state(self) -> GameState:
        return self._state

    @property
    def score(self) -> int:
        return self._score

    @property
    def lives(self) -> int:
        return self._lives

    @property
    def level(self) -> int:
        return self._level

    def update(self) -> None:
        if self._state == GameState.PAUSED:
            return

        if self._state == GameState.READY:
            self._ready_timer += 1
            if self._ready_timer >= 20:
                self._state = GameState.PLAYING
            return

        if self._state == GameState.WON_LEVEL:
            self._won_timer += 1
            if self._won_timer >= 30:
                self._advance_level()
            return

        if self._state != GameState.PLAYING:
            return

        self._tick += 1

        # Move Pac-Man
        self.pacman.move(self.maze)

        # Eat pellet at new position
        self._eat_pellet()

        # Update ghost modes and release
        self._update_ghosts()

        # Move ghosts
        blinky_pos = self.ghosts[0].position if self.ghosts else None
        for ghost in self.ghosts:
            ghost.move(self.maze, self.pacman, blinky_pos)

        # Check collisions
        self._check_collisions()

        # Check level complete
        self._check_level_complete()

        # Update frightened timer
        if self._frightened_timer > 0:
            self._frightened_timer -= 1
            if self._frightened_timer == 0:
                for ghost in self.ghosts:
                    if ghost.mode == GhostMode.FRIGHTENED:
                        ghost.set_mode(GhostMode.CHASE)
                self._ghost_eat_count = 0

    def handle_input(self, direction: Direction) -> None:
        if self._state == GameState.PLAYING:
            self.pacman.set_direction(direction)

    def _update_ghosts(self) -> None:
        for i, ghost in enumerate(self.ghosts):
            if ghost.mode == GhostMode.IN_HOUSE:
                release_time = GHOST_RELEASE_TIMES[i] if i < len(GHOST_RELEASE_TIMES) else 90
                if self._tick >= release_time:
                    ghost.set_mode(GhostMode.LEAVING_HOUSE)

        # Scatter/chase mode switching based on tick
        phase_ticks = [70, 270, 340, 540, 610, 810, 880]
        mode = GhostMode.SCATTER
        for t in phase_ticks:
            if self._tick >= t:
                mode = GhostMode.CHASE if mode == GhostMode.SCATTER else GhostMode.SCATTER
        for ghost in self.ghosts:
            if ghost.mode in (GhostMode.CHASE, GhostMode.SCATTER):
                if ghost.mode != mode:
                    ghost.set_mode(mode)

    def _check_collisions(self) -> None:
        pr, pc = self.pacman.position
        for ghost in self.ghosts:
            if ghost.position == (pr, pc):
                if ghost.mode == GhostMode.FRIGHTENED:
                    # Eat ghost
                    ghost.eat()
                    idx = min(self._ghost_eat_count, len(GHOST_SCORES) - 1)
                    self._score += GHOST_SCORES[idx]
                    self._ghost_eat_count += 1
                elif ghost.mode in (GhostMode.CHASE, GhostMode.SCATTER):
                    self._lose_life()
                    return

    def _eat_pellet(self) -> None:
        pr, pc = self.pacman.position
        pellet = self.maze.eat_pellet(pr, pc)
        if pellet == Tile.PELLET:
            self._score += PELLET_SCORE
        elif pellet == Tile.POWER_PELLET:
            self._score += POWER_PELLET_SCORE
            self._frightened_timer = FRIGHTENED_DURATION
            self._ghost_eat_count = 0
            for ghost in self.ghosts:
                ghost.frighten()

    def _check_level_complete(self) -> None:
        if self.maze.remaining_pellets() == 0:
            self._state = GameState.WON_LEVEL
            self._won_timer = 0

    def _lose_life(self) -> None:
        self._lives -= 1
        if self._lives <= 0:
            self._state = GameState.GAME_OVER
        else:
            # Reset positions
            self.pacman.reset(PACMAN_START_ROW, PACMAN_START_COL)
            for personality, (row, col, _) in GHOST_STARTS.items():
                for ghost in self.ghosts:
                    if ghost.personality == personality:
                        ghost.reset(row, col)
            self._state = GameState.READY
            self._ready_timer = 0

    def _advance_level(self) -> None:
        self._level += 1
        self.maze.reset()
        self.pacman.reset(PACMAN_START_ROW, PACMAN_START_COL)
        for personality, (row, col, _) in GHOST_STARTS.items():
            for ghost in self.ghosts:
                if ghost.personality == personality:
                    ghost.reset(row, col)
        self._tick = 0
        self._frightened_timer = 0
        self._ghost_eat_count = 0
        self._state = GameState.READY
        self._ready_timer = 0

    def start(self) -> None:
        self._state = GameState.PLAYING
        self._tick = 0

    def toggle_pause(self) -> None:
        if self._state == GameState.PLAYING:
            self._state = GameState.PAUSED
        elif self._state == GameState.PAUSED:
            self._state = GameState.PLAYING
