"""Tests for data models."""

import unittest

from models import (
    Attendee, Calendar, Event, EventList, EventTime,
    FreeSlot, FreeTimeResult, MeetingTimeOption, MeetingTimesResult,
)


class TestEventTime(unittest.TestCase):
    def test_timed_event(self):
        et = EventTime(date_time="2026-03-28T09:00:00-04:00", time_zone="America/New_York")
        self.assertFalse(et.is_all_day)

    def test_all_day_event(self):
        et = EventTime(date="2026-03-28")
        self.assertTrue(et.is_all_day)

    def test_empty(self):
        et = EventTime()
        self.assertFalse(et.is_all_day)


class TestAttendee(unittest.TestCase):
    def test_defaults(self):
        a = Attendee(email="test@example.com")
        self.assertEqual(a.response_status, "needsAction")
        self.assertFalse(a.is_optional)
        self.assertFalse(a.is_organizer)
        self.assertFalse(a.is_self)


class TestCalendar(unittest.TestCase):
    def test_defaults(self):
        c = Calendar(calendar_id="primary", summary="My Calendar")
        self.assertFalse(c.primary)
        self.assertEqual(c.access_role, "reader")
        self.assertTrue(c.selected)


class TestEvent(unittest.TestCase):
    def test_creation(self):
        e = Event(
            event_id="evt1",
            summary="Test Event",
            start=EventTime(date_time="2026-03-28T09:00:00"),
            end=EventTime(date_time="2026-03-28T10:00:00"),
        )
        self.assertEqual(e.event_id, "evt1")
        self.assertEqual(e.summary, "Test Event")
        self.assertEqual(e.status, "confirmed")
        self.assertEqual(e.attendees, [])
        self.assertEqual(e.recurrence, [])

    def test_attendees_independent(self):
        e1 = Event(event_id="1", summary="A",
                    start=EventTime(), end=EventTime())
        e2 = Event(event_id="2", summary="B",
                    start=EventTime(), end=EventTime())
        e1.attendees.append(Attendee(email="x@y.com"))
        self.assertEqual(len(e2.attendees), 0)


class TestEventList(unittest.TestCase):
    def test_defaults(self):
        el = EventList()
        self.assertEqual(el.events, [])
        self.assertEqual(el.next_page_token, "")

    def test_with_events(self):
        e = Event(event_id="1", summary="E",
                  start=EventTime(), end=EventTime())
        el = EventList(events=[e], next_page_token="abc")
        self.assertEqual(len(el.events), 1)
        self.assertEqual(el.next_page_token, "abc")


class TestFreeSlot(unittest.TestCase):
    def test_creation(self):
        s = FreeSlot(start="2026-03-28T08:00:00", end="2026-03-28T12:00:00",
                     duration_minutes=240)
        self.assertEqual(s.duration_minutes, 240)


class TestFreeTimeResult(unittest.TestCase):
    def test_defaults(self):
        r = FreeTimeResult()
        self.assertEqual(r.slots, [])
        self.assertEqual(r.summary, "")


class TestMeetingTimeOption(unittest.TestCase):
    def test_creation(self):
        o = MeetingTimeOption(
            start="2026-03-28T10:00:00",
            end="2026-03-28T11:00:00",
            duration_minutes=60,
            attendee_count=3,
        )
        self.assertEqual(o.duration_minutes, 60)
        self.assertEqual(o.attendee_count, 3)


class TestMeetingTimesResult(unittest.TestCase):
    def test_defaults(self):
        r = MeetingTimesResult()
        self.assertEqual(r.options, [])
        self.assertEqual(r.attendees, [])


if __name__ == "__main__":
    unittest.main()
