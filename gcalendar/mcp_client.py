"""Abstract base class for Google Calendar MCP client."""

from abc import ABC, abstractmethod
from typing import Optional

from models import (
    Calendar, Event, EventList, FreeTimeResult, MeetingTimesResult,
)


class CalendarMCPClient(ABC):
    """Interface for interacting with Google Calendar via MCP."""

    @abstractmethod
    async def list_calendars(self) -> list[Calendar]:
        """List all calendars in the user's calendar list."""
        ...

    @abstractmethod
    async def list_events(
        self,
        calendar_id: str = "primary",
        time_min: Optional[str] = None,
        time_max: Optional[str] = None,
        q: Optional[str] = None,
        max_results: int = 50,
        page_token: Optional[str] = None,
    ) -> EventList:
        """List events within a time range, with optional search."""
        ...

    @abstractmethod
    async def get_event(self, calendar_id: str, event_id: str) -> Event:
        """Get full details for a single event."""
        ...

    @abstractmethod
    async def create_event(
        self,
        summary: str,
        start_date_time: Optional[str] = None,
        end_date_time: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        time_zone: str = "UTC",
        description: str = "",
        location: str = "",
        attendees: Optional[list[str]] = None,
        calendar_id: str = "primary",
    ) -> Event:
        """Create a new calendar event."""
        ...

    @abstractmethod
    async def update_event(
        self,
        calendar_id: str,
        event_id: str,
        summary: Optional[str] = None,
        start_date_time: Optional[str] = None,
        end_date_time: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        time_zone: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        attendees: Optional[list[str]] = None,
    ) -> Event:
        """Update an existing event."""
        ...

    @abstractmethod
    async def delete_event(self, calendar_id: str, event_id: str) -> bool:
        """Delete an event. Returns True on success."""
        ...

    @abstractmethod
    async def respond_to_event(
        self,
        event_id: str,
        response: str,
        calendar_id: str = "primary",
        comment: str = "",
    ) -> Event:
        """Respond to an event invitation (accepted/declined/tentative)."""
        ...

    @abstractmethod
    async def find_free_time(
        self,
        calendar_ids: list[str],
        time_min: str,
        time_max: str,
        time_zone: str = "UTC",
        min_duration: int = 30,
    ) -> FreeTimeResult:
        """Find free time slots across calendars."""
        ...

    @abstractmethod
    async def find_meeting_times(
        self,
        attendees: list[str],
        duration: int,
        time_min: str,
        time_max: str,
        time_zone: str = "UTC",
    ) -> MeetingTimesResult:
        """Find times when all attendees are available."""
        ...
