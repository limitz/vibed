"""Main module - entry point, game loop, and input handling."""

import curses
import time

from game import Game, GameState
from entities import Direction
from renderer import Renderer


TICK_RATE = 0.1  # seconds per game tick

KEY_MAP = {
    curses.KEY_UP: Direction.UP,
    curses.KEY_DOWN: Direction.DOWN,
    curses.KEY_LEFT: Direction.LEFT,
    curses.KEY_RIGHT: Direction.RIGHT,
    ord('w'): Direction.UP,
    ord('s'): Direction.DOWN,
    ord('a'): Direction.LEFT,
    ord('d'): Direction.RIGHT,
    ord('W'): Direction.UP,
    ord('S'): Direction.DOWN,
    ord('A'): Direction.LEFT,
    ord('D'): Direction.RIGHT,
}


def main(stdscr: curses.window) -> None:
    """Main game loop."""
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(int(TICK_RATE * 1000))

    game = Game()
    renderer = Renderer(stdscr)

    running = True
    while running:
        # Handle input
        running = handle_input(stdscr, game)

        # Update game state
        game.update()

        # Render
        renderer.draw(game)

        # Check for restart on game over
        if game.state == GameState.GAME_OVER:
            # Wait for key to restart or quit
            stdscr.timeout(-1)  # blocking
            key = stdscr.getch()
            if key == ord('q') or key == ord('Q') or key == 27:
                running = False
            else:
                game = Game()
                game.start()
                stdscr.timeout(int(TICK_RATE * 1000))


def handle_input(stdscr: curses.window, game: Game) -> bool:
    """Process keyboard input. Returns False to quit."""
    key = stdscr.getch()

    if key == ord('q') or key == ord('Q') or key == 27:  # q, Q, ESC
        return False

    if key == ord('p') or key == ord('P'):
        game.toggle_pause()
        return True

    if key == ord('r') or key == ord('R'):
        if game.state == GameState.GAME_OVER:
            game.__init__()
            game.start()
        return True

    direction = KEY_MAP.get(key)
    if direction:
        game.handle_input(direction)

    return True


if __name__ == "__main__":
    curses.wrapper(main)
