"""Renderer module - curses-based terminal rendering for the Pac-Man game."""

import curses
from typing import Optional, List, Tuple

from maze import Maze, Tile
from entities import PacMan, Ghost, GhostMode, Direction, GhostPersonality
from game import Game, GameState


# Color pair IDs
COLOR_WALL = 1
COLOR_PELLET = 2
COLOR_POWER_PELLET = 3
COLOR_PACMAN = 4
COLOR_BLINKY = 5   # Red
COLOR_PINKY = 6    # Pink/Magenta
COLOR_INKY = 7     # Cyan
COLOR_CLYDE = 8    # Yellow/Orange
COLOR_FRIGHTENED = 9
COLOR_EATEN = 10
COLOR_HUD = 11
COLOR_READY = 12
COLOR_GAMEOVER = 13
COLOR_GHOST_DOOR = 14

# Character representations
WALL_CHAR = '#'
PELLET_CHAR = '.'
POWER_PELLET_CHAR = 'o'
PACMAN_CHARS = {
    Direction.RIGHT: '>',
    Direction.LEFT: '<',
    Direction.UP: 'V',
    Direction.DOWN: '^',
    Direction.NONE: '>',
}
GHOST_CHAR = 'M'
GHOST_DOOR_CHAR = '-'
EMPTY_CHAR = ' '
EYES_CHAR = '"'

# RGB-like color constants for screenshot
COLORS_RGB = {
    'wall': (33, 33, 222),       # Blue
    'pellet': (255, 183, 174),   # Peach
    'power_pellet': (255, 183, 174),
    'pacman': (255, 255, 0),     # Yellow
    'blinky': (255, 0, 0),       # Red
    'pinky': (255, 184, 255),    # Pink
    'inky': (0, 255, 255),       # Cyan
    'clyde': (255, 184, 82),     # Orange
    'frightened': (33, 33, 222), # Blue
    'eaten': (255, 255, 255),    # White
    'hud': (255, 255, 255),      # White
    'ready': (255, 255, 0),      # Yellow
    'gameover': (255, 0, 0),     # Red
    'ghost_door': (255, 184, 255),
    'bg': (0, 0, 0),            # Black
    'empty': (0, 0, 0),
}


