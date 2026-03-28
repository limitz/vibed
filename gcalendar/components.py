"""Reusable curses UI components for the Google Calendar client."""

import curses
import textwrap
from datetime import datetime, timedelta
from typing import Optional

from models import Attendee, Calendar, Event, EventTime, FreeSlot, MeetingTimeOption
from colors import (
    EMOJI,
    PAIR_NORMAL, PAIR_HEADER, PAIR_SIDEBAR, PAIR_SIDEBAR_SELECTED,
    PAIR_STATUS_BAR, PAIR_EVENT_NORMAL, PAIR_EVENT_DIM,
    PAIR_EVENT_SELECTED, PAIR_EVENT_SELECTED_BOLD,
    PAIR_ACCENT_RED, PAIR_ACCENT_BLUE, PAIR_ACCENT_GREEN,
    PAIR_ACCENT_YELLOW, PAIR_ACCENT_PURPLE,
    PAIR_INPUT, PAIR_BORDER, PAIR_SNIPPET, PAIR_DATE,
    PAIR_CAL_BLUE, PAIR_TITLE, PAIR_COMPOSE_FIELD,
    PAIR_HELP_KEY, PAIR_HELP_DESC, PAIR_TAB_ACTIVE, PAIR_TAB_INACTIVE,
    PAIR_SEARCH_BOX, PAIR_CAL_GREEN, PAIR_CAL_RED, PAIR_CAL_PURPLE,
    PAIR_CAL_YELLOW, PAIR_CAL_ORANGE, PAIR_CAL_GRAPHITE,
    PAIR_STATUS_MSG, PAIR_STATUS_ERR, PAIR_TODAY_HIGHLIGHT,
    PAIR_LINK, PAIR_NOW_LINE,
)


# ---------------------------------------------------------------------------
# Safe drawing helpers
# ---------------------------------------------------------------------------

def safe_addstr(win, y: int, x: int, text: str, attr: int = 0, max_width: int = 0) -> None:
    """Write text to window, clipping to avoid curses errors at boundaries."""
    h, w = win.getmaxyx()
    if y < 0 or y >= h or x >= w:
        return
    if max_width > 0:
        available = min(max_width, w - x)
    else:
        available = w - x
    if available <= 0:
        return
    clipped = text[:available]
    try:
        win.addstr(y, x, clipped, attr)
    except curses.error:
        pass


def fill_line(win, y: int, attr: int, start_x: int = 0) -> None:
    """Fill the rest of a line with the given attribute."""
    h, w = win.getmaxyx()
    if y < 0 or y >= h:
        return
    remaining = w - start_x
    if remaining > 0:
        safe_addstr(win, y, start_x, " " * remaining, attr)


# ---------------------------------------------------------------------------
# Date / time formatting helpers
# ---------------------------------------------------------------------------

def parse_event_datetime(et: EventTime) -> Optional[datetime]:
    """Parse an EventTime into a datetime object."""
    if et.date_time:
        s = et.date_time
        # Strip timezone suffix: Z, +HH:MM, -HH:MM
        if s.endswith("Z"):
            s = s[:-1]
        else:
            # Look for +/-HH:MM offset after the time part (index 19+)
            for sep_idx in range(len(s) - 1, 9, -1):
                if s[sep_idx] in ("+", "-") and ":" in s[sep_idx:]:
                    s = s[:sep_idx]
                    break
        try:
            return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            try:
                return datetime.strptime(s, "%Y-%m-%dT%H:%M")
            except ValueError:
                return None
    elif et.date:
        try:
            return datetime.strptime(et.date, "%Y-%m-%d")
        except ValueError:
            return None
    return None


def format_time(et: EventTime) -> str:
    """Format an EventTime as a short time string like '9:00 AM'."""
    dt = parse_event_datetime(et)
    if not dt:
        return ""
    if et.is_all_day:
        return "All day"
    return dt.strftime("%-I:%M %p").lstrip("0")


