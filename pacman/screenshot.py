"""Generate a screenshot of the Pac-Man game as screenshot.png."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw, ImageFont
from game import Game, GameState
from entities import Direction, GhostMode, GhostPersonality
from renderer import Renderer, COLORS_RGB, PACMAN_CHARS, GHOST_CHAR, WALL_CHAR, PELLET_CHAR, POWER_PELLET_CHAR, GHOST_DOOR_CHAR
from maze import Tile

# Cell dimensions
CELL_W = 10
CELL_H = 18

# Try to load a monospace font
FONT = None
FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
    "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
]
for fp in FONT_PATHS:
    if os.path.exists(fp):
        FONT = ImageFont.truetype(fp, 14)
        break
if FONT is None:
    FONT = ImageFont.load_default()


def setup_demo_state():
    """Set up a realistic mid-game demo state."""
    game = Game()
    game.start()

    # Simulate some gameplay to eat some pellets
    game.handle_input(Direction.LEFT)
    for _ in range(8):
        game.update()

    game.handle_input(Direction.DOWN)
    for _ in range(3):
        game.update()

    game.handle_input(Direction.LEFT)
    for _ in range(5):
        game.update()

    game.handle_input(Direction.DOWN)
    for _ in range(2):
        game.update()

    game.handle_input(Direction.RIGHT)
    for _ in range(10):
        game.update()

    game.handle_input(Direction.UP)
    for _ in range(8):
        game.update()

    game.handle_input(Direction.LEFT)
    for _ in range(14):
        game.update()

    game.handle_input(Direction.UP)
    for _ in range(6):
        game.update()

    game.handle_input(Direction.RIGHT)
    for _ in range(10):
        game.update()

    # Now adjust ghosts for a nice screenshot at valid walkable positions
    pr, pc = game.pacman.position

    # Blinky (red) - chasing from a corridor behind pac-man
    blinky = game.ghosts[0]
    blinky._mode = GhostMode.CHASE
    blinky._row = 19
    blinky._col = 21
    blinky._direction = Direction.LEFT

    # Pinky (pink) - approaching from above
    pinky = game.ghosts[1]
    pinky._mode = GhostMode.CHASE
    pinky._row = 19
    pinky._col = 6
    pinky._direction = Direction.RIGHT

    # Inky (cyan) - frightened, running away
    inky = game.ghosts[2]
    inky._mode = GhostMode.FRIGHTENED
    inky._row = 24
    inky._col = 6
    inky._direction = Direction.LEFT

    # Clyde (orange) - in scatter mode
    clyde = game.ghosts[3]
    clyde._mode = GhostMode.SCATTER
    clyde._row = 7
    clyde._col = 1
    clyde._direction = Direction.RIGHT

    # Set score and state for a nice look
    game._score = 1870
    game._lives = 3
    game._state = GameState.PLAYING

    # Make pacman face right for the classic look
    game.pacman._direction = Direction.RIGHT

    return game


def render_buffer(game):
    """Build the text buffer from game state."""
    maze = game.maze
    bg = COLORS_RGB['bg']
    total_rows = maze.height + 3
    total_cols = maze.width

    buffer = [[('' , (0,0,0), (0,0,0)) for _ in range(total_cols)] for _ in range(total_rows)]

    # Draw maze tiles
    for r in range(maze.height):
        for c in range(maze.width):
            tile = maze.get_tile(r, c)
            if tile == Tile.WALL:
                buffer[r][c] = (WALL_CHAR, COLORS_RGB['wall'], bg)
            elif tile == Tile.PELLET:
                buffer[r][c] = (PELLET_CHAR, COLORS_RGB['pellet'], bg)
            elif tile == Tile.POWER_PELLET:
                buffer[r][c] = (POWER_PELLET_CHAR, COLORS_RGB['power_pellet'], bg)
            elif tile == Tile.GHOST_DOOR:
                buffer[r][c] = (GHOST_DOOR_CHAR, COLORS_RGB['ghost_door'], bg)
            else:
                buffer[r][c] = (' ', bg, bg)

    # Draw ghosts
    for ghost in game.ghosts:
        gr, gc = ghost.position
        if 0 <= gr < maze.height and 0 <= gc < maze.width:
            if ghost.mode == GhostMode.FRIGHTENED:
                fg = COLORS_RGB['frightened']
            elif ghost.mode == GhostMode.EATEN:
                fg = COLORS_RGB['eaten']
            else:
                personality_map = {
                    GhostPersonality.BLINKY: 'blinky',
                    GhostPersonality.PINKY: 'pinky',
                    GhostPersonality.INKY: 'inky',
                    GhostPersonality.CLYDE: 'clyde',
                }
                fg = COLORS_RGB[personality_map[ghost.personality]]
            ch = GHOST_CHAR if ghost.mode != GhostMode.EATEN else '"'
            buffer[gr][gc] = (ch, fg, bg)

    # Draw Pac-Man
    pr, pc = game.pacman.position
    if 0 <= pr < maze.height and 0 <= pc < maze.width:
        ch = PACMAN_CHARS.get(game.pacman.direction, '>')
        buffer[pr][pc] = (ch, COLORS_RGB['pacman'], bg)

    # HUD
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

    return buffer, total_rows, total_cols


def render_to_image(buffer, total_rows, total_cols):
    """Render the character buffer to a PIL Image."""
    img_w = total_cols * CELL_W
    img_h = total_rows * CELL_H
    img = Image.new('RGB', (img_w, img_h), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    for r in range(total_rows):
        for c in range(total_cols):
            ch, fg, bg_color = buffer[r][c]
            x = c * CELL_W
            y = r * CELL_H

            # Draw background
            if bg_color != (0, 0, 0):
                draw.rectangle([x, y, x + CELL_W - 1, y + CELL_H - 1], fill=bg_color)

            # Draw character
            if ch and ch.strip():
                draw.text((x + 1, y + 1), ch, fill=fg, font=FONT)

    return img


def main():
    game = setup_demo_state()
    buffer, total_rows, total_cols = render_buffer(game)
    img = render_to_image(buffer, total_rows, total_cols)

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshot.png')
    img.save(output_path)
    print(f"Screenshot saved to {output_path}")
    print(f"Image size: {img.size}")


if __name__ == "__main__":
    main()
