"""Main application controller for the Google Calendar console client."""

import asyncio
import curses
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Optional

from models import Calendar, Event, EventList, FreeSlot, MeetingTimeOption
from mcp_client import CalendarMCPClient
from colors import (
    init_colors, EMOJI, PAIR_NORMAL, PAIR_ACCENT_RED, PAIR_ACCENT_BLUE,
    PAIR_ACCENT_GREEN, PAIR_STATUS_BAR, PAIR_TITLE,
)
from components import (
    safe_addstr, fill_line, draw_header, draw_status_bar, draw_sidebar,
    draw_event_list, draw_event_detail, draw_event_form, draw_search_bar,
    draw_week_header, draw_free_time_results, draw_meeting_time_results,
    format_date_header, FORM_FIELDS,
)


class View(Enum):
    AGENDA = auto()
    EVENT_DETAIL = auto()
    CREATE_EVENT = auto()
    EDIT_EVENT = auto()
    SEARCH = auto()
    FREE_TIME = auto()
    MEETING_TIMES = auto()
    HELP = auto()


HELP_TEXT = [
    ("Navigation", [
        ("↑/↓, j/k", "Move up / down"),
        ("Enter", "Open event details"),
        ("Esc, q", "Go back / quit"),
        ("Tab", "Switch focus (sidebar ↔ list)"),
    ]),
    ("Day Navigation", [
        ("←/[/h", "Previous day"),
        ("→/]/l", "Next day"),
        ("t", "Jump to today"),
    ]),
    ("Actions", [
        ("n", "Create new event"),
        ("/", "Search events"),
        ("f", "Find free time"),
        ("R", "Refresh events"),
    ]),
    ("Event Detail", [
        ("e", "Edit event"),
        ("D", "Delete event (Shift+D)"),
        ("a", "Accept invitation"),
        ("x", "Decline invitation"),
        ("m", "Maybe (tentative)"),
    ]),
    ("Form", [
        ("Tab", "Next field"),
        ("Shift+Tab", "Previous field"),
        ("Ctrl+S", "Save event"),
        ("Esc", "Cancel"),
    ]),
]


# Sidebar items definition
def _build_sidebar_items(calendars: list[Calendar]) -> list[dict]:
    """Build the sidebar navigation items."""
    items: list[dict] = []
    items.append({"name": "New Event", "emoji": EMOJI["plus"], "action": "new_event", "is_action": True})
    items.append({"name": "─────────────", "emoji": "", "action": "", "is_separator": True})
    items.append({"name": "Today", "emoji": EMOJI["today"], "action": "today"})
    items.append({"name": "< Prev Day", "emoji": EMOJI["back"], "action": "prev_day"})
    items.append({"name": "Next Day >", "emoji": EMOJI["forward"], "action": "next_day"})
    items.append({"name": "Search", "emoji": EMOJI["search"], "action": "search"})
    items.append({"name": "Free Time", "emoji": EMOJI["free_time"], "action": "free_time"})
    items.append({"name": "─────────────", "emoji": "", "action": "", "is_separator": True})
    items.append({"name": "Calendars", "emoji": "", "action": "", "is_heading": True})

    for cal in calendars:
        dot = EMOJI.get("dot_blue", "●")
        name_lower = cal.summary.lower()
        if "family" in name_lower:
            dot = EMOJI.get("dot_purple", "●")
        elif "work" in name_lower:
            dot = EMOJI.get("dot_green", "●")
        elif "birthday" in name_lower:
            dot = EMOJI.get("dot_red", "●")
        elif "holiday" in name_lower:
            dot = EMOJI.get("dot_orange", "●")
        items.append({"name": cal.summary, "emoji": dot, "action": f"calendar:{cal.calendar_id}"})

    items.append({"name": "─────────────", "emoji": "", "action": "", "is_separator": True})
    items.append({"name": "Help", "emoji": EMOJI["question"], "action": "help"})
    items.append({"name": "Quit", "emoji": EMOJI["cross"], "action": "quit"})
    return items


