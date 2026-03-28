"""Tests for mock calendar client."""

import asyncio
import unittest

from mock_client import MockCalendarClient


def run(coro):
    """Helper to run async tests."""
    return asyncio.get_event_loop().run_until_complete(coro)


class TestMockClientCalendars(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()

    def test_list_calendars(self):
        cals = run(self.client.list_calendars())
        self.assertGreater(len(cals), 0)
        primary = [c for c in cals if c.primary]
        self.assertEqual(len(primary), 1)

    def test_calendar_fields(self):
        cals = run(self.client.list_calendars())
        for c in cals:
            self.assertTrue(c.calendar_id)
            self.assertTrue(c.summary)


class TestMockClientEvents(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()

    def test_list_events_all(self):
        result = run(self.client.list_events())
        self.assertGreater(len(result.events), 0)

    def test_list_events_time_range(self):
        result = run(self.client.list_events(
            time_min="2026-03-28T00:00:00",
            time_max="2026-03-28T23:59:59",
        ))
        for e in result.events:
            start = e.start.date_time or e.start.date or ""
            self.assertGreaterEqual(start, "2026-03-28")

    def test_list_events_search(self):
        result = run(self.client.list_events(q="standup"))
        for e in result.events:
            self.assertIn("standup", e.summary.lower())

    def test_list_events_pagination(self):
        result = run(self.client.list_events(max_results=3))
        self.assertLessEqual(len(result.events), 3)
        if result.next_page_token:
            result2 = run(self.client.list_events(
                max_results=3, page_token=result.next_page_token))
            self.assertGreater(len(result2.events), 0)

    def test_get_event(self):
        event = run(self.client.get_event("primary", "evt_standup_mon"))
        self.assertEqual(event.summary, "Daily Standup")

    def test_get_event_not_found(self):
        with self.assertRaises(ValueError):
            run(self.client.get_event("primary", "nonexistent"))


class TestMockClientCreateEvent(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()

    def test_create_event(self):
        event = run(self.client.create_event(
            summary="Test Meeting",
            start_date_time="2026-03-30T14:00:00",
            end_date_time="2026-03-30T15:00:00",
            time_zone="America/New_York",
            description="A test meeting",
            location="Room 101",
        ))
        self.assertEqual(event.summary, "Test Meeting")
        self.assertTrue(event.event_id.startswith("evt_"))
        # Verify it's in the list
        result = run(self.client.list_events(q="Test Meeting"))
        self.assertEqual(len(result.events), 1)

    def test_create_all_day_event(self):
        event = run(self.client.create_event(
            summary="Day Off",
            start_date="2026-04-01",
            end_date="2026-04-02",
        ))
        self.assertTrue(event.start.is_all_day)

    def test_create_with_attendees(self):
        event = run(self.client.create_event(
            summary="Group Meeting",
            start_date_time="2026-03-30T10:00:00",
            end_date_time="2026-03-30T11:00:00",
            attendees=["alice@example.com", "bob@example.com"],
        ))
        self.assertEqual(len(event.attendees), 2)


class TestMockClientUpdateEvent(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()

    def test_update_summary(self):
        event = run(self.client.update_event(
            "primary", "evt_standup_mon", summary="Morning Standup"))
        self.assertEqual(event.summary, "Morning Standup")

    def test_update_location(self):
        event = run(self.client.update_event(
            "primary", "evt_sprint_plan", location="Room 202"))
        self.assertEqual(event.location, "Room 202")

    def test_update_not_found(self):
        with self.assertRaises(ValueError):
            run(self.client.update_event("primary", "nonexistent", summary="X"))


class TestMockClientDeleteEvent(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()

    def test_delete_event(self):
        result = run(self.client.delete_event("primary", "evt_run"))
        self.assertTrue(result)
        with self.assertRaises(ValueError):
            run(self.client.get_event("primary", "evt_run"))

    def test_delete_not_found(self):
        with self.assertRaises(ValueError):
            run(self.client.delete_event("primary", "nonexistent"))


class TestMockClientRespond(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()

    def test_accept(self):
        event = run(self.client.respond_to_event("evt_design_review", "accepted"))
        self.assertEqual(event.my_response_status, "accepted")

    def test_decline(self):
        event = run(self.client.respond_to_event("evt_design_review", "declined"))
        self.assertEqual(event.my_response_status, "declined")

    def test_tentative(self):
        event = run(self.client.respond_to_event("evt_design_review", "tentative"))
        self.assertEqual(event.my_response_status, "tentative")

    def test_respond_not_found(self):
        with self.assertRaises(ValueError):
            run(self.client.respond_to_event("nonexistent", "accepted"))


class TestMockClientFreeTime(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()

    def test_find_free_time(self):
        result = run(self.client.find_free_time(
            ["primary"], "2026-03-28T00:00:00", "2026-03-30T23:59:59"))
        self.assertGreater(len(result.slots), 0)
        for slot in result.slots:
            self.assertTrue(slot.start)
            self.assertGreater(slot.duration_minutes, 0)


class TestMockClientMeetingTimes(unittest.TestCase):
    def setUp(self):
        self.client = MockCalendarClient()

    def test_find_meeting_times(self):
        result = run(self.client.find_meeting_times(
            ["sarah@company.com"], 60,
            "2026-03-30T00:00:00", "2026-04-01T23:59:59"))
        self.assertGreater(len(result.options), 0)
        self.assertEqual(result.duration_minutes, 60)


if __name__ == "__main__":
    unittest.main()
