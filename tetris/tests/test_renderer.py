"""Tests for renderer module (using mock curses window)."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import curses as real_curses
from unittest.mock import MagicMock, patch, call
from game import GameState
from pieces import PieceType, COLORS


class TestRenderer:
    def _patch_and_create(self):
        """Create a Renderer with curses fully mocked."""
        mock_stdscr = MagicMock()
        mock_stdscr.getmaxyx.return_value = (40, 80)

        # We need to patch curses at the module level before importing
        mock_curses = MagicMock()
        mock_curses.A_BOLD = 0
        mock_curses.A_DIM = 0
        mock_curses.A_REVERSE = 0
        mock_curses.color_pair = MagicMock(return_value=0)
        mock_curses.COLOR_CYAN = 6
        mock_curses.COLOR_YELLOW = 3
        mock_curses.COLOR_MAGENTA = 5
        mock_curses.COLOR_GREEN = 2
        mock_curses.COLOR_RED = 1
        mock_curses.COLOR_BLUE = 4
        mock_curses.COLOR_WHITE = 7
        mock_curses.error = real_curses.error

        with patch.dict('sys.modules', {'curses': mock_curses}):
            # Force reimport of renderer with mocked curses
            if 'renderer' in sys.modules:
                del sys.modules['renderer']
            import renderer as rmod
            r = rmod.Renderer(mock_stdscr)
            return r, mock_stdscr, mock_curses, rmod

    def test_setup_colors_calls_init_pair(self):
        r, mock_stdscr, mock_curses, _ = self._patch_and_create()
        assert mock_curses.init_pair.call_count >= 7

    def test_draw_does_not_crash(self):
        r, mock_stdscr, _, _ = self._patch_and_create()
        state = GameState(seed=42)
        r.draw(state)

    def test_draw_game_over_does_not_crash(self):
        r, mock_stdscr, _, _ = self._patch_and_create()
        state = GameState(seed=42)
        state.game_over = True
        r.draw(state)

    def test_refresh_called(self):
        r, mock_stdscr, _, _ = self._patch_and_create()
        state = GameState(seed=42)
        r.draw(state)
        mock_stdscr.refresh.assert_called()
