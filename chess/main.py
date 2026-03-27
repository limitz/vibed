"""Chess game entry point."""

import curses

from input_handler import GameLoop


def main(stdscr: 'curses.window') -> None:
    """Main function called by curses.wrapper."""
    game_loop = GameLoop(stdscr)
    game_loop.run()


if __name__ == '__main__':
    curses.wrapper(main)
