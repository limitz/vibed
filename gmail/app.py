"""Main application controller for the Gmail console client."""

import asyncio
import curses
from enum import Enum, auto
from typing import Optional

from models import EmailHeader, Email, Thread, Draft, Label, Profile, SearchResult
from mcp_client import GmailMCPClient
from colors import (
    init_colors, EMOJI, PAIR_NORMAL, PAIR_ACCENT_RED, PAIR_ACCENT_BLUE,
    PAIR_ACCENT_GREEN, PAIR_STATUS_BAR,
)
from components import (
    safe_addstr, fill_line, draw_header, draw_status_bar, draw_sidebar,
    draw_email_list, draw_message_view, draw_compose_screen,
    draw_thread_view, draw_search_bar, draw_draft_list,
)


class View(Enum):
    INBOX = auto()
    MESSAGE = auto()
    THREAD = auto()
    COMPOSE = auto()
    SEARCH = auto()
    DRAFTS = auto()
    HELP = auto()


# Sidebar items mapping
SIDEBAR_ITEMS = [
    {"name": "Compose", "emoji": EMOJI["compose"], "label_id": "__COMPOSE__", "is_action": True},
    {"name": "─────────────", "emoji": "", "label_id": "__SEP__", "is_separator": True},
    {"name": "Inbox", "emoji": EMOJI["inbox"], "label_id": "INBOX"},
    {"name": "Starred", "emoji": EMOJI["starred"], "label_id": "STARRED"},
    {"name": "Important", "emoji": EMOJI["important"], "label_id": "IMPORTANT"},
    {"name": "Sent", "emoji": EMOJI["sent"], "label_id": "SENT"},
    {"name": "Drafts", "emoji": EMOJI["drafts"], "label_id": "DRAFT"},
    {"name": "Spam", "emoji": EMOJI["spam"], "label_id": "SPAM"},
    {"name": "Trash", "emoji": EMOJI["trash"], "label_id": "TRASH"},
    {"name": "All Mail", "emoji": EMOJI["all_mail"], "label_id": ""},
    {"name": "─────────────", "emoji": "", "label_id": "__SEP__", "is_separator": True},
]

HELP_TEXT = [
    ("Navigation", [
        ("↑/↓, j/k", "Move up / down"),
        ("Enter", "Open email / select"),
        ("Esc, q", "Go back / quit"),
        ("Tab", "Switch focus (sidebar ↔ list)"),
    ]),
    ("Actions", [
        ("c", "Compose new email"),
        ("/", "Search messages"),
        ("r", "Reply (create draft)"),
        ("t", "View thread"),
        ("s", "Toggle star"),
        ("d", "View drafts"),
    ]),
    ("Views", [
        ("1-7", "Quick jump to sidebar items"),
        ("?", "Toggle this help"),
        ("R", "Refresh inbox"),
    ]),
]


