"""Tests for input_handler module: key bindings."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import curses
from input_handler import get_command, Command, KEY_BINDINGS


class TestGetCommand:
    def test_space_toggles_pause(self):
        assert get_command(ord(' ')) == Command.TOGGLE_PAUSE

    def test_right_arrow_speed_forward(self):
        assert get_command(curses.KEY_RIGHT) == Command.SPEED_FORWARD

    def test_left_arrow_speed_rewind(self):
        assert get_command(curses.KEY_LEFT) == Command.SPEED_REWIND

    def test_l_speed_forward(self):
        assert get_command(ord('l')) == Command.SPEED_FORWARD

    def test_h_speed_rewind(self):
        assert get_command(ord('h')) == Command.SPEED_REWIND

    def test_n_next_scene(self):
        assert get_command(ord('n')) == Command.NEXT_SCENE

    def test_p_prev_scene(self):
        assert get_command(ord('p')) == Command.PREV_SCENE

    def test_q_quit(self):
        assert get_command(ord('q')) == Command.QUIT

    def test_escape_quit(self):
        assert get_command(27) == Command.QUIT

    def test_r_restart(self):
        assert get_command(ord('r')) == Command.RESTART

    def test_unknown_key_returns_none(self):
        assert get_command(ord('z')) is None

    def test_page_down_next_scene(self):
        assert get_command(curses.KEY_NPAGE) == Command.NEXT_SCENE

    def test_page_up_prev_scene(self):
        assert get_command(curses.KEY_PPAGE) == Command.PREV_SCENE
