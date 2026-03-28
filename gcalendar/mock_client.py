"""Mock implementation of CalendarMCPClient with realistic data."""

import copy
import uuid
from typing import Optional

from models import (
    Attendee, Calendar, Event, EventList, EventTime,
    FreeSlot, FreeTimeResult, MeetingTimeOption, MeetingTimesResult,
)
from mcp_client import CalendarMCPClient

# ---------------------------------------------------------------------------
# Mock data
# ---------------------------------------------------------------------------

MOCK_CALENDARS: list[Calendar] = [
    Calendar(
        calendar_id="primary",
        summary="Alex Johnson",
        primary=True,
        access_role="owner",
        background_color="#4285f4",
        foreground_color="#ffffff",
        time_zone="America/New_York",
        selected=True,
    ),
    Calendar(
        calendar_id="work@company.com",
        summary="Work",
        access_role="owner",
        background_color="#0b8043",
        foreground_color="#ffffff",
        time_zone="America/New_York",
        selected=True,
    ),
    Calendar(
        calendar_id="family123@group.calendar.google.com",
        summary="Family",
        access_role="owner",
        background_color="#8e24aa",
        foreground_color="#ffffff",
        time_zone="America/New_York",
        selected=True,
    ),
    Calendar(
        calendar_id="birthdays@group.calendar.google.com",
        summary="Birthdays",
        access_role="reader",
        background_color="#ad1457",
        foreground_color="#ffffff",
        time_zone="America/New_York",
        selected=True,
    ),
    Calendar(
        calendar_id="holidays@group.calendar.google.com",
        summary="US Holidays",
        access_role="reader",
        background_color="#616161",
        foreground_color="#ffffff",
        time_zone="America/New_York",
        selected=False,
        description="United States holidays",
    ),
]