class CalendarApp:
    """Main application state and controller."""

    def __init__(self, client: CalendarMCPClient):
        self.client = client
        self.running = True

        # State
        self.view = View.AGENDA
        self.prev_view: Optional[View] = None

        # Calendar data
        self.calendars: list[Calendar] = []
        self.events: list[Event] = []
        self.current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Sidebar
        self.sidebar_items: list[dict] = []
        self.sidebar_idx = 0
        self.sidebar_scroll = 0
        self.sidebar_focused = False
        self.sidebar_width = 26

        # Event list
        self.event_idx = 0
        self.event_scroll = 0

        # Event detail
        self.detail_event: Optional[Event] = None
        self.detail_scroll = 0

        # Form state (create/edit)
        self.form_values: dict[str, str] = {}
        self.form_field_idx = 0
        self.editing_event: Optional[Event] = None

        # Search state
        self.search_query = ""
        self.search_active = False

        # Free time state
        self.free_slots: list[FreeSlot] = []

        # Meeting times state
        self.meeting_options: list[MeetingTimeOption] = []

        # Status message
        self.status_message = ""
        self.status_is_error = False

        # Loading
        self.loading = False

    async def init(self) -> None:
        """Load initial data."""
        self.loading = True
        try:
            self.calendars = await self.client.list_calendars()
            self.sidebar_items = _build_sidebar_items(self.calendars)
            await self._load_events()
        finally:
            self.loading = False

    async def _load_events(self, query: str = "") -> None:
        """Load events for the selected day, or search across all events."""
        self.loading = True
        try:
            if query:
                # Search across all events (no time range restriction)
                result = await self.client.list_events(
                    q=query,
                    max_results=100,
                )
            else:
                # Single day view
                time_min = self.current_date.strftime("%Y-%m-%dT00:00:00")
                time_max = (self.current_date + timedelta(days=1)).strftime("%Y-%m-%dT00:00:00")
                result = await self.client.list_events(
                    time_min=time_min,
                    time_max=time_max,
                    max_results=100,
                )
            self.events = result.events
            self.event_idx = 0
            self.event_scroll = 0
            if not query:
                self.status_message = f"Loaded {len(self.events)} events"
            else:
                self.status_message = f"{EMOJI['search']} Found {len(self.events)} for: {query}"
        except Exception as e:
            self.status_message = f"Error: {e}"
            self.status_is_error = True
        finally:
            self.loading = False

    def _get_status_hints(self) -> list[tuple[str, str]]:
        """Get context-appropriate key hints for the status bar."""
        if self.view == View.HELP:
            return [("Esc", "Close help")]
        elif self.view in (View.CREATE_EVENT, View.EDIT_EVENT):
            return [("Tab", "Next field"), ("Ctrl+S", "Save"), ("Esc", "Cancel")]
        elif self.view == View.EVENT_DETAIL:
            return [("Esc", "Back"), ("e", "Edit"), ("a", "Accept"), ("x", "Decline"), ("↑↓", "Scroll")]
        elif self.view == View.SEARCH:
            return [("Enter", "Search"), ("Esc", "Cancel")]
        elif self.view in (View.FREE_TIME, View.MEETING_TIMES):
            return [("Esc", "Back")]
        else:
            return [("↑↓", "Navigate"), ("←→", "Day"), ("Enter", "Open"),
                    ("/", "Search"), ("n", "New"), ("?", "Help"), ("q", "Quit")]

    # -----------------------------------------------------------------------
    # Drawing
    # -----------------------------------------------------------------------

    def draw(self, stdscr) -> None:
        """Render the full UI."""
        h, w = stdscr.getmaxyx()
        if h < 10 or w < 40:
            stdscr.clear()
            safe_addstr(stdscr, 0, 0, "Terminal too small!", curses.A_BOLD)
            return

        stdscr.bkgd(" ", curses.color_pair(PAIR_NORMAL))

        # Header (line 0)
        date_label = format_date_header(self.current_date)
        view_name = {
            View.AGENDA: "Agenda",
            View.EVENT_DETAIL: "Event",
            View.CREATE_EVENT: "New Event",
            View.EDIT_EVENT: "Edit Event",
            View.SEARCH: "Search",
            View.FREE_TIME: "Free Time",
            View.MEETING_TIMES: "Meeting Times",
            View.HELP: "Help",
        }.get(self.view, "")
        y = draw_header(stdscr, 0, view_name, date_label=date_label)

        # Margin line below header
        fill_line(stdscr, y, curses.color_pair(PAIR_NORMAL))
        y += 1

        # Search bar — only visible when actively searching
        if self.view == View.SEARCH and self.search_active:
            draw_search_bar(
                stdscr, y, self.sidebar_width,
                self.search_query, self.search_active,
            )
            y += 1

        # Single bottom status bar (last line)
        status_y = h - 1
        hints = self._get_status_hints()
        draw_status_bar(stdscr, status_y, hints, self.status_message, self.status_is_error)

        content_y_start = y
        content_y_end = status_y

        # Sidebar (left panel) — always visible except compose/help
        if self.view not in (View.CREATE_EVENT, View.EDIT_EVENT, View.HELP):
            draw_sidebar(
                stdscr,
                content_y_start,
                content_y_end,
                self.sidebar_width,
                self.sidebar_items,
                self.sidebar_idx,
                self.sidebar_scroll,
            )
            main_x = self.sidebar_width
        else:
            main_x = 0

        # Week header (only in agenda view)
        if self.view in (View.AGENDA, View.SEARCH):
            week_start = self.current_date - timedelta(days=self.current_date.weekday())
            selected_day_off = (self.current_date - week_start).days
            next_y = draw_week_header(stdscr, content_y_start, main_x,
                                       w - main_x, week_start, selected_day_off)
            # Separator
            fill_line(stdscr, next_y, curses.color_pair(PAIR_NORMAL), main_x)
            safe_addstr(stdscr, next_y, main_x + 1, "─" * (w - main_x - 2),
                        curses.color_pair(PAIR_ACCENT_BLUE))
            next_y += 1
            event_y_start = next_y
        else:
            event_y_start = content_y_start

        # Main content area
        if self.view == View.AGENDA:
            draw_event_list(
                stdscr,
                event_y_start,
                content_y_end,
                main_x,
                self.events,
                self.event_idx,
                self.event_scroll,
            )

        elif self.view == View.EVENT_DETAIL and self.detail_event:
            draw_event_detail(
                stdscr,
                content_y_start,
                content_y_end,
                main_x,
                self.detail_event,
                self.detail_scroll,
            )

        elif self.view in (View.CREATE_EVENT, View.EDIT_EVENT):
            active_field = FORM_FIELDS[self.form_field_idx]
            draw_event_form(
                stdscr,
                content_y_start,
                content_y_end,
                main_x,
                self.form_values,
                active_field,
                is_edit=(self.view == View.EDIT_EVENT),
            )

        elif self.view == View.SEARCH:
            draw_event_list(
                stdscr,
                event_y_start,
                content_y_end,
                main_x,
                self.events,
                self.event_idx,
                self.event_scroll,
            )

        elif self.view == View.FREE_TIME:
            draw_free_time_results(
                stdscr,
                content_y_start,
                content_y_end,
                main_x,
                self.free_slots,
            )

        elif self.view == View.MEETING_TIMES:
            draw_meeting_time_results(
                stdscr,
                content_y_start,
                content_y_end,
                main_x,
                self.meeting_options,
            )

        elif self.view == View.HELP:
            self._draw_help(stdscr, content_y_start, content_y_end)

    def _draw_help(self, stdscr, y_start: int, y_end: int) -> None:
        """Draw the help screen (full-screen, same style as Gmail)."""
        h, w = stdscr.getmaxyx()
        attr_normal = curses.color_pair(PAIR_NORMAL)
        attr_title = curses.color_pair(PAIR_ACCENT_BLUE) | curses.A_BOLD
        attr_key = curses.color_pair(PAIR_ACCENT_BLUE) | curses.A_BOLD
        attr_desc = curses.color_pair(PAIR_NORMAL)
        attr_border = curses.color_pair(PAIR_ACCENT_BLUE)

        y = y_start + 1
        fill_line(stdscr, y, attr_normal)
        safe_addstr(stdscr, y, 4, f"{'─' * (w - 8)}", attr_border)
        y += 1
        fill_line(stdscr, y, attr_normal)
        safe_addstr(stdscr, y, 4, f"{EMOJI['calendar']}  Calendar — Keyboard Shortcuts", attr_title)
        y += 1
        fill_line(stdscr, y, attr_normal)
        safe_addstr(stdscr, y, 4, f"{'─' * (w - 8)}", attr_border)
        y += 2

        for section_title, shortcuts in HELP_TEXT:
            if y >= y_end - 2:
                break
            fill_line(stdscr, y, attr_normal)
            safe_addstr(stdscr, y, 6, section_title, attr_title)
            y += 1

            for key, desc in shortcuts:
                if y >= y_end - 2:
                    break
                fill_line(stdscr, y, attr_normal)
                safe_addstr(stdscr, y, 8, f"{key:>12}", attr_key)
                safe_addstr(stdscr, y, 22, desc, attr_desc)
                y += 1
            y += 1

        while y < y_end:
            fill_line(stdscr, y, attr_normal)
            y += 1

    # -----------------------------------------------------------------------
    # Key handling
    # -----------------------------------------------------------------------

    async def handle_key(self, key: int) -> None:
        """Handle a keypress and update state."""
        self.status_message = ""
        self.status_is_error = False

        if self.view == View.HELP:
            if key in (27, ord("q"), ord("?")):
                self.view = self.prev_view or View.AGENDA
            return

        if self.view == View.SEARCH and self.search_active:
            await self._handle_search_input(key)
            return

        if self.view in (View.CREATE_EVENT, View.EDIT_EVENT):
            await self._handle_form_input(key)
            return

        # Global keys
        if key == ord("q"):
            if self.view == View.AGENDA and not self.sidebar_focused:
                self.running = False
            elif self.view in (View.EVENT_DETAIL, View.SEARCH, View.FREE_TIME, View.MEETING_TIMES):
                self.view = View.AGENDA
            elif self.sidebar_focused:
                self.sidebar_focused = False
            return

        if key == 27:  # Escape
            if self.view in (View.EVENT_DETAIL, View.FREE_TIME, View.MEETING_TIMES):
                self.view = self.prev_view or View.AGENDA
                self.detail_event = None
                self.detail_scroll = 0
            elif self.view == View.SEARCH:
                self.search_active = False
                self.view = View.AGENDA
            elif self.sidebar_focused:
                self.sidebar_focused = False
            return

        if key == ord("?"):
            self.prev_view = self.view
            self.view = View.HELP
            return

        if key == ord("n"):
            self._start_create_event()
            return

        if key == ord("/"):
            self.search_query = ""
            self.search_active = True
            self.view = View.SEARCH
            return

        if key == ord("f"):
            await self._load_free_time()
            return

        if key == ord("R"):
            await self._load_events()
            self.status_message = f"{EMOJI['refresh']} Refreshed!"
            return

        # Tab: toggle sidebar focus
        if key == 9:  # Tab
            if self.view in (View.AGENDA, View.SEARCH):
                self.sidebar_focused = not self.sidebar_focused
            return

        # Number keys: quick jump
        if ord("1") <= key <= ord("9"):
            idx = key - ord("1")
            selectable = [i for i, item in enumerate(self.sidebar_items)
                          if not item.get("is_separator") and not item.get("is_heading")]
            if idx < len(selectable):
                self.sidebar_idx = selectable[idx]
                item = self.sidebar_items[selectable[idx]]
                await self._handle_sidebar_action(item.get("action", ""))
            return

        # View-specific keys
        if self.sidebar_focused:
            await self._handle_sidebar_keys(key)
        elif self.view == View.AGENDA:
            await self._handle_agenda_keys(key)
        elif self.view == View.EVENT_DETAIL:
            await self._handle_detail_keys(key)

    def _skip_separators(self, idx: int, direction: int) -> int:
        """Skip separator/heading items when navigating sidebar."""
        while 0 <= idx < len(self.sidebar_items):
            if self.sidebar_items[idx].get("is_separator") or self.sidebar_items[idx].get("is_heading"):
                idx += direction
            else:
                break
        return max(0, min(idx, len(self.sidebar_items) - 1))

    async def _handle_sidebar_keys(self, key: int) -> None:
        """Handle keys when sidebar is focused."""
        if key in (curses.KEY_UP, ord("k")):
            new_idx = self._skip_separators(self.sidebar_idx - 1, -1)
            self.sidebar_idx = new_idx
        elif key in (curses.KEY_DOWN, ord("j")):
            new_idx = self._skip_separators(self.sidebar_idx + 1, 1)
            self.sidebar_idx = new_idx
        elif key in (curses.KEY_ENTER, 10, 13):
            item = self.sidebar_items[self.sidebar_idx]
            action = item.get("action", "")
            await self._handle_sidebar_action(action)

    async def _handle_sidebar_action(self, action: str) -> None:
        """Execute a sidebar action."""
        if action == "quit":
            self.running = False
        elif action == "today":
            self.current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            self.sidebar_focused = False
            self.view = View.AGENDA
            await self._load_events()
        elif action == "prev_day":
            self.current_date -= timedelta(days=1)
            self.sidebar_focused = False
            await self._load_events()
        elif action == "next_day":
            self.current_date += timedelta(days=1)
            self.sidebar_focused = False
            await self._load_events()
        elif action == "new_event":
            self._start_create_event()
            self.sidebar_focused = False
        elif action == "search":
            self.search_query = ""
            self.search_active = True
            self.view = View.SEARCH
            self.sidebar_focused = False
        elif action == "free_time":
            self.sidebar_focused = False
            await self._load_free_time()
        elif action == "help":
            self.prev_view = self.view
            self.view = View.HELP
            self.sidebar_focused = False

    async def _handle_agenda_keys(self, key: int) -> None:
        """Handle keys in agenda view."""
        if key in (curses.KEY_UP, ord("k")):
            self.event_idx = max(0, self.event_idx - 1)
            self._adjust_event_scroll()
        elif key in (curses.KEY_DOWN, ord("j")):
            self.event_idx = min(len(self.events) - 1, self.event_idx + 1)
            self._adjust_event_scroll()
        elif key in (curses.KEY_ENTER, 10, 13):
            await self._open_event_detail()
        elif key == ord("t"):
            self.current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            await self._load_events()
        elif key in (ord("]"), ord("l"), curses.KEY_RIGHT):
            self.current_date += timedelta(days=1)
            await self._load_events()
        elif key in (ord("["), ord("h"), curses.KEY_LEFT):
            self.current_date -= timedelta(days=1)
            await self._load_events()

    async def _handle_detail_keys(self, key: int) -> None:
        """Handle keys in event detail view."""
        if key in (curses.KEY_UP, ord("k")):
            self.detail_scroll = max(0, self.detail_scroll - 1)
        elif key in (curses.KEY_DOWN, ord("j")):
            self.detail_scroll += 1
        elif key == curses.KEY_PPAGE:
            self.detail_scroll = max(0, self.detail_scroll - 10)
        elif key == curses.KEY_NPAGE:
            self.detail_scroll += 10
        elif key == ord("e"):
            if self.detail_event:
                self._start_edit_event(self.detail_event)
        elif key == ord("D"):
            if self.detail_event:
                await self._delete_event(self.detail_event)
        elif key == ord("a"):
            if self.detail_event:
                await self._respond_event(self.detail_event, "accepted")
        elif key == ord("x"):
            if self.detail_event:
                await self._respond_event(self.detail_event, "declined")
        elif key == ord("m"):
            if self.detail_event:
                await self._respond_event(self.detail_event, "tentative")

    async def _handle_search_input(self, key: int) -> None:
        """Handle keys during search input."""
        if key == 27:  # Escape
            self.search_active = False
            self.view = View.AGENDA
        elif key in (curses.KEY_ENTER, 10, 13):
            self.search_active = False
            if self.search_query:
                await self._load_events(query=self.search_query)
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            self.search_query = self.search_query[:-1]
        elif 32 <= key <= 126:
            self.search_query += chr(key)

    async def _handle_form_input(self, key: int) -> None:
        """Handle keys in compose/create/edit view."""
        if key == 27:  # Escape
            self.view = self.prev_view or View.AGENDA
        elif key == 19:  # Ctrl+S
            await self._save_event()
        elif key == 9:  # Tab — next field
            self.form_field_idx = (self.form_field_idx + 1) % len(FORM_FIELDS)
        elif key == 353:  # Shift+Tab
            self.form_field_idx = (self.form_field_idx - 1) % len(FORM_FIELDS)
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            field = FORM_FIELDS[self.form_field_idx]
            self.form_values[field] = self.form_values.get(field, "")[:-1]
        elif 32 <= key <= 126:
            field = FORM_FIELDS[self.form_field_idx]
            self.form_values[field] = self.form_values.get(field, "") + chr(key)

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    async def _open_event_detail(self) -> None:
        """Open the currently selected event."""
        if not self.events or self.event_idx >= len(self.events):
            return
        self.detail_event = self.events[self.event_idx]
        self.detail_scroll = 0
        self.prev_view = self.view
        self.view = View.EVENT_DETAIL

    def _start_create_event(self) -> None:
        self.form_values = {
            "summary": "",
            "date": self.current_date.strftime("%Y-%m-%d"),
            "start_time": "09:00",
            "end_time": "10:00",
            "location": "",
            "description": "",
            "attendees": "",
        }
        self.form_field_idx = 0
        self.editing_event = None
        self.prev_view = self.view
        self.view = View.CREATE_EVENT

    def _start_edit_event(self, event: Event) -> None:
        dt_start = ""
        dt_end = ""
        date_val = ""

        if event.start.date_time and "T" in event.start.date_time:
            date_val = event.start.date_time.split("T")[0]
            dt_start = event.start.date_time.split("T")[1][:5]
        elif event.start.date:
            date_val = event.start.date

        if event.end.date_time and "T" in event.end.date_time:
            dt_end = event.end.date_time.split("T")[1][:5]

        self.form_values = {
            "summary": event.summary,
            "date": date_val,
            "start_time": dt_start,
            "end_time": dt_end,
            "location": event.location,
            "description": event.description.replace("\n", " "),
            "attendees": ", ".join(a.email for a in event.attendees if not a.is_self),
        }
        self.form_field_idx = 0
        self.editing_event = event
        self.prev_view = self.view
        self.view = View.EDIT_EVENT

    async def _save_event(self) -> None:
        summary = self.form_values.get("summary", "").strip()
        if not summary:
            self.status_message = "Title is required"
            self.status_is_error = True
            return

        date_str = self.form_values.get("date", "")
        start_time = self.form_values.get("start_time", "")
        end_time = self.form_values.get("end_time", "")
        location = self.form_values.get("location", "")
        description = self.form_values.get("description", "")
        attendees_str = self.form_values.get("attendees", "")

        attendees = [a.strip() for a in attendees_str.split(",") if a.strip()] if attendees_str else None
        tz = "America/New_York"

        start_dt = None
        end_dt = None
        start_d = None
        end_d = None

        if start_time and date_str:
            start_dt = f"{date_str}T{start_time}:00"
            end_dt = f"{date_str}T{end_time}:00" if end_time else f"{date_str}T{start_time}:00"
        elif date_str:
            start_d = date_str
            try:
                end_date = datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)
                end_d = end_date.strftime("%Y-%m-%d")
            except ValueError:
                end_d = date_str

        try:
            if self.editing_event:
                await self.client.update_event(
                    calendar_id=self.editing_event.calendar_id or "primary",
                    event_id=self.editing_event.event_id,
                    summary=summary,
                    start_date_time=start_dt,
                    end_date_time=end_dt,
                    start_date=start_d,
                    end_date=end_d,
                    time_zone=tz,
                    description=description,
                    location=location,
                    attendees=attendees,
                )
                self.status_message = f"{EMOJI['check']} Updated: {summary}"
            else:
                await self.client.create_event(
                    summary=summary,
                    start_date_time=start_dt,
                    end_date_time=end_dt,
                    start_date=start_d,
                    end_date=end_d,
                    time_zone=tz,
                    description=description,
                    location=location,
                    attendees=attendees,
                )
                self.status_message = f"{EMOJI['check']} Created: {summary}"
        except Exception as e:
            self.status_message = f"Error: {e}"
            self.status_is_error = True
            return

        self.view = View.AGENDA
        await self._load_events()

    async def _delete_event(self, event: Event) -> None:
        try:
            await self.client.delete_event(event.calendar_id or "primary", event.event_id)
            self.status_message = f"Deleted: {event.summary}"
            self.view = View.AGENDA
            self.detail_event = None
            await self._load_events()
        except Exception as e:
            self.status_message = f"Error: {e}"
            self.status_is_error = True

    async def _respond_event(self, event: Event, response: str) -> None:
        try:
            updated = await self.client.respond_to_event(
                event_id=event.event_id,
                response=response,
                calendar_id=event.calendar_id or "primary",
            )
            self.detail_event = updated
            label = {"accepted": "Accepted", "declined": "Declined", "tentative": "Maybe"}.get(response, response)
            self.status_message = f"{EMOJI['check']} {label}: {event.summary}"
        except Exception as e:
            self.status_message = f"Error: {e}"
            self.status_is_error = True

    async def _load_free_time(self) -> None:
        try:
            time_min = self.current_date.strftime("%Y-%m-%dT00:00:00")
            time_max = (self.current_date + timedelta(days=3)).strftime("%Y-%m-%dT23:59:59")
            result = await self.client.find_free_time(
                calendar_ids=["primary"],
                time_min=time_min,
                time_max=time_max,
                time_zone="America/New_York",
            )
            self.free_slots = result.slots
            self.prev_view = self.view
            self.view = View.FREE_TIME
        except Exception as e:
            self.status_message = f"Error: {e}"
            self.status_is_error = True

    def _adjust_event_scroll(self, visible_height: int = 30) -> None:
        """Adjust scroll to keep selected event visible."""
        lines_per_event = 3
        visible_events = max(1, visible_height // lines_per_event)
        if self.event_idx < self.event_scroll:
            self.event_scroll = self.event_idx
        elif self.event_idx >= self.event_scroll + visible_events:
            self.event_scroll = self.event_idx - visible_events + 1


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_app(client: CalendarMCPClient) -> None:
    """Main entry point for the curses app."""

    app = CalendarApp(client)

    def curses_main(stdscr):
        init_colors()
        curses.curs_set(0)
        stdscr.nodelay(False)
        stdscr.timeout(100)
        curses.mousemask(0)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(app.init())

        while app.running:
            try:
                stdscr.erase()
                app.draw(stdscr)
                stdscr.refresh()

                key = stdscr.getch()
                if key == -1:
                    continue

                if key == curses.KEY_RESIZE:
                    stdscr.clear()
                    continue

                loop.run_until_complete(app.handle_key(key))

            except KeyboardInterrupt:
                break

        loop.close()

    curses.wrapper(curses_main)
