"""Production implementation of CalendarMCPClient using Google Calendar MCP tools."""

from typing import Any, Callable, Coroutine, Optional

from models import (
    Attendee, Calendar, Event, EventList, EventTime,
    FreeSlot, FreeTimeResult, MeetingTimeOption, MeetingTimesResult,
)
from mcp_client import CalendarMCPClient


class RealCalendarClient(CalendarMCPClient):
    """Calls the real Google Calendar MCP tools."""

    def __init__(
        self,
        list_calendars_tool: Callable[..., Coroutine],
        list_events_tool: Callable[..., Coroutine],
        get_event_tool: Callable[..., Coroutine],
        create_event_tool: Callable[..., Coroutine],
        update_event_tool: Callable[..., Coroutine],
        delete_event_tool: Callable[..., Coroutine],
        respond_to_event_tool: Callable[..., Coroutine],
        find_free_time_tool: Callable[..., Coroutine],
        find_meeting_times_tool: Callable[..., Coroutine],
    ) -> None:
        self._list_calendars = list_calendars_tool
        self._list_events = list_events_tool
        self._get_event = get_event_tool
        self._create_event = create_event_tool
        self._update_event = update_event_tool
        self._delete_event = delete_event_tool
        self._respond_to_event = respond_to_event_tool
        self._find_free_time = find_free_time_tool
        self._find_meeting_times = find_meeting_times_tool

    # ---- helpers ----

    @staticmethod
    def _parse_calendar(data: dict[str, Any]) -> Calendar:
        return Calendar(
            calendar_id=data.get("id", ""),
            summary=data.get("summaryOverride") or data.get("summary", ""),
            primary=data.get("primary", False),
            access_role=data.get("accessRole", "reader"),
            background_color=data.get("backgroundColor", "#4285f4"),
            foreground_color=data.get("foregroundColor", "#ffffff"),
            time_zone=data.get("timeZone", "UTC"),
            selected=data.get("selected", True),
            description=data.get("description", ""),
        )

    @staticmethod
    def _parse_attendee(data: dict[str, Any]) -> Attendee:
        return Attendee(
            email=data.get("email", ""),
            display_name=data.get("displayName", ""),
            response_status=data.get("responseStatus", "needsAction"),
            is_optional=data.get("optional", False),
            is_organizer=data.get("organizer", False),
            is_self=data.get("self", False),
        )

    @staticmethod
    def _parse_event_time(data: dict[str, Any] | None) -> EventTime:
        if not data:
            return EventTime()
        return EventTime(
            date_time=data.get("dateTime"),
            date=data.get("date"),
            time_zone=data.get("timeZone", "UTC"),
        )

    @classmethod
    def _parse_event(cls, data: dict[str, Any]) -> Event:
        attendees_data = data.get("attendees", [])
        attendees = [cls._parse_attendee(a) for a in attendees_data] if attendees_data else []
        # Extract conference link
        conference_link = ""
        conf_data = data.get("conferenceData")
        if conf_data:
            for ep in conf_data.get("entryPoints", []):
                if ep.get("entryPointType") == "video":
                    conference_link = ep.get("uri", "")
                    break

        creator = data.get("creator", {})
        organizer = data.get("organizer", {})
        return Event(
            event_id=data.get("id", ""),
            summary=data.get("summary", "(No title)"),
            start=cls._parse_event_time(data.get("start")),
            end=cls._parse_event_time(data.get("end")),
            calendar_id=data.get("calendarId", "primary"),
            description=data.get("description", ""),
            location=data.get("location", ""),
            status=data.get("status", "confirmed"),
            my_response_status=data.get("myResponseStatus", "needsAction"),
            html_link=data.get("htmlLink", ""),
            creator_email=creator.get("email", ""),
            creator_name=creator.get("displayName", ""),
            organizer_email=organizer.get("email", ""),
            organizer_name=organizer.get("displayName", ""),
            attendees=attendees,
            recurrence=data.get("recurrence", []),
            recurring_event_id=data.get("recurringEventId", ""),
            color_id=data.get("colorId", ""),
            has_attachments=data.get("hasAttachments", False),
            created=data.get("created", ""),
            updated=data.get("updated", ""),
            conference_link=conference_link,
        )

    # ---- interface ----

    async def list_calendars(self) -> list[Calendar]:
        result = await self._list_calendars()
        calendars_data = result.get("calendars", []) if isinstance(result, dict) else []
        return [self._parse_calendar(c) for c in calendars_data]

    async def list_events(
        self,
        calendar_id: str = "primary",
        time_min: str | None = None,
        time_max: str | None = None,
        q: str | None = None,
        max_results: int = 50,
        page_token: str | None = None,
    ) -> EventList:
        kwargs: dict[str, Any] = {"calendarId": calendar_id, "maxResults": max_results}
        if time_min:
            kwargs["timeMin"] = time_min
        if time_max:
            kwargs["timeMax"] = time_max
        if q:
            kwargs["q"] = q
        if page_token:
            kwargs["pageToken"] = page_token
        result = await self._list_events(**kwargs)
        items = result.get("items", []) if isinstance(result, dict) else []
        events = [self._parse_event(e) for e in items]
        next_token = result.get("nextPageToken", "") if isinstance(result, dict) else ""
        return EventList(events=events, next_page_token=next_token)

    async def get_event(self, calendar_id: str, event_id: str) -> Event:
        result = await self._get_event(calendarId=calendar_id, eventId=event_id)
        return self._parse_event(result if isinstance(result, dict) else {})

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
        event_data: dict[str, Any] = {"summary": summary}
        start: dict[str, str] = {}
        end: dict[str, str] = {}
        if start_date_time:
            start["dateTime"] = start_date_time
        if start_date:
            start["date"] = start_date
        if time_zone:
            start["timeZone"] = time_zone
        if end_date_time:
            end["dateTime"] = end_date_time
        if end_date:
            end["date"] = end_date
        if time_zone:
            end["timeZone"] = time_zone
        event_data["start"] = start
        event_data["end"] = end
        if description:
            event_data["description"] = description
        if location:
            event_data["location"] = location
        if attendees:
            event_data["attendees"] = [{"email": e} for e in attendees]
        result = await self._create_event(calendarId=calendar_id, event=event_data)
        return self._parse_event(result if isinstance(result, dict) else {})

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
        event_data: dict[str, Any] = {}
        if summary is not None:
            event_data["summary"] = summary
        if description is not None:
            event_data["description"] = description
        if location is not None:
            event_data["location"] = location
        if start_date_time or start_date:
            start: dict[str, str] = {}
            if start_date_time:
                start["dateTime"] = start_date_time
            if start_date:
                start["date"] = start_date
            if time_zone:
                start["timeZone"] = time_zone
            event_data["start"] = start
        if end_date_time or end_date:
            end: dict[str, str] = {}
            if end_date_time:
                end["dateTime"] = end_date_time
            if end_date:
                end["date"] = end_date
            if time_zone:
                end["timeZone"] = time_zone
            event_data["end"] = end
        if attendees is not None:
            event_data["attendees"] = [{"email": e} for e in attendees]
        result = await self._update_event(calendarId=calendar_id, eventId=event_id, event=event_data)
        return self._parse_event(result if isinstance(result, dict) else {})

    async def delete_event(self, calendar_id: str, event_id: str) -> bool:
        await self._delete_event(calendarId=calendar_id, eventId=event_id)
        return True

    async def respond_to_event(
        self,
        event_id: str,
        response: str,
        calendar_id: str = "primary",
        comment: str = "",
    ) -> Event:
        kwargs: dict[str, Any] = {
            "eventId": event_id,
            "response": response,
            "calendarId": calendar_id,
        }
        if comment:
            kwargs["comment"] = comment
        result = await self._respond_to_event(**kwargs)
        return self._parse_event(result if isinstance(result, dict) else {})

    async def find_free_time(
        self,
        calendar_ids: list[str],
        time_min: str,
        time_max: str,
        time_zone: str = "UTC",
        min_duration: int = 30,
    ) -> FreeTimeResult:
        result = await self._find_free_time(
            calendarIds=calendar_ids,
            timeMin=time_min,
            timeMax=time_max,
            timeZone=time_zone,
            minDuration=min_duration,
        )
        if not isinstance(result, dict):
            return FreeTimeResult()
        slots = []
        for s in result.get("freeSlots", []):
            slots.append(FreeSlot(
                start=s.get("start", ""),
                end=s.get("end", ""),
                start_formatted=s.get("startFormatted", ""),
                end_formatted=s.get("endFormatted", ""),
                duration_minutes=int(s.get("duration", 0)),
            ))
        return FreeTimeResult(
            slots=slots,
            time_zone=result.get("timeRange", {}).get("timeZone", time_zone),
            summary=result.get("summary", ""),
        )

    async def find_meeting_times(
        self,
        attendees: list[str],
        duration: int,
        time_min: str,
        time_max: str,
        time_zone: str = "UTC",
    ) -> MeetingTimesResult:
        result = await self._find_meeting_times(
            attendees=attendees,
            duration=duration,
            timeMin=time_min,
            timeMax=time_max,
            timeZone=time_zone,
        )
        if not isinstance(result, dict):
            return MeetingTimesResult()
        options = []
        # Parse the formatted text output into options
        # The actual response is formatted text, so we return a summary
        return MeetingTimesResult(
            options=options,
            attendees=attendees,
            duration_minutes=duration,
            summary=str(result) if result else "",
        )
