"""Data models for the Google Calendar console client."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Calendar:
    """A Google Calendar."""
    calendar_id: str
    summary: str
    primary: bool = False
    access_role: str = "reader"
    background_color: str = "#4285f4"
    foreground_color: str = "#ffffff"
    time_zone: str = "UTC"
    selected: bool = True
    description: str = ""


@dataclass
class Attendee:
    """An event attendee."""
    email: str
    display_name: str = ""
    response_status: str = "needsAction"  # accepted, declined, tentative, needsAction
    is_optional: bool = False
    is_organizer: bool = False
    is_self: bool = False


@dataclass
class EventTime:
    """Start or end time for an event."""
    date_time: Optional[str] = None  # RFC3339 for timed events
    date: Optional[str] = None       # YYYY-MM-DD for all-day events
    time_zone: str = "UTC"

    @property
    def is_all_day(self) -> bool:
        return self.date is not None and self.date_time is None


@dataclass
class Event:
    """A calendar event."""
    event_id: str
    summary: str
    start: EventTime
    end: EventTime
    calendar_id: str = "primary"
    description: str = ""
    location: str = ""
    status: str = "confirmed"  # confirmed, tentative, cancelled
    my_response_status: str = "accepted"
    html_link: str = ""
    creator_email: str = ""
    creator_name: str = ""
    organizer_email: str = ""
    organizer_name: str = ""
    attendees: list[Attendee] = field(default_factory=list)
    recurrence: list[str] = field(default_factory=list)
    recurring_event_id: str = ""
    color_id: str = ""
    has_attachments: bool = False
    created: str = ""
    updated: str = ""
    conference_link: str = ""


@dataclass
class EventList:
    """Paginated list of events."""
    events: list[Event] = field(default_factory=list)
    next_page_token: str = ""


@dataclass
class FreeSlot:
    """A free time slot."""
    start: str  # ISO 8601
    end: str
    start_formatted: str = ""
    end_formatted: str = ""
    duration_minutes: int = 0


@dataclass
class FreeTimeResult:
    """Result of a free time search."""
    slots: list[FreeSlot] = field(default_factory=list)
    time_zone: str = "UTC"
    summary: str = ""


@dataclass
class MeetingTimeOption:
    """A suggested meeting time slot."""
    start: str  # ISO 8601
    end: str
    start_formatted: str = ""
    end_formatted: str = ""
    duration_minutes: int = 0
    attendee_count: int = 0


@dataclass
class MeetingTimesResult:
    """Result of finding meeting times."""
    options: list[MeetingTimeOption] = field(default_factory=list)
    attendees: list[str] = field(default_factory=list)
    duration_minutes: int = 0
    summary: str = ""