class Renderer:
    """Handles all curses-based rendering for the game."""

    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr
        self.offset_row = 1
        self.offset_col = 1
        self._init_colors()

    def _init_colors(self) -> None:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(COLOR_WALL, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PELLET, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(COLOR_POWER_PELLET, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PACMAN, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(COLOR_BLINKY, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PINKY, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(COLOR_INKY, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(COLOR_CLYDE, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(COLOR_FRIGHTENED, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(COLOR_EATEN, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(COLOR_HUD, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(COLOR_READY, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(COLOR_GAMEOVER, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(COLOR_GHOST_DOOR, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    def draw(self, game: Game) -> None:
        self.stdscr.erase()
        self._draw_maze(game)
        self._draw_entities(game)
        self._draw_hud(game)

        if game.state == GameState.READY:
            self._draw_ready()
        elif game.state == GameState.GAME_OVER:
            self._draw_game_over()
        elif game.state == GameState.PAUSED:
            self._draw_paused()

        self.stdscr.refresh()

    def _draw_maze(self, game: Game) -> None:
        maze = game.maze
        for r in range(maze.height):
            for c in range(maze.width):
                tile = maze.get_tile(r, c)
                ch, color = self._tile_to_char(tile)
                try:
                    self.stdscr.addstr(
                        r + self.offset_row, c + self.offset_col,
                        ch, curses.color_pair(color)
                    )
                except curses.error:
                    pass

    def _tile_to_char(self, tile: Tile) -> Tuple[str, int]:
        if tile == Tile.WALL:
            return WALL_CHAR, COLOR_WALL
        elif tile == Tile.PELLET:
            return PELLET_CHAR, COLOR_PELLET
        elif tile == Tile.POWER_PELLET:
            return POWER_PELLET_CHAR, COLOR_POWER_PELLET
        elif tile == Tile.GHOST_DOOR:
            return GHOST_DOOR_CHAR, COLOR_GHOST_DOOR
        elif tile == Tile.GHOST_HOUSE:
            return EMPTY_CHAR, 0
        else:
            return EMPTY_CHAR, 0

    def _draw_entities(self, game: Game) -> None:
        # Draw Pac-Man
        pr, pc = game.pacman.position
        ch = PACMAN_CHARS.get(game.pacman.direction, '>')
        try:
            self.stdscr.addstr(
                pr + self.offset_row, pc + self.offset_col,
                ch, curses.color_pair(COLOR_PACMAN) | curses.A_BOLD
            )
        except curses.error:
            pass

        # Draw ghosts
        for ghost in game.ghosts:
            gr, gc = ghost.position
            ch, color = self._ghost_char_color(ghost)
            try:
                self.stdscr.addstr(
                    gr + self.offset_row, gc + self.offset_col,
                    ch, curses.color_pair(color) | curses.A_BOLD
                )
            except curses.error:
                pass

    def _ghost_char_color(self, ghost: Ghost) -> Tuple[str, int]:
        if ghost.mode == GhostMode.FRIGHTENED:
            return GHOST_CHAR, COLOR_FRIGHTENED
        elif ghost.mode == GhostMode.EATEN:
            return EYES_CHAR, COLOR_EATEN
        elif ghost.mode in (GhostMode.IN_HOUSE, GhostMode.LEAVING_HOUSE):
            return GHOST_CHAR, self.get_color_pair(ghost.personality)
        else:
            return GHOST_CHAR, self.get_color_pair(ghost.personality)

    def _draw_hud(self, game: Game) -> None:
        hud_row = game.maze.height + self.offset_row + 1
        # Score
        score_text = f"SCORE: {game.score:>6}"
        try:
            self.stdscr.addstr(
                hud_row, self.offset_col,
                score_text, curses.color_pair(COLOR_HUD) | curses.A_BOLD
            )
        except curses.error:
            pass

        # Lives
        lives_text = f"LIVES: {'> ' * game.lives}"
        try:
            self.stdscr.addstr(
                hud_row, self.offset_col + 16,
                lives_text, curses.color_pair(COLOR_PACMAN)
            )
        except curses.error:
            pass

        # Level
        level_text = f"LVL: {game.level}"
        try:
            self.stdscr.addstr(
                hud_row + 1, self.offset_col,
                level_text, curses.color_pair(COLOR_HUD)
            )
        except curses.error:
            pass

    def _draw_game_over(self) -> None:
        text = "GAME OVER"
        row = 15 + self.offset_row
        col = 10 + self.offset_col
        try:
            self.stdscr.addstr(
                row, col, text,
                curses.color_pair(COLOR_GAMEOVER) | curses.A_BOLD
            )
        except curses.error:
            pass

    def _draw_ready(self) -> None:
        text = "READY!"
        row = 16 + self.offset_row
        col = 11 + self.offset_col
        try:
            self.stdscr.addstr(
                row, col, text,
                curses.color_pair(COLOR_READY) | curses.A_BOLD
            )
        except curses.error:
            pass

    def _draw_paused(self) -> None:
        text = "PAUSED"
        row = 15 + self.offset_row
        col = 11 + self.offset_col
        try:
            self.stdscr.addstr(
                row, col, text,
                curses.color_pair(COLOR_READY) | curses.A_BOLD
            )
        except curses.error:
            pass

    def get_color_pair(self, personality: Optional[GhostPersonality] = None,
                       mode: Optional[GhostMode] = None) -> int:
        if mode == GhostMode.FRIGHTENED:
            return COLOR_FRIGHTENED
        if mode == GhostMode.EATEN:
            return COLOR_EATEN
        if personality == GhostPersonality.BLINKY:
            return COLOR_BLINKY
        elif personality == GhostPersonality.PINKY:
            return COLOR_PINKY
        elif personality == GhostPersonality.INKY:
            return COLOR_INKY
        elif personality == GhostPersonality.CLYDE:
            return COLOR_CLYDE
        return COLOR_HUD

    def draw_to_buffer(self, game: Game) -> List[List[Tuple[str, Tuple[int, int, int], Tuple[int, int, int]]]]:
        """Draw game state to a character buffer for screenshot generation.
        Returns 2D grid of (char, fg_rgb, bg_rgb) tuples."""
        maze = game.maze
        bg = COLORS_RGB['bg']

        # Total rows: maze height + 3 (HUD)
        total_rows = maze.height + 3
        total_cols = maze.width

        buffer = [[(EMPTY_CHAR, COLORS_RGB['empty'], bg) for _ in range(total_cols)]
                  for _ in range(total_rows)]

        # Draw maze
        for r in range(maze.height):
            for c in range(maze.width):
                tile = maze.get_tile(r, c)
                ch, fg = self._tile_to_char_rgb(tile)
                buffer[r][c] = (ch, fg, bg)

        # Draw ghosts
        for ghost in game.ghosts:
            gr, gc = ghost.position
            if 0 <= gr < maze.height and 0 <= gc < maze.width:
                ch, fg = self._ghost_char_color_rgb(ghost)
                buffer[gr][gc] = (ch, fg, bg)

        # Draw Pac-Man
        pr, pc = game.pacman.position
        if 0 <= pr < maze.height and 0 <= pc < maze.width:
            ch = PACMAN_CHARS.get(game.pacman.direction, '>')
            buffer[pr][pc] = (ch, COLORS_RGB['pacman'], bg)

        # Draw HUD
        hud_row = maze.height + 1
        score_text = f"SCORE: {game.score:>6}"
        for i, ch in enumerate(score_text):
            if i < total_cols:
                buffer[hud_row][i] = (ch, COLORS_RGB['hud'], bg)

        lives_text = f"LIVES: {'> ' * game.lives}"
        for i, ch in enumerate(lives_text):
            col = 16 + i
            if col < total_cols:
                buffer[hud_row][col] = (ch, COLORS_RGB['pacman'], bg)

        level_text = f"LVL: {game.level}"
        for i, ch in enumerate(level_text):
            if i < total_cols:
                buffer[hud_row + 1][i] = (ch, COLORS_RGB['hud'], bg)

        # Draw overlays
        if game.state == GameState.READY:
            self._overlay_text(buffer, 16, 11, "READY!", COLORS_RGB['ready'])
        elif game.state == GameState.GAME_OVER:
            self._overlay_text(buffer, 15, 10, "GAME OVER", COLORS_RGB['gameover'])

        return buffer

    def _overlay_text(self, buffer, row, col, text, fg):
        bg = COLORS_RGB['bg']
        for i, ch in enumerate(text):
            c = col + i
            if 0 <= row < len(buffer) and 0 <= c < len(buffer[0]):
                buffer[row][c] = (ch, fg, bg)

    def _tile_to_char_rgb(self, tile: Tile) -> Tuple[str, Tuple[int, int, int]]:
        if tile == Tile.WALL:
            return WALL_CHAR, COLORS_RGB['wall']
        elif tile == Tile.PELLET:
            return PELLET_CHAR, COLORS_RGB['pellet']
        elif tile == Tile.POWER_PELLET:
            return POWER_PELLET_CHAR, COLORS_RGB['power_pellet']
        elif tile == Tile.GHOST_DOOR:
            return GHOST_DOOR_CHAR, COLORS_RGB['ghost_door']
        elif tile == Tile.GHOST_HOUSE:
            return EMPTY_CHAR, COLORS_RGB['empty']
        else:
            return EMPTY_CHAR, COLORS_RGB['empty']

    def _ghost_char_color_rgb(self, ghost: Ghost) -> Tuple[str, Tuple[int, int, int]]:
        if ghost.mode == GhostMode.FRIGHTENED:
            return GHOST_CHAR, COLORS_RGB['frightened']
        elif ghost.mode == GhostMode.EATEN:
            return EYES_CHAR, COLORS_RGB['eaten']
        else:
            personality_colors = {
                GhostPersonality.BLINKY: 'blinky',
                GhostPersonality.PINKY: 'pinky',
                GhostPersonality.INKY: 'inky',
                GhostPersonality.CLYDE: 'clyde',
            }
            key = personality_colors.get(ghost.personality, 'blinky')
            return GHOST_CHAR, COLORS_RGB[key]
