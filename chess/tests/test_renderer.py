"""Tests for renderer module."""

import curses
import pytest
from unittest.mock import MagicMock, patch, call
from renderer import Renderer
from game import GameState


class MockWindow:
    """Mock curses window for testing."""
    def __init__(self):
        self.calls = []
        self._max_y = 40
        self._max_x = 100

    def getmaxyx(self):
        return (self._max_y, self._max_x)

    def addstr(self, *args):
        self.calls.append(('addstr', args))

    def erase(self):
        self.calls.append(('erase',))

    def refresh(self):
        self.calls.append(('refresh',))

    def attron(self, *args):
        pass

    def attroff(self, *args):
        pass


class TestRendererInit:
    @patch('curses.start_color')
    @patch('curses.use_default_colors')
    @patch('curses.init_pair')
    @patch('curses.can_change_color', return_value=False)
    @patch('curses.curs_set')
    @patch('curses.color_pair', return_value=0)
    def test_init_does_not_crash(self, mock_cp, mock_curs, mock_can, mock_init, mock_default, mock_start):
        win = MockWindow()
        renderer = Renderer(win)
        assert renderer is not None

    @patch('curses.start_color')
    @patch('curses.use_default_colors')
    @patch('curses.init_pair')
    @patch('curses.can_change_color', return_value=False)
    @patch('curses.curs_set')
    @patch('curses.color_pair', return_value=0)
    def test_setup_colors_called(self, mock_cp, mock_curs, mock_can, mock_init, mock_default, mock_start):
        win = MockWindow()
        renderer = Renderer(win)
        assert mock_init.called


class TestRendererDraw:
    @patch('curses.start_color')
    @patch('curses.use_default_colors')
    @patch('curses.init_pair')
    @patch('curses.can_change_color', return_value=False)
    @patch('curses.curs_set')
    @patch('curses.color_pair', return_value=0)
    @patch('moves.get_legal_moves', return_value=[])
    def test_draw_initial_state(self, mock_moves, mock_cp, mock_curs, mock_can, mock_init, mock_default, mock_start):
        win = MockWindow()
        renderer = Renderer(win)
        state = GameState()
        renderer.draw(state)
        # Should have called erase and refresh
        erase_calls = [c for c in win.calls if c[0] == 'erase']
        refresh_calls = [c for c in win.calls if c[0] == 'refresh']
        assert len(erase_calls) >= 1
        assert len(refresh_calls) >= 1
