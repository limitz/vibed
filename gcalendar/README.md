# Google Calendar Console Client

```
Do the same as project ../gmail, but for google calendar.
```

![Screenshot](screenshot.png)

## Overview

A console-based Google Calendar client powered by the Google Calendar MCP. Features a dark RGB color theme with emoji-rich sidebar, single-day agenda view with week navigation bar, full event detail/create/edit/search/free-time views, and vim-style keyboard navigation. Includes a complete mock client with 25+ realistic events for safe development — never touches real Google Calendar.

## Features

- **Agenda View**: Single-day event list with color-coded dots, time ranges, durations, and location details
- **Week Navigation**: Header bar showing the current week with today highlighted; left/right arrows to change day
- **Event Detail**: Full event view with date, time, location, video link, description, attendees with RSVP status
- **Create/Edit Events**: Form with title, date, start/end time, location, description, and attendees fields
- **Search**: Free-text search across all events
- **Free Time**: Find available time slots across your calendars
- **RSVP**: Accept, decline, or tentatively respond to event invitations
- **Delete Events**: Remove events directly from the detail view
- **Sidebar**: Navigation (Today, Prev/Next Day, Search, Free Time) and calendar list with color dots
- **Dark Theme**: Gmail-inspired dark purple color scheme with full RGB support
- **Keyboard-Driven**: Vim keys (j/k/h/l), arrow keys, Tab for sidebar, `/` for search, `?` for help

## Architecture

| Module | Purpose |
|---|---|
| `models.py` | Data models (Calendar, Event, Attendee, EventTime, FreeSlot, etc.) |
| `mcp_client.py` | Abstract base class defining the MCP interface |
| `mock_client.py` | Mock implementation with 25+ realistic events |
| `real_client.py` | Production implementation using real Google Calendar MCP tools |
| `colors.py` | Dark purple RGB theme with 37 color pairs and emoji constants |
| `components.py` | Curses UI drawing functions (header, sidebar, event list, detail, form, search) |
| `app.py` | Application controller with state machine and key handling |
| `main.py` | Entry point with `--live` flag support |

## Running

```bash
cd gcalendar
python main.py          # Mock mode (safe, no real MCP)
python main.py --live   # Live mode (not yet implemented)
```

## Testing

```bash
cd gcalendar
python -m pytest test_models.py test_mock_client.py test_components.py test_app.py -v
```

109 tests covering models, mock client, UI component helpers, and the full application controller.

## Built with

[Claude Code](https://claude.com/claude-code) — Claude Opus 4.6 (`claude-opus-4-6`)