def format_time_range(start: EventTime, end: EventTime) -> str:
    """Format a start-end time range like '9:00 AM – 10:30 AM'."""
    if start.is_all_day:
        return "All day"
    s = format_time(start)
    e = format_time(end)
    if s and e:
        return f"{s} – {e}"
    return s or e or ""


def format_date_header(dt: datetime) -> str:
    """Format a date for use as a section header."""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    delta = (dt.replace(hour=0, minute=0, second=0, microsecond=0) - today).days
    day_name = dt.strftime("%A")
    date_str = dt.strftime("%b %-d")
    if delta == 0:
        return f"Today · {day_name}, {date_str}"
    elif delta == 1:
        return f"Tomorrow · {day_name}, {date_str}"
    elif delta == -1:
        return f"Yesterday · {day_name}, {date_str}"
    else:
        return f"{day_name}, {date_str}"


def format_event_duration(start: EventTime, end: EventTime) -> str:
    """Calculate and format event duration."""
    s = parse_event_datetime(start)
    e = parse_event_datetime(end)
    if not s or not e:
        return ""
    delta = e - s
    minutes = int(delta.total_seconds() // 60)
    if minutes < 60:
        return f"{minutes}m"
    hours = minutes // 60
    mins = minutes % 60
    if mins:
        return f"{hours}h {mins}m"
    return f"{hours}h"


def response_status_symbol(status: str) -> str:
    """Get a symbol for an attendee's response status."""
    return {
        "accepted": EMOJI["accepted"],
        "declined": EMOJI["declined"],
        "tentative": EMOJI["tentative"],
        "needsAction": EMOJI["pending"],
    }.get(status, "?")


def response_status_pair(status: str) -> int:
    """Get a color pair for a response status."""
    return {
        "accepted": PAIR_ACCENT_GREEN,
        "declined": PAIR_ACCENT_RED,
        "tentative": PAIR_ACCENT_YELLOW,
        "needsAction": PAIR_SNIPPET,
    }.get(status, PAIR_NORMAL)


def event_color_pair(color_id: str) -> int:
    """Map a Google Calendar colorId to a curses color pair."""
    return {
        "1": PAIR_CAL_PURPLE,    # Lavender
        "2": PAIR_CAL_GREEN,     # Sage
        "3": PAIR_CAL_PURPLE,    # Grape
        "4": PAIR_CAL_RED,       # Flamingo
        "5": PAIR_CAL_YELLOW,    # Banana
        "6": PAIR_CAL_ORANGE,    # Tangerine
        "7": PAIR_CAL_BLUE,      # Peacock
        "8": PAIR_CAL_GRAPHITE,  # Graphite
        "9": PAIR_CAL_BLUE,      # Blueberry
        "10": PAIR_CAL_GREEN,    # Basil
        "11": PAIR_CAL_RED,      # Tomato
    }.get(color_id, PAIR_CAL_BLUE)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

def draw_header(win, y: int, current_view: str, date_label: str = "") -> int:
    """Draw the top header bar. Returns next y position."""
    h, w = win.getmaxyx()
    attr = curses.color_pair(PAIR_HEADER) | curses.A_BOLD

    fill_line(win, y, attr)

    # Calendar icon + title
    safe_addstr(win, y, 1, EMOJI["calendar"], attr)
    safe_addstr(win, y, 4, "Calendar", attr)

    # Current view indicator
    safe_addstr(win, y, 13, current_view, attr)

    # Date label on right
    if date_label:
        safe_addstr(win, y, w - len(date_label) - 2, date_label, attr)

    return y + 1


# ---------------------------------------------------------------------------
# Status bar
# ---------------------------------------------------------------------------

def draw_status_bar(
    win,
    y: int,
    hints: list[tuple[str, str]],
    status_message: str = "",
    status_is_error: bool = False,
) -> int:
    """Draw the single bottom status bar with key hints and status message."""
    h, w = win.getmaxyx()
    attr_bar = curses.color_pair(PAIR_STATUS_BAR)
    attr_key = curses.color_pair(PAIR_HELP_KEY) | curses.A_BOLD
    attr_desc = curses.color_pair(PAIR_HELP_DESC)

    fill_line(win, y, attr_bar)

    x = 1
    if status_message:
        attr_msg = curses.color_pair(PAIR_STATUS_ERR) if status_is_error else curses.color_pair(PAIR_STATUS_MSG)
        safe_addstr(win, y, x, f" {status_message} ", attr_msg)
        x += len(status_message) + 3
        safe_addstr(win, y, x, "│", attr_bar)
        x += 2

    for key, desc in hints:
        if x >= w - 10:
            break
        safe_addstr(win, y, x, f" {key} ", attr_key)
        x += len(key) + 2
        safe_addstr(win, y, x, f" {desc}", attr_desc)
        x += len(desc) + 3

    return y + 1


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

def draw_sidebar(
    win,
    y_start: int,
    y_end: int,
    width: int,
    items: list[dict],
    selected_idx: int,
    scroll_offset: int = 0,
) -> None:
    """Draw the sidebar with navigation items and calendar list.

    Each item dict has: name, emoji, count (optional)
    Supports: is_separator (divider line), is_action (button style), is_heading
    """
    attr_normal = curses.color_pair(PAIR_SIDEBAR)
    attr_selected = curses.color_pair(PAIR_SIDEBAR_SELECTED) | curses.A_BOLD
    attr_border = curses.color_pair(PAIR_BORDER)
    attr_action = curses.color_pair(PAIR_ACCENT_BLUE) | curses.A_BOLD
    attr_action_sel = curses.color_pair(PAIR_TAB_ACTIVE) | curses.A_BOLD

    visible = y_end - y_start
    for i in range(visible):
        idx = i + scroll_offset
        y = y_start + i

        if idx >= len(items):
            fill_line(win, y, attr_normal, 0)
            safe_addstr(win, y, width - 1, "│", attr_border)
            continue

        item = items[idx]
        is_selected = idx == selected_idx
        is_separator = item.get("is_separator", False)
        is_action = item.get("is_action", False)
        is_heading = item.get("is_heading", False)

        # Separator line
        if is_separator:
            fill_line(win, y, attr_normal, 0)
            safe_addstr(win, y, 2, "─" * (width - 4), attr_border)
            safe_addstr(win, y, width - 1, "│", attr_border)
            continue

        # Section heading
        if is_heading:
            fill_line(win, y, attr_normal, 0)
            name = item.get("name", "")
            safe_addstr(win, y, 2, name, attr_normal | curses.A_BOLD)
            safe_addstr(win, y, width - 1, "│", attr_border)
            continue

        # Action button style (like Compose in Gmail)
        if is_action:
            if is_selected:
                fill_line(win, y, attr_action_sel, 0)
                safe_addstr(win, y, 0, "▌", curses.color_pair(PAIR_ACCENT_GREEN) | curses.A_BOLD)
            else:
                fill_line(win, y, attr_normal, 0)
            emoji = item.get("emoji", "")
            name = item.get("name", "")
            text = f" {emoji} {name} "
            attr = attr_action_sel if is_selected else attr_action
            safe_addstr(win, y, 2, text, attr)
            safe_addstr(win, y, width - 1, "│", attr_border)
            continue

        # Normal item
        attr = attr_selected if is_selected else attr_normal
        fill_line(win, y, attr, 0)

        # Selection indicator
        if is_selected:
            safe_addstr(win, y, 0, "▌", curses.color_pair(PAIR_ACCENT_BLUE) | curses.A_BOLD)

        x = 2
        emoji = item.get("emoji", "")
        if emoji:
            safe_addstr(win, y, x, emoji, attr)
            x += 3

        name = item.get("name", "")
        max_name_w = width - x - 3
        if len(name) > max_name_w:
            name = name[:max_name_w - 1] + "…"
        safe_addstr(win, y, x, name, attr)

        # Right border
        safe_addstr(win, y, width - 1, "│", attr_border)


# ---------------------------------------------------------------------------
# Event list (agenda view) — similar to Gmail's email list
# ---------------------------------------------------------------------------

def _build_agenda_lines(events: list[Event], selected_idx: int = -1,
                        show_date_headers: bool = True) -> list[dict]:
    """Build display lines for agenda view."""
    lines: list[dict] = []
    current_date = ""

    for idx, event in enumerate(events):
        dt = parse_event_datetime(event.start)
        if dt and show_date_headers:
            date_key = dt.strftime("%Y-%m-%d")
            if date_key != current_date:
                current_date = date_key
                header = format_date_header(dt)
                today_str = datetime.now().strftime("%Y-%m-%d")
                is_today = date_key == today_str
                lines.append({
                    "type": "date_header",
                    "text": header,
                    "is_today": is_today,
                    "event_idx": -1,
                })

        lines.append({
            "type": "event",
            "event": event,
            "event_idx": idx,
        })

    return lines


def draw_event_list(
    win,
    y_start: int,
    y_end: int,
    x_start: int,
    events: list[Event],
    selected_idx: int,
    scroll_offset: int = 0,
    show_date_headers: bool = True,
) -> None:
    """Draw the event list. Each event gets 2 lines + separator (3 total)."""
    h, w = win.getmaxyx()
    attr_normal = curses.color_pair(PAIR_NORMAL)

    if not events:
        fill_line(win, y_start + 2, attr_normal, x_start)
        safe_addstr(win, y_start + 2, x_start + 4,
                    "No events found.", curses.color_pair(PAIR_SNIPPET))
        fill_line(win, y_start + 3, attr_normal, x_start)
        safe_addstr(win, y_start + 3, x_start + 4,
                    f"Press 'n' to create a new event.",
                    curses.color_pair(PAIR_SNIPPET))
        return

    lines = _build_agenda_lines(events, selected_idx, show_date_headers)
    content_w = w - x_start

    y = y_start
    event_i = 0  # track which event we're drawing for scroll
    draw_i = 0   # track scroll position

    for line in lines:
        if y >= y_end:
            break

        if line["type"] == "date_header":
            if draw_i < scroll_offset:
                draw_i += 1
                continue
            draw_i += 1

            attr_hdr = curses.color_pair(PAIR_TODAY_HIGHLIGHT if line["is_today"] else PAIR_EVENT_DIM) | curses.A_BOLD
            fill_line(win, y, attr_hdr if line["is_today"] else attr_normal, x_start)
            safe_addstr(win, y, x_start + 2, f" {line['text']}", attr_hdr)
            y += 1
            if y >= y_end:
                break
            # Separator after header
            fill_line(win, y, attr_normal, x_start)
            safe_addstr(win, y, x_start + 2, "─" * (content_w - 4), curses.color_pair(PAIR_BORDER))
            y += 1
            continue

        # Event entry (3 lines: line1, line2, separator)
        if draw_i < scroll_offset:
            draw_i += 1
            continue
        draw_i += 1

        event = line["event"]
        idx = line["event_idx"]
        is_selected = idx == selected_idx

        color_pair = event_color_pair(event.color_id) if event.color_id else PAIR_CAL_BLUE

        if is_selected:
            attr_main = curses.color_pair(PAIR_EVENT_SELECTED_BOLD) | curses.A_BOLD
            attr_detail = curses.color_pair(PAIR_EVENT_SELECTED)
        else:
            attr_main = curses.color_pair(PAIR_EVENT_NORMAL)
            attr_detail = curses.color_pair(PAIR_SNIPPET)

        # Line 1: [▌] [●] time  title  (duration)
        fill_line(win, y, curses.color_pair(PAIR_EVENT_SELECTED if is_selected else PAIR_NORMAL), x_start)
        x = x_start + 1

        if is_selected:
            safe_addstr(win, y, x_start, "▌", curses.color_pair(PAIR_ACCENT_BLUE) | curses.A_BOLD)

        # Color dot
        safe_addstr(win, y, x, EMOJI["dot"], curses.color_pair(color_pair))
        x += 2

        # Time
        time_str = format_time_range(event.start, event.end)
        max_time = min(24, content_w // 3)
        safe_addstr(win, y, x, time_str[:max_time], attr_main)
        x += max_time + 1

        # Title
        title = event.summary
        duration = format_event_duration(event.start, event.end)
        dur_text = f" ({duration})" if duration and not event.start.is_all_day else ""

        # Date on the right
        right_text = ""
        if event.my_response_status and event.my_response_status != "accepted":
            sym = response_status_symbol(event.my_response_status)
            right_text = f" {sym} "
        right_x = w - len(right_text) - 1 if right_text else w

        max_title = right_x - x - len(dur_text) - 1
        if max_title > 0:
            if len(title) > max_title:
                title = title[:max_title - 1] + "…"
            safe_addstr(win, y, x, title, attr_main)
            safe_addstr(win, y, x + len(title), dur_text,
                        curses.color_pair(PAIR_DATE if not is_selected else PAIR_EVENT_SELECTED))

        if right_text:
            safe_addstr(win, y, right_x, right_text,
                        curses.color_pair(response_status_pair(event.my_response_status)))

        y += 1
        if y >= y_end:
            break

        # Line 2: detail (location / video / attendees)
        fill_line(win, y, curses.color_pair(PAIR_EVENT_SELECTED if is_selected else PAIR_NORMAL), x_start)
        detail = ""
        if event.location:
            detail = f"{EMOJI['location']} {event.location}"
        elif event.conference_link:
            detail = f"{EMOJI['video']} Video call"
        elif event.attendees:
            count = len(event.attendees)
            detail = f"{EMOJI['people']} {count} attendee{'s' if count != 1 else ''}"

        if detail:
            safe_addstr(win, y, x_start + 6, detail[:content_w - 8], attr_detail)

        y += 1
        if y >= y_end:
            break

        # Separator
        fill_line(win, y, attr_normal, x_start)
        safe_addstr(win, y, x_start + 1, "─" * (content_w - 2), curses.color_pair(PAIR_BORDER))
        y += 1

    # Fill remaining
    while y < y_end:
        fill_line(win, y, attr_normal, x_start)
        y += 1


# ---------------------------------------------------------------------------
# Event detail view
# ---------------------------------------------------------------------------

def _build_event_detail_lines(event: Event, width: int) -> list[tuple[str, int]]:
    """Build rendered lines for a detailed event view."""
    lines: list[tuple[str, int]] = []
    attr_title = curses.color_pair(PAIR_TITLE) | curses.A_BOLD
    attr_field = curses.color_pair(PAIR_ACCENT_BLUE)
    attr_body = curses.color_pair(PAIR_NORMAL)
    attr_dim = curses.color_pair(PAIR_SNIPPET)
    attr_border = curses.color_pair(PAIR_BORDER)
    attr_link = curses.color_pair(PAIR_LINK)

    # Title
    lines.append(("", attr_body))
    for sub_line in textwrap.wrap(event.summary, width - 2):
        lines.append((f" {sub_line}", attr_title))
    lines.append(("", attr_body))
    lines.append((" " + "─" * (width - 2), attr_border))
    lines.append(("", attr_body))

    # Date + time
    dt_start = parse_event_datetime(event.start)
    if event.start.is_all_day:
        if dt_start:
            lines.append((f" {EMOJI['calendar']} Date:  {dt_start.strftime('%A, %B %-d, %Y')}", attr_field))
        lines.append((f" {EMOJI['clock']} Time:  All day", attr_dim))
    else:
        if dt_start:
            lines.append((f" {EMOJI['calendar']} Date:  {dt_start.strftime('%A, %B %-d, %Y')}", attr_field))
        time_range = format_time_range(event.start, event.end)
        duration = format_event_duration(event.start, event.end)
        lines.append((f" {EMOJI['clock']} Time:  {time_range}  ({duration})", attr_dim))

    # Location
    if event.location:
        lines.append((f" {EMOJI['location']} Where: {event.location}", attr_field))

    # Video link
    if event.conference_link:
        lines.append((f" {EMOJI['video']} Meet:  {event.conference_link}", attr_link))

    # Recurrence
    if event.recurrence:
        lines.append((f" {EMOJI['refresh']} Recurring event", attr_dim))

    lines.append(("", attr_body))

    # Description
    if event.description:
        lines.append((" " + "─" * (width - 2), attr_border))
        lines.append(("", attr_body))
        for paragraph in event.description.split("\n"):
            if paragraph.strip() == "":
                lines.append(("", attr_body))
            else:
                wrapped = textwrap.wrap(paragraph, width - 4)
                for wl in wrapped:
                    lines.append((f"  {wl}", attr_body))
        lines.append(("", attr_body))

    # Organizer
    if event.organizer_email:
        name = event.organizer_name or event.organizer_email
        lines.append((f" {EMOJI['person']} Organizer: {name}", attr_dim))
        lines.append(("", attr_body))

    # Attendees
    if event.attendees:
        count = len(event.attendees)
        lines.append((" " + "─" * (width - 2), attr_border))
        lines.append(("", attr_body))
        lines.append((f" {EMOJI['people']} {count} Attendee{'s' if count != 1 else ''}", attr_field | curses.A_BOLD))
        lines.append(("", attr_body))
        for att in event.attendees:
            sym = response_status_symbol(att.response_status)
            name = att.display_name or att.email
            opt = " (optional)" if att.is_optional else ""
            org = " · organizer" if att.is_organizer else ""
            me = " (you)" if att.is_self else ""
            lines.append((f"    {sym} {name}{me}{org}{opt}",
                          curses.color_pair(response_status_pair(att.response_status))))
        lines.append(("", attr_body))

    # Your response
    if event.my_response_status:
        sym = response_status_symbol(event.my_response_status)
        status_label = {
            "accepted": "Accepted",
            "declined": "Declined",
            "tentative": "Maybe",
            "needsAction": "Not responded",
        }.get(event.my_response_status, event.my_response_status)
        lines.append((" " + "─" * (width - 2), attr_border))
        lines.append(("", attr_body))
        lines.append((f" Your status: {sym} {status_label}",
                      curses.color_pair(response_status_pair(event.my_response_status)) | curses.A_BOLD))

    lines.append(("", attr_body))
    return lines


def draw_event_detail(
    win,
    y_start: int,
    y_end: int,
    x_start: int,
    event: Event,
    scroll_offset: int = 0,
) -> None:
    """Draw the event detail view."""
    h, w = win.getmaxyx()
    attr_normal = curses.color_pair(PAIR_NORMAL)
    content_w = w - x_start - 2

    lines = _build_event_detail_lines(event, content_w)

    y = y_start
    for i, (text, attr) in enumerate(lines):
        if i < scroll_offset:
            continue
        if y >= y_end:
            break
        fill_line(win, y, attr_normal, x_start)
        safe_addstr(win, y, x_start + 1, text, attr, max_width=content_w)
        y += 1

    while y < y_end:
        fill_line(win, y, attr_normal, x_start)
        y += 1


# ---------------------------------------------------------------------------
# Create / Edit event form
# ---------------------------------------------------------------------------

FORM_FIELDS = ["summary", "date", "start_time", "end_time", "location", "description", "attendees"]
FORM_LABELS = {
    "summary": "Title:   ",
    "date": "Date:    ",
    "start_time": "Start:   ",
    "end_time": "End:     ",
    "location": "Where:   ",
    "description": "Details: ",
    "attendees": "Guests:  ",
}


def draw_event_form(
    win,
    y_start: int,
    y_end: int,
    x_start: int,
    fields: dict[str, str],
    active_field: str,
    is_edit: bool = False,
) -> None:
    """Draw the create/edit event form."""
    h, w = win.getmaxyx()
    attr_normal = curses.color_pair(PAIR_NORMAL)
    attr_label = curses.color_pair(PAIR_ACCENT_BLUE) | curses.A_BOLD
    attr_field = curses.color_pair(PAIR_COMPOSE_FIELD)
    attr_active = curses.color_pair(PAIR_INPUT) | curses.A_UNDERLINE
    content_w = w - x_start - 4

    y = y_start + 1

    # Title
    fill_line(win, y, attr_normal, x_start)
    title = "Edit Event" if is_edit else "New Event"
    safe_addstr(win, y, x_start + 2, f"{EMOJI['edit']} {title}",
                curses.color_pair(PAIR_TITLE) | curses.A_BOLD)
    y += 1
    fill_line(win, y, attr_normal, x_start)
    safe_addstr(win, y, x_start + 2, "─" * (content_w - 2), curses.color_pair(PAIR_BORDER))
    y += 2

    for field_key in FORM_FIELDS:
        fill_line(win, y, attr_normal, x_start)
        is_active = field_key == active_field
        label = FORM_LABELS.get(field_key, f"{field_key}:")
        safe_addstr(win, y, x_start + 2, label, attr_label)

        value = fields.get(field_key, "")
        field_attr = attr_active if is_active else attr_field

        field_w = content_w - len(label) - 4
        display_val = value[:field_w] if value else ""
        padded = display_val + " " * max(0, field_w - len(display_val))
        safe_addstr(win, y, x_start + 2 + len(label) + 1, padded, field_attr)
        y += 2

    while y < y_end:
        fill_line(win, y, attr_normal, x_start)
        y += 1


# ---------------------------------------------------------------------------
# Search bar
# ---------------------------------------------------------------------------

def draw_search_bar(
    win,
    y: int,
    x_start: int,
    query: str,
    is_active: bool,
) -> None:
    """Draw the search input bar."""
    h, w = win.getmaxyx()
    attr = curses.color_pair(PAIR_SEARCH_BOX)
    attr_active = curses.color_pair(PAIR_INPUT) | curses.A_UNDERLINE

    fill_line(win, y, curses.color_pair(PAIR_NORMAL), x_start)

    # Search icon
    safe_addstr(win, y, x_start + 1, f" {EMOJI['search']} ", curses.color_pair(PAIR_ACCENT_BLUE))

    # Input field
    field_w = w - x_start - 8
    if is_active:
        display = query[:field_w]
        padded = display + " " * max(0, field_w - len(display))
        safe_addstr(win, y, x_start + 5, padded, attr_active)
    else:
        if query:
            safe_addstr(win, y, x_start + 5, query[:field_w], attr)
        else:
            safe_addstr(win, y, x_start + 5, "Search events…"[:field_w],
                        curses.color_pair(PAIR_SNIPPET))


# ---------------------------------------------------------------------------
# Week header bar
# ---------------------------------------------------------------------------

def draw_week_header(win, y: int, x_start: int, width: int,
                     week_start: datetime, selected_day_offset: int = 0) -> int:
    """Draw a week day header row. Returns next y."""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    col_width = max(1, (width - 2) // 7)
    attr_normal = curses.color_pair(PAIR_SNIPPET)

    fill_line(win, y, curses.color_pair(PAIR_NORMAL), x_start)

    for d in range(7):
        day = week_start + timedelta(days=d)
        col_x = x_start + 1 + d * col_width
        day_name = day.strftime("%a")
        day_num = day.strftime("%-d")
        is_today = day.date() == today.date()
        is_selected = d == selected_day_offset

        label = f"{day_name} {day_num}"

        if is_selected and is_today:
            attr = curses.color_pair(PAIR_TAB_ACTIVE) | curses.A_BOLD
        elif is_today:
            attr = curses.color_pair(PAIR_TODAY_HIGHLIGHT) | curses.A_BOLD
        elif is_selected:
            attr = curses.color_pair(PAIR_EVENT_SELECTED_BOLD) | curses.A_BOLD
        else:
            attr = attr_normal

        centered = label[:col_width].center(col_width)
        safe_addstr(win, y, col_x, centered, attr)

    return y + 1


# ---------------------------------------------------------------------------
# Free time / meeting times results
# ---------------------------------------------------------------------------

def draw_free_time_results(
    win,
    y_start: int,
    y_end: int,
    x_start: int,
    slots: list[FreeSlot],
    title: str = "Free Time Slots",
) -> None:
    """Draw free time results."""
    h, w = win.getmaxyx()
    attr_normal = curses.color_pair(PAIR_NORMAL)
    content_w = w - x_start

    y = y_start
    fill_line(win, y, attr_normal, x_start)
    safe_addstr(win, y, x_start + 2, f"{EMOJI['free_time']} {title}",
                curses.color_pair(PAIR_TITLE) | curses.A_BOLD)
    y += 1
    fill_line(win, y, attr_normal, x_start)
    safe_addstr(win, y, x_start + 2, "─" * (content_w - 4), curses.color_pair(PAIR_BORDER))
    y += 2

    if not slots:
        fill_line(win, y, attr_normal, x_start)
        safe_addstr(win, y, x_start + 4, "No free slots found",
                    curses.color_pair(PAIR_SNIPPET))
        return

    for i, slot in enumerate(slots):
        if y >= y_end - 1:
            break
        fill_line(win, y, attr_normal, x_start)
        time_text = f"{slot.start_formatted} – {slot.end_formatted}"
        dur_text = f"({slot.duration_minutes}m)" if slot.duration_minutes else ""
        safe_addstr(win, y, x_start + 4,
                    f"{EMOJI['check']}  {time_text}  {dur_text}",
                    curses.color_pair(PAIR_ACCENT_GREEN))
        y += 2

    while y < y_end:
        fill_line(win, y, attr_normal, x_start)
        y += 1


def draw_meeting_time_results(
    win,
    y_start: int,
    y_end: int,
    x_start: int,
    options: list[MeetingTimeOption],
    title: str = "Available Meeting Times",
) -> None:
    """Draw meeting time suggestions."""
    h, w = win.getmaxyx()
    attr_normal = curses.color_pair(PAIR_NORMAL)
    content_w = w - x_start

    y = y_start
    fill_line(win, y, attr_normal, x_start)
    safe_addstr(win, y, x_start + 2, f"{EMOJI['meeting']} {title}",
                curses.color_pair(PAIR_TITLE) | curses.A_BOLD)
    y += 1
    fill_line(win, y, attr_normal, x_start)
    safe_addstr(win, y, x_start + 2, "─" * (content_w - 4), curses.color_pair(PAIR_BORDER))
    y += 2

    if not options:
        fill_line(win, y, attr_normal, x_start)
        safe_addstr(win, y, x_start + 4, "No available times found",
                    curses.color_pair(PAIR_SNIPPET))
        return

    for i, opt in enumerate(options):
        if y + 1 >= y_end:
            break
        fill_line(win, y, attr_normal, x_start)
        safe_addstr(win, y, x_start + 4,
                    f"Option {i+1}: {opt.start_formatted} – {opt.end_formatted}",
                    curses.color_pair(PAIR_ACCENT_BLUE) | curses.A_BOLD)
        y += 1
        fill_line(win, y, attr_normal, x_start)
        safe_addstr(win, y, x_start + 6,
                    f"{EMOJI['people']} {opt.attendee_count} attendees available",
                    curses.color_pair(PAIR_ACCENT_GREEN))
        y += 2

    while y < y_end:
        fill_line(win, y, attr_normal, x_start)
        y += 1
