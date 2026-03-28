"""Tests for the application controller."""

import asyncio
import curses
import unittest
from datetime import datetime, timedelta

from models import Event, EventTime, Attendee
from mock_client import MockCalendarClient
from app import CalendarApp, View
from components import FORM_FIELDS


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


class TestAppInit(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()
        self.app = CalendarApp(self.client)

    def test_initial_state(self):
        self.assertEqual(self.app.view, View.AGENDA)
        self.assertEqual(self.app.events, [])
        self.assertFalse(self.app.sidebar_focused)

    def test_init_loads_data(self):
        run(self.app.init())
        self.assertGreater(len(self.app.calendars), 0)
        self.assertGreater(len(self.app.events), 0)
        self.assertGreater(len(self.app.sidebar_items), 0)


class TestAppNavigation(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()
        self.app = CalendarApp(self.client)
        run(self.app.init())

    def test_arrow_down(self):
        self.app.event_idx = 0
        run(self.app.handle_key(curses.KEY_DOWN))
        self.assertEqual(self.app.event_idx, 1)

    def test_arrow_up(self):
        self.app.event_idx = 2
        run(self.app.handle_key(curses.KEY_UP))
        self.assertEqual(self.app.event_idx, 1)

    def test_arrow_up_at_top(self):
        self.app.event_idx = 0
        run(self.app.handle_key(curses.KEY_UP))
        self.assertEqual(self.app.event_idx, 0)

    def test_arrow_down_at_bottom(self):
        self.app.event_idx = len(self.app.events) - 1
        run(self.app.handle_key(curses.KEY_DOWN))
        self.assertEqual(self.app.event_idx, len(self.app.events) - 1)

    def test_vim_j_k(self):
        self.app.event_idx = 0
        run(self.app.handle_key(ord("j")))
        self.assertEqual(self.app.event_idx, 1)
        run(self.app.handle_key(ord("k")))
        self.assertEqual(self.app.event_idx, 0)


class TestAppSidebar(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()
        self.app = CalendarApp(self.client)
        run(self.app.init())

    def test_tab_toggles_sidebar(self):
        self.assertFalse(self.app.sidebar_focused)
        run(self.app.handle_key(9))  # Tab
        self.assertTrue(self.app.sidebar_focused)
        run(self.app.handle_key(9))
        self.assertFalse(self.app.sidebar_focused)


class TestAppOpenEvent(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()
        self.app = CalendarApp(self.client)
        run(self.app.init())

    def test_enter_opens_detail(self):
        self.app.event_idx = 0
        run(self.app.handle_key(10))  # Enter
        self.assertEqual(self.app.view, View.EVENT_DETAIL)
        self.assertIsNotNone(self.app.detail_event)

    def test_escape_closes_detail(self):
        self.app.event_idx = 0
        run(self.app.handle_key(10))
        self.assertEqual(self.app.view, View.EVENT_DETAIL)
        run(self.app.handle_key(27))  # Escape
        self.assertEqual(self.app.view, View.AGENDA)
        self.assertIsNone(self.app.detail_event)


class TestAppCreateEvent(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()
        self.app = CalendarApp(self.client)
        run(self.app.init())

    def test_n_opens_create(self):
        run(self.app.handle_key(ord("n")))
        self.assertEqual(self.app.view, View.CREATE_EVENT)
        self.assertIn("summary", self.app.form_values)

    def test_escape_cancels_create(self):
        run(self.app.handle_key(ord("n")))
        run(self.app.handle_key(27))
        self.assertEqual(self.app.view, View.AGENDA)

    def test_tab_cycles_fields(self):
        run(self.app.handle_key(ord("n")))
        self.assertEqual(self.app.form_field_idx, 0)
        run(self.app.handle_key(9))  # Tab
        self.assertEqual(self.app.form_field_idx, 1)
        run(self.app.handle_key(9))
        self.assertEqual(self.app.form_field_idx, 2)

    def test_shift_tab_goes_back(self):
        run(self.app.handle_key(ord("n")))
        self.app.form_field_idx = 2
        run(self.app.handle_key(353))  # Shift+Tab
        self.assertEqual(self.app.form_field_idx, 1)

    def test_typing_in_field(self):
        run(self.app.handle_key(ord("n")))
        run(self.app.handle_key(ord("T")))
        run(self.app.handle_key(ord("e")))
        run(self.app.handle_key(ord("s")))
        run(self.app.handle_key(ord("t")))
        self.assertEqual(self.app.form_values["summary"], "Test")

    def test_backspace_in_field(self):
        run(self.app.handle_key(ord("n")))
        run(self.app.handle_key(ord("A")))
        run(self.app.handle_key(ord("B")))
        run(self.app.handle_key(127))  # Backspace
        self.assertEqual(self.app.form_values["summary"], "A")

    def test_save_creates_event(self):
        run(self.app.handle_key(ord("n")))
        for c in "New Meeting":
            run(self.app.handle_key(ord(c)))
        run(self.app._save_event())
        self.assertEqual(self.app.view, View.AGENDA)
        result = run(self.client.list_events(q="New Meeting"))
        self.assertEqual(len(result.events), 1)

    def test_save_empty_title_fails(self):
        run(self.app.handle_key(ord("n")))
        run(self.app._save_event())
        self.assertIn("Title is required", self.app.status_message)
        self.assertEqual(self.app.view, View.CREATE_EVENT)


class TestAppSearch(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()
        self.app = CalendarApp(self.client)
        run(self.app.init())

    def test_slash_opens_search(self):
        run(self.app.handle_key(ord("/")))
        self.assertEqual(self.app.view, View.SEARCH)
        self.assertTrue(self.app.search_active)

    def test_escape_cancels_search(self):
        run(self.app.handle_key(ord("/")))
        run(self.app.handle_key(27))
        self.assertEqual(self.app.view, View.AGENDA)

    def test_typing_search_query(self):
        run(self.app.handle_key(ord("/")))
        run(self.app.handle_key(ord("s")))
        run(self.app.handle_key(ord("p")))
        self.assertEqual(self.app.search_query, "sp")

    def test_backspace_in_search(self):
        run(self.app.handle_key(ord("/")))
        run(self.app.handle_key(ord("a")))
        run(self.app.handle_key(ord("b")))
        run(self.app.handle_key(127))
        self.assertEqual(self.app.search_query, "a")

    def test_execute_search(self):
        run(self.app.handle_key(ord("/")))
        for c in "standup":
            run(self.app.handle_key(ord(c)))
        run(self.app.handle_key(10))  # Enter
        self.assertFalse(self.app.search_active)
        self.assertGreater(len(self.app.events), 0)
        for e in self.app.events:
            self.assertIn("standup", e.summary.lower())


class TestAppHelp(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()
        self.app = CalendarApp(self.client)
        run(self.app.init())

    def test_question_shows_help(self):
        run(self.app.handle_key(ord("?")))
        self.assertEqual(self.app.view, View.HELP)

    def test_escape_closes_help(self):
        run(self.app.handle_key(ord("?")))
        self.assertEqual(self.app.view, View.HELP)
        run(self.app.handle_key(27))
        self.assertEqual(self.app.view, View.AGENDA)


class TestAppQuit(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()
        self.app = CalendarApp(self.client)
        run(self.app.init())

    def test_q_quits(self):
        run(self.app.handle_key(ord("q")))
        self.assertFalse(self.app.running)

    def test_q_doesnt_quit_in_create(self):
        run(self.app.handle_key(ord("n")))
        # In create view, q types 'q' into the field, doesn't quit
        run(self.app.handle_key(ord("q")))
        self.assertTrue(self.app.running)

    def test_q_doesnt_quit_in_search(self):
        run(self.app.handle_key(ord("/")))
        run(self.app.handle_key(ord("q")))
        self.assertTrue(self.app.running)


class TestAppEventDetailActions(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()
        self.app = CalendarApp(self.client)
        run(self.app.init())
        run(self.app.handle_key(10))  # Open first event

    def test_scroll_detail(self):
        self.assertEqual(self.app.detail_scroll, 0)
        run(self.app.handle_key(curses.KEY_DOWN))
        self.assertEqual(self.app.detail_scroll, 1)
        run(self.app.handle_key(curses.KEY_UP))
        self.assertEqual(self.app.detail_scroll, 0)

    def test_edit_from_detail(self):
        run(self.app.handle_key(ord("e")))
        self.assertEqual(self.app.view, View.EDIT_EVENT)
        self.assertIsNotNone(self.app.editing_event)

    def test_respond_accept(self):
        run(self.app._respond_event(self.app.detail_event, "accepted"))
        self.assertEqual(self.app.detail_event.my_response_status, "accepted")

    def test_respond_decline(self):
        run(self.app._respond_event(self.app.detail_event, "declined"))
        self.assertEqual(self.app.detail_event.my_response_status, "declined")

    def test_delete_from_detail(self):
        event_id = self.app.detail_event.event_id
        run(self.app._delete_event(self.app.detail_event))
        self.assertEqual(self.app.view, View.AGENDA)
        with self.assertRaises(ValueError):
            run(self.client.get_event("primary", event_id))


class TestAppDayNavigation(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()
        self.app = CalendarApp(self.client)
        run(self.app.init())

    def test_next_day(self):
        original = self.app.current_date
        run(self.app.handle_key(ord("]")))
        self.assertGreater(self.app.current_date, original)

    def test_prev_day(self):
        original = self.app.current_date
        run(self.app.handle_key(ord("[")))
        self.assertLess(self.app.current_date, original)

    def test_jump_today(self):
        self.app.current_date += timedelta(days=10)
        run(self.app.handle_key(ord("t")))
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.assertEqual(self.app.current_date, today)


class TestAppFreeTime(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()
        self.app = CalendarApp(self.client)
        run(self.app.init())

    def test_load_free_time(self):
        run(self.app._load_free_time())
        self.assertEqual(self.app.view, View.FREE_TIME)
        self.assertGreater(len(self.app.free_slots), 0)

    def test_escape_from_free_time(self):
        run(self.app._load_free_time())
        run(self.app.handle_key(27))
        self.assertEqual(self.app.view, View.AGENDA)


class TestAppStatusHints(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()
        self.app = CalendarApp(self.client)
        run(self.app.init())

    def test_agenda_hints(self):
        hints = self.app._get_status_hints()
        keys = [h[0] for h in hints]
        self.assertIn("↑↓", keys)
        self.assertIn("q", keys)

    def test_detail_hints(self):
        self.app.view = View.EVENT_DETAIL
        hints = self.app._get_status_hints()
        keys = [h[0] for h in hints]
        self.assertIn("Esc", keys)
        self.assertIn("e", keys)

    def test_create_hints(self):
        self.app.view = View.CREATE_EVENT
        hints = self.app._get_status_hints()
        keys = [h[0] for h in hints]
        self.assertIn("Tab", keys)
        self.assertIn("Ctrl+S", keys)


if __name__ == "__main__":
    unittest.main()
