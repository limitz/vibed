"""2001: A Space Odyssey - ASCII Art Re-enactment.

Controls:
  SPACE       - play/pause
  RIGHT / l   - cycle forward speed (1x -> 2x -> 4x)
  LEFT / h    - cycle rewind speed (-1x -> -2x -> -4x)
  n / PgDn    - next scene
  p / PgUp    - previous scene
  r           - restart
  q / ESC     - quit
"""

import curses
import time

from renderer import ScreenBuffer, CursesRenderer
from timeline import Timeline
from player import Player, PlayerState
from input_handler import handle_input
from hud import draw_hud
from scenes import create_all_scenes


TARGET_FPS = 10
FRAME_TIME = 1.0 / TARGET_FPS


def main(stdscr):
    """Main application loop."""
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(int(FRAME_TIME * 1000))

    renderer = CursesRenderer(stdscr)

    scenes = create_all_scenes()
    timeline = Timeline(scenes)
    player = Player(timeline)
    player.play()

    max_y, max_x = stdscr.getmaxyx()
    buffer = ScreenBuffer(max_x, max_y)

    last_time = time.monotonic()

    while True:
        # Handle input
        if not handle_input(stdscr, player):
            break

        # Update timing
        now = time.monotonic()
        dt = now - last_time
        last_time = now

        # Update player
        player.update(dt)

        # Check terminal resize
        new_y, new_x = stdscr.getmaxyx()
        if new_x != buffer.width or new_y != buffer.height:
            buffer = ScreenBuffer(new_x, new_y)
            stdscr.clear()

        # Render
        buffer.clear()
        player.get_current_frame(buffer)
        draw_hud(buffer, player)
        renderer.render(buffer)

        # Show pause indicator
        if player.state == PlayerState.PAUSED:
            pause_text = " ⏸ PAUSED "
            px = (buffer.width - len(pause_text)) // 2
            py = buffer.height // 2
            try:
                pair = renderer.get_color_pair(0, 7)  # black on white
                stdscr.addstr(py, px, pause_text, curses.color_pair(pair) | curses.A_BOLD)
                stdscr.noutrefresh()
                curses.doupdate()
            except curses.error:
                pass


if __name__ == "__main__":
    curses.wrapper(main)