class GmailApp:
    """Main application state and controller."""

    def __init__(self, client: GmailMCPClient):
        self.client = client
        self.running = True

        # State
        self.view = View.INBOX
        self.prev_view: Optional[View] = None
        self.profile: Optional[Profile] = None
        self.labels: list[Label] = []

        # Sidebar
        self.sidebar_items: list[dict] = list(SIDEBAR_ITEMS)
        self.sidebar_idx = 0
        self.sidebar_scroll = 0
        self.sidebar_focused = False
        self.sidebar_width = 26

        # Email list
        self.emails: list[EmailHeader] = []
        self.email_idx = 0
        self.email_scroll = 0
        self.current_query = ""
        self.current_label = "INBOX"
        self.next_page_token: Optional[str] = None

        # Message view
        self.current_email: Optional[Email] = None
        self.message_scroll = 0

        # Thread view
        self.current_thread: Optional[Thread] = None
        self.thread_scroll = 0

        # Compose
        self.compose_fields: dict[str, str] = {
            "to": "", "cc": "", "bcc": "", "subject": "", "body": ""
        }
        self.compose_active_field = "to"
        self.compose_field_order = ["to", "cc", "bcc", "subject", "body"]

        # Search
        self.search_query = ""
        self.search_active = False

        # Drafts
        self.drafts: list[Draft] = []
        self.draft_idx = 0

        # Status message
        self.status_message = ""
        self.status_is_error = False

        # Loading state
        self.loading = False

    async def init(self) -> None:
        """Load initial data."""
        self.loading = True
        try:
            self.profile = await self.client.get_profile()
            self.labels = await self.client.list_labels()
            self._update_sidebar_counts()
            await self._load_inbox()
        finally:
            self.loading = False

    def _update_sidebar_counts(self) -> None:
        """Update sidebar unread counts from labels."""
        label_map = {l.id: l for l in self.labels}
        user_labels = [l for l in self.labels if l.label_type == "user"]

        for item in self.sidebar_items:
            lid = item.get("label_id", "")
            if lid in label_map:
                item["unread"] = label_map[lid].unread_count
                item["count"] = label_map[lid].message_count

        # Add user labels to sidebar
        for ul in user_labels:
            self.sidebar_items.append({
                "name": ul.name,
                "emoji": EMOJI["label"],
                "label_id": ul.id,
                "unread": ul.unread_count,
                "count": ul.message_count,
            })

    async def _load_inbox(self, query: str = "", label: str = "") -> None:
        """Load emails into the list."""
        self.loading = True
        try:
            if label and label != "STARRED":
                q = f"label:{label}" if label else ""
            elif label == "STARRED":
                q = "is:starred"
            else:
                q = query

            if label == "DRAFT":
                # Load drafts instead
                result = await self.client.list_drafts()
                self.drafts = result.drafts
                self.draft_idx = 0
                self.view = View.DRAFTS
                return

            result = await self.client.search_messages(query=q, max_results=20)
            self.emails = result.messages
            self.next_page_token = result.next_page_token
            self.email_idx = 0
            self.email_scroll = 0
            self.current_query = q
            self.current_label = label or "INBOX"
            self.status_message = f"Loaded {len(self.emails)} messages"
        except Exception as e:
            self.status_message = f"Error: {e}"
            self.status_is_error = True
        finally:
            self.loading = False

    async def _open_message(self) -> None:
        """Open the currently selected email."""
        if not self.emails or self.email_idx >= len(self.emails):
            return
        header = self.emails[self.email_idx]
        self.loading = True
        try:
            self.current_email = await self.client.read_message(header.message_id)
            self.message_scroll = 0
            self.prev_view = self.view
            self.view = View.MESSAGE
        except Exception as e:
            self.status_message = f"Error loading message: {e}"
            self.status_is_error = True
        finally:
            self.loading = False

    async def _open_thread(self) -> None:
        """Open thread view for current email."""
        email = self.current_email
        if not email:
            if self.emails and self.email_idx < len(self.emails):
                email_header = self.emails[self.email_idx]
                thread_id = email_header.thread_id
            else:
                return
        else:
            thread_id = email.thread_id

        self.loading = True
        try:
            self.current_thread = await self.client.read_thread(thread_id)
            self.thread_scroll = 0
            self.prev_view = self.view
            self.view = View.THREAD
        except Exception as e:
            self.status_message = f"Error loading thread: {e}"
            self.status_is_error = True
        finally:
            self.loading = False

    def _start_compose(self, reply_to: Optional[Email] = None) -> None:
        """Open compose screen, optionally as reply."""
        self.compose_fields = {
            "to": "", "cc": "", "bcc": "", "subject": "", "body": ""
        }
        if reply_to:
            self.compose_fields["to"] = reply_to.sender_email
            subj = reply_to.subject
            if not subj.lower().startswith("re:"):
                subj = f"Re: {subj}"
            self.compose_fields["subject"] = subj
        self.compose_active_field = "to"
        self.prev_view = self.view
        self.view = View.COMPOSE

    async def _save_draft(self) -> None:
        """Save the current compose as a draft."""
        f = self.compose_fields
        if not f["body"].strip():
            self.status_message = "Cannot save empty draft"
            self.status_is_error = True
            return

        self.loading = True
        try:
            await self.client.create_draft(
                body=f["body"],
                to=f["to"] or None,
                subject=f["subject"] or None,
                cc=f["cc"] or None,
                bcc=f["bcc"] or None,
            )
            self.status_message = f"{EMOJI['check']} Draft saved!"
            self.status_is_error = False
            self.view = self.prev_view or View.INBOX
        except Exception as e:
            self.status_message = f"Error saving draft: {e}"
            self.status_is_error = True
        finally:
            self.loading = False

    def _get_status_hints(self) -> list[tuple[str, str]]:
        """Get context-appropriate key hints for the status bar."""
        if self.view == View.HELP:
            return [("Esc", "Close help")]
        elif self.view == View.COMPOSE:
            return [("Tab", "Next field"), ("Ctrl+S", "Save draft"), ("Esc", "Cancel")]
        elif self.view == View.MESSAGE:
            return [("Esc", "Back"), ("t", "Thread"), ("r", "Reply"), ("↑↓", "Scroll")]
        elif self.view == View.THREAD:
            return [("Esc", "Back"), ("r", "Reply"), ("↑↓", "Scroll")]
        elif self.view == View.SEARCH:
            return [("Enter", "Search"), ("Esc", "Cancel")]
        elif self.view == View.DRAFTS:
            return [("Enter", "Edit"), ("Esc", "Back"), ("?", "Help")]
        else:
            return [("↑↓", "Navigate"), ("Enter", "Open"), ("/", "Search"),
                    ("c", "Compose"), ("?", "Help"), ("q", "Quit")]

    def draw(self, stdscr) -> None:
        """Render the full UI."""
        h, w = stdscr.getmaxyx()
        if h < 10 or w < 40:
            stdscr.clear()
            safe_addstr(stdscr, 0, 0, "Terminal too small!", curses.A_BOLD)
            return

        stdscr.bkgd(" ", curses.color_pair(PAIR_NORMAL))

        # Header (line 0)
        email = self.profile.email if self.profile else "loading..."
        view_name = self.view.name.title()
        if self.current_label and self.view in (View.INBOX, View.MESSAGE, View.THREAD):
            # Find label display name
            for item in self.sidebar_items:
                if item.get("label_id") == self.current_label:
                    view_name = item["name"]
                    break
        y = draw_header(stdscr, 0, email, view_name)

        # Margin line below header
        fill_line(stdscr, y, curses.color_pair(PAIR_NORMAL))
        y += 1

        # Search bar — only visible when actively searching
        if self.view == View.SEARCH and self.search_active:
            draw_search_bar(
                stdscr, y, self.sidebar_width,
                self.search_query, self.search_active
            )
            y += 1

        # Single bottom status bar (last line)
        status_y = h - 1
        hints = self._get_status_hints()
        draw_status_bar(stdscr, status_y, hints, self.status_message, self.status_is_error, self.loading)

        content_y_start = y
        content_y_end = status_y

        # Sidebar (left panel) — always visible except compose/help
        if self.view not in (View.COMPOSE, View.HELP):
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

        # Main content area
        if self.view == View.INBOX:
            if self.emails:
                draw_email_list(
                    stdscr,
                    content_y_start,
                    content_y_end,
                    main_x,
                    self.emails,
                    self.email_idx,
                    self.email_scroll,
                )
            else:
                fill_line(stdscr, content_y_start + 2, curses.color_pair(PAIR_NORMAL), main_x)
                safe_addstr(stdscr, content_y_start + 2, main_x + 4,
                            "No messages found.", curses.color_pair(PAIR_NORMAL))

        elif self.view == View.MESSAGE and self.current_email:
            draw_message_view(
                stdscr,
                content_y_start,
                content_y_end,
                main_x,
                self.current_email,
                self.message_scroll,
            )

        elif self.view == View.THREAD and self.current_thread:
            draw_thread_view(
                stdscr,
                content_y_start,
                content_y_end,
                main_x,
                self.current_thread,
                self.thread_scroll,
            )

        elif self.view == View.COMPOSE:
            draw_compose_screen(
                stdscr,
                content_y_start,
                content_y_end,
                main_x,
                self.compose_fields,
                self.compose_active_field,
            )

        elif self.view == View.SEARCH:
            if self.emails:
                draw_email_list(
                    stdscr,
                    content_y_start,
                    content_y_end,
                    main_x,
                    self.emails,
                    self.email_idx,
                    self.email_scroll,
                )

        elif self.view == View.DRAFTS:
            draw_draft_list(
                stdscr,
                content_y_start,
                content_y_end,
                main_x,
                self.drafts,
                self.draft_idx,
            )

        elif self.view == View.HELP:
            self._draw_help(stdscr, content_y_start, content_y_end)

    def _draw_help(self, stdscr, y_start: int, y_end: int) -> None:
        """Draw the help overlay."""
        h, w = stdscr.getmaxyx()
        attr_normal = curses.color_pair(PAIR_NORMAL)
        attr_title = curses.color_pair(PAIR_ACCENT_RED) | curses.A_BOLD
        attr_key = curses.color_pair(PAIR_ACCENT_BLUE) | curses.A_BOLD
        attr_desc = curses.color_pair(PAIR_NORMAL)
        attr_border = curses.color_pair(PAIR_ACCENT_RED)

        y = y_start + 1
        fill_line(stdscr, y, attr_normal)
        safe_addstr(stdscr, y, 4, f"{'─' * (w - 8)}", attr_border)
        y += 1
        fill_line(stdscr, y, attr_normal)
        safe_addstr(stdscr, y, 4, f"{EMOJI['mail']}  Gmail Client — Keyboard Shortcuts", attr_title)
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

    async def handle_key(self, key: int) -> None:
        """Handle a keypress and update state."""
        self.status_message = ""
        self.status_is_error = False

        if self.view == View.HELP:
            if key in (27, ord("q"), ord("?")):  # Esc, q, ?
                self.view = self.prev_view or View.INBOX
            return

        if self.view == View.SEARCH and self.search_active:
            await self._handle_search_input(key)
            return

        if self.view == View.COMPOSE:
            await self._handle_compose_input(key)
            return

        # Global keys
        if key == ord("q"):
            if self.view == View.INBOX and not self.sidebar_focused:
                self.running = False
            elif self.view in (View.MESSAGE, View.THREAD, View.SEARCH, View.DRAFTS):
                self.view = View.INBOX
            elif self.sidebar_focused:
                self.sidebar_focused = False
            return

        if key == 27:  # Escape
            if self.view in (View.MESSAGE, View.THREAD, View.DRAFTS):
                self.view = self.prev_view or View.INBOX
            elif self.view == View.SEARCH:
                self.search_active = False
                self.view = View.INBOX
            elif self.sidebar_focused:
                self.sidebar_focused = False
            return

        if key == ord("?"):
            self.prev_view = self.view
            self.view = View.HELP
            return

        if key == ord("c"):
            self._start_compose()
            return

        if key == ord("/"):
            self.search_query = ""
            self.search_active = True
            self.view = View.SEARCH
            return

        if key == ord("d"):
            self.loading = True
            try:
                result = await self.client.list_drafts()
                self.drafts = result.drafts
                self.draft_idx = 0
                self.prev_view = self.view
                self.view = View.DRAFTS
            finally:
                self.loading = False
            return

        if key == ord("R"):
            await self._load_inbox(label=self.current_label)
            self.status_message = f"{EMOJI['refresh']} Refreshed!"
            return

        # Tab: toggle sidebar focus
        if key == 9:  # Tab
            if self.view in (View.INBOX, View.SEARCH):
                self.sidebar_focused = not self.sidebar_focused
            return

        # Number keys: quick jump to sidebar items
        if ord("1") <= key <= ord("9"):
            idx = key - ord("1")
            if idx < len(self.sidebar_items):
                item = self.sidebar_items[idx]
                if item.get("is_separator"):
                    return
                self.sidebar_idx = idx
                label_id = item.get("label_id", "")
                if label_id == "DRAFT":
                    result = await self.client.list_drafts()
                    self.drafts = result.drafts
                    self.draft_idx = 0
                    self.prev_view = self.view
                    self.view = View.DRAFTS
                elif label_id == "STARRED":
                    await self._load_inbox(query="is:starred", label="STARRED")
                    self.view = View.INBOX
                elif label_id:
                    await self._load_inbox(label=label_id)
                    self.view = View.INBOX
                else:
                    await self._load_inbox()
                    self.view = View.INBOX
            return

        # View-specific keys
        if self.sidebar_focused:
            await self._handle_sidebar_keys(key)
        elif self.view == View.INBOX:
            await self._handle_inbox_keys(key)
        elif self.view == View.MESSAGE:
            await self._handle_message_keys(key)
        elif self.view == View.THREAD:
            await self._handle_thread_keys(key)
        elif self.view == View.DRAFTS:
            await self._handle_draft_keys(key)

    def _skip_separators(self, idx: int, direction: int) -> int:
        """Skip separator items when navigating sidebar."""
        while 0 <= idx < len(self.sidebar_items):
            if self.sidebar_items[idx].get("is_separator"):
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
            label_id = item.get("label_id", "")
            if label_id == "__COMPOSE__":
                self._start_compose()
                self.sidebar_focused = False
                return
            if label_id == "__SEP__":
                return
            if label_id == "DRAFT":
                result = await self.client.list_drafts()
                self.drafts = result.drafts
                self.draft_idx = 0
                self.prev_view = self.view
                self.view = View.DRAFTS
            elif label_id == "STARRED":
                await self._load_inbox(query="is:starred", label="STARRED")
            elif label_id:
                await self._load_inbox(label=label_id)
            else:
                await self._load_inbox()
            self.sidebar_focused = False

    async def _handle_inbox_keys(self, key: int) -> None:
        """Handle keys in inbox view."""
        if key in (curses.KEY_UP, ord("k")):
            self.email_idx = max(0, self.email_idx - 1)
            self._adjust_email_scroll()
        elif key in (curses.KEY_DOWN, ord("j")):
            self.email_idx = min(len(self.emails) - 1, self.email_idx + 1)
            self._adjust_email_scroll()
        elif key in (curses.KEY_ENTER, 10, 13):
            await self._open_message()
        elif key == ord("t"):
            await self._open_thread()
        elif key == ord("r"):
            if self.emails and self.email_idx < len(self.emails):
                header = self.emails[self.email_idx]
                # Quick reply — just open compose with sender
                email = Email(
                    message_id=header.message_id,
                    thread_id=header.thread_id,
                    subject=header.subject,
                    sender=header.sender,
                    sender_email=header.sender_email,
                    to="",
                )
                self._start_compose(reply_to=email)
        elif key == ord("s"):
            if self.emails and self.email_idx < len(self.emails):
                self.emails[self.email_idx].is_starred = not self.emails[self.email_idx].is_starred
                star_state = "starred" if self.emails[self.email_idx].is_starred else "unstarred"
                self.status_message = f"{EMOJI['starred']} Message {star_state}"

    async def _handle_message_keys(self, key: int) -> None:
        """Handle keys in message view."""
        if key in (curses.KEY_UP, ord("k")):
            self.message_scroll = max(0, self.message_scroll - 1)
        elif key in (curses.KEY_DOWN, ord("j")):
            self.message_scroll += 1
        elif key == curses.KEY_PPAGE:
            self.message_scroll = max(0, self.message_scroll - 10)
        elif key == curses.KEY_NPAGE:
            self.message_scroll += 10
        elif key == ord("t"):
            await self._open_thread()
        elif key == ord("r"):
            if self.current_email:
                self._start_compose(reply_to=self.current_email)

    async def _handle_thread_keys(self, key: int) -> None:
        """Handle keys in thread view."""
        if key in (curses.KEY_UP, ord("k")):
            self.thread_scroll = max(0, self.thread_scroll - 1)
        elif key in (curses.KEY_DOWN, ord("j")):
            self.thread_scroll += 1
        elif key == curses.KEY_PPAGE:
            self.thread_scroll = max(0, self.thread_scroll - 10)
        elif key == curses.KEY_NPAGE:
            self.thread_scroll += 10
        elif key == ord("r"):
            if self.current_thread and self.current_thread.messages:
                last_msg = self.current_thread.messages[-1]
                reply_email = Email(
                    message_id=last_msg.message_id,
                    thread_id=self.current_thread.thread_id,
                    subject=self.current_thread.subject,
                    sender=last_msg.sender,
                    sender_email=last_msg.sender_email,
                    to="",
                )
                self._start_compose(reply_to=reply_email)

    async def _handle_draft_keys(self, key: int) -> None:
        """Handle keys in draft list view."""
        if key in (curses.KEY_UP, ord("k")):
            self.draft_idx = max(0, self.draft_idx - 1)
        elif key in (curses.KEY_DOWN, ord("j")):
            self.draft_idx = min(len(self.drafts) - 1, self.draft_idx + 1)
        elif key in (curses.KEY_ENTER, 10, 13):
            if self.drafts and self.draft_idx < len(self.drafts):
                draft = self.drafts[self.draft_idx]
                self.compose_fields = {
                    "to": draft.to,
                    "cc": draft.cc,
                    "bcc": draft.bcc,
                    "subject": draft.subject,
                    "body": draft.body,
                }
                self.compose_active_field = "body"
                self.prev_view = View.DRAFTS
                self.view = View.COMPOSE

    async def _handle_search_input(self, key: int) -> None:
        """Handle keys during search input."""
        if key == 27:  # Escape
            self.search_active = False
            self.view = View.INBOX
        elif key in (curses.KEY_ENTER, 10, 13):
            self.search_active = False
            if self.search_query:
                await self._load_inbox(query=self.search_query)
                self.status_message = f"{EMOJI['search']} Results for: {self.search_query}"
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            self.search_query = self.search_query[:-1]
        elif 32 <= key <= 126:
            self.search_query += chr(key)

    async def _handle_compose_input(self, key: int) -> None:
        """Handle keys in compose view."""
        if key == 27:  # Escape
            self.view = self.prev_view or View.INBOX
        elif key == 19:  # Ctrl+S
            await self._save_draft()
        elif key == 9:  # Tab — next field
            idx = self.compose_field_order.index(self.compose_active_field)
            idx = (idx + 1) % len(self.compose_field_order)
            self.compose_active_field = self.compose_field_order[idx]
        elif key == 353:  # Shift+Tab — prev field
            idx = self.compose_field_order.index(self.compose_active_field)
            idx = (idx - 1) % len(self.compose_field_order)
            self.compose_active_field = self.compose_field_order[idx]
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            field = self.compose_active_field
            self.compose_fields[field] = self.compose_fields[field][:-1]
        elif key == 10 and self.compose_active_field == "body":
            self.compose_fields["body"] += "\n"
        elif 32 <= key <= 126:
            self.compose_fields[self.compose_active_field] += chr(key)

    def _adjust_email_scroll(self, visible_height: int = 30) -> None:
        """Adjust scroll to keep selected email visible."""
        # Each email takes 3 lines (2 content + 1 separator)
        lines_per_email = 3
        visible_emails = max(1, visible_height // lines_per_email)

        if self.email_idx < self.email_scroll:
            self.email_scroll = self.email_idx
        elif self.email_idx >= self.email_scroll + visible_emails:
            self.email_scroll = self.email_idx - visible_emails + 1


def run_app(client: GmailMCPClient) -> None:
    """Main entry point for the curses app."""

    app = GmailApp(client)

    def curses_main(stdscr):
        """Inner curses wrapper."""
        # Initialize colors
        init_colors()

        # Curses settings
        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(False)
        stdscr.timeout(100)  # 100ms timeout for responsive UI
        curses.mousemask(0)

        # Create event loop for async MCP calls
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Initialize app data
        loop.run_until_complete(app.init())

        while app.running:
            try:
                # Draw
                stdscr.erase()
                app.draw(stdscr)
                stdscr.refresh()

                # Get input
                key = stdscr.getch()
                if key == -1:
                    continue  # Timeout, no input

                # Handle resize
                if key == curses.KEY_RESIZE:
                    stdscr.clear()
                    continue

                # Process key
                loop.run_until_complete(app.handle_key(key))

            except KeyboardInterrupt:
                break

        loop.close()

    curses.wrapper(curses_main)