MOCK_EVENTS: list[Event] = [
    # --- Monday 2026-03-23 ---
    Event(
        event_id="evt_standup_mon",
        summary="Daily Standup",
        start=EventTime(date_time="2026-03-23T09:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-23T09:15:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        location="https://meet.google.com/abc-defg-hij",
        status="confirmed",
        my_response_status="accepted",
        creator_email="alex.johnson@company.com",
        organizer_email="alex.johnson@company.com",
        recurrence=["RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR"],
        conference_link="https://meet.google.com/abc-defg-hij",
        attendees=[
            Attendee(email="alex.johnson@company.com", display_name="Alex Johnson", response_status="accepted", is_self=True),
            Attendee(email="sarah.chen@company.com", display_name="Sarah Chen", response_status="accepted"),
            Attendee(email="mike.wilson@company.com", display_name="Mike Wilson", response_status="accepted"),
            Attendee(email="lisa.park@company.com", display_name="Lisa Park", response_status="tentative"),
        ],
    ),
    Event(
        event_id="evt_sprint_plan",
        summary="Sprint Planning",
        start=EventTime(date_time="2026-03-23T10:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-23T11:30:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        description="Review backlog items and plan Sprint 24.\n\nAgenda:\n1. Review velocity\n2. Story pointing\n3. Sprint goal",
        location="Conference Room B",
        status="confirmed",
        my_response_status="accepted",
        creator_email="sarah.chen@company.com",
        creator_name="Sarah Chen",
        organizer_email="sarah.chen@company.com",
        organizer_name="Sarah Chen",
        conference_link="https://meet.google.com/sprint-plan",
        attendees=[
            Attendee(email="alex.johnson@company.com", display_name="Alex Johnson", response_status="accepted", is_self=True),
            Attendee(email="sarah.chen@company.com", display_name="Sarah Chen", response_status="accepted", is_organizer=True),
            Attendee(email="mike.wilson@company.com", display_name="Mike Wilson", response_status="accepted"),
            Attendee(email="david.kumar@company.com", display_name="David Kumar", response_status="declined"),
            Attendee(email="lisa.park@company.com", display_name="Lisa Park", response_status="accepted"),
        ],
    ),
    Event(
        event_id="evt_lunch_mon",
        summary="Lunch with Jamie",
        start=EventTime(date_time="2026-03-23T12:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-23T13:00:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        location="Shake Shack, 691 8th Ave",
        status="confirmed",
        my_response_status="accepted",
        creator_email="alex.johnson@company.com",
        attendees=[
            Attendee(email="alex.johnson@company.com", display_name="Alex Johnson", response_status="accepted", is_self=True),
            Attendee(email="jamie.taylor@gmail.com", display_name="Jamie Taylor", response_status="accepted"),
        ],
    ),
    # --- Tuesday 2026-03-24 ---
    Event(
        event_id="evt_standup_tue",
        summary="Daily Standup",
        start=EventTime(date_time="2026-03-24T09:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-24T09:15:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        location="https://meet.google.com/abc-defg-hij",
        status="confirmed",
        my_response_status="accepted",
        recurring_event_id="evt_standup_mon",
        conference_link="https://meet.google.com/abc-defg-hij",
        attendees=[
            Attendee(email="alex.johnson@company.com", display_name="Alex Johnson", response_status="accepted", is_self=True),
            Attendee(email="sarah.chen@company.com", display_name="Sarah Chen", response_status="accepted"),
            Attendee(email="mike.wilson@company.com", display_name="Mike Wilson", response_status="accepted"),
        ],
    ),
    Event(
        event_id="evt_1on1_sarah",
        summary="1:1 with Sarah",
        start=EventTime(date_time="2026-03-24T11:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-24T11:30:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        description="Weekly 1:1 sync.\n\nTopics:\n- Project status\n- Career growth\n- Blockers",
        status="confirmed",
        my_response_status="accepted",
        creator_email="alex.johnson@company.com",
        conference_link="https://meet.google.com/one-on-one",
        attendees=[
            Attendee(email="alex.johnson@company.com", display_name="Alex Johnson", response_status="accepted", is_self=True),
            Attendee(email="sarah.chen@company.com", display_name="Sarah Chen", response_status="accepted"),
        ],
        recurrence=["RRULE:FREQ=WEEKLY;BYDAY=TU"],
    ),
    Event(
        event_id="evt_design_review",
        summary="Design Review: New Dashboard",
        start=EventTime(date_time="2026-03-24T14:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-24T15:00:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        description="Review the new analytics dashboard mockups.\n\nFigma link: https://figma.com/file/abc123",
        location="Design Lab",
        status="confirmed",
        my_response_status="tentative",
        creator_email="emma.wright@company.com",
        creator_name="Emma Wright",
        organizer_email="emma.wright@company.com",
        organizer_name="Emma Wright",
        attendees=[
            Attendee(email="alex.johnson@company.com", display_name="Alex Johnson", response_status="tentative", is_self=True),
            Attendee(email="emma.wright@company.com", display_name="Emma Wright", response_status="accepted", is_organizer=True),
            Attendee(email="sarah.chen@company.com", display_name="Sarah Chen", response_status="accepted"),
            Attendee(email="carlos.mendez@company.com", display_name="Carlos Mendez", response_status="needsAction"),
        ],
        color_id="7",
    ),
    # --- Wednesday 2026-03-25 ---
    Event(
        event_id="evt_standup_wed",
        summary="Daily Standup",
        start=EventTime(date_time="2026-03-25T09:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-25T09:15:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        status="confirmed",
        my_response_status="accepted",
        recurring_event_id="evt_standup_mon",
        conference_link="https://meet.google.com/abc-defg-hij",
    ),
    Event(
        event_id="evt_deep_work",
        summary="Deep Work Block",
        start=EventTime(date_time="2026-03-25T10:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-25T12:00:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        description="Focus time - no meetings. Working on API refactor.",
        status="confirmed",
        my_response_status="accepted",
        creator_email="alex.johnson@company.com",
        color_id="8",
    ),
    Event(
        event_id="evt_team_lunch",
        summary="Team Lunch",
        start=EventTime(date_time="2026-03-25T12:30:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-25T13:30:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        location="Chipotle, 304 W 34th St",
        status="confirmed",
        my_response_status="accepted",
        creator_email="mike.wilson@company.com",
        creator_name="Mike Wilson",
        attendees=[
            Attendee(email="alex.johnson@company.com", display_name="Alex Johnson", response_status="accepted", is_self=True),
            Attendee(email="mike.wilson@company.com", display_name="Mike Wilson", response_status="accepted"),
            Attendee(email="sarah.chen@company.com", display_name="Sarah Chen", response_status="accepted"),
            Attendee(email="lisa.park@company.com", display_name="Lisa Park", response_status="declined"),
        ],
    ),
    Event(
        event_id="evt_retro",
        summary="Sprint Retrospective",
        start=EventTime(date_time="2026-03-25T15:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-25T16:00:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        description="Sprint 23 retrospective.\n\nFormat: Start/Stop/Continue",
        location="https://meet.google.com/retro-meeting",
        status="confirmed",
        my_response_status="accepted",
        creator_email="sarah.chen@company.com",
        conference_link="https://meet.google.com/retro-meeting",
        attendees=[
            Attendee(email="alex.johnson@company.com", display_name="Alex Johnson", response_status="accepted", is_self=True),
            Attendee(email="sarah.chen@company.com", display_name="Sarah Chen", response_status="accepted", is_organizer=True),
            Attendee(email="mike.wilson@company.com", display_name="Mike Wilson", response_status="accepted"),
            Attendee(email="lisa.park@company.com", display_name="Lisa Park", response_status="accepted"),
            Attendee(email="david.kumar@company.com", display_name="David Kumar", response_status="tentative"),
        ],
    ),
    # --- Thursday 2026-03-26 ---
    Event(
        event_id="evt_standup_thu",
        summary="Daily Standup",
        start=EventTime(date_time="2026-03-26T09:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-26T09:15:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        status="confirmed",
        my_response_status="accepted",
        recurring_event_id="evt_standup_mon",
        conference_link="https://meet.google.com/abc-defg-hij",
    ),
    Event(
        event_id="evt_interview",
        summary="Interview: Senior Backend Engineer",
        start=EventTime(date_time="2026-03-26T10:30:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-26T11:30:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        description="Technical interview - system design round.\n\nCandidate: Priya Sharma\nResume: https://drive.google.com/file/resume123",
        location="Interview Room 2",
        status="confirmed",
        my_response_status="accepted",
        creator_email="hr@company.com",
        creator_name="HR Team",
        organizer_email="hr@company.com",
        attendees=[
            Attendee(email="alex.johnson@company.com", display_name="Alex Johnson", response_status="accepted", is_self=True),
            Attendee(email="sarah.chen@company.com", display_name="Sarah Chen", response_status="accepted"),
            Attendee(email="priya.sharma@email.com", display_name="Priya Sharma", response_status="accepted"),
        ],
        color_id="11",
    ),
    Event(
        event_id="evt_product_sync",
        summary="Product Sync",
        start=EventTime(date_time="2026-03-26T14:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-26T14:45:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        description="Weekly product alignment meeting.",
        conference_link="https://meet.google.com/product-sync",
        status="confirmed",
        my_response_status="accepted",
        creator_email="product@company.com",
        attendees=[
            Attendee(email="alex.johnson@company.com", display_name="Alex Johnson", response_status="accepted", is_self=True),
            Attendee(email="nina.patel@company.com", display_name="Nina Patel", response_status="accepted", is_organizer=True),
            Attendee(email="sarah.chen@company.com", display_name="Sarah Chen", response_status="accepted"),
        ],
        recurrence=["RRULE:FREQ=WEEKLY;BYDAY=TH"],
    ),
    # --- Friday 2026-03-27 ---
    Event(
        event_id="evt_standup_fri",
        summary="Daily Standup",
        start=EventTime(date_time="2026-03-27T09:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-27T09:15:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        status="confirmed",
        my_response_status="accepted",
        recurring_event_id="evt_standup_mon",
        conference_link="https://meet.google.com/abc-defg-hij",
    ),
    Event(
        event_id="evt_demo",
        summary="Sprint Demo",
        start=EventTime(date_time="2026-03-27T11:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-27T12:00:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        description="Sprint 23 demo to stakeholders.\n\nPresenting:\n- New dashboard features\n- API performance improvements\n- Bug fixes",
        location="Main Conference Room",
        status="confirmed",
        my_response_status="accepted",
        creator_email="sarah.chen@company.com",
        conference_link="https://meet.google.com/sprint-demo",
        attendees=[
            Attendee(email="alex.johnson@company.com", display_name="Alex Johnson", response_status="accepted", is_self=True),
            Attendee(email="sarah.chen@company.com", display_name="Sarah Chen", response_status="accepted", is_organizer=True),
            Attendee(email="mike.wilson@company.com", display_name="Mike Wilson", response_status="accepted"),
            Attendee(email="nina.patel@company.com", display_name="Nina Patel", response_status="accepted"),
            Attendee(email="cto@company.com", display_name="James Liu", response_status="tentative"),
        ],
        color_id="9",
    ),
    Event(
        event_id="evt_happy_hour",
        summary="Team Happy Hour",
        start=EventTime(date_time="2026-03-27T17:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-27T19:00:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        description="End of sprint celebration! Drinks on the company.",
        location="The Brass Monkey, 55 Little W 12th St",
        status="confirmed",
        my_response_status="accepted",
        creator_email="mike.wilson@company.com",
        creator_name="Mike Wilson",
    ),
    # --- Saturday 2026-03-28 (today) ---
    Event(
        event_id="evt_run",
        summary="Morning Run",
        start=EventTime(date_time="2026-03-28T07:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-28T08:00:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        description="5K in Central Park",
        status="confirmed",
        my_response_status="accepted",
        creator_email="alex.johnson@company.com",
        color_id="2",
    ),
    Event(
        event_id="evt_brunch",
        summary="Brunch with Family",
        start=EventTime(date_time="2026-03-28T11:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-28T13:00:00-04:00", time_zone="America/New_York"),
        calendar_id="family123@group.calendar.google.com",
        location="Sarabeth's, 40 Central Park S",
        status="confirmed",
        my_response_status="accepted",
        creator_email="alex.johnson@company.com",
    ),
    # --- Sunday 2026-03-29 ---
    Event(
        event_id="evt_yoga",
        summary="Yoga Class",
        start=EventTime(date_time="2026-03-29T09:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-29T10:00:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        location="YogaWorks, 459 Broadway",
        status="confirmed",
        my_response_status="accepted",
        color_id="2",
    ),
    Event(
        event_id="evt_meal_prep",
        summary="Meal Prep",
        start=EventTime(date_time="2026-03-29T14:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-29T16:00:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        description="Prep lunches for the week",
        status="confirmed",
        my_response_status="accepted",
    ),
    # --- Monday 2026-03-30 (next week) ---
    Event(
        event_id="evt_standup_next_mon",
        summary="Daily Standup",
        start=EventTime(date_time="2026-03-30T09:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-30T09:15:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        status="confirmed",
        my_response_status="accepted",
        recurring_event_id="evt_standup_mon",
        conference_link="https://meet.google.com/abc-defg-hij",
    ),
    Event(
        event_id="evt_all_hands",
        summary="Company All-Hands",
        start=EventTime(date_time="2026-03-30T13:00:00-04:00", time_zone="America/New_York"),
        end=EventTime(date_time="2026-03-30T14:00:00-04:00", time_zone="America/New_York"),
        calendar_id="primary",
        description="Monthly all-hands meeting.\n\nTopics:\n- Q1 results\n- Q2 goals\n- New hires",
        location="Town Hall / Livestream",
        status="confirmed",
        my_response_status="accepted",
        creator_email="ceo@company.com",
        creator_name="CEO",
        conference_link="https://meet.google.com/all-hands",
    ),
    # --- All-day events ---
    Event(
        event_id="evt_birthday_mom",
        summary="Mom's Birthday",
        start=EventTime(date="2026-03-28", time_zone="America/New_York"),
        end=EventTime(date="2026-03-29", time_zone="America/New_York"),
        calendar_id="birthdays@group.calendar.google.com",
        status="confirmed",
        my_response_status="accepted",
        color_id="4",
    ),
    Event(
        event_id="evt_deadline",
        summary="Q1 Report Deadline",
        start=EventTime(date="2026-03-31", time_zone="America/New_York"),
        end=EventTime(date="2026-04-01", time_zone="America/New_York"),
        calendar_id="work@company.com",
        status="confirmed",
        my_response_status="accepted",
        color_id="11",
        description="Final deadline for Q1 quarterly report submission.",
    ),
    Event(
        event_id="evt_pto",
        summary="PTO - Alex",
        start=EventTime(date="2026-04-03", time_zone="America/New_York"),
        end=EventTime(date="2026-04-06", time_zone="America/New_York"),
        calendar_id="primary",
        status="confirmed",
        my_response_status="accepted",
        description="Long weekend getaway",
        color_id="10",
    ),
]


class MockCalendarClient(CalendarMCPClient):
    """Mock client with realistic calendar data for safe development."""

    def __init__(self) -> None:
        self._calendars = copy.deepcopy(MOCK_CALENDARS)
        self._events = copy.deepcopy(MOCK_EVENTS)

    # -- helpers --

    @staticmethod
    def _normalize_dt(s: str) -> str:
        """Normalize a datetime string for comparison.

        Strips timezone offsets and expands date-only to midnight:
        '2026-03-28T07:00:00-04:00' -> '2026-03-28T07:00:00'
        '2026-03-28T07:00:00Z'      -> '2026-03-28T07:00:00'
        '2026-03-28'                 -> '2026-03-28T00:00:00'
        """
        if not s:
            return s
        if s.endswith("Z"):
            return s[:-1]
        # Strip +/-HH:MM offset
        t_pos = s.find("T")
        if t_pos == -1:
            # Date-only: expand to midnight
            return s + "T00:00:00"
        for i in range(len(s) - 1, t_pos, -1):
            if s[i] in ("+", "-") and ":" in s[i:]:
                return s[:i]
        return s

    def _match_time_range(self, event: Event, time_min: str | None, time_max: str | None) -> bool:
        """Check whether an event falls within the given time window."""
        evt_start = self._normalize_dt(event.start.date_time or event.start.date or "")
        evt_end = self._normalize_dt(event.end.date_time or event.end.date or "")
        if time_min and evt_end and evt_end <= time_min:
            return False
        if time_max and evt_start and evt_start >= time_max:
            return False
        return True

    def _match_query(self, event: Event, q: str) -> bool:
        q_lower = q.lower()
        return (
            q_lower in event.summary.lower()
            or q_lower in event.description.lower()
            or q_lower in event.location.lower()
            or any(q_lower in a.display_name.lower() or q_lower in a.email.lower() for a in event.attendees)
        )

    # -- interface --

    async def list_calendars(self) -> list[Calendar]:
        return list(self._calendars)

    async def list_events(
        self,
        calendar_id: str = "primary",
        time_min: str | None = None,
        time_max: str | None = None,
        q: str | None = None,
        max_results: int = 50,
        page_token: str | None = None,
    ) -> EventList:
        filtered = [e for e in self._events if self._match_time_range(e, time_min, time_max)]
        if q:
            filtered = [e for e in filtered if self._match_query(e, q)]
        # Sort: all-day first, then by start time
        filtered.sort(key=lambda e: (0 if e.start.is_all_day else 1, e.start.date_time or e.start.date or ""))
        # Pagination
        start_idx = 0
        if page_token:
            try:
                start_idx = int(page_token)
            except ValueError:
                start_idx = 0
        page = filtered[start_idx : start_idx + max_results]
        next_token = ""
        if start_idx + max_results < len(filtered):
            next_token = str(start_idx + max_results)
        return EventList(events=page, next_page_token=next_token)

    async def get_event(self, calendar_id: str, event_id: str) -> Event:
        for e in self._events:
            if e.event_id == event_id:
                return copy.deepcopy(e)
        raise ValueError(f"Event not found: {event_id}")

    async def create_event(
        self,
        summary: str,
        start_date_time: str | None = None,
        end_date_time: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        time_zone: str = "UTC",
        description: str = "",
        location: str = "",
        attendees: list[str] | None = None,
        calendar_id: str = "primary",
    ) -> Event:
        event = Event(
            event_id=f"evt_{uuid.uuid4().hex[:8]}",
            summary=summary,
            start=EventTime(date_time=start_date_time, date=start_date, time_zone=time_zone),
            end=EventTime(date_time=end_date_time, date=end_date, time_zone=time_zone),
            calendar_id=calendar_id,
            description=description,
            location=location,
            status="confirmed",
            my_response_status="accepted",
            creator_email="alex.johnson@company.com",
            attendees=[Attendee(email=e) for e in (attendees or [])],
        )
        self._events.append(event)
        return event

    async def update_event(
        self,
        calendar_id: str,
        event_id: str,
        summary: str | None = None,
        start_date_time: str | None = None,
        end_date_time: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        time_zone: str | None = None,
        description: str | None = None,
        location: str | None = None,
        attendees: list[str] | None = None,
    ) -> Event:
        for e in self._events:
            if e.event_id == event_id:
                if summary is not None:
                    e.summary = summary
                if description is not None:
                    e.description = description
                if location is not None:
                    e.location = location
                if start_date_time is not None:
                    e.start.date_time = start_date_time
                if end_date_time is not None:
                    e.end.date_time = end_date_time
                if start_date is not None:
                    e.start.date = start_date
                if end_date is not None:
                    e.end.date = end_date
                if time_zone is not None:
                    e.start.time_zone = time_zone
                    e.end.time_zone = time_zone
                if attendees is not None:
                    e.attendees = [Attendee(email=a) for a in attendees]
                return copy.deepcopy(e)
        raise ValueError(f"Event not found: {event_id}")

    async def delete_event(self, calendar_id: str, event_id: str) -> bool:
        for i, e in enumerate(self._events):
            if e.event_id == event_id:
                self._events.pop(i)
                return True
        raise ValueError(f"Event not found: {event_id}")

    async def respond_to_event(
        self,
        event_id: str,
        response: str,
        calendar_id: str = "primary",
        comment: str = "",
    ) -> Event:
        for e in self._events:
            if e.event_id == event_id:
                e.my_response_status = response
                for a in e.attendees:
                    if a.is_self:
                        a.response_status = response
                return copy.deepcopy(e)
        raise ValueError(f"Event not found: {event_id}")

    async def find_free_time(
        self,
        calendar_ids: list[str],
        time_min: str,
        time_max: str,
        time_zone: str = "UTC",
        min_duration: int = 30,
    ) -> FreeTimeResult:
        return FreeTimeResult(
            slots=[
                FreeSlot(
                    start="2026-03-28T08:00:00-04:00",
                    end="2026-03-28T11:00:00-04:00",
                    start_formatted="8:00 AM",
                    end_formatted="11:00 AM",
                    duration_minutes=180,
                ),
                FreeSlot(
                    start="2026-03-28T13:00:00-04:00",
                    end="2026-03-28T17:00:00-04:00",
                    start_formatted="1:00 PM",
                    end_formatted="5:00 PM",
                    duration_minutes=240,
                ),
                FreeSlot(
                    start="2026-03-29T10:00:00-04:00",
                    end="2026-03-29T14:00:00-04:00",
                    start_formatted="10:00 AM",
                    end_formatted="2:00 PM",
                    duration_minutes=240,
                ),
            ],
            time_zone=time_zone or "America/New_York",
            summary="3 free slots found",
        )

    async def find_meeting_times(
        self,
        attendees: list[str],
        duration: int,
        time_min: str,
        time_max: str,
        time_zone: str = "UTC",
    ) -> MeetingTimesResult:
        return MeetingTimesResult(
            options=[
                MeetingTimeOption(
                    start="2026-03-30T09:30:00-04:00",
                    end="2026-03-30T10:30:00-04:00",
                    start_formatted="Mon 9:30 AM",
                    end_formatted="10:30 AM",
                    duration_minutes=duration,
                    attendee_count=len(attendees) + 1,
                ),
                MeetingTimeOption(
                    start="2026-03-30T15:00:00-04:00",
                    end="2026-03-30T16:00:00-04:00",
                    start_formatted="Mon 3:00 PM",
                    end_formatted="4:00 PM",
                    duration_minutes=duration,
                    attendee_count=len(attendees) + 1,
                ),
                MeetingTimeOption(
                    start="2026-03-31T10:00:00-04:00",
                    end="2026-03-31T11:00:00-04:00",
                    start_formatted="Tue 10:00 AM",
                    end_formatted="11:00 AM",
                    duration_minutes=duration,
                    attendee_count=len(attendees) + 1,
                ),
            ],
            attendees=attendees,
            duration_minutes=duration,
            summary=f"3 times found for {len(attendees) + 1} attendees",
        )
