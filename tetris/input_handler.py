"""Input mapping and game loop."""

import curses
import time
from enum import Enum, auto
from typing import Optional

from game import GameState
from renderer import Renderer


class Action(Enum):
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    MOVE_DOWN = auto()
    ROTATE_CW = auto()
    ROTATE_CCW = auto()
    HARD_DROP = auto()
    QUIT = auto()
    PAUSE = auto()
    RESTART = auto()


KEY_MAP = {
    curses.KEY_LEFT: Action.MOVE_LEFT,
    curses.KEY_RIGHT: Action.MOVE_RIGHT,
    curses.KEY_DOWN: Action.MOVE_DOWN,
    curses.KEY_UP: Action.ROTATE_CW,
    ord('z'): Action.ROTATE_CCW,
    ord('Z'): Action.ROTATE_CCW,
    ord(' '): Action.HARD_DROP,
    ord('q'): Action.QUIT,
    ord('Q'): Action.QUIT,
    ord('p'): Action.PAUSE,
    ord('P'): Action.PAUSE,
    ord('r'): Action.RESTART,
    ord('R'): Action.RESTART,
}


def map_key(key: int) -> Optional[Action]:
    return KEY_MAP.get(key)


class GameLoop:
    def __init__(self, stdscr: curses.window, seed: Optional[int] = None):
        self.stdscr = stdscr
        self.seed = seed
        self.state = GameState(seed=seed)
        self.renderer = Renderer(stdscr)
        self.paused = False

    def run(self) -> int:
        self.stdscr.nodelay(True)
        curses.curs_set(0)
        last_tick = time.time()

        while True:
            # Handle input
            try:
                key = self.stdscr.getch()
            except curses.error:
                key = -1

            if key != -1:
                action = map_key(key)
                if action == Action.QUIT:
                    break
                if action == Action.RESTART:
                    self.state = GameState(seed=self.seed)
                    self.paused = False
                    last_tick = time.time()
                elif action == Action.PAUSE:
                    self.paused = not self.paused
                elif action is not None and not self.paused and not self.state.game_over:
                    self.handle_action(action)

            # Gravity tick
            if not self.paused and not self.state.game_over:
                now = time.time()
                interval = self.state.get_gravity_interval_ms() / 1000.0
                if now - last_tick >= interval:
                    self.state.tick()
                    last_tick = now

            # Draw
            self.renderer.draw(self.state)

            # Sleep to avoid busy loop (~60fps)
            time.sleep(0.016)

        return self.state.score

    def handle_action(self, action: Action) -> None:
        if action == Action.MOVE_LEFT:
            self.state.move_left()
        elif action == Action.MOVE_RIGHT:
            self.state.move_right()
        elif action == Action.MOVE_DOWN:
            self.state.move_down()
        elif action == Action.ROTATE_CW:
            self.state.rotate_cw()
        elif action == Action.ROTATE_CCW:
            self.state.rotate_ccw()
        elif action == Action.HARD_DROP:
            self.state.hard_drop()
