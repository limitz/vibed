"""Tests for input_handler module."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import curses
from input_handler import map_key, Action


class TestKeyMapping:
    def test_left_arrow(self):
        assert map_key(curses.KEY_LEFT) == Action.MOVE_LEFT

    def test_right_arrow(self):
        assert map_key(curses.KEY_RIGHT) == Action.MOVE_RIGHT

    def test_down_arrow(self):
        assert map_key(curses.KEY_DOWN) == Action.MOVE_DOWN

    def test_up_arrow(self):
        assert map_key(curses.KEY_UP) == Action.ROTATE_CW

    def test_space_hard_drop(self):
        assert map_key(ord(' ')) == Action.HARD_DROP

    def test_q_quit(self):
        assert map_key(ord('q')) == Action.QUIT

    def test_z_rotate_ccw(self):
        assert map_key(ord('z')) == Action.ROTATE_CCW

    def test_p_pause(self):
        assert map_key(ord('p')) == Action.PAUSE

    def test_unknown_key_returns_none(self):
        assert map_key(ord('x')) is None
