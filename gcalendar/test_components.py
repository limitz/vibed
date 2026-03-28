"""Tests for UI component helper functions (non-curses)."""

import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from models import Attendee, Event, EventTime
from components import (
    parse_event_datetime, format_time, format_time_range,
    format_date_header, format_event_duration,
    response_status_symbol, response_status_pair, event_color_pair,
    _build_agenda_lines,
)
from colors import (
    EMOJI, PAIR_CAL_BLUE, PAIR_CAL_RED, PAIR_CAL_GREEN,
    PAIR_ACCENT_GREEN, PAIR_ACCENT_RED, PAIR_ACCENT_YELLOW, PAIR_SNIPPET,
)


def _mock_curses_for_build():
    """Patch curses.color_pair and curses.A_BOLD for testing without a terminal."""
    return patch.multiple(
        "curses",
        color_pair=lambda x: x,
        A_BOLD=0,
        A_UNDERLINE=0,
    )


class TestParseEventDatetime(unittest.TestCase):
    def test_datetime_with_offset(self):
        et = EventTime(date_time="2026-03-28T09:00:00-04:00")
        dt = parse_event_datetime(et)
        self.assertIsNotNone(dt)
        self.assertEqual(dt.hour, 9)
        self.assertEqual(dt.minute, 0)

    def test_datetime_utc(self):
        et = EventTime(date_time="2026-03-28T14:30:00Z")
        dt = parse_event_datetime(et)
        self.assertIsNotNone(dt)
        self.assertEqual(dt.hour, 14)
        self.assertEqual(dt.minute, 30)

    def test_date_only(self):
        et = EventTime(date="2026-03-28")
        dt = parse_event_datetime(et)
        self.assertIsNotNone(dt)
        self.assertEqual(dt.month, 3)
        self.assertEqual(dt.day, 28)

    def test_empty(self):
        et = EventTime()
        self.assertIsNone(parse_event_datetime(et))


class TestFormatTime(unittest.TestCase):
    def test_timed_event(self):
        et = EventTime(date_time="2026-03-28T09:00:00-04:00")
        result = format_time(et)
        self.assertIn("9", result)
        self.assertIn("AM", result)

    def test_all_day(self):
        et = EventTime(date="2026-03-28")
        self.assertEqual(format_time(et), "All day")

    def test_pm_time(self):
        et = EventTime(date_time="2026-03-28T14:30:00-04:00")
        result = format_time(et)
        self.assertIn("2", result)
        self.assertIn("PM", result)


class TestFormatTimeRange(unittest.TestCase):
    def test_normal_range(self):
        start = EventTime(date_time="2026-03-28T09:00:00-04:00")
        end = EventTime(date_time="2026-03-28T10:30:00-04:00")
        result = format_time_range(start, end)
        self.assertIn("9:00 AM", result)
        self.assertIn("10:30 AM", result)

    def test_all_day(self):
        start = EventTime(date="2026-03-28")
        end = EventTime(date="2026-03-29")
        self.assertEqual(format_time_range(start, end), "All day")


class TestFormatDateHeader(unittest.TestCase):
    def test_today(self):
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        result = format_date_header(today)
        self.assertIn("Today", result)

    def test_tomorrow(self):
        tomorrow = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        result = format_date_header(tomorrow)
        self.assertIn("Tomorrow", result)

    def test_yesterday(self):
        yesterday = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        result = format_date_header(yesterday)
        self.assertIn("Yesterday", result)

    def test_other_day(self):
        other = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=5)
        result = format_date_header(other)
        self.assertNotIn("Today", result)
        self.assertNotIn("Tomorrow", result)


class TestFormatEventDuration(unittest.TestCase):
    def test_short(self):
        start = EventTime(date_time="2026-03-28T09:00:00-04:00")
        end = EventTime(date_time="2026-03-28T09:15:00-04:00")
        self.assertEqual(format_event_duration(start, end), "15m")

    def test_one_hour(self):
        start = EventTime(date_time="2026-03-28T09:00:00-04:00")
        end = EventTime(date_time="2026-03-28T10:00:00-04:00")
        self.assertEqual(format_event_duration(start, end), "1h")

    def test_mixed(self):
        start = EventTime(date_time="2026-03-28T09:00:00-04:00")
        end = EventTime(date_time="2026-03-28T10:30:00-04:00")
        self.assertEqual(format_event_duration(start, end), "1h 30m")


class TestResponseStatusSymbol(unittest.TestCase):
    def test_accepted(self):
        self.assertEqual(response_status_symbol("accepted"), EMOJI["accepted"])

    def test_declined(self):
        self.assertEqual(response_status_symbol("declined"), EMOJI["declined"])

    def test_tentative(self):
        self.assertEqual(response_status_symbol("tentative"), EMOJI["tentative"])

    def test_needs_action(self):
        self.assertEqual(response_status_symbol("needsAction"), EMOJI["pending"])


