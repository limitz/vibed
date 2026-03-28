"""Input handling: maps curses keys to player commands."""

import curses


class Command:
    """Enumeration of player commands."""
    TOGGLE_PAUSE = 'toggle_pause'
    SPEED_FORWARD = 'speed_forward'
    SPEED_REWIND = 'speed_rewind'
    NEXT_SCENE = 'next_scene'
    PREV_SCENE = 'prev_scene'
    RESTART = 'restart'
    QUIT = 'quit'


KEY_BINDINGS = {
    ord(' '): Command.TOGGLE_PAUSE,
    curses.KEY_RIGHT: Command.SPEED_FORWARD,
    ord('l'): Command.SPEED_FORWARD,
    curses.KEY_LEFT: Command.SPEED_REWIND,
    ord('h'): Command.SPEED_REWIND,
    ord('n'): Command.NEXT_SCENE,
    curses.KEY_NPAGE: Command.NEXT_SCENE,
    ord('p'): Command.PREV_SCENE,
    curses.KEY_PPAGE: Command.PREV_SCENE,
    ord('r'): Command.RESTART,
    ord('q'): Command.QUIT,
    27: Command.QUIT,  # ESC
}


def get_command(key):
    """Translate a curses key code to a Command, or None."""
    return KEY_BINDINGS.get(key)


def handle_input(stdscr, player):
    """Read input from stdscr and apply commands to the player.

    Returns False if quit was requested, True otherwise.
    """
    key = stdscr.getch()
    if key == -1:
        return True

    cmd = get_command(key)
    if cmd is None:
        return True

    if cmd == Command.QUIT:
        return False
    elif cmd == Command.TOGGLE_PAUSE:
        player.toggle_pause()
    elif cmd == Command.SPEED_FORWARD:
        player.play()
        player.cycle_forward_speed()
    elif cmd == Command.SPEED_REWIND:
        player.play()
        player.cycle_rewind_speed()
    elif cmd == Command.NEXT_SCENE:
        player.skip_scene_forward()
    elif cmd == Command.PREV_SCENE:
        player.skip_scene_back()
    elif cmd == Command.RESTART:
        player.restart()

    return True
