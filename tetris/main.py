"""Tetris - Entry point."""

import curses
from input_handler import GameLoop


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    loop = GameLoop(stdscr)
    loop.run()


if __name__ == "__main__":
    curses.wrapper(main)