class TestResponseStatusPair(unittest.TestCase):
    def test_accepted(self):
        self.assertEqual(response_status_pair("accepted"), PAIR_ACCENT_GREEN)

    def test_declined(self):
        self.assertEqual(response_status_pair("declined"), PAIR_ACCENT_RED)

    def test_tentative(self):
        self.assertEqual(response_status_pair("tentative"), PAIR_ACCENT_YELLOW)

    def test_needs_action(self):
        self.assertEqual(response_status_pair("needsAction"), PAIR_SNIPPET)


class TestEventColorPair(unittest.TestCase):
    def test_known_colors(self):
        self.assertEqual(event_color_pair("7"), PAIR_CAL_BLUE)
        self.assertEqual(event_color_pair("11"), PAIR_CAL_RED)
        self.assertEqual(event_color_pair("2"), PAIR_CAL_GREEN)

    def test_default(self):
        self.assertEqual(event_color_pair(""), PAIR_CAL_BLUE)
        self.assertEqual(event_color_pair("99"), PAIR_CAL_BLUE)


class TestBuildAgendaLines(unittest.TestCase):
    def test_empty(self):
        lines = _build_agenda_lines([], -1, True)
        self.assertEqual(lines, [])

    def test_single_event(self):
        event = Event(
            event_id="e1",
            summary="Test Meeting",
            start=EventTime(date_time="2026-03-28T10:00:00-04:00"),
            end=EventTime(date_time="2026-03-28T11:00:00-04:00"),
        )
        lines = _build_agenda_lines([event], 0, True)
        self.assertGreater(len(lines), 0)
        event_lines = [l for l in lines if l["type"] == "event"]
        self.assertEqual(len(event_lines), 1)
        self.assertEqual(event_lines[0]["event"].summary, "Test Meeting")

    def test_with_date_headers(self):
        event = Event(
            event_id="e1",
            summary="Lunch",
            start=EventTime(date_time="2026-03-28T12:00:00-04:00"),
            end=EventTime(date_time="2026-03-28T13:00:00-04:00"),
        )
        lines = _build_agenda_lines([event], -1, True)
        header_lines = [l for l in lines if l["type"] == "date_header"]
        self.assertGreater(len(header_lines), 0)


class TestBuildEventDetailLines(unittest.TestCase):
    def test_basic_event(self):
        with _mock_curses_for_build():
            from components import _build_event_detail_lines
            event = Event(
                event_id="e1",
                summary="Team Sync",
                start=EventTime(date_time="2026-03-28T10:00:00-04:00"),
                end=EventTime(date_time="2026-03-28T11:00:00-04:00"),
                description="Weekly sync meeting",
                location="Room A",
                my_response_status="accepted",
            )
            lines = _build_event_detail_lines(event, 80)
            text = " ".join(l[0] for l in lines)
            self.assertIn("Team Sync", text)
            self.assertIn("Room A", text)
            self.assertIn("Weekly sync", text)
            self.assertIn("Accepted", text)

    def test_all_day_event(self):
        with _mock_curses_for_build():
            from components import _build_event_detail_lines
            event = Event(
                event_id="e1",
                summary="Holiday",
                start=EventTime(date="2026-03-28"),
                end=EventTime(date="2026-03-29"),
            )
            lines = _build_event_detail_lines(event, 80)
            text = " ".join(l[0] for l in lines)
            self.assertIn("All day", text)

    def test_with_attendees(self):
        with _mock_curses_for_build():
            from components import _build_event_detail_lines
            event = Event(
                event_id="e1",
                summary="Meeting",
                start=EventTime(date_time="2026-03-28T09:00:00-04:00"),
                end=EventTime(date_time="2026-03-28T10:00:00-04:00"),
                attendees=[
                    Attendee(email="alice@co.com", display_name="Alice", response_status="accepted"),
                    Attendee(email="bob@co.com", display_name="Bob", response_status="declined"),
                ],
            )
            lines = _build_event_detail_lines(event, 80)
            text = " ".join(l[0] for l in lines)
            self.assertIn("Alice", text)
            self.assertIn("Bob", text)
            self.assertIn("2 Attendees", text)

    def test_with_conference_link(self):
        with _mock_curses_for_build():
            from components import _build_event_detail_lines
            event = Event(
                event_id="e1",
                summary="Video Call",
                start=EventTime(date_time="2026-03-28T09:00:00-04:00"),
                end=EventTime(date_time="2026-03-28T10:00:00-04:00"),
                conference_link="https://meet.google.com/abc",
            )
            lines = _build_event_detail_lines(event, 80)
            text = " ".join(l[0] for l in lines)
            self.assertIn("meet.google.com", text)


if __name__ == "__main__":
    unittest.main()
